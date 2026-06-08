# Technical Architecture

## Current Stack

Phase 3 was changed by project owner request from Next.js to a Python/FastAPI stack.

| Layer | MVP choice | Upgrade path |
| --- | --- | --- |
| Web server | FastAPI | Keep for API/admin/AI endpoints |
| HTML rendering | Jinja2 templates | Add HTMX or selective JS only if workflow needs it |
| Styling | Tailwind CSS v4 CLI | Add design tokens/components as CSS layers |
| Client behavior | Vanilla JavaScript | Add focused libraries only for real complexity |
| Database ORM | SQLAlchemy 2 async | Keep with PostgreSQL |
| Migrations | Alembic | Required for every schema change |
| Local database | SQLite via `aiosqlite` | Dev only |
| Production database | PostgreSQL via `psycopg` | Supabase/Neon/managed Postgres/VPS Postgres |
| AI | Gemini adapter with grounded fallback | Swap model/provider by env when budget or quality needs change |
| Deployment | Docker FastAPI host | Render/Railway/Fly/VPS, Cloudflare DNS/CDN |
| Analytics | GA4/Search Console later | Server-side events and CRM attribution |

## MVP Architecture

```text
Browser
  |
  | HTTPS
  v
FastAPI app
  |-- Jinja public pages
  |-- Admin HTML pages
  |-- JSON API routes
  |-- Static assets: Tailwind CSS, JS, images
  |-- AI adapter later
  |
  v
Database
  |-- SQLite local dev
  |-- PostgreSQL production
  |
  v
Integrations
  |-- Phone/Zalo deep links
  |-- Email/notification later
  |-- Google Sheets/CRM optional
  |-- AI provider
```

## Phase 3 App Files

- `app/main.py`: FastAPI app factory, static mounts and router registration.
- `app/routers/pages.py`: Jinja pages and HTML form lead submission.
- `app/routers/admin.py`: admin login, dashboard, lead, vehicle, price and content management.
- `app/routers/api.py`: health, lead API, AI API and protected revalidation hook.
- `app/core/admin_auth.py`: HMAC signed-cookie admin auth for MVP.
- `app/services/ai_service.py`: grounded AI retrieval, tools, guardrails, handoff and logs.
- `app/templates/`: server-rendered HTML.
- `app/static/css/input.css`: Tailwind source.
- `app/static/css/styles.css`: generated CSS.
- `app/static/js/app.js`: lightweight client behavior.
- `app/models/`: SQLAlchemy models.
- `alembic/`: database migrations.
- `Dockerfile`: production container baseline.

## Core Database Entities

Current migrations through Phase 6:

```text
vehicles
vehicle_variants
vehicle_prices
leads
content_items
ai_documents
ai_conversations
ai_messages
ai_feedback
audit_logs
```

Planned expansions:

```text
sales_profiles
vehicle_specs
vehicle_media
promotions
registration_fees
loan_assumptions
lead_activities
test_drive_requests
ai_document_chunks
consent_records
admin_users
```

## Lead Flow

```text
User submits quote/test-drive/contact form
  -> FastAPI validates form/API payload with Pydantic
  -> SQLAlchemy creates lead
  -> Audit log records lead creation
  -> Audit log records notification.pending for admin/email/Zalo/Sheets adapter
  -> Page redirects to success state
  -> Future: deliver pending notifications by email/Zalo/Sheets
```

## Admin Flow

```text
Admin opens /admin
  -> Signed admin cookie is checked
  -> If missing/invalid, redirect to /admin/login
  -> Admin reviews dashboard, leads, vehicle data and content freshness
  -> Updates write audit logs
  -> Vehicle/price/content updates write cache.revalidate audit events
```

Phase 5 admin is an MVP gate, not final enterprise auth. Production launch must
set strong `ADMIN_PASSWORD`, strong `SECRET_KEY`, HTTPS and `APP_ENV=production`.

## Freshness And Cache Flow

FastAPI does not use Next.js `revalidatePath` or `revalidateTag`.

MVP freshness flow:

```text
Admin/source update happens
  -> Write audit log
  -> Mark affected data freshness status
  -> Rebuild/purge CDN cache if production cache is enabled
  -> Notify admin/anh Huy if data is stale or expired
```

Current Phase 3 includes `/api/revalidate` as a protected audit hook. Phase 5/8 should connect it to real cache purge or static rebuild logic depending on final host.

## AI Flow

```text
User asks question
  -> /api/ai/chat logs the user message
  -> AI service retrieves approved/fresh ai_documents
  -> Guardrail detector classifies high-risk sales intents
  -> Calculator tools answer on-road or loan estimate questions
  -> Assistant answer is logged with sources, tool and risk flags
  -> /api/ai/handoff creates a lead when human confirmation is needed
  -> /api/ai/feedback records simple feedback
```

Current Phase 6 provider is `gemini` with `gemini-2.5-flash-lite` by default.
`app/services/ai_service.py` keeps deterministic retrieval, calculator tools
and guardrails before the provider call. If Gemini fails or is not configured,
the endpoint falls back to the internal grounded answer while keeping the same
logs and handoff behavior.

## Security Baseline

- Environment variables are never committed.
- `SECRET_KEY` and `REVALIDATION_SECRET` must be changed before production.
- Public form/API validation uses Pydantic.
- Admin routes need authentication before public launch.
- Phase 5 admin routes use HMAC signed HTTP-only cookies.
- Rate limit public forms and AI endpoint before public launch.
- AI must keep source, freshness and handoff guardrails when a paid provider is added.
- Store consent timestamp for public leads in Phase 5.
- Audit important admin and freshness actions.
- Use PostgreSQL backups before production changes.

## Performance Baseline

- Use server-rendered HTML for public pages.
- Serve compiled Tailwind CSS from `/static`.
- Keep JavaScript small and progressive.
- Use approved/local images with stable dimensions.
- Put Cloudflare CDN in front when a custom domain is available.
- Use Docker production server with multiple workers only after measuring need.

## Deployment Direction

FastAPI requires a Python runtime, so Cloudflare Pages is not the primary app host anymore.

Recommended:

- Docker deploy to Render/Railway/Fly.io for MVP.
- Or deploy to a small VPS with Caddy/Nginx, HTTPS, Docker and backups.
- Use Cloudflare for DNS, CDN and WAF when a custom domain is selected.

Before public launch:

- Configure canonical domain and HTTPS.
- Use production PostgreSQL.
- Run migrations.
- Configure secrets.
- Add monitoring/error logging.
- Add database backup/export.
- Submit sitemap/Search Console after public pages exist.
