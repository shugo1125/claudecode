# 00 MCP セットアップ（Claude Code + Supabase + Serena）

Claude Code で Supabase MCP / Serena MCP を使うための設定。

## 手順

1. **Supabase でアクセストークンを取得**
   - [Supabase Dashboard](https://supabase.com/dashboard) → 右上アカウント → **Access Tokens**
   - **Generate new token** → 名前（例: `claude-mcp`）を入力 → 生成
   - トークンをコピー（一度しか表示されないので注意）

2. **設定ファイルを用意**
   ```bash
   cp claude_mcp_config.example.json claude_mcp_config.json
   ```
   `claude_mcp_config.json` の `YOUR_SUPABASE_ACCESS_TOKEN_HERE` を取得したトークンに置き換える。

3. **Claude Code を MCP 付きで起動**
   ```bash
   claude --mcp-config claude_mcp_config.json
   ```
   エイリアスを使っている場合（例: `ccmcp`）も同様に設定を渡す。

4. **接続確認**
   - Claude Code 内で `/mcp` を実行し、Supabase にチェックが入っているか確認
   - 例: 「このプロジェクトの Supabase を探して」と聞いて `list_projects` が動けば OK

## Serena MCP の追加

1. **`uv` / `uvx` をインストール**
   ```bash
   brew install uv
   ```

2. **設定ファイルに Serena を追加**
   `claude_mcp_config.json` に以下のような `serena` エントリを追加する。

   ```json
   "serena": {
     "command": "uvx",
     "args": [
       "--from",
       "git+https://github.com/oraios/serena",
       "serena",
       "start-mcp-server",
       "--context",
       "claude-code",
       "--project",
       "/Users/apple/ClaudeCode/newcode-course-platform"
     ]
   }
   ```

3. **Claude Code を再起動**
   ```bash
   claude --mcp-config claude_mcp_config.json
   ```

4. **接続確認**
   - `/mcp` を開いて `serena` にチェックが入っているか確認
   - 例: 「Serena MCP を使ってこのプロジェクト構成を見て」と聞く
   - 初回実行時に `.serena/project.yml` が作成される場合がある

## 補足

- `claude_mcp_config.json` は `.gitignore` に含まれており、トークンがリポジトリにコミットされることはありません。
- Playwright などの他の MCP を追加する場合は、`mcpServers` にエントリを足してください。
- Serena は大規模コードベースで特に効果を発揮します。小規模でも使えますが、導入メリットが大きくなるのはファイル数が増えてからです。
