# Decisions

Use this file for architecture and product decisions. New entries should be added at the top.

## ADR-0014 - Phase 8 deploy readiness uses production guardrails and smoke tests

Date: 2026-06-08

Status: Accepted

Decision:

Use a Docker/Python host for the FastAPI app with a startup script that runs
`alembic upgrade head` before Uvicorn. Require strong production secrets,
`APP_DEBUG=false`, non-local `APP_URL` and PostgreSQL when `APP_ENV=production`.
Add `/api/health/db` and a post-deploy smoke script to verify the public host
before UAT or launch.

Reason:

The MVP is ready locally, but public launch risk is now operational: weak
secrets, missing migrations, wrong canonical URLs, SQLite in production and
unverified forms. These failures should be blocked by config validation and
detected by a repeatable smoke script.

Consequences:

- `.env.example` must never contain real API keys.
- Host env vars are the source of truth for production secrets.
- Provider PostgreSQL URLs are normalized to SQLAlchemy async URLs.
- `CANONICAL_REDIRECT` stays off until the real canonical host is chosen.
- Real deployment still requires host/domain/DNS credentials and UAT approval.

## ADR-0013 - Phase 7 local QA blocks launch-gate regressions

Date: 2026-06-08

Status: Accepted

Decision:

Treat Phase 7 as local QA hardening, not production launch. Add automated
regression tests for lead validation, SEO metadata, admin noindex, revalidation
audit events, admin status validation, accessibility labels and public
brand/media gates. Public templates must not use the Ford logo, external
fallback media or wording that implies an official Ford Vietnam site until a
permission record exists.

Reason:

The MVP can be technically complete but still unsafe to launch if it leaks
unapproved brand media, accepts invalid leads, hides broken mobile UI or lets
SEO/revalidation regress. These risks are cheap to catch locally and expensive
to discover after launch.

Consequences:

- Phase 7 can close for local QA while UAT and production checks stay open.
- Tests must fail if public pages reintroduce Wikimedia/Unsplash/Placehold
  fallback media or Ford-logo usage.
- Performance metrics, HTTPS, canonical redirects, analytics and Search Console
  remain Phase 8 production responsibilities.
- UAT with anh Huy remains a release gate before public launch.

## ADR-0012 - Use Gemini 2.5 Flash-Lite as the first live LLM provider

Date: 2026-06-07

Status: Accepted

Decision:

Set `AI_PROVIDER=gemini` and `AI_MODEL=gemini-2.5-flash-lite` as the default
live LLM configuration. Keep calculator tools, retrieval, guardrails and
handoff logic inside `app/services/ai_service.py` before any provider call.

Reason:

The project needs a low-cost/free-tier path before paid scaling. The official
Google AI pricing page currently lists `gemini-2.5-flash-lite` paid text token
pricing lower than the newer Flash-Lite option, while Google AI Studio handles
the actual free-tier and paid-tier rate limits per project/tier. The app should
therefore optimize for cost now and keep the model configurable by env.

Reference:

- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/models/gemini

Consequences:

- Public AI answers can use Gemini for natural wording after approved document
  retrieval.
- Calculator and high-risk guardrail answers do not spend Gemini requests.
- Gemini failures, timeouts or unsafe generated answers fall back to the
  internal grounded answer.
- Real API keys should live in `.env` or host environment variables before
  Git/deploy; `.env.example` remains a local convenience only while the project
  is private.

## ADR-0011 - Phase 6 AI starts as grounded mock assistant

Date: 2026-06-07

Status: Accepted, provider superseded by ADR-0012

Decision:

Build the Phase 6 assistant with approved AI documents, deterministic retrieval,
calculator tools, guardrails, chat logging, feedback and lead handoff before
connecting any paid LLM provider.

Reason:

The website must not invent price, stock, deposit, loan approval or dealership
commitments. A grounded mock assistant gives the project a working UI, data
model, logs and safety behavior on free-tier infrastructure. A paid LLM adapter
can be added later behind the same service boundary.

Consequences:

- `/tro-ly-ai`, `/api/ai/chat`, `/api/ai/handoff`, `/api/ai/feedback` and `/admin/ai` are live locally.
- AI documents require source, owner, approval status, freshness status and risk level.
- High-risk intents hand off to anh Huy instead of receiving a final answer.
- `AI_DAILY_QUOTA` controls simple quota fallback.
- Gemini integration in ADR-0012 preserves the same guardrails and logging.

## ADR-0010 - Phase 5 admin uses lean signed-cookie auth and audit-first workflows

Date: 2026-06-07

Status: Accepted

Decision:

