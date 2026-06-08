# Hosting, Traffic And Freshness Plan

## Purpose

This document defines how the website moves from development to a public hosted site, how it handles internet traffic, and how vehicle/price/promotion information stays fresh after launch.

The website is a consultation and lead-generation site. Traffic optimization means the site stays fast, searchable, resilient and accurate, not that it supports online checkout.

## Hosting Decision Matrix

| Requirement | MVP target | Notes |
| --- | --- | --- |
| Public HTTPS domain | Required | Domain must be owned by the project/owner. |
| CDN edge delivery | Required | Static assets and public pages should be served near users. |
| Preview deploys | Required | Every change should be reviewed before production. |
| Environment variables | Required | Separate local, preview and production secrets. |
| Build cache | Recommended | Speeds up deploys and reduces failed build friction. |
| Redirect/header rules | Required | Canonical host, old URLs, cache headers and security headers. |
| Commercial terms | Required | Free tier must allow public lead-generation use. |
| Export path | Required | Content, leads and database must be exportable. |
| Upgrade path | Required | Clear move to paid plan when quota or SLA requires it. |

Recommended MVP:

- Use a Docker/Python host for FastAPI, such as Render/Railway/Fly.io/VPS or equivalent low-cost platform.
- Use PostgreSQL for production; Supabase/Neon/managed Postgres/VPS Postgres are all acceptable options.
- Use Cloudflare for DNS/CDN/WAF when a custom domain is available.
- Use domain-level analytics plus GA4/Search Console.
- Use a provider adapter for AI so quota/provider can change without rewriting the app.

Before choosing a host, verify current limits and commercial terms on the provider's official docs.

## Phase 0 URL And Host

Temporary production URL: `https://huy-ford-dong-thap.pages.dev`.

Canonical strategy:

- During MVP preview/public test, `pages.dev` can be the temporary public URL.
- When a paid/custom domain is selected, the custom domain becomes canonical.
- The temporary URL should redirect to the canonical domain after Search Console and sitemap are moved.
- All absolute URLs in sitemap, canonical tags, Open Graph and structured data must use the current canonical host.

This decision closes Phase 0 for URL planning, but does not replace the need for a final custom domain before serious SEO work.

## Production Deployment Checklist

- [x] Temporary URL selected: `https://huy-ford-dong-thap.pages.dev`.
- [x] Phase 0 temporary URL selected on Cloudflare Pages.
- [x] Phase 3 selected FastAPI, so the app host must be Docker/Python runtime.
- [ ] Final custom domain selected and owned by project/owner.
- [ ] DNS configured with canonical `www` or apex decision.
- [ ] HTTPS active.
- [ ] Redirect non-canonical host to canonical host.
- [ ] `robots.txt` includes sitemap URL.
- [ ] `sitemap.xml` generated with absolute canonical URLs.
- [ ] Sitemap submitted in Google Search Console.
- [ ] Environment variables separated for preview and production.
- [ ] Production PostgreSQL database separated from local/dev SQLite.
- [ ] Database backup/export process tested.
- [ ] Lead form tested in production.
- [ ] Zalo/phone/email links verified.
- [ ] Analytics and conversion events verified.
- [ ] Error tracking/log drain verified.
- [ ] Uptime monitor configured.
- [ ] AI quota and fallback tested.
- [ ] Admin login tested with least privilege.
- [ ] Security headers configured.

Phase 8 deploy-readiness now includes:

- Docker startup script that runs Alembic migrations before Uvicorn.
- Render blueprint baseline with Docker web service and managed PostgreSQL placeholder.
- Production settings validation for strong secrets, non-local `APP_URL`, disabled debug and PostgreSQL.
- `/api/health/db` for database readiness.
- `scripts/smoke.py` for post-deploy verification.

## Traffic Optimization Strategy

### Static-first pages

Use static or incrementally revalidated pages for:

- Home.
- Vehicle listing.
- Vehicle detail.
- Promotions.
- FAQ/articles.

Use dynamic rendering only for:

- Admin screens.
- Authenticated lead management.
- AI chat/session endpoints.
- Fresh server-only actions.

### Cache and revalidation

Recommended cache model:

| Data type | Cache strategy | Revalidation |
| --- | --- | --- |
| Sales profile | Static/ISR | Revalidate after admin update |
| Vehicle list | Static/ISR | Revalidate after vehicle update |
| Vehicle detail | Static/ISR | Revalidate after vehicle/price/promo update |
| Promotions | Static/ISR | Revalidate after promo update and expiry job |
| Articles/FAQ | Static/ISR | Revalidate after publish/update |
| Lead forms | No cache for mutation | Always server-side validate |
| Admin | No public cache | Authenticated dynamic |
| AI chat | No public cache | Rate-limited dynamic |

Implementation notes:

- Use FastAPI audit hooks for admin content updates.
- If CDN/static caching is enabled, connect `/api/revalidate` to CDN purge or static rebuild logic.
- Test production cache behavior on the actual Docker/Python host, not only local Uvicorn dev mode.
- Do not serve stale price/promotion/AI content silently; mark it review_due/expired or route to anh Huy.

