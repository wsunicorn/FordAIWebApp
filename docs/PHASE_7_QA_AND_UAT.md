# Phase 7 - QA And UAT

Date: 2026-06-08
Status: Done for local QA; external UAT and production checks pending

## Goal

Phase 7 hardens the local MVP before launch work. The scope is quality gates,
regression tests, responsive smoke checks, accessibility fixes and UAT script
readiness. Production deploy, custom domain, HTTPS, Search Console, analytics
and uptime/error monitoring remain Phase 8 launch operations.

## Fixes Completed

- Removed public use of the Ford logo from the header and replaced it with the
  custom `assets/brand/huy-dang-huy-logo.svg`.
- Removed external fallback image calls to Wikimedia, Unsplash and Placehold
  from public templates.
- Rewrote public copy that could imply an official Ford Vietnam website or a
  final commercial commitment.
- Added accessible labels for vehicle search, calculator controls, AI chat and
  AI handoff fields.
- Added safer validation handling for `/lead` form submissions.
- Removed production UI motion issues from source: `transition-all`, endless AI
  pulse, floating profile animation and aggressive vehicle image scale.
- Tightened mobile header and hero layout so CTA, text and navigation fit on
  mobile smoke viewports.

## Regression Coverage Added

`tests/test_app.py` now covers:

- SEO canonical and Open Graph URL for public pages.
- Admin login noindex.
- Public branding/media launch gates: no unapproved logo or external fallback
  media URLs in rendered pages.
- Static source quality gates for blocked media URLs and broad transition
  usage.
- Accessibility labels on Phase 7 surfaces.
- Public lead form success redirect and validation errors.
- API lead validation errors.
- Revalidation auth and `cache.revalidate` audit logging.
- Admin rejection of invalid lead status values.

## Local QA Commands

```powershell
npm run css:build
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m pytest -q
```

Results on 2026-06-08:

- CSS build passed.
- Alembic head check passed on local SQLite.
- Ruff passed.
- Pytest passed: 18 tests.

Pytest currently emits one third-party deprecation warning from FastAPI
TestClient/Starlette about future `httpx2` usage. It does not fail the suite.

## Browser Smoke

Local server:

```text
http://127.0.0.1:8001/
```

Opened for manual review through Windows Edge protocol:

```text
microsoft-edge:http://127.0.0.1:8001/
```

Headless browser screenshots were generated in:

```text
docs/qa-artifacts/
```

Artifacts:

- `phase7-home-desktop.png`
- `phase7-home-mobile.png`
- `phase7-vehicles-desktop.png`
- `phase7-ai-mobile.png`

Chrome headless on this Windows environment has a minimum practical viewport
around 482px, so final mobile artifacts use a 500px-wide smoke viewport. The
layout still exercises mobile navigation and bottom CTA behavior.

## Remaining UAT Script

Anh Huy should validate on a real phone before launch:

1. Open homepage and confirm name, title, phone, Zalo and dealership text.
2. Open `/xe` and one vehicle detail page.
3. Confirm vehicle/price/source wording is acceptable.
4. Submit a quote test lead.
5. Confirm the lead appears in admin.
6. Run on-road and loan calculators with a real customer scenario.
7. Ask AI a common question.
8. Ask AI for final price or stock and confirm it hands off.
9. Confirm there is no checkout, deposit or hold-car flow.
10. Confirm wording does not imply this is an official Ford Vietnam website.

## Not Closed In Phase 7

- Real lead notifications to email/Zalo/Google Sheets.
- Production host, HTTPS and canonical redirects.
- Analytics/Search Console.
- Lighthouse or field LCP/CLS/INP numbers on production.
- Uptime/error monitoring.
- Backup automation.
- Written permission for official Ford/dealer media.
