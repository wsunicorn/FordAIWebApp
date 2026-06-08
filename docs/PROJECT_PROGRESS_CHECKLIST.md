# Project Progress Checklist

Cap nhat file nay moi khi hoan thanh mot dau viec. Trang thai de xuat: `Not started`, `In progress`, `Blocked`, `Done`.

## Summary

| Area | Status | Owner | Notes |
| --- | --- | --- | --- |
| Product scope | Done | Team | MVP la website tu van va thu lead, khong ecommerce. |
| Design system | Done | Team | Phase 2 UX/UI direction, motion spec, component inventory and design review are documented. |
| Data collection | Done | Anh Huy + Dev | Phase 1 seed da hoan thanh trong `docs/PHASE_1_DISCOVERY_AND_CONTENT.md`. |
| Frontend build | Done for public MVP | Dev | Phase 4 public pages, forms, calculators, SEO files and tests are complete locally. |
| Backend/data | Done for admin MVP | Dev | Phase 5 adds admin auth, lead care, content/vehicle freshness data and migrations. |
| AI assistant | Done for grounded MVP | Dev | Phase 6 adds KB, retrieval, tools, guardrails, handoff, logs and Gemini fallback provider. |
| QA/UAT | Done for local QA | Team + Anh Huy | Phase 7 local QA hardening, regression tests and browser smoke complete; UAT voi anh Huy van can lam truoc launch. |
| Hosting/traffic | In progress | Dev | Render Free host can dung ten cu `https://huy-ford-dong-thap.onrender.com`; can sua service/subdomain tren Render, chay production smoke, roi cau hinh domain/monitoring. |
| Content freshness | Done for admin MVP | Anh Huy + Dev | Admin can seed/update source, review due, approval and freshness status locally. |
| Launch | In progress | Team | Phase 8 deploy-readiness da co; public launch van cho host, domain, HTTPS, UAT, monitoring. |

## Phase 0 - Project Setup

- [x] Tao tai lieu de xuat goc.
- [x] Tach `PRODUCT.md` cho product context.
- [x] Tach `DESIGN.md` cho design context.
- [x] Tao bo docs trong `docs/`.
- [x] Chot ten hien thi: Huỳnh Đang Huy.
- [x] Chot vai tro: Tư Vấn Bán Hàng.
- [x] Chot don vi/ten dai ly hien thi: Đồng Tháp Ford.
- [x] Chot temporary production URL: `https://huy-ford-dong-thap.onrender.com`.
- [x] Chot temporary URL Phase 0: Cloudflare Pages placeholder/redirect, co duong dung Cloudflare DNS/CDN sau nay.
- [x] Chot brand/logo MVP: dung custom wordmark rieng, khong dung/khong mo phong logo Ford.
- [x] Tao file logo MVP: `assets/brand/huy-dang-huy-logo.svg`.
- [x] Tao favicon/browser tab icon tu logo MVP.
- [x] Chot nguon site chinh de hoc va ingest: https://dongthapford.com/.
- [x] Tao source ingestion plan: `docs/SOURCE_SITE_INGESTION_PLAN.md`.
- [x] Chot kenh lien he chinh: dien thoai 0766994952, Zalo 0818655369, email hh753741@gmail.com, Facebook.
- [x] Chuyen quyen su dung logo/hinh/catalogue chinh thuc thanh release gate truoc public launch.

## Phase 1 - Discovery And Content

- [x] Thu thap ten, chuc danh, don vi, hotline, Zalo, email, Facebook.
- [x] Xac dinh source site chinh va sitemap can theo doi.
- [x] Lap danh sach URL product/page ban dau tu sitemap chinh.
- [x] Di chuyen anh cua anh Huy vao `assets/images/people/huy-dang-huy.jpg`.
- [x] Xac nhan quyen public-use cho anh cua anh Huy trong MVP theo yeu cau cua project owner.
- [x] Chot policy gio lam viec MVP: khong cong bo gio co dinh, form/Zalo nhan lead 24/7, anh Huy phan hoi som.
- [x] Xac nhan khu vuc phuc vu seed: Dong Thap la chinh, khu vuc lan can/DBSCL theo nguon va can anh Huy xac nhan tung lead.
- [x] Import metadata danh sach xe, phien ban, model year tu source site vao Phase 1 seed.
- [x] Import metadata bang gia va ngay hieu luc tu source site vao Phase 1 seed.
- [x] Import metadata uu dai va dieu kien ap dung tu source site vao Phase 1 seed.
- [x] Import metadata phi lan banh theo khu vuc vao Phase 1 seed.
- [x] Import metadata lai suat/chuong trinh tra gop tham khao vao Phase 1 seed.
- [x] Thu thap FAQ seed tu source flow va nhu cau tu van.
- [x] Xac dinh cau AI khong duoc tra loi.
- [x] Xac dinh quy trinh cap nhat du lieu sau launch.
- [x] Ghi nhan quyen su dung logo Ford/dai ly, showroom, catalogue, vehicle media la release gate neu muon public.

