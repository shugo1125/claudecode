# PR → Claude レビュー

GitHub PR の差分を取得し、Claude API でコードレビューするスクリプト。

## セットアップ

```bash
cd scripts/pr-review
pip install -r requirements.txt
```

## 環境変数

| 変数 | 必須 | 説明 |
|------|------|------|
| `ANTHROPIC_API_KEY` | ✅ | Claude API キー |
| `GITHUB_TOKEN` | △ | private repo の場合、GitHub トークン |

## 使い方

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."  # private repo のとき

python claude_pr_review.py <owner> <repo> <PR番号>
```

### 例

```bash
python claude_pr_review.py apple newcode-course-platform 1
```

## 出力

レビュー結果が標準出力に表示される。ファイルに保存する例：

```bash
python claude_pr_review.py apple newcode-course-platform 1 > review.md
```

## PR コメントに投稿する

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_TOKEN="ghp_..."

python claude_pr_review.py shugo1125 claudecode 1 --post-comment
```

- 既存の Claude レビューコメントがあれば更新します
- なければ新規コメントを追加します

## GitHub Actions で自動レビューする

このリポジトリには `.github/workflows/pr-review.yml` を追加しています。
PR の `opened` / `synchronize` / `reopened` / `ready_for_review` で実行され、
Claude のレビュー結果を PR コメントに投稿します。

### 必要な GitHub Secrets / Variables

- `ANTHROPIC_API_KEY` : 必須
- `CLAUDE_MODEL` : 任意。省略時は `claude-3-5-sonnet-20241022`
- `MAX_DIFF_CHARS` : 任意。省略時は `120000`