Use HMAC-signed HTTP-only admin cookies for the local admin MVP. Add admin pages for dashboard, lead care, vehicle/price freshness and content management. Use audit logs for notification pending events and cache revalidation events until production providers are selected.

Reason:

The project needs an internal operating surface now, but it does not yet have production credentials, provider choices or multiple admin users. A lean signed-cookie gate keeps Phase 5 deployable on free/low-cost hosting while avoiding a premature auth subsystem.

Consequences:

- Production must set strong `ADMIN_PASSWORD` and `SECRET_KEY`.
- Admin cookies are marked secure when `APP_ENV=production`.
- Lead creation writes both `lead.created` and `notification.pending` audit events.
- Admin updates write entity audit events plus `cache.revalidate` events for affected public routes.
- Email/Zalo/Google Sheets delivery remains a provider integration release gate.
- Future multi-user admin should replace this with an `admin_users` table, password hashing and role-based permissions.

## ADR-0009 - Phase 4 public MVP is server-rendered and source-backed

Date: 2026-06-07

Status: Accepted

Decision:

Build Phase 4 public pages as FastAPI/Jinja server-rendered templates with Tailwind CSS and vanilla JavaScript. Keep vehicle, price, promotion, calculator and FAQ seed data in `app/data/site_content.py` until Phase 5 moves this content into admin-managed database tables.

Reason:

The website needs to be fast, SEO-friendly and easy to operate for a single sales consultant. Server-rendered pages are enough for the public MVP, while JavaScript should only enhance search, mobile navigation, lead-success feedback and calculators.

Consequences:

- Public route coverage now includes homepage, profile, vehicle list/detail, comparison, prices, promotions, calculators, quote/test-drive/contact forms, FAQ, robots and sitemap.
- Prices, promotions and calculator outputs must remain "tham khao" and hand off final confirmation to anh Huy.
- Official Ford/dealer logo, showroom photos, catalogues and vehicle media are still blocked until a permission record exists.
- SEO metadata and sitemap use the configured `APP_URL`, so production launch must set the canonical domain correctly.
- Phase 5 should add admin CRUD/freshness workflow before relying on the seed data for high-traffic production use.

## ADR-0008 - Switch Phase 3 foundation to FastAPI

Date: 2026-06-07

Status: Accepted

Decision:

Remove the Next.js technical foundation and use Python FastAPI with Jinja2 templates, Tailwind CSS CLI, vanilla JavaScript, SQLAlchemy, Alembic and Docker.

Reason:

The project owner explicitly requested deleting the previous direction and switching to Python FastAPI plus related frameworks while still using Tailwind CSS, JavaScript and HTML. FastAPI also fits the desired consultative site because it can serve SEO-friendly HTML and JSON APIs from one backend without a large frontend framework.

Consequences:

- `docs/TECH_ARCHITECTURE.md` is updated to FastAPI as the current source of truth.
- Cloudflare Pages is no longer the main app host for the FastAPI app; Cloudflare can still be DNS/CDN/WAF.
- Deployment should use Docker on Render/Railway/Fly.io/VPS or similar Python runtime.
- Tailwind stays as a CSS build tool through npm, but React/Next dependencies are removed.
- Phase 4 public pages should be built as Jinja templates and progressive vanilla JavaScript.
- Phase 5 admin/auth should use FastAPI sessions/JWT and SQLAlchemy models.

## ADR-0007 - Phase 2 UX/UI direction is consultation-first

Date: 2026-06-07

Status: Superseded by ADR-0008

Decision:

Use `docs/PHASE_2_UX_UI_DIRECTION.md` as the source of truth for public/admin sitemap, wireframes, component inventory and motion rules. Use `docs/USER_DESIGN_REVIEW_PHASE_2.md` as the action list for adapting the user's pasted HTML concept into production UI.

Reason:

The pasted HTML has a strong visual starting point, but it still behaves like a product/detail demo and includes placeholder contacts, demo-hosted images, hardcoded prices, English labels, ecommerce wording and overly broad animation defaults. The actual product needs a trust-first consultation flow for anh Huynh Dang Huy.

Consequences:

- Home first viewport must show anh Huy, Dong Thap Ford context, phone, Zalo and quote CTA.
- Vehicle detail pages can be model-first but must keep consultation CTA and source/update metadata visible.
- All prices, promotions and calculator assumptions must come from structured source-backed data.
- Production UI must avoid CDN/demo assets, `transition-all`, endless pulse and unapproved official media.
- Phase 3 should scaffold from these docs instead of copying the pasted HTML directly.

## ADR-0006 - Phase 1 discovery seed is source-backed

Date: 2026-06-07

Status: Accepted

Decision:

