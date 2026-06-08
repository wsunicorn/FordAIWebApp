# Phase 8 - Launch And Operations

Status: In progress, deploy-ready baseline prepared; real production deploy pending host/domain credentials

Updated: 2026-06-08

## Goal

Move the local MVP into a public Docker/Python deployment path with production
guardrails, smoke tests and handover steps. Phase 8 is not complete until a real
host, domain, HTTPS, database, secrets, UAT and monitoring are confirmed.

## Completed In This Pass

- Added production settings guardrails for strong secrets, disabled debug,
  non-local `APP_URL` and PostgreSQL-only production database.
- Normalized provider database URLs from `postgres://...` or `postgresql://...`
  to `postgresql+psycopg://...` for SQLAlchemy async.
- Added optional app-level canonical redirects via `CANONICAL_REDIRECT`.
- Added baseline security headers and HTTPS HSTS in production.
- Added `/api/health/db` for database readiness checks.
- Added `scripts/start.sh` so Docker runs `alembic upgrade head` before Uvicorn.
- Updated Docker startup to read `${PORT:-8000}` and use proxy headers.
- Added `.dockerignore`.
- Updated `render.yaml` with Docker web service, PostgreSQL placeholder, health
  check path and secret env placeholders.
- Removed the real-looking AI key from `.env.example`.
- Added `scripts/smoke.py` for post-deploy checks.
- Updated local PowerShell scripts to use `.venv` when available.
- Added optional GA4 injection through `GA_MEASUREMENT_ID`.
- Added optional Sentry initialization through `SENTRY_DSN`.
- Created local ignored `.env.production.local` with generated production
  secrets and placeholders for provider keys.

## Production Env Vars Required

Set these on the host. Do not put real values in `.env.example`.

```text
APP_ENV=production
APP_DEBUG=false
APP_URL=https://<canonical-host>
CANONICAL_REDIRECT=false
SECRET_KEY=<strong 32+ chars>
DATABASE_URL=<provider postgres url>
DATABASE_ECHO=false
REVALIDATION_SECRET=<strong 32+ chars>
ADMIN_USERNAME=<admin username>
ADMIN_PASSWORD=<strong 32+ chars>
AI_PROVIDER=gemini
AI_API_KEY=<optional live Gemini key>
AI_DAILY_QUOTA=500
AI_MODEL=gemini-2.5-flash-lite
GA_MEASUREMENT_ID=<optional G-...>
SENTRY_DSN=<optional Sentry DSN>
SENTRY_TRACES_SAMPLE_RATE=0.1
```

After the canonical domain is final and redirects are tested:

```text
CANONICAL_REDIRECT=true
```

## Deploy Flow

1. Choose host: Render, Railway, Fly.io or VPS with Docker.
2. Create PostgreSQL production database.
3. Set all production env vars.
4. Deploy Docker app.
5. Confirm deploy logs show `alembic upgrade head`.
6. Run smoke test:

```powershell
.\.venv\Scripts\python.exe scripts\smoke.py https://<public-host> --check-db
```

7. Submit a real smoke lead only when acceptable:

```powershell
.\.venv\Scripts\python.exe scripts\smoke.py https://<public-host> --check-db --submit-lead
```

8. Open `/admin/login`, log in, verify lead/admin flows.
9. Run UAT script in `docs/PHASE_7_QA_AND_UAT.md` with anh Huy.
10. Configure domain, HTTPS, redirects, Search Console, analytics and uptime
    monitor.

## Pre-Deploy Checks

```powershell
.\scripts\check.ps1
.\.venv\Scripts\python.exe -m alembic current
```

Docker build check when Docker Desktop is running:

```powershell
docker build -t ford-ai-webapp:phase8 .
```

## Smoke Test Coverage

`scripts/smoke.py` checks:

- `/api/health`
- Optional `/api/health/db`
- Homepage canonical URL
- MVP logo asset and old wordmark absence
- Logo static serving as SVG
- `robots.txt` sitemap URL
- `sitemap.xml` canonical URLs
- Admin login `noindex`
- Optional lead API submission

## Still Blocked By External Info

- Public host choice/account access.
- Production PostgreSQL URL or managed database setup.
- Canonical domain decision: apex or `www`.
- DNS/Cloudflare access.
- Strong production secrets.
- Admin password to use in production.
- Gemini API key if live AI provider should be enabled.
- Analytics/Search Console account access.
- Uptime/error tracking provider choice.
- UAT approval from anh Huy on a real phone.

## Release Gate

Do not public-launch for SEO traffic until these are done:

- HTTPS is active.
- `APP_URL` equals the canonical public URL.
- `robots.txt` and `sitemap.xml` show the public canonical URL.
- Lead form works in production and a test lead appears in admin/export.
- Phone/Zalo/email links are verified.
- Admin password and secret keys are changed.
- UAT script is accepted by anh Huy.
- Backup/export path is confirmed.
