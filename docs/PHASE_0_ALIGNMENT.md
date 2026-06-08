# Phase 0 Alignment

## Status

Phase 0 is completed for MVP planning.

This does not mean the site is publicly launched. It means the core business direction, owner identity, temporary URL, source site, deploy direction and brand/media policy are now decided well enough to start Phase 1 and implementation.

## Confirmed Decisions

| Item | Decision |
| --- | --- |
| Product scope | Website tư vấn cá nhân và thu lead, không phải web mua bán xe trực tuyến. |
| Sales owner | Huỳnh Đang Huy, Tư Vấn Bán Hàng. |
| Dealer/unit text | Đồng Tháp Ford. |
| Temporary production URL | `https://huy-ford-dong-thap.pages.dev` |
| MVP deploy target | Cloudflare Pages as temporary free/low-cost host, with upgrade path to paid plan later. |
| Primary source site to study | https://dongthapford.com/ |
| Logo policy | Use custom personal mark `assets/brand/huy-dang-huy-logo.svg` for MVP. Do not mimic Ford logo. |
| Official media policy | Ford/dealer logo, showroom photos, catalogues and vehicle media can be tracked as source references, but require permission before public reuse. |
| Local portrait image | `assets/images/people/huy-dang-huy.jpg`, approved for MVP use by project owner request on 2026-06-07. |

## Confirmed Sales Information

| Field | Value |
| --- | --- |
| Name | Huỳnh Đang Huy |
| Role | Tư Vấn Bán Hàng |
| Unit | Đồng Tháp Ford |
| Phone | 0766994952 |
| Zalo | 0818655369 |
| Email | hh753741@gmail.com |
| Facebook | https://www.facebook.com/share/1X2vMYQ3T4/?mibextid=wwXIfr |

## Source Site Snapshot

Checked on: 2026-06-07.

| Source | Latest sitemap timestamp observed | Notes |
| --- | --- | --- |
| https://dongthapford.com/sitemap_index.xml | 2026-06-06T01:26:49+00:00 | Root discovery source. |
| https://dongthapford.com/page-sitemap.xml | 2026-05-14T06:45:16+00:00 | Public pages, calculators, local SEO pages, contact pages. |
| https://dongthapford.com/product-sitemap.xml | 2026-04-06T15:28:19+00:00 | Vehicle/product URLs and media references. |
| https://dongthapford.com/post-sitemap.xml | 2026-06-06T01:26:49+00:00 | News, promotion and article URLs. |

Source-site content to learn from:

- Homepage structure, vehicle categories, price/promotion presentation and lead forms.
- Vehicle pages for Territory, Ranger, Everest, Transit, Mustang Mach-E, Ranger Raptor and Explorer.
- Calculators for lăn bánh and trả góp.
- Contact, quotation, test-drive and service-booking flows.
- Showroom/dealer information and media references.
- News, promotion, service, local event and used-car article patterns from post sitemap.

See [SOURCE_SITE_INGESTION_PLAN.md](SOURCE_SITE_INGESTION_PLAN.md) for the ingestion rules.

## Suggested Public Display

Hero identity:

```text
Huỳnh Đang Huy
Tư Vấn Bán Hàng tại Đồng Tháp Ford
Tham khảo xe Ford, nhận báo giá và đặt lịch lái thử trực tiếp với anh Huy.
```

Primary CTAs:

- Gọi anh Huy: 0766994952.
- Zalo tư vấn: 0818655369.
- Nhận báo giá.
- Đăng ký lái thử.

Footer/contact block:

```text
Huỳnh Đang Huy
Tư Vấn Bán Hàng, Đồng Tháp Ford
Điện thoại: 0766994952
Zalo: 0818655369
Email: hh753741@gmail.com
Facebook: https://www.facebook.com/share/1X2vMYQ3T4/?mibextid=wwXIfr
```

## Remaining Release Gates

These do not block Phase 0, but must be resolved before public launch:

| Item | Why it matters | Required action |
| --- | --- | --- |
| Final custom domain | Needed for stable SEO and Search Console | Buy/select domain, then redirect temporary URL to canonical host. |
| Official logo/media rights | Prevents trademark/copyright misuse | Keep permission record before using Ford/dealer logo, showroom photos, catalogues or source media publicly. |
| Work hours | Improves contact UX and expectation setting | Confirm normal working hours with anh Huy. |
| Service area | Helps local SEO and expectation setting | Confirm Đồng Tháp only or neighboring provinces too. |
| Source content approval | Prevents stale or copied content | Import from source, rewrite, then mark approved before publish/AI indexing. |

## Phase 0 Exit Criteria

- [x] Sales identity is confirmed.
- [x] Main contact channels are confirmed.
- [x] Dealer/unit text is confirmed as Đồng Tháp Ford.
- [x] Temporary production URL is confirmed: `https://huy-ford-dong-thap.pages.dev`.
- [x] Deploy platform direction is selected: Cloudflare Pages for MVP.
- [x] MVP logo decision is confirmed: custom wordmark, not Ford logo mimic.
- [x] Primary source site is confirmed: https://dongthapford.com/.
- [x] Source ingestion rules are documented.
- [x] Brand/media permission is moved to release gate with safe MVP fallback.

Resolved in Phase 1 seed:

- [x] Work-hours fallback policy and service-area seed are documented in `docs/PHASE_1_DISCOVERY_AND_CONTENT.md`.