## Phase 2 - UX/UI

- [x] Lap sitemap public.
- [x] Lap sitemap admin.
- [x] Wireframe trang chu mobile-first.
- [x] Wireframe danh sach xe.
- [x] Wireframe chi tiet xe.
- [x] Wireframe calculator lan banh.
- [x] Wireframe calculator tra gop.
- [x] Wireframe form bao gia/lai thu.
- [x] Wireframe AI assistant va handoff.
- [x] Tao design tokens.
- [x] Tao component library co ban.
- [x] Kiem tra contrast, responsive, focus state.
- [x] Review ban HTML concept user da paste va ghi action truoc khi build.
- [x] Luu design-skill notes vao `D:\AISkills`.

## Phase 3 - Technical Foundation

- [x] Xoa scaffold Next.js theo yeu cau moi cua project owner.
- [x] Scaffold FastAPI app package.
- [x] Cau hinh Jinja2 templates va StaticFiles.
- [x] Cai Tailwind CSS CLI va build `app/static/css/styles.css`.
- [x] Them vanilla JavaScript entry.
- [x] Cau hinh Python env vars trong `.env.example`.
- [x] Cau hinh Ruff/Pytest.
- [x] Tao SQLAlchemy models foundation.
- [x] Tao Alembic migration MVP cho xe, phien ban, gia, lead va audit log.
- [x] Cau hinh SQLite local dev, PostgreSQL production-ready URL.
- [x] Tao API health, lead API, HTML lead form va protected revalidation hook.
- [x] Tao audit log service cho lead/revalidation.
- [x] Tao Dockerfile va `render.yaml` deploy baseline.
- [x] Chay migration local va smoke test API.

## Phase 4 - Public Website MVP

- [x] Trang chu.
- [x] Trang gioi thieu anh Huy.
- [x] Danh sach xe.
- [x] Chi tiet xe.
- [x] So sanh phien ban.
- [x] Bang gia tham khao.
- [x] Uu dai/khuyen mai.
- [x] Calculator lan banh.
- [x] Calculator tra gop.
- [x] Form nhan bao gia.
- [x] Form dang ky lai thu.
- [x] Trang lien he.
- [x] SEO metadata.
- [x] Sitemap XML va robots.txt.

## Phase 5 - Admin And Lead Flow

- [x] Dang nhap admin.
- [x] Quan ly xe.
- [x] Quan ly phien ban.
- [x] Quan ly gia va uu dai.
- [x] Quan ly bai viet/FAQ.
- [x] Quan ly lead.
- [x] Lead detail va ghi chu cham soc.
- [x] Trang thai lead va follow-up.
- [x] Tao `notification.pending` audit/outbox cho lead moi, san sang noi email/Zalo/Sheets.
- [x] Export lead.
- [x] Sau khi cap nhat xe/gia/uu dai, ghi audit `cache.revalidate` cho trang lien quan.
- [x] Quan ly `effective_to`, `review_due_at`, `approval_status`.

## Phase 6 - AI Assistant

- [x] Dinh nghia prompt system.
- [x] Tao knowledge base ban dau.
- [x] Gan metadata nguon, ngay cap nhat, owner.
- [x] Tao retrieval flow.
- [x] Tao calculator tool.
- [x] Tao lead handoff tool.
- [x] Guardrail gia chot, ton kho, vay, dat coc.
- [x] Log hoi thoai va feedback.
- [x] Test bo cau hoi chuan.
- [x] Cau hinh quota va fallback khi het free tier.

## Phase 7 - QA And UAT

- [x] Test responsive mobile/desktop local smoke.
- [x] Test form validation.
- [x] Test tao lead.
- [x] Test calculator bang du lieu mau qua AI/tool va calculator UI smoke.
- [x] Test admin CRUD/status guardrails.
- [x] Test AI hallucination guardrails.
- [x] Test SEO metadata.
- [ ] Test performance LCP/CLS/INP bang Lighthouse tren production/preview.
- [x] Test accessibility labels/focus baseline.
- [x] Test cache/revalidation audit hook local.
- [x] Test sitemap, robots, canonical local.
- [ ] Test production redirects sau khi co canonical domain.
- [x] Test expired/freshness status path local qua admin metadata.
- [ ] UAT voi anh Huy.

## Phase 8 - Launch And Operations

