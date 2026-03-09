# 01 Supabase セットアップ & DB スキーマ

Supabase プロジェクトの初期設定とテーブル作成。以降のすべてのチケットの前提となる。

## Todo

- [ ] Supabase プロジェクトを作成し、URL・anon key を `.env.local` に設定
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [ ] `@supabase/supabase-js` をインストール
- [ ] Supabase クライアントのユーティリティを作成
  - `lib/supabase/client.ts` — ブラウザ用
  - `lib/supabase/server.ts` — Server Component / Server Action 用
- [ ] 以下のテーブルを SQL エディタで作成

```sql
-- courses
create table courses (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  slug text unique not null,
  description text,
  thumbnail_url text,
  is_published boolean default false,
  created_at timestamp default now()
);

-- sections
create table sections (
  id uuid primary key default gen_random_uuid(),
  course_id uuid references courses(id) on delete cascade,
  title text not null,
  "order" int not null,
  created_at timestamp default now()
);

-- lessons
create table lessons (
  id uuid primary key default gen_random_uuid(),
  section_id uuid references sections(id) on delete cascade,
  title text not null,
  youtube_url text not null,
  "order" int not null,
  is_free boolean default false,
  created_at timestamp default now()
);

-- user_course_access
create table user_course_access (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  course_id uuid references courses(id) on delete cascade,
  granted_at timestamp default now(),
  unique(user_id, course_id)
);

-- lesson_progress
create table lesson_progress (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  lesson_id uuid references lessons(id) on delete cascade,
  watched_at timestamp default now(),
  unique(user_id, lesson_id)
);
```

- [ ] `auth.users` に `role` カラムを追加（管理者識別用）
  ```sql
  alter table auth.users add column if not exists role text default 'user';
  ```
- [ ] Row Level Security (RLS) を各テーブルに設定
  - `courses` / `sections` / `lessons` — 公開データは全員読み取り可、書き込みは管理者のみ
  - `user_course_access` — 自分のレコードのみ読み取り可、書き込みは管理者のみ
  - `lesson_progress` — 自分のレコードのみ読み書き可
- [ ] `supabase gen types typescript` で型を生成し `types/supabase.ts` に配置
