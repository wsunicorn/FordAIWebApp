# Operations And Deployment

## Environment Strategy

| Environment | Purpose |
| --- | --- |
| Local | Development |
| Preview/Staging | Review and UAT |
| Production | Public website |

Each environment needs separate:

- Environment variables.
- Database/project.
- AI keys.
- Storage buckets.
- Analytics IDs.

## Free/Low-cost Deployment Policy

Use free tier only when:

- Terms allow the intended public lead-generation use.
- Quota is enough for expected traffic.
- Data can be exported.
- Upgrade path is clear.
- There is a fallback if quota is exceeded.

Before launch, verify terms for:

- Hosting/deploy platform.
- PostgreSQL/hosting database plan.
- AI provider.
- Email provider.
- Analytics/tracking.

## Recommended MVP Setup

- Hosting: Docker/Python host for FastAPI, with Cloudflare DNS/CDN later.
- Database/Auth/Storage: PostgreSQL production database; local dev uses SQLite.
- AI: provider adapter with free-tier testing and usage caps.
- Notification: email webhook, Zalo deep link, Google Sheets optional.
- Analytics: GA4 and Search Console.
- Error tracking: Sentry free tier or platform logs.

## Phase 0 Hosting Decision

Temporary production URL from Phase 0: `https://huy-ford-dong-thap.pages.dev`.

Phase 3 stack changed to FastAPI, so the MVP app now needs a Python/Docker runtime. Cloudflare Pages can remain a parked/redirect/static placeholder or DNS/CDN layer, but it is no longer the primary FastAPI app host.

When a paid/custom domain is ready:

- Set the custom domain as canonical.
- Redirect `https://huy-ford-dong-thap.pages.dev` to the canonical host.
- Update sitemap, robots, canonical URLs, Open Graph URLs and Search Console property.
- Keep the temporary URL as a fallback only if it does not create duplicate-indexing risk.

## Host Selection And Production Readiness

The host is not considered ready until it supports:

- Public HTTPS domain.
- Preview deploys for every change.
- Separate production environment variables.
- CDN delivery for public pages/assets.
- Redirect rules for canonical domain and old URLs.
- Header rules for cache and security.
- Build logs and rollback path.
- Documented quota and commercial terms.
- Clear upgrade path when traffic grows.

Before public launch, create or verify:

- Canonical domain decision: apex or `www`.
- Redirect from the non-canonical host.
- `robots.txt` with sitemap URL.
- `sitemap.xml` with absolute canonical URLs.
- Search Console property and sitemap submission.
- Production smoke test script.
- Emergency fallback contact block if forms or AI fail.

Detailed host, traffic and freshness rules live in [HOSTING_TRAFFIC_AND_FRESHNESS.md](HOSTING_TRAFFIC_AND_FRESHNESS.md).

## Backup

Minimum:

- Weekly database export during MVP, with off-site copy.
- Backup before schema migration.
- Export leads before major release.
- Store content source files outside the app.
- Test restore/export at least once before launch.

Production with budget:

- Daily automatic backups.
- Point-in-time recovery if available.
- Separate storage backup for media/documents.

## Monitoring

Track:

- Website uptime.
- Lead form failures.
- AI errors.
- AI quota/cost.
- Slow pages.
- Core Web Vitals: LCP, INP, CLS.
- Cache/revalidation failures.
- Content freshness: expired prices/promotions/AI documents.
- 404s.
- Admin login failures.

Alert priority:

| Issue | Priority |
| --- | --- |
| Website down | Critical |
| Lead form broken | Critical |
| Wrong phone/Zalo shown | Critical |
| AI down but forms work | High |
| Expired price/promotion visible | High |
| Sitemap/robots blocked or broken | High |
| Admin content bug | Medium |
| Minor visual issue | Low |

## Release Process

1. Merge changes.
2. Run lint/tests/build.
3. Deploy preview.
4. Smoke test public pages.
5. Smoke test lead form.
6. Verify sitemap, robots, canonical URL and redirects.
7. Verify cache/revalidation behavior for updated content.
8. UAT by anh Huy for content-sensitive changes.
9. Deploy production.
10. Verify analytics, lead notification, Search Console sitemap and uptime monitor.

Current Phase 8 local command:

```powershell
.\scripts\check.ps1
.\.venv\Scripts\python.exe -m alembic current
```

Post-deploy smoke test:

```powershell
.\.venv\Scripts\python.exe scripts\smoke.py https://<public-host> --check-db
```

Use `--submit-lead` only when it is acceptable to create a real test lead in
production.

## Handover

Prepare:

- Admin login instructions.
- How to update price/promotion.
- How to review leads.
- How to update AI documents.
- How to export leads.
- What to do when AI quota runs out.
- Who to contact for technical support.

## Monthly Maintenance

- Review prices/promotions.
- Review expired AI documents.
- Check backup restore.
- Review leads and conversion.
- Check Search Console issues.
- Review AI failure cases.
- Patch dependencies.

## Weekly Freshness Maintenance

- Review records with `review_due_at` in the next 7 days.
- Expire promotions past `effective_to`.
- Confirm high-traffic vehicle pages still show current source/date.
- Re-index approved AI documents after content updates.
- Revalidate affected public pages after price/promotion/article changes.
- Send freshness report to anh Huy.

## Traffic Review Cadence

Weekly during first month after launch:

- Review page views, lead conversion and top traffic sources.
- Review LCP/INP/CLS on mobile.
- Review 404s and redirect needs.
- Review AI quota and form spam.
- Update FAQ/content for recurring customer questions.

Monthly after stable operation:

- Review SEO queries in Search Console.
- Update content calendar.
- Check provider free-tier usage.
- Decide whether paid hosting/database/AI is needed.