Move anh Huy's provided image to `assets/images/people/huy-dang-huy.jpg` and treat it as approved for MVP use. Use `docs/PHASE_1_DISCOVERY_AND_CONTENT.md` as the Phase 1 seed for sales profile, dealer/source context, service area, vehicle price table, calculator assumptions, FAQ topics, AI handoff boundaries and source update workflow.

Reason:

The project needs enough real content to design and scaffold the MVP without inventing data. The seed keeps source URLs and update dates attached, while preserving the rule that prices, promotions, fees and loan estimates are consultative and need anh Huy's confirmation before final use.

Consequences:

- Phase 1 can be marked complete for discovery/content.
- Frontend can use `assets/images/people/huy-dang-huy.jpg` for hero/profile surfaces.
- Public pricing/loan/fee UI must show "tham khảo" and source/update date.
- Official Ford/dealer media still requires a separate permission record before public reuse.

## ADR-0005 - Phase 0 URL, brand asset and source site are selected

Date: 2026-06-07

Status: Accepted

Decision:

Use `https://huy-ford-dong-thap.pages.dev` as the temporary production URL on Cloudflare Pages. Use a custom personal mark at `assets/brand/huy-dang-huy-logo.svg` for MVP. Use https://dongthapford.com/ as the primary source site to study and ingest metadata from.

Reason:

The project needs a concrete URL and deploy direction to move past planning, but it should not wait for a paid domain or official brand asset approval. A custom wordmark avoids Ford-logo trademark risk while still giving the MVP a usable identity. The official source site gives the project current vehicle, page, calculator, promotion and media references without pretending those assets can be copied freely.

Consequences:

- Phase 0 can be marked complete for planning.
- Final custom domain remains a launch/SEO release gate.
- Ford/dealer logo, showroom photos, catalogues and source media require a permission record before public reuse.
- Source-site updates must be reviewed before publishing or AI indexing.
- When a custom domain is selected, redirect the temporary URL to the canonical domain and update sitemap/Search Console.

## ADR-0004 - Production must include traffic and freshness controls

Date: 2026-06-07

Status: Accepted

Decision:

Before public launch, the project must have canonical domain redirects, HTTPS, sitemap/robots, Search Console, CDN/static asset caching, production smoke tests, uptime/error monitoring, data backup/export, and a content freshness workflow.

Reason:

The site's value depends on being findable, fast and accurate. Vehicle prices, promotions, fees and AI documents can become outdated quickly, so freshness must be part of operations, not a manual afterthought.

Consequences:

- Every price/promotion/AI document needs source, owner, effective dates and review due date.
- Admin updates must trigger revalidation of affected public pages.
- Expired promotions and AI documents must be removed from active surfaces.
- Launch is blocked if lead flow, canonical URLs, sitemap or freshness checks fail.

## ADR-0001 - MVP is consultation and lead generation, not ecommerce

Date: 2026-06-07

Status: Accepted

Decision:

The MVP will help customers browse Ford information, estimate cost, ask AI and contact anh Huynh Dang Huy. It will not include cart, checkout, deposit, hold-car or online payment.

Reason:

The business goal is to help customers research and contact a trusted sales consultant. Online transaction flows introduce legal, payment, brand, inventory and operational risk that is not needed for the first launch.

Consequences:

- CTA copy must use consultation language.
- AI must hand off final price and transaction intent.
- Any future deposit/payment feature requires separate approval.

## ADR-0002 - Use a lean full-stack architecture first

Date: 2026-06-07

Status: Superseded by ADR-0008

Decision:

Use Next.js App Router + TypeScript with Supabase for MVP. Avoid separate FastAPI, Redis, Qdrant and VPS until measured need appears.

Superseded decision:

ADR-0008 replaces this with a FastAPI/Jinja/Tailwind/SQLAlchemy foundation after the project owner changed the stack direction.

Reason:

This project starts as a free/low-cost build for one sales consultant. A single full-stack app reduces maintenance and speeds up launch.

Consequences:

- API routes/server actions handle MVP backend logic.
- pgvector is enough for early RAG if needed.
- The architecture must keep an upgrade path to workers, Redis, Qdrant and paid deploy later.

## ADR-0003 - AI must be grounded and conservative

Date: 2026-06-07

Status: Accepted

Decision:

AI will only answer from approved documents and structured tools. It must hand off to anh Huy for final price, stock, delivery time, deposit, loan approval, complaints and conflicting data.

Reason:

The product depends on trust. Wrong price or invented availability can damage reputation.

Consequences:

- All AI documents need metadata and approval status.
- Evaluation tests are required before launch.
- AI logs and feedback must be reviewed.
