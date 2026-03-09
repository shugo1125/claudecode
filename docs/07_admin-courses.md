# 07 管理画面 — 講座 CRUD

管理者が講座を作成・編集・削除・公開設定できる画面。`/admin/courses` に対応。

## Todo

- [ ] 管理画面共通レイアウトを作成
  - `app/admin/layout.tsx` — サーバー側でセッションの `role` を確認、`admin` 以外は `/login` にリダイレクト
  - 管理者用ナビゲーション（講座管理・ユーザー管理へのリンク）
- [ ] `/admin` トップページ（`app/admin/page.tsx`）— 管理メニューの表示
- [ ] 講座一覧ページ（`app/admin/courses/page.tsx`）
  - 全講座（公開・非公開問わず）を一覧表示
  - 公開ステータスの表示
  - 編集・削除ボタン
  - 新規作成ボタン
- [ ] 講座作成・編集フォームを実装
  - `app/admin/courses/new/page.tsx`
  - `app/admin/courses/[id]/page.tsx`（編集）
  - フィールド：title, slug, description, thumbnail_url, is_published
  - Server Action で `courses` テーブルに insert / update
  - 保存後 `revalidatePath('/admin/courses')` と `revalidatePath('/')` を実行
- [ ] 講座削除の Server Action
  - 削除前に確認（Client Component でダイアログ）
  - cascade により sections・lessons も削除される
