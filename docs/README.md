# Project Docs Index

Bo tai lieu nay tach tu de xuat tong the thanh cac file de build, kiem tra va ban giao du an website tu van Ford ca nhan cho anh Huynh Dang Huy.

## Core Context

- [PRODUCT.md](../PRODUCT.md): san pham, nguoi dung, dinh vi, nguyen tac thiet ke.
- [DESIGN.md](../DESIGN.md): huong thiet ke, tokens, component rules, motion va pre-flight UI.
- [De_xuat_Website_AI_Sales_Ford_Huynh_Dang_Huy.md](../De_xuat_Website_AI_Sales_Ford_Huynh_Dang_Huy.md): tai lieu de xuat goc.

## Implementation Docs

- [UX_UI_REQUIREMENTS.md](UX_UI_REQUIREMENTS.md): IA, trang, component va yeu cau UX.
- [TECH_ARCHITECTURE.md](TECH_ARCHITECTURE.md): stack, kien truc MVP, database, deployment.
- [AI_ASSISTANT_SPEC.md](AI_ASSISTANT_SPEC.md): vai tro AI, RAG, guardrails, handoff, evaluation.
- [CONTENT_AND_DATA_GOVERNANCE.md](CONTENT_AND_DATA_GOVERNANCE.md): du lieu xe, gia, noi dung, phe duyet, freshness.
- [SOURCE_SITE_INGESTION_PLAN.md](SOURCE_SITE_INGESTION_PLAN.md): source site Dong Thap Ford, sitemap, URL nhap lieu va quy tac khong de stale/copy.
- [PHASE_1_DISCOVERY_AND_CONTENT.md](PHASE_1_DISCOVERY_AND_CONTENT.md): Phase 1 seed ve sales profile, asset anh Huy, xe/gia, calculator, FAQ, AI guardrails va quy trinh cap nhat.
- [PHASE_2_UX_UI_DIRECTION.md](PHASE_2_UX_UI_DIRECTION.md): sitemap, wireframes, component inventory, motion tokens va acceptance cho Phase 2.
- [USER_DESIGN_REVIEW_PHASE_2.md](USER_DESIGN_REVIEW_PHASE_2.md): review ban HTML user da paste va cac cai tien can lam truoc khi build.
- [PHASE_3_TECHNICAL_FOUNDATION.md](PHASE_3_TECHNICAL_FOUNDATION.md): FastAPI/Jinja/Tailwind/SQLAlchemy foundation, commands, deployment and validation.
- [PHASE_4_PUBLIC_WEBSITE_MVP.md](PHASE_4_PUBLIC_WEBSITE_MVP.md): public website MVP routes, source-backed data, UI notes and validation.
- [PHASE_5_ADMIN_AND_LEAD_FLOW.md](PHASE_5_ADMIN_AND_LEAD_FLOW.md): admin login, lead inbox, vehicle/price/content management, freshness and validation.
- [PHASE_6_AI_ASSISTANT.md](PHASE_6_AI_ASSISTANT.md): grounded AI assistant, KB, retrieval, guardrails, tools, handoff and validation.
- [PHASE_7_QA_AND_UAT.md](PHASE_7_QA_AND_UAT.md): local QA hardening, regression tests, responsive screenshots and UAT script.
- [PHASE_8_LAUNCH_AND_OPERATIONS.md](PHASE_8_LAUNCH_AND_OPERATIONS.md): production deploy baseline, env vars, smoke tests and launch gates.
- [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md): lo trinh lam viec theo giai doan.
- [QA_ACCEPTANCE.md](QA_ACCEPTANCE.md): test plan va tieu chi nghiem thu.
- [OPERATIONS_AND_DEPLOYMENT.md](OPERATIONS_AND_DEPLOYMENT.md): van hanh, free tier, backup, monitoring.
- [HOSTING_TRAFFIC_AND_FRESHNESS.md](HOSTING_TRAFFIC_AND_FRESHNESS.md): host production, traffic/cache/CDN, SEO va freshness automation.
- [RENDER_CLOUDFLARE_LAUNCH_RUNBOOK.md](RENDER_CLOUDFLARE_LAUNCH_RUNBOOK.md): huong dan deploy Render, Cloudflare DNS, GA4, Search Console va Sentry.
- [DESIGN_QUALITY_PLAYBOOK.md](DESIGN_QUALITY_PLAYBOOK.md): cach ap dung impeccable, taste skill va Emil vao giao dien.
- [PROJECT_PROGRESS_CHECKLIST.md](PROJECT_PROGRESS_CHECKLIST.md): checklist tien do va trang thai hoan thanh.
- [DECISIONS.md](DECISIONS.md): ADR va quyet dinh quan trong.
- [PHASE_0_ALIGNMENT.md](PHASE_0_ALIGNMENT.md): thong tin da chot va release gates sau Phase 0.

