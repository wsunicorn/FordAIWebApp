# Phase 4 - Public Website MVP

Date: 2026-06-07
Status: Done for local MVP

## Goal

Phase 4 turns the FastAPI foundation into a public consultation website for
anh Huynh Dang Huy at Dong Thap Ford.

The site is intentionally not an ecommerce website. It helps visitors:

- Understand available Ford model groups.
- Review reference prices and assumptions.
- Compare model groups quickly.
- Estimate on-road cost and installment scenarios.
- Send quote, test-drive or contact requests to anh Huy.

Final price, stock, color, promotion, delivery timeline, loan approval and
paperwork must be confirmed directly by anh Huy.

## Implemented Public Routes

| Route | Purpose |
| --- | --- |
| `/` | Consultation-first homepage with hero, featured vehicles, process and lead form. |
| `/anh-huy` | Profile page for anh Huy, role, contact channels and trust framing. |
| `/xe` | Vehicle list with lightweight search/filter. |
| `/xe/{slug}` | Vehicle detail page with variants, reference prices and lead CTA. |
| `/so-sanh` | Quick comparison table for vehicle groups. |
| `/bang-gia` | Source-backed reference price table. |
| `/uu-dai` | Promotion/offer groups that require direct confirmation. |
| `/du-toan-lan-banh` | On-road cost estimator using documented assumptions. |
| `/du-toan-tra-gop` | Installment estimator using client-side JavaScript. |
| `/bao-gia` | Quote request form. |
| `/lai-thu` | Test-drive request form. |
| `/lien-he` | Contact page with phone, Zalo, email, Facebook and form. |
| `/faq` | Common questions and conservative answers. |
| `/robots.txt` | Search crawler directives. |
| `/sitemap.xml` | XML sitemap for public routes. |

## Data Source And Freshness

Seed vehicle and price data live in:

```text
app/data/site_content.py
```

Current source metadata:

- Primary price source: https://dongthapford.com/bang-gia-xe/
- Displayed source period: `6/2026`
- Source checked date: `2026-06-07`
- Source rechecked during Phase 4 against the live official price page.

Public copy must always show that price/promotion/calculator results are
reference information only. Anh Huy must confirm current details before the
customer makes a buying decision.

Future Phase 5/6 work should move this seed data into admin-managed database
tables with `source_url`, `effective_from`, `effective_to`, `review_due_at`,
`approval_status` and audit logs.

## Visual And Interaction Notes

The MVP uses:

- Server-rendered Jinja templates for SEO and low runtime complexity.
- Tailwind CSS v4 compiled into one static stylesheet.
- Vanilla JavaScript for progressive interactions only.
- A real approved portrait of anh Huy.
- Custom project wordmark instead of Ford/dealer logo.

Official Ford/dealer logos, showroom photos, catalogue files and vehicle media
remain a release gate until there is a saved permission record. Public pages
therefore use structured content and neutral media placeholders for vehicle
surfaces.

## Implemented Components

| File | Purpose |
| --- | --- |
| `app/templates/base.html` | Shared layout, navigation, SEO metadata and footer. |
| `app/templates/components/forms.html` | Reusable lead form macro. |
| `app/templates/components/vehicle_card.html` | Reusable vehicle card macro. |
| `app/static/css/input.css` | Tailwind source with component classes. |
| `app/static/js/app.js` | Lead success notice, mobile nav, search and calculators. |
| `app/routers/pages.py` | Public page routing, lead form POST, robots and sitemap. |

## Validation Completed

Commands:

```powershell
npm run css:build
.\.venv\Scripts\python.exe -m ruff check app tests
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

- CSS build passed.
- Ruff passed.
- Pytest passed: 5 tests.
- Tests cover health, homepage, all Phase 4 public routes, vehicle 404,
  `robots.txt` and `sitemap.xml`.
- Local Uvicorn HTTP smoke passed for public routes, `/api/health`, lead form
  redirect and source period display.

## Known Limits

- Lead forms currently create database leads through the existing Phase 3
  service, but there is not yet an admin lead dashboard.
- Calculators are estimates for consultation, not legal/financial quotes.
- Prices and promotions are seed data and need a freshness/admin workflow before
  serious production traffic.
- No official vehicle media is published until permission is confirmed.
- Final production host/domain, Search Console and monitoring belong to Phase 8.
