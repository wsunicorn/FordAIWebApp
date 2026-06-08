# UX/UI Requirements

## Primary User Journeys

### Journey 1 - Browse And Contact

1. Khach vao trang chu.
2. Thay ro anh Huy, Ford Dong Thap, so dien thoai/Zalo.
3. Xem dong xe noi bat.
4. Mo chi tiet xe.
5. Bam nhan bao gia, goi hoac Zalo.

Success: khach de lai lead hoac lien he truc tiep.

### Journey 2 - Compare And Estimate

1. Khach chon mau xe.
2. So sanh 2-3 phien ban.
3. Tinh chi phi lan banh/tra gop tham khao.
4. Gui phuong an cho anh Huy.

Success: lead co context ro ve xe, ngan sach, khu vuc, nhu cau.

### Journey 3 - Ask AI Then Handoff

1. Khach hoi AI ve xe, gia, tra gop, phien ban.
2. AI tra loi bang du lieu duoc duyet.
3. Khi can gia chot, ton kho, uu dai rieng hoac giu xe, AI chuyen sang anh Huy.

Success: AI giam cau hoi lap lai nhung khong vuot quyen.

## Public Pages

| Page | Purpose | Required CTA |
| --- | --- | --- |
| Home | Gioi thieu anh Huy va xe Ford | Goi, Zalo, nhan bao gia |
| About/Sales Profile | Tao niem tin ca nhan | Lien he anh Huy |
| Vehicles | Tim va loc xe | Xem chi tiet, so sanh |
| Vehicle Detail | Hieu xe, gia, phien ban | Nhan bao gia, lai thu |
| Compare | Chon phien ban phu hop | Gui so sanh cho sales |
| On-road Calculator | Uoc tinh chi phi | Luu phuong an va lien he |
| Loan Calculator | Uoc tinh tra gop | Nhan tu van tra gop |
| Promotions | Xem uu dai co hieu luc | Kiem tra uu dai voi anh Huy |
| Articles/FAQ | SEO va giai thich | Hoi AI hoac lien he |
| Contact | Tat ca kenh lien he | Goi/Zalo/form |

## Phase 2 Public Sitemap

| Route | Page | Primary job |
| --- | --- | --- |
| `/` | Home | Introduce anh Huy, show featured vehicles, guide to quote/contact. |
| `/anh-huy` | Sales profile | Build personal trust and show direct contact channels. |
| `/xe` | Vehicle listing | Browse, filter and compare Ford models. |
| `/xe/[slug]` | Vehicle detail | Review variants, specs, source-backed price and request quote. |
| `/so-sanh` | Compare | Compare 2-3 models/variants and send context to anh Huy. |
| `/bang-gia` | Price table | Show reference prices with source/update metadata. |
| `/du-toan-lan-banh` | On-road calculator | Estimate on-road cost by model/area. |
| `/du-toan-tra-gop` | Loan calculator | Estimate loan scenarios and request loan consultation. |
| `/uu-dai` | Promotions | Show active promotions and conditions. |
| `/faq` | FAQ | Answer common questions and route to AI/human. |
| `/lien-he` | Contact | Collect lead or connect by phone/Zalo/email/Facebook. |
| `/lai-thu` | Test-drive request | Request preferred model/time/area. |
| `/bao-gia` | Quote request | Submit interested model and contact details. |

## Confirmed Contact Channels

| Channel | Value | UI use |
| --- | --- | --- |
| Phone | 0766994952 | Primary call CTA |
| Zalo | 0818655369 | Primary chat CTA |
| Email | hh753741@gmail.com | Footer/contact form fallback |
| Facebook | https://www.facebook.com/share/1X2vMYQ3T4/?mibextid=wwXIfr | Social profile link |
| Temporary URL | https://huy-ford-dong-thap.pages.dev | Preview/public MVP URL |

## Confirmed Brand And Source Decisions

| Item | Decision | UI impact |
| --- | --- | --- |
| Dealer/unit text | Đồng Tháp Ford | Show as text with anh Huy's role, not as an official corporate site claim. |
| MVP logo | `assets/brand/huy-dang-huy-logo.svg` | Use custom personal mark in header/footer until official media rights are confirmed. |
| Source site | https://dongthapford.com/ | Use for structure and metadata ingestion, then rewrite/approve public content. |
| Official media | Requires permission | Do not publish Ford/dealer logo, showroom photos, catalogue or source vehicle images until approved. |

## Admin Screens

| Screen | Purpose |
| --- | --- |
| Login | Bao ve admin |
| Dashboard | Xem lead moi, viec can follow-up |
| Leads | Quan ly lead va trang thai |
| Vehicles | Cap nhat dong xe/phien ban |
| Prices | Cap nhat gia, uu dai, ngay hieu luc |
| Content | Bai viet, FAQ, tai lieu AI |
| AI Logs | Xem cau hoi, loi, feedback |
| Settings | Thong tin sales, kenh lien he, cau hinh |

