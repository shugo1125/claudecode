# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev      # Start development server at localhost:3000
npm run build    # Production build
npm run lint     # Run ESLint
```

No test runner is configured yet.

## Architecture

This is a **Next.js 16 App Router** project (React 19, TypeScript, Tailwind CSS v4) bootstrapped with `create-next-app`. It is in an early/empty state — only the default scaffold exists.

- `app/` — App Router root. `layout.tsx` defines the root layout with Geist fonts; `page.tsx` is the home page.
- `app/globals.css` — Global styles (Tailwind entry point).
- Path alias `@/*` maps to the repo root.

Tailwind CSS v4 is used via `@tailwindcss/postcss` (PostCSS plugin approach, no `tailwind.config` file).

## Product Overview

Udemy-style online course platform using YouTube-hosted videos. Target users: engineers and non-engineers who want to develop with AI.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / Backend | Next.js App Router |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth — Google OAuth only |
| Video | YouTube embed (`youtube-nocookie.com`) |
| Deploy | Vercel |

## Route Structure

```
/                               # Course listing (top page)
/login                          # Google OAuth login
/courses/[slug]                 # Course detail + curriculum
/courses/[slug]/lessons/[id]    # Video player page
/admin                          # Admin top
/admin/courses                  # Course CRUD
/admin/courses/[id]/edit        # Section & lesson CRUD, reorder
/admin/users                    # User list + per-course access grant/revoke
```

## Data Model (Supabase)

3-tier hierarchy: **Course → Section → Lesson**

- `courses`: id, title, slug, description, thumbnail_url, is_published
- `sections`: id, course_id, title, order
- `lessons`: id, section_id, title, youtube_url, order, is_free
- `user_course_access`: user_id, course_id, granted_at  ← admin-managed
- `lesson_progress`: user_id, lesson_id, watched_at (unique per pair)

## Access Control

| State | Access |
|---|---|
| Not logged in | First lesson of each course only (`is_free = true`) |
| Logged in, no access grant | First lesson only |
| Logged in + access granted | All lessons in that course |

- Access is per-course; having access to Course A does not grant Course B.
- Admin identified by `role` column in Supabase; `/admin` routes are protected by this.

## Next.js Best Practices

### Server vs Client Components
- **Default to Server Components.** Add `'use client'` only when the component needs browser APIs, event handlers, or React hooks (`useState`, `useEffect`, etc.).
- Keep Client Components as leaf nodes — push `'use client'` as far down the tree as possible.
- Data fetching belongs in Server Components or Route Handlers, not in Client Components with `useEffect`.

### Data Fetching
- Fetch data in `page.tsx` / `layout.tsx` (Server Components) and pass as props; avoid prop-drilling through many layers by co-locating fetches close to where data is consumed.
- Use `next/cache` (`revalidatePath`, `revalidateTag`) after mutations instead of full page reloads.
- Prefer **Server Actions** (`'use server'`) for form submissions and mutations over separate API routes.

### Routing & Layouts
- Use route groups `(group)` to share layouts without affecting the URL (e.g., `(user)` vs `(admin)`).
- Place loading UI in `loading.tsx` and error boundaries in `error.tsx` alongside each `page.tsx`.
- Use `middleware.ts` at the root for auth-gating (redirect unauthenticated users before the page renders).

### Performance
- Use `next/image` for all images (automatic optimization, lazy loading).
- Use `next/link` for all internal navigation.
- Prefer `generateStaticParams` for dynamic routes that can be statically rendered (e.g., `/courses/[slug]`).

### TypeScript
- Strict mode is enabled — no `any`, no `// @ts-ignore` without a comment explaining why.
- Type Supabase query results; use the generated types from `supabase gen types typescript`.

## MVP Scope

**In scope:** Auth (Google OAuth), course/section/lesson CRUD in admin, video playback page, access control, manual watched-status checkbox per lesson, user access grant/revoke in admin.

**Out of scope (Phase 2):** Stripe payments, progress bar, completion certificate, resume-playback, comments/Q&A, email notifications.
