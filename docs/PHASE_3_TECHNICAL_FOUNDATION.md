# Phase 3 - Technical Foundation

Date: 2026-06-07
Status: Done for FastAPI foundation

## Stack Decision

The previous Next.js scaffold was removed per project owner request. Phase 3 now uses:

- Python 3.11
- FastAPI
- Jinja2 server-rendered templates
- Tailwind CSS v4 CLI
- Vanilla JavaScript
- SQLAlchemy 2 async
- Alembic migrations
- SQLite for local development
- PostgreSQL-compatible `DATABASE_URL` for production
- Docker deployment baseline

This keeps the website simple, fast and SEO-friendly while still allowing API routes for leads, AI, admin and future integrations.

## Created Structure

```text
app/
  main.py
  core/
  db/
  models/
  routers/
  schemas/
  services/
  static/
    css/
    js/
  templates/
alembic/
tests/
scripts/
Dockerfile
render.yaml
pyproject.toml
requirements.txt
requirements-dev.txt
package.json
```

## Runtime Routes

| Route | Type | Purpose |
| --- | --- | --- |
| `/` | HTML | FastAPI/Jinja home foundation with anh Huy contact and lead form. |
| `/admin` | HTML | Admin foundation placeholder for Phase 5. |
| `/lead` | HTML form POST | Creates a lead and redirects to success state. |
| `/api/health` | JSON | Health check. |
| `/api/leads` | JSON POST | Creates a lead from API clients. |
| `/api/revalidate` | JSON POST | Protected freshness/cache audit hook. |

## Database Foundation

Local development uses:

```text
sqlite+aiosqlite:///./local.db
```

Production should use PostgreSQL:

```text
postgresql+psycopg://USER:PASSWORD@HOST:PORT/DB
```

Alembic migration `20260607_0001_phase3_foundation.py` creates:

- `vehicles`
- `vehicle_variants`
- `vehicle_prices`
- `leads`
- `audit_logs`

The schema is intentionally lean for Phase 3. Phase 5 can expand admin/auth tables and Phase 6 can add AI document/chunk tables.

## Tailwind And Assets

Tailwind source:

```text
app/static/css/input.css
```

Generated CSS:

```text
app/static/css/styles.css
```

Commands:

```powershell
npm install
npm run css:build
```

JavaScript entry:

```text
app/static/js/app.js
```

Current JS only enhances the lead success state. Public interactions should stay lightweight unless a real workflow requires more.

## Development Commands

Create/install Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Run migrations:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

Run dev server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or:

```powershell
.\scripts\dev.ps1
```

Run checks:

```powershell
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m pytest
npm audit --audit-level=moderate
```

## Deployment Baseline

FastAPI requires a Python server runtime. Cloudflare Pages is no longer the primary app host for this stack.

Recommended MVP host options:

- Render/Railway/Fly.io using Docker.
- A small VPS with Docker, Caddy/Nginx, HTTPS and backups.
- Cloudflare can still be used for DNS/CDN/WAF in front of the FastAPI host.

Files prepared:

- `Dockerfile`
- `render.yaml`

Before production:

- Set `APP_ENV=production`.
- Set `APP_DEBUG=false`.
- Set strong `SECRET_KEY` and `REVALIDATION_SECRET`.
- Use PostgreSQL instead of SQLite.
- Configure HTTPS/canonical domain.
- Add backup/export job.
- Add uptime/error monitoring.

## Validation Completed

- Removed Next.js scaffold and old Node app files.
- Installed Python dependencies in `.venv`.
- Installed Tailwind CLI dependencies with npm.
- Built Tailwind CSS.
- Ran Alembic migration against local SQLite.
- Verified `/api/health`.
- Verified API lead creation.
- Ran Ruff successfully.
- Ran Pytest successfully: 2 tests passed.
- Ran npm audit successfully: 0 vulnerabilities.

## Known Notes

- `local.db` is a generated development database and is ignored by `.gitignore`.
- TestClient currently emits a Starlette deprecation warning recommending `httpx2`; it does not break tests.
- Official Ford/dealer media permission remains a release gate before public launch.