## Phase 2 Admin Sitemap

| Route | Screen | Primary job |
| --- | --- | --- |
| `/admin` | Dashboard | Leads, stale data, recent updates, review due alerts. |
| `/admin/leads` | Leads | List, filter, status, follow-up and export leads. |
| `/admin/leads/[id]` | Lead detail | Notes, requested model, quote context and next action. |
| `/admin/vehicles` | Vehicles | Manage models, variants, specs and media records. |
| `/admin/prices` | Prices/promotions | Manage price, effective dates, review due and source. |
| `/admin/content` | Content | FAQ, articles, static copy and approval status. |
| `/admin/ai-documents` | AI documents | Approved knowledge base with source metadata. |
| `/admin/settings` | Settings | Contact info, source URLs and notification settings. |
| `/admin/audit-log` | Audit log | Track updates and revalidation events. |

## Phase 2 Wireframe Requirements

### Home

- First viewport shows anh Huy identity, role, Dong Thap Ford, phone/Zalo and quote CTA.
- Use `assets/images/people/huy-dang-huy.jpg` for the personal trust block.
- Vehicle/showroom imagery must be approved or source-tracked before public use.
- Include quick finder, featured vehicles, calculator entry, AI entry, trust/process, latest updates and footer contact.

### Vehicle Listing

- Filters for category, use case, seats and budget.
- Cards show image, price-from, update date, key use case and CTAs.
- Compare tray supports up to 3 models/variants.
- Empty state offers reset and contact anh Huy.

### Vehicle Detail

- Model hero with source/update badge.
- Variant tabs are scrollable on mobile and keyboard-accessible.
- Price block says reference only and routes final confirmation to anh Huy.
- Specs grouped by performance, safety, comfort and dimensions.
- Sticky mobile CTA includes call, Zalo, quote and AI.

### Calculators

- On-road calculator: model, variant, area, fee assumptions, insurance/options, output breakdown.
- Loan calculator: price, down payment, term, interest assumption and monthly estimate.
- Every output has source/update date and disclaimer.
- Save scenario into quote form context.

### Forms

- Quote and test-drive forms must be short on mobile.
- Required fields: name, phone, interested model, area, need type and consent.
- Inline errors, loading state, success state and retry state are required.
- Success screen shows direct phone/Zalo immediately.

### AI Assistant

- Floating entry is calm and not continuously pulsing.
- Suggested prompts cover variants, fees, promotions and comparison.
- Answers cite source/update date when possible.
- Final price, stock, delivery, loan approval and deposit intent must hand off to anh Huy.

## CTA Hierarchy

Primary:

- Goi anh Huy: 0766994952.
- Nhan bao gia.
- Dang ky lai thu.

Secondary:

- Zalo anh Huy: 0818655369.
- Hoi AI.
- So sanh phien ban.

Tertiary:

- Doc FAQ.
- Xem bai viet lien quan.
- Tai catalogue neu duoc phep.

Avoid:

- Mua ngay.
- Dat coc.
- Thanh toan.
- Giu xe online trong MVP.

## Form Requirements

Minimum lead fields:

- Ho ten.
- So dien thoai.
- Xe quan tam.
- Khu vuc.
- Nhu cau: bao gia, lai thu, tra gop, khac.
- Dong y xu ly thong tin.

Nice to have:

- Khoang ngan sach.
- Thoi gian du kien mua.
- Kenh lien he mong muon.
- Ghi chu.

Rules:

- Form ngan tren mobile.
- Loi hien thi gan truong nhap.
- Sau khi submit thanh cong, hien so/Zalo de khach lien he ngay.
- Khong thu CCCD, giay to vay hoac thong tin nhay cam tren form cong khai.

## States

Every interactive surface needs:

- Loading state.
- Empty state.
- Error state.
- Success state.
- Disabled state.
- Focus state.

## Motion And Polish Requirements

- Button active feedback uses about `scale(0.97)`.
- Common UI animations should usually stay under 300ms.
- Use exact transition properties, not `transition-all`.
- Prefer `transform` and `opacity`.
- Vehicle card image hover scale should stay subtle, around 1.01-1.03.
- Remove endless pulse/attention animations unless the UI has a temporary urgent state.
- Popovers and tooltips should animate from the trigger origin.
- Add reduced-motion fallback for all non-essential motion.
- Admin screens avoid decorative motion for repeated tasks.

## Mobile Requirements

- Sticky bottom CTA on vehicle pages.
- Tap targets at least 44px.
- Tables scroll horizontally with clear affordance.
- Hero content visible without feeling like a poster.
- Text never overlaps images or controls.

## Copy Rules

- Say "gia tham khao" when not official.
- Say "anh Huy se xac nhan" for price, stock, promotion and delivery time.
- Avoid claims that sound legally binding.
- Use direct button labels: "Nhan bao gia", "Goi anh Huy", "Tinh chi phi".