### Asset optimization

- Use WebP/AVIF images.
- Store image dimensions or aspect ratios to prevent CLS.
- Compress hero images carefully because they affect LCP.
- Lazy-load below-fold images.
- Do not lazy-load the LCP hero image.
- Use a CDN-backed image path.
- Avoid heavy third-party scripts before first interaction.

### API and AI protection

- Rate limit lead forms and AI endpoints.
- Add spam protection after traffic appears, or earlier if forms are abused.
- Debounce duplicate lead submissions.
- Add AI daily/monthly quota.
- When AI quota is exceeded, show form + phone/Zalo fallback.
- Log failed notification delivery.

## SEO And Internet Visibility

Minimum launch SEO:

- Unique title and description for each key page.
- Canonical URL per page.
- Sitemap at site root.
- `robots.txt` references sitemap.
- Structured data for local business/person where legally appropriate.
- Vehicle/article pages use descriptive slugs.
- Open Graph image for social sharing.
- Search Console property verified.
- 404 page and redirects for renamed URLs.

Ongoing SEO:

- Publish local content around Ford models, Dong Thap registration, on-road cost, test-drive guidance and finance questions.
- Update high-traffic pages when price/promotion/source changes.
- Review Search Console monthly for indexing errors and queries.
- Avoid duplicate pages with only tiny content differences.

## Freshness Model

Every public data record that can become outdated needs:

- `source`
- `verified_by`
- `verified_at`
- `effective_from`
- `effective_to`
- `review_due_at`
- `approval_status`

Freshness statuses:

| Status | Meaning | Public behavior |
| --- | --- | --- |
| `fresh` | Verified and within review window | Show normally with update date |
| `review_due` | Still visible but needs review | Show note and notify admin |
| `expired` | No longer reliable | Hide from active surfaces or show unavailable |
| `conflicting` | Sources disagree | Do not let AI answer as fact, handoff to anh Huy |

## Official Source Tracking

Primary source site: https://dongthapford.com/.

Tracked sitemaps:

- https://dongthapford.com/sitemap_index.xml
- https://dongthapford.com/page-sitemap.xml
- https://dongthapford.com/product-sitemap.xml
- https://dongthapford.com/post-sitemap.xml

In production, the app should not blindly mirror source changes. Sitemap changes create review tasks. Only approved updates should revalidate public pages and AI documents.

## Freshness Automation

Daily scheduled job:

- Find price/promotion/AI documents past `effective_to`.
- Mark as `expired`.
- Remove expired content from active promotion surfaces.
- Exclude expired documents from RAG.
- Notify admin/anh Huy.
- Revalidate affected public paths.

Weekly scheduled job:

- Find records with `review_due_at` within 7 days.
- Notify admin/anh Huy.
- Generate freshness report.

After admin update:

- Record audit log.
- Set approval status.
- Update `verified_at` and `review_due_at`.
- Trigger revalidation for affected pages.
- Re-index affected AI documents if approved.

## Freshness Report

Weekly report should include:

- Active prices by model and update date.
- Promotions expiring in the next 7 days.
- Expired records hidden from public pages.
- AI documents due for review.
- Pages revalidated this week.
- Top lead sources and high-traffic pages.
- Search Console issues if available.

## Traffic Scaling Triggers

Move from free/low-cost MVP to paid/scaled setup when any happens:

- Lead form or AI endpoint hits provider quota.
- Public traffic causes slow LCP/INP or failed deploys.
- Need SLA for production uptime.
- Need daily automatic backups or point-in-time recovery.
- Need custom email delivery reputation.
- Need advanced CRM or multi-sales permissions.
- AI cost/quality requires paid provider.

## Incident Playbook

### Website down

1. Check hosting status and latest deploy.
2. Roll back to last working deploy if needed.
3. Verify DNS/HTTPS.
4. Post temporary contact link if available.

### Lead form broken

1. Disable broken flow if it causes data loss.
2. Show direct phone/Zalo fallback.
3. Check server logs, database, notification provider.
4. Test production submission.
5. Export and recover any partial leads.

### Outdated/wrong price shown

1. Hide or mark affected price as needing confirmation.
2. Notify anh Huy.
3. Update source and effective date.
4. Purge CDN/rebuild affected pages if caching is enabled.
5. Check AI documents for the same outdated data.

### AI gives unsafe answer

1. Disable AI or route to handoff mode.
2. Save conversation ID.
3. Update prompt/guardrail/test case.
4. Remove or correct bad source.
5. Re-test before enabling.

## Source Notes Checked On 2026-06-07

- FastAPI requires an ASGI server such as Uvicorn or an equivalent production runner.
- Tailwind CSS is built through the Tailwind CLI and served as a static CSS asset.
- Docker deployment keeps the FastAPI runtime portable across Render/Railway/Fly.io/VPS-style hosts.
- PostgreSQL providers should support regular export/backup; verify backup/PITR terms before production.
- Google recommends sitemaps with absolute canonical URLs, accurate `<lastmod>`, Search Console submission or `robots.txt` reference.
