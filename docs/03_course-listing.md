# 03 講座一覧ページ（トップページ）

公開中の講座をカード形式で一覧表示する。`/` に対応。

## Todo

- [ ] `app/page.tsx` を講座一覧ページとして実装（Server Component）
  - `is_published = true` の講座を Supabase から取得
- [ ] 講座カードコンポーネントを作成
  - `components/CourseCard.tsx`
  - サムネイル（`next/image`）、タイトル、説明文の一部を表示
  - 講座詳細ページ（`/courses/[slug]`）へ `next/link` でリンク
- [ ] ローディング UI を追加（`app/loading.tsx`）
- [ ] 講座が 0 件のときの空状態表示