## Current Direction

MVP uu tien website tham khao, tu van va thu lead. Khong xay luong mua ban xe, dat coc hay thanh toan online trong giai doan dau.

Thong tin Phase 0 da chot:

- Huỳnh Đang Huy, Tư Vấn Bán Hàng, Đồng Tháp Ford.
- Dien thoai: 0766994952.
- Zalo: 0818655369.
- Email: hh753741@gmail.com.
- Facebook: https://www.facebook.com/share/1X2vMYQ3T4/?mibextid=wwXIfr
- Temporary URL: `https://huy-ford-dong-thap.pages.dev`.
- Source site chinh: https://dongthapford.com/.
- Logo MVP: `assets/brand/huy-dang-huy-logo.svg`.
- Anh Huy portrait: `assets/images/people/huy-dang-huy.jpg`.

Stack uu tien sau Phase 3:

- FastAPI + Jinja2 server-rendered HTML.
- Tailwind CSS v4 CLI + vanilla JavaScript.
- SQLAlchemy 2 + Alembic.
- SQLite local dev, PostgreSQL production.
- AI Gemini adapter voi grounded fallback sau Phase 6.
- Docker host cho FastAPI, Cloudflare dung cho DNS/CDN khi co domain.

Public MVP sau Phase 4:

- Da co trang chu, profile anh Huy, danh sach xe, chi tiet xe, so sanh, bang gia, uu dai, FAQ, lien he, bao gia va lai thu.
- Da co calculator lan banh va calculator tra gop bang vanilla JavaScript.
- Da co SEO metadata, canonical URL, `robots.txt` va `sitemap.xml`.
- Gia/uu dai/calculator la thong tin tham khao, can anh Huy xac nhan truc tiep.

Admin MVP sau Phase 5:

- Da co login/logout admin bang HMAC session cookie.
- Da co dashboard, lead inbox, lead detail, ghi chu cham soc, follow-up va CSV export.
- Da co seed/admin xe, phien ban, gia, freshness metadata va audit revalidation event.
- Da co content item admin cho promotion, FAQ va article.
- Notification lead moi hien la `notification.pending` audit/outbox, chua noi provider email/Zalo/Sheets that.

AI MVP sau Phase 6:

- Da co `/tro-ly-ai`, `/api/ai/chat`, `/api/ai/handoff`, `/api/ai/feedback` va `/admin/ai`.
- Da co AI document KB, conversation log, message log va feedback table.
- Da co retrieval keyword-based, calculator tools, guardrails va handoff sang lead.
- Hien dung `AI_PROVIDER=gemini` voi `AI_MODEL=gemini-2.5-flash-lite`; service fallback ve grounded answer neu provider loi.

Local QA sau Phase 7:

- Da bo public Ford logo/external fallback media khoi templates va them regression test chan tai pham.
- Da them test SEO canonical, admin noindex, form validation, lead success, revalidation audit va invalid admin status.
- Da them label a11y cho search/calculator/AI form va sua mobile header/hero overflow.
- Da co browser smoke artifacts trong `docs/qa-artifacts/`.
- UAT voi anh Huy va cac production checks van thuoc release gate truoc launch.

Brand/media policy:

- Dung custom wordmark rieng trong MVP.
- Khong tao logo giong Ford.
- Chi dung logo Ford/dai ly, showroom photos, catalogue va source media tren public site khi co permission record.
- Source site duoc dung de hoc/cap nhat metadata, nhung copy public phai duoc viet lai va phe duyet.

## Update Rule

Khi scope thay doi, cap nhat theo thu tu:

1. `PRODUCT.md`
2. `DESIGN.md`
3. File docs lien quan
4. `PROJECT_PROGRESS_CHECKLIST.md`
5. `DECISIONS.md`
