# 09 管理画面 — ユーザー権限管理

ユーザーに対して講座ごとのアクセス権を付与・剥奪する画面。`/admin/users` に対応。

## Todo

- [ ] `app/admin/users/page.tsx` を作成（Server Component）
  - `auth.users` からユーザー一覧を取得（email, role, id）
  - 各ユーザーに対してどの講座のアクセス権を持つか表示
- [ ] ユーザー詳細 / 権限編集
  - ユーザーごとに全講座のチェックリストを表示
  - チェック ON → `user_course_access` に insert
  - チェック OFF → `user_course_access` から delete
  - Server Action で処理し `revalidatePath('/admin/users')` を実行
- [ ] 管理者ロール付与・剥奪（任意）
  - `auth.users.role` を `'admin'` または `'user'` に変更する Server Action