- [x] Chot temporary production URL: `https://huy-ford-dong-thap.pages.dev`.
- [x] Chot Phase 0 temporary URL tren Cloudflare Pages.
- [x] Chot Phase 3 FastAPI can Docker/Python host thay cho Pages-only hosting.
- [x] Them production settings guardrails cho secret, debug, `APP_URL` va PostgreSQL.
- [x] Chuan hoa provider Postgres URL sang SQLAlchemy async URL.
- [x] Them DB health endpoint `/api/health/db`.
- [x] Them Docker start script chay Alembic migration va dung `$PORT`.
- [x] Them `.dockerignore`.
- [x] Cap nhat `render.yaml` baseline voi Docker web service, Postgres va secret placeholders.
- [x] Tao production smoke script `scripts/smoke.py`.
- [x] Them favicon vao production smoke script.
- [x] Deploy production/preview len Render Free.
- [x] Xoa AI key that khoi `.env.example`.
- [x] Tao `.env.production.local` bi ignore voi production secrets da generate.
- [x] Them optional GA4 qua `GA_MEASUREMENT_ID`.
- [x] Them optional Sentry qua `SENTRY_DSN`.
- [x] Tao runbook Render/Cloudflare/GA4/Search Console/Sentry.
- [ ] Chot domain rieng.
- [ ] Cau hinh DNS/HTTPS.
- [ ] Chot canonical host apex hoac `www`.
- [ ] Cau hinh redirect non-canonical sang canonical.
- [ ] Cau hinh production env canonical `APP_URL=https://huy-ford-dong-thap.onrender.com`.
- [ ] Cau hinh backup.
- [ ] Cau hinh analytics va Search Console.
- [ ] Submit sitemap trong Search Console.
- [ ] Cau hinh uptime monitor.
- [ ] Cau hinh error tracking/logging.
- [ ] Cau hinh AI quota va fallback sang form/Zalo.
- [ ] Cau hinh weekly freshness report.
- [ ] Cau hinh job expire gia/uu dai/tai lieu AI het han.
- [ ] Tao tai lieu ban giao.
- [ ] Ban giao tai khoan va huong dan admin.
- [ ] Chot lich bao tri va update du lieu.

## Blockers And Release Gates

| Date | Item | Impact | Owner | Next action | Status |
| --- | --- | --- | --- | --- | --- |
| 2026-06-07 | Quyen dung logo/hinh/catalogue chinh thuc chua co bang chung | Chua the public Ford/dealer media | Anh Huy | Luu bang chung phe duyet truoc launch | Release gate |
| 2026-06-07 | Chua co domain rieng | Tam thoi dung `pages.dev`, SEO dai han chua toi uu | Team | Mua/chot domain khi san sang | Release gate |
| 2026-06-07 | Chua co production deploy/cache/freshness automation | Render Free preview da len, DB health OK | Dev | Doi Render host ve ten cu, sua canonical APP_URL, chay smoke production va cau hinh monitoring | Partially resolved |
| 2026-06-07 | Chua co provider email/Zalo/Sheets credential | Notification moi la audit/outbox noi bo | Team | Chot provider va credential khi deploy production | Release gate |
| 2026-06-08 | UAT voi anh Huy chua thuc hien tren dien thoai that | Chua nen launch public du local QA pass | Anh Huy + Dev | Chay UAT script trong `docs/PHASE_7_QA_AND_UAT.md` | Release gate |
| 2026-06-08 | Chua co Lighthouse/field performance tren production | Chua co LCP/CLS/INP thuc te | Dev | Do tren preview/production sau deploy | Phase 8 gate |
| 2026-06-08 | Chua co domain rieng/final production secrets | Da co Render preview; SEO dai han va secret rotation van can lam | Team + Dev | Chot domain, rotate secrets truoc launch public, them API key neu dung AI live | Release gate |

## Weekly Progress Notes

### Week 1

- Created project documentation set.
- Added confirmed sales/contact information for Huỳnh Đang Huy.
- Closed Phase 0 with temporary URL, deploy direction, source site, custom wordmark and brand/media policy.
- Closed Phase 1 discovery/content seed, moved anh Huy image into assets and prepared vehicle/price/calculator/FAQ/AI guardrail seed.
- Closed Phase 2 UX/UI spec: sitemap, wireframes, component inventory, motion rules and pasted-design review.
- Switched Phase 3 from Next.js to FastAPI per project owner request.
- Closed Phase 3 technical foundation with FastAPI/Jinja/Tailwind/SQLAlchemy/Alembic, local migration and smoke tests.
- Closed Phase 4 public website MVP with homepage, profile, vehicles, detail, comparison, prices, promotions, calculators, quote/test-drive/contact forms, FAQ, SEO metadata, robots and sitemap.
- Closed Phase 5 admin MVP with admin auth, dashboard, lead inbox/detail/update/export, vehicle/price/content management, freshness metadata, notification pending audit and revalidation audit events.
- Closed Phase 6 grounded AI assistant MVP with public AI page, AI APIs, KB seed, retrieval, calculator tools, guardrails, Gemini adapter, handoff lead flow, admin AI dashboard, quota fallback and tests.
- Closed Phase 7 local QA with launch-gate branding/media fixes, accessibility labels, mobile responsive fixes, lead validation, revalidation/admin/SEO regression tests, browser smoke artifacts and UAT script.
- Started Phase 8 launch operations: production guardrails, Postgres URL normalization, DB health endpoint, Docker migration start script, Render baseline, smoke script and env hardening.
- Render Free preview is live, but project owner wants the old host `https://huy-ford-dong-thap.onrender.com`; next focus is fixing Render subdomain/canonical `APP_URL`, running production smoke, then configuring domain/monitoring and UAT with anh Huy.
