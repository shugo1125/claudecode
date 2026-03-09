# 08 管理画面 — セクション・動画 CRUD

講座内のセクションと動画を管理し、順序変更もできる画面。`/admin/courses/[id]/edit` に対応。

## Todo

- [ ] `app/admin/courses/[id]/edit/page.tsx` を作成（Server Component）
  - 対象講座とその sections・lessons を order 順に取得して表示
- [ ] セクション CRUD
  - セクション追加フォーム（title・order）→ Server Action で insert
  - セクション名インライン編集 → Server Action で update
  - セクション削除 → Server Action で delete（cascade で lessons も削除）
- [ ] 動画（Lesson）CRUD
  - 動画追加フォーム（title, youtube_url, order, is_free）→ Server Action で insert
  - 動画編集（各フィールドの変更）→ Server Action で update
  - 動画削除 → Server Action で delete
- [ ] 順序変更
  - 上下ボタンで order の値を入れ替える（ドラッグ＆ドロップは Phase 2 以降）
  - Server Action で対象行の `order` を update し `revalidatePath` を実行
- [ ] 各 Server Action 実行後に `revalidatePath('/admin/courses/[id]/edit')` および関連するユーザー向けページを再検証
