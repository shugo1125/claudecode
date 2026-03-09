# 02 認証（Google OAuth）

Supabase Auth を使った Google ログイン・ログアウトと、ルート保護のミドルウェア。

## Todo

- [ ] Supabase ダッシュボードで Google OAuth プロバイダーを有効化
- [ ] `/login` ページを作成
  - `app/login/page.tsx`
  - 「Google でログイン」ボタン → `supabase.auth.signInWithOAuth({ provider: 'google' })` を呼ぶ Client Component
- [ ] OAuth コールバックルートを作成
  - `app/auth/callback/route.ts` — code を受け取りセッションを確立して `/` にリダイレクト
- [ ] ログアウト処理を実装
  - Server Action または Route Handler で `supabase.auth.signOut()` を呼び `/login` にリダイレクト
- [ ] `middleware.ts` を作成してルート保護
  - `/admin/*` — 未ログイン or `role !== 'admin'` の場合は `/login` にリダイレクト
  - セッション Cookie のリフレッシュ処理を含める（`@supabase/ssr` 推奨）
- [ ] ヘッダーにログイン状態の表示とログアウトボタンを追加（共通 layout）
