# 06 視聴済みチェック機能

ユーザーが動画ごとに「視聴済み」を手動でマークできる機能。

## Todo

- [ ] 「視聴済みにする」チェックボタンコンポーネントを作成
  - `components/WatchedButton.tsx`（Client Component）
  - チェック済み／未チェックで見た目を切り替え
  - ログイン済みユーザーのみ表示
- [ ] Server Action を作成
  - `app/actions/progress.ts`
  - `markAsWatched(lessonId)` — `lesson_progress` に upsert
  - `markAsUnwatched(lessonId)` — `lesson_progress` から delete
  - 実行後に `revalidatePath` で該当ページを再検証
- [ ] 動画視聴ページ（05）のサイドバーと連携して視聴済み状態を表示
