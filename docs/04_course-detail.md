# 04 講座詳細ページ

講座の説明・カリキュラム（セクション・動画一覧）を表示する。`/courses/[slug]` に対応。

## Todo

- [ ] `app/courses/[slug]/page.tsx` を作成（Server Component）
  - slug から `courses` を取得
  - 紐づく `sections` と `lessons` を合わせて取得（order 順）
  - 存在しない slug は `notFound()` を返す
  - `generateStaticParams` で公開講座の slug を静的生成
- [ ] 講座説明セクションの表示
  - サムネイル、タイトル、description
- [ ] カリキュラム一覧コンポーネントを作成
  - `components/Curriculum.tsx`
  - セクションごとに動画タイトルをアコーディオンまたはリストで表示
  - `is_free` の動画には「無料視聴」バッジを表示
  - 各動画は `/courses/[slug]/lessons/[id]` へリンク
- [ ] ローディング UI（`app/courses/[slug]/loading.tsx`）
- [ ] エラー UI（`app/courses/[slug]/error.tsx`）
