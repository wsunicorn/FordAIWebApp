# QA And Acceptance

## Test Layers

| Layer | What to test |
| --- | --- |
| Unit | Calculator formulas, validators, formatting helpers |
| Integration | Lead creation, notifications, PostgreSQL writes, AI tools |
| UI | Forms, navigation, responsive layout, admin flows |
| Accessibility | Keyboard, focus, contrast, labels, reduced motion |
| Performance | LCP, CLS, INP, image size, JS bundle |
| AI | Grounding, guardrails, handoff, refusal cases |
| UAT | Anh Huy validates content, price notes, lead process |

## MVP Acceptance Criteria

- [x] Public pages work on mobile and desktop locally.
- [x] Home page clearly states this is anh Huy's consultation channel.
- [x] No checkout, cart, deposit or payment flow exists in MVP.
- [x] Vehicle data displays source and update date where relevant.
- [x] Quote/test-drive/contact forms create leads.
- [ ] Lead notification reaches anh Huy or configured channel.
- [x] Admin can update vehicles, prices, promotions and content locally.
- [x] Calculator results match local approved smoke cases.
- [x] AI passes core evaluation set.
- [x] AI hands off for final price, inventory, deposit and loan approval.
- [x] SEO metadata exists for key pages.
- [ ] Analytics tracks key CTA and form conversions.
- [ ] Backup and handover docs exist.
- [ ] Production host has HTTPS, canonical redirect, sitemap and robots.
- [ ] Search Console is configured and sitemap is submitted.
- [ ] Cache/revalidation works after admin updates price, vehicle and article data.
- [ ] Expired promotions are hidden or marked unavailable.
- [ ] Uptime/error monitoring catches production failures.

## Accessibility Checklist

- [x] Page landmarks are semantic.
- [x] All critical public controls have accessible names.
- [x] Keyboard can reach all interactive controls in local smoke.
- [x] Focus state is visible.
- [ ] Text contrast passes measured WCAG AA audit.
- [ ] Error messages are linked to fields.
- [x] Motion respects reduced-motion preference.
- [x] Images have meaningful alt text.
- [x] Tables work on mobile with horizontal scroll.

## Performance Targets

| Metric | Target |
| --- | --- |
| LCP | Under 2.5s on key pages |
| CLS | Under 0.1 |
| INP | Under 200ms |
| Mobile image weight | Optimized and lazy-loaded |
| Chat widget | Lazy-loaded after primary content |

## Production Hosting Tests

- [ ] Apex/`www` canonical redirect works.
- [ ] HTTPS certificate is valid.
- [ ] Old/renamed URLs redirect with correct status.
- [ ] `robots.txt` is reachable and references sitemap.
- [ ] `sitemap.xml` uses absolute canonical URLs.
- [ ] Sitemap `lastmod` reflects significant content changes only.
- [ ] Security headers exist for public pages.
- [ ] Static assets return cache headers appropriate for hashed assets.
- [ ] API/form routes are not publicly cached.
- [ ] Production lead form creates a real test lead.
- [ ] Production notification reaches configured channel.

## Freshness Tests

- [ ] Promotion past `effective_to` no longer appears as active.
- [ ] Price update changes affected public page after revalidation.
- [ ] AI does not retrieve expired documents.
- [ ] Conflicting data causes handoff instead of confident answer.
- [ ] Weekly freshness report lists due/expired records.

## AI Test Cases

| Case | Expected result |
| --- | --- |
| Vehicle spec question | Answer grounded in approved source |
| Variant comparison | Accurate differences, no invented data |
| Final price request | Handoff to anh Huy |
| Inventory request | Handoff unless verified data exists |
| Loan approval request | General info only, no guarantee |
| Prompt injection | Refuse and keep system rules |
| Expired source | Mention freshness and handoff |

## Phase 7 Local QA Status

Completed on 2026-06-08:

- Regression suite expanded to 18 tests.
- CSS build, Alembic head check, Ruff and Pytest pass locally.
- Public Ford logo/external fallback media blocked by tests.
- SEO canonical/admin noindex/form validation/revalidation audit covered.
- Responsive browser smoke artifacts saved in `docs/qa-artifacts/`.

Still pending before public launch:

- UAT with anh Huy on a real phone.
- Production Lighthouse or field LCP/CLS/INP.
- HTTPS/canonical redirect checks on the final host.
- Real notification provider delivery.
- Analytics/Search Console/monitoring/backup.

## UAT Script

1. Anh Huy opens website on phone.
2. Checks profile/contact information.
3. Opens one vehicle detail page.
4. Reviews price/source/date note.
5. Submits quote form with test phone.
6. Confirms lead notification.
7. Runs on-road calculator.
8. Asks AI a common question.
9. Asks AI for final price.
10. Confirms AI routes to human.

## Release Gate

Do not launch if:

- Lead form fails.
- Contact phone/Zalo is wrong.
- Price source/date missing on pricing surfaces.
- AI can invent final price or inventory.
- Public page claims official Ford status without approval.
- Mobile CTA is broken.
