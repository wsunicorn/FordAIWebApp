# Implementation Plan

## Goal

Xay dung MVP website tu van Ford ca nhan cho anh Huynh Dang Huy, tap trung vao tham khao thong tin, tao lead va lien he truc tiep. Lam nhe, dung free/low-cost tier hop le truoc, san sang nang cap khi co ngan sach.

## Principles

- Launch useful before building complex.
- No ecommerce in MVP.
- Data first: khong co nguon thi khong hien thi nhu thong tin chinh thuc.
- AI supports, human confirms.
- Mobile-first from the first screen.

## Phase 0 - Documentation And Alignment

Deliverables:

- `PRODUCT.md`
- `DESIGN.md`
- Project docs in `docs/`
- Content checklist for anh Huy
- Initial architecture and progress checklist
- Temporary URL, MVP host, source site and logo policy

Exit criteria:

- Scope MVP ro.
- Cong nghe duoc chot.
- Du lieu can cung cap duoc liet ke.
- Ranh gioi "khong mua ban online" duoc dong thuan.
- URL tam da chot: `https://huy-ford-dong-thap.pages.dev`.
- Phase 0 temporary URL da chot tren Cloudflare Pages; sau Phase 3 FastAPI can Docker/Python host cho app chinh.
- Source site da chot: https://dongthapford.com/.
- Logo MVP da chot: custom wordmark, khong mo phong logo Ford.

## Phase 1 - Discovery And Content

Build:

- Move and register approved local portrait asset.
- Build source-backed content seed from official site.
- Seed vehicle, price, promotion, calculator, FAQ and AI handoff rules.
- Define content freshness workflow.

Exit criteria:

- Anh Huy image is in the project asset folder.
- Source URLs and sitemaps are tracked.
- Vehicle/price/calculator data has source and update date.
- FAQ and AI handoff boundaries are ready for Phase 2/3.

## Phase 2 - Prototype

Build:

- Static landing/home page.
- Vehicle listing with mock data.
- Vehicle detail with source/date placeholders.
- Lead form mock.
- Basic AI assistant mock or disabled state.

Exit criteria:

- Anh Huy xem duoc flow tren mobile.
- CTA va copy dung dinh vi.
- Visual direction duoc duyet.

## Phase 3 - MVP Foundation

Build:

- FastAPI app package.
- Jinja2 templates and StaticFiles.
- Tailwind CSS CLI and vanilla JavaScript.
- SQLAlchemy models and Alembic migrations.
- SQLite local dev and PostgreSQL production-ready config.
- Vehicle, price, lead and audit-log foundation tables.
- Docker deployment baseline.

Exit criteria:

- FastAPI app starts locally.
- Tailwind CSS builds locally.
- Alembic migration runs locally.
- Lead form/API tao record thanh cong.
- Health endpoint works.
- Ruff/Pytest pass.

## Phase 4 - Public MVP

Build:

- Trang chu.
- Danh sach xe.
- Chi tiet xe.
- So sanh phien ban.
- Calculator lan banh.
- Calculator tra gop.
- Form bao gia.
- Form lai thu.
- Lien he/Zalo/call sticky CTA.
- SEO metadata and sitemap.

Exit criteria:

- Khach co the tim xe, uoc tinh chi phi, de lai lead.
- Khong co pattern gio hang/thanh toan.
- Noi dung co ngay cap nhat va nguon.

## Phase 5 - Admin MVP

Build:

- CRUD xe/phien ban.
- CRUD gia/uu dai.
- CRUD bai viet/FAQ.
- Quan ly lead.
- Lead status and notes.
- Export or sync Google Sheets if needed.

Exit criteria:

- Anh Huy/admin co the cap nhat noi dung khong can code.
- Lead moi khong bi bo sot.

## Phase 6 - AI MVP

Build:

- FAQ assistant.
- Vehicle recommendation by needs.
- RAG over approved documents.
- Tool calls for calculator and lead handoff.
- Guardrails and refusal cases.
- Feedback logging.

Exit criteria:

- AI pass bo cau hoi test.
- AI khong bao gia chot, khong xac nhan ton kho, khong cam ket vay.
- AI de xuat lien he anh Huy o dung thoi diem.

## Phase 7 - Launch

Build:

- Production deploy.
- Domain and HTTPS.
- Analytics and Search Console.
- Error tracking.
- Backup.
- Handover docs.

Exit criteria:

- Website public.
- Lead flow tested end-to-end.
- Anh Huy co tai khoan admin va huong dan su dung.

## Phase 8 - Improve

Options:

- SEO articles.
- PDF quotation request summary.
- Zalo OA.
- CRM paid integration.
- AI paid tier.
- Inventory integration if official API exists.
- Multi-sales or multi-branch.

## Suggested Timeline

| Week | Focus | Output |
| --- | --- | --- |
| 1 | Scope, content, prototype | Wireframe, design direction, mock pages |
| 2 | Foundation | FastAPI, Jinja, Tailwind, SQLAlchemy, Alembic, Docker |
| 3 | Public MVP | Home, vehicles, detail, forms, calculators |
| 4 | Admin MVP | CRUD, lead management, content update |
| 5 | AI MVP | RAG, guardrails, lead handoff, evaluation |
| 6 | QA and launch | UAT, bugfix, production, handover |
