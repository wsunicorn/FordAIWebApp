# Phase 5 - Admin And Lead Flow

Date: 2026-06-07
Status: Done for local admin MVP

## Goal

Phase 5 adds the internal operating layer for anh Huynh Dang Huy and the dev
team. The public site can now collect leads, while admin can review, care for,
export and audit them.

This is still a lightweight MVP admin, not a full CRM. It is built to run on the
same FastAPI app with no paid services required.

## Implemented Admin Routes

| Route | Purpose |
| --- | --- |
| `/admin/login` | Admin login form. |
| `/admin/logout` | Clears admin session cookie. |
| `/admin` | Dashboard with lead counts, freshness counts, recent leads and audit logs. |
| `/admin/leads` | Lead inbox with status filter, search and CSV export link. |
| `/admin/leads/export.csv` | CSV export for current lead dataset. |
| `/admin/leads/{lead_id}` | Lead detail, contact shortcuts, status, internal note and follow-up fields. |
| `/admin/vehicles` | Vehicle/price admin list and source seed action. |
| `/admin/vehicles/{vehicle_id}` | Vehicle detail, variant edit and price freshness edit. |
| `/admin/content` | Promotion, FAQ and article content item management. |

## Authentication

Admin auth uses an HMAC-signed, HTTP-only cookie for the MVP.

Required production env vars:

```text
ADMIN_USERNAME=...
ADMIN_PASSWORD=...
SECRET_KEY=...
ADMIN_SESSION_TTL_SECONDS=43200
```

Before public production launch:

- Change `ADMIN_PASSWORD`.
- Change `SECRET_KEY`.
- Keep `APP_ENV=production` so the admin cookie is marked `Secure`.
- Put HTTPS in front of the app.

Future upgrade path:

- Real `admin_users` table.
- Password hash storage.
- Password reset.
- 2FA if the site starts receiving meaningful traffic.

## Lead Flow

Lead creation now writes:

- `lead.created` audit log.
- `notification.pending` audit log with target channels: admin, email, Zalo and Sheets.

Admin can:

- Filter leads by status.
- Search by name, phone, vehicle or area.
- Open lead detail.
- Update status.
- Add internal care note.
- Set follow-up datetime.
- Set last contacted datetime.
- Export CSV.

Current statuses:

```text
new, contacted, quoted, test_drive, won, lost
```

## Vehicle, Price And Freshness Flow

Admin can seed vehicle/price data from the Phase 4 source-backed seed in:

```text
app/data/site_content.py
```

Seed action upserts:

- Vehicles.
- Variants.
- Prices.
- Source URL.
- Source updated date.
- Review due date.
- Effective-to date for prices.
- Approval and freshness status.

Admin update actions write audit logs and a `cache.revalidate` audit event for
the affected public routes. FastAPI is server-rendered, so this is a local
freshness/audit hook now. Production CDN purge can attach to the same event
later.

## Content Flow

The new `content_items` table supports:

- Promotions.
- FAQ.
- Articles.

Each item stores:

- Kind.
- Title.
- Body.
- Source URL.
- Source updated date.
- Effective-to date.
- Review due date.
- Approval status.
- Freshness status.

Public pages still use Phase 4 seed data for now. Phase 6/7 can move public FAQ,
promotions and AI knowledge base reads to `content_items` after UAT.

## Database Changes

Migration:

```text
alembic/versions/20260607_0002_phase5_admin.py
```

Added to `leads`:

- `admin_note`
- `follow_up_at`
- `last_contacted_at`

Added to vehicles/prices:

- `review_due_at`

New table:

- `content_items`

## Implemented Files

| File | Purpose |
| --- | --- |
| `app/core/admin_auth.py` | HMAC admin session cookie helper. |
| `app/routers/admin.py` | Admin routes and form handlers. |
| `app/services/admin_service.py` | Admin queries, seed, update and audit helpers. |
| `app/templates/admin/*` | Admin login, shell, dashboard, leads, vehicles and content UI. |
| `app/models/content.py` | Content item model. |
| `app/static/css/input.css` | Admin UI component styles. |

## Validation Completed

Commands:

```powershell
npm run css:build
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

- CSS build passed.
- Alembic Phase 5 migration applied locally.
- Ruff passed.
- Pytest passed: 8 tests.
- Tests cover admin login gate, login success, dashboard, seed routes, CSV export
  and lead status update.

## Known Limits

- Notification is currently a pending audit/outbox event, not a real email/Zalo
  or Google Sheets integration.
- Public pages still read Phase 4 seed data, not admin database content.
- Admin auth is intentionally lean for MVP and must be hardened before public
  production launch.
- No role-based permissions yet.
