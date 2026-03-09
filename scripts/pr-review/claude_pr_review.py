#!/usr/bin/env python3
"""
GitHub PR の差分を取得し、Claude API でコードレビューするスクリプト。

Usage:
  python claude_pr_review.py <owner> <repo> <pr_number> [--post-comment]

Env:
  GITHUB_TOKEN       - GitHub token（private repo や PR コメント投稿で使用）
  ANTHROPIC_API_KEY  - Claude API キー
  CLAUDE_MODEL       - Claude モデル名（省略時は既定値）
  MAX_DIFF_CHARS     - Claude に送る diff の最大文字数
"""

import argparse
import os
import sys

import requests
from anthropic import Anthropic


COMMENT_MARKER = "<!-- claude-pr-review -->"
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
DEFAULT_MAX_DIFF_CHARS = 120_000


def github_headers(token: str | None = None, accept: str = "application/json") -> dict[str, str]:
    headers = {
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_pr_diff(owner: str, repo: str, pr_number: int, token: str | None = None) -> str:
    """GitHub API で PR の diff を取得"""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    resp = requests.get(url, headers=github_headers(token, "application/vnd.github.v3.diff"))
    resp.raise_for_status()
    return resp.text


def trim_diff(diff: str, max_chars: int) -> tuple[str, bool]:
    if len(diff) <= max_chars:
        return diff, False
    return diff[:max_chars], True


def review_with_claude(diff: str, api_key: str, was_truncated: bool) -> str:
    """Claude API に diff を送ってレビュー結果を取得"""
    client = Anthropic(api_key=api_key)

    system_prompt = """あなたはコードレビュアーです。以下の GitHub PR の差分をレビューしてください。
- バグの可能性
- セキュリティ上の問題
- ベストプラクティス違反
- 改善提案
を指摘してください。日本語で回答してください。
レビューは次の形式にしてください。
## Summary
## Findings
- 重要な指摘
## Risks
## Suggested fixes"""

    user_content = f"""以下の PR 差分をレビューしてください：

```
{diff}
```"""

    if was_truncated:
        user_content += (
            "\n\n注記: 差分が長いため一部を省略しています。"
            " 見えている範囲で高リスクな点を優先してレビューしてください。"
        )

    model = os.environ.get("CLAUDE_MODEL", DEFAULT_MODEL)
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )

    return message.content[0].text


def format_comment_body(review: str, was_truncated: bool) -> str:
    notes = []
    if was_truncated:
        notes.append(
            "- 差分が長いため、レビュー対象は一部に切り詰められています。大きな PR では補助レビューとして扱ってください。"
        )

    note_block = ""
    if notes:
        note_block = "\n".join(["## Notes", *notes, ""])

    return f"""{COMMENT_MARKER}
## Claude PR Review

{review}

{note_block}_Generated automatically by `scripts/pr-review/claude_pr_review.py`._
"""


def upsert_pr_comment(owner: str, repo: str, pr_number: int, body: str, token: str) -> None:
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    resp = requests.get(comments_url, headers=github_headers(token))
    resp.raise_for_status()

    existing_comment = None
    for comment in resp.json():
        if COMMENT_MARKER in comment.get("body", ""):
            existing_comment = comment
            break

    if existing_comment:
        update_url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{existing_comment['id']}"
        update_resp = requests.patch(
            update_url,
            headers=github_headers(token),
            json={"body": body},
        )
        update_resp.raise_for_status()
        return

    create_resp = requests.post(
        comments_url,
        headers=github_headers(token),
        json={"body": body},
    )
    create_resp.raise_for_status()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("pr_number", type=int)
    parser.add_argument(
        "--post-comment",
        action="store_true",
        help="レビュー結果を PR コメントとして投稿または更新する",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    github_token = os.environ.get("GITHUB_TOKEN")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    max_diff_chars = int(os.environ.get("MAX_DIFF_CHARS", DEFAULT_MAX_DIFF_CHARS))

    if not anthropic_key:
        print("Error: ANTHROPIC_API_KEY を設定してください", file=sys.stderr)
        sys.exit(1)

    if args.post_comment and not github_token:
        print("Error: --post-comment を使う場合は GITHUB_TOKEN が必要です", file=sys.stderr)
        sys.exit(1)

    print("PR 差分を取得中...", file=sys.stderr)
    diff = get_pr_diff(args.owner, args.repo, args.pr_number, github_token)

    if not diff:
        print("差分がありません", file=sys.stderr)
        sys.exit(0)

    diff, was_truncated = trim_diff(diff, max_diff_chars)
    print("Claude でレビュー中...", file=sys.stderr)
    result = review_with_claude(diff, anthropic_key, was_truncated)

    if args.post_comment:
        print("PR コメントを投稿中...", file=sys.stderr)
        comment_body = format_comment_body(result, was_truncated)
        upsert_pr_comment(args.owner, args.repo, args.pr_number, comment_body, github_token)
        print("PR コメントを更新しました", file=sys.stderr)

    print(result)


if __name__ == "__main__":
    main()
