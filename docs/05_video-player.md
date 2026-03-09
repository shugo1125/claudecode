# 05 動画視聴ページ

YouTube 埋め込みで動画を再生する。アクセス制御も本ページで実施。`/courses/[slug]/lessons/[id]` に対応。

## Todo

- [ ] `app/courses/[slug]/lessons/[id]/page.tsx` を作成（Server Component）
  - lesson・section・course を取得
  - **アクセス制御** をサーバー側で判定
    - `is_free = true` → 全員視聴可
    - `is_free = false` かつ未ログイン → ログインを促すメッセージ表示（リダイレクトではなく制限表示）
    - `is_free = false` かつログイン済みで `user_course_access` なし → アクセス不可メッセージ
    - `is_free = false` かつログイン済みで `user_course_access` あり → 視聴可
- [ ] YouTube 埋め込みコンポーネントを作成
  - `components/YoutubePlayer.tsx`（Client Component）
  - `youtube-nocookie.com` を使用（例：`https://www.youtube-nocookie.com/embed/{videoId}`）
  - youtube_url から video ID を抽出するユーティリティ関数
- [ ] サイドバーにセクション・動画一覧を表示
  - 現在視聴中の動画をハイライト
  - 視聴済みの動画にチェックマークを表示（`lesson_progress` 参照）
  - 各動画へのリンク（アクセス不可の場合はロックアイコン）
- [ ] ローディング UI（`app/courses/[slug]/lessons/[id]/loading.tsx`）
