# Content And Data Governance

## Goal

Keep vehicle, price, promotion and AI answers accurate enough for consultation while making clear that final transaction details must be confirmed by anh Huy or the dealership.

The website should learn from official/current sources, but public content must be rewritten, verified and approved before display or AI indexing.

## Primary Source Site

Primary source for Phase 1 ingestion: https://dongthapford.com/

Last checked: 2026-06-07.

Tracked source sitemaps:

- https://dongthapford.com/sitemap_index.xml
- https://dongthapford.com/page-sitemap.xml
- https://dongthapford.com/product-sitemap.xml
- https://dongthapford.com/post-sitemap.xml

See [SOURCE_SITE_INGESTION_PLAN.md](SOURCE_SITE_INGESTION_PLAN.md) for URL groups and ingestion rules.

## Data Categories

| Category | Examples | Owner | Freshness |
| --- | --- | --- | --- |
| Sales profile | Name, phone, Zalo, branch, work hours | Anh Huy | Review monthly |
| Dealer/source profile | Source address, source hotline, dealer pages | Admin/Anh Huy | Review monthly |
| Vehicle catalogue | Models, variants, specs, colors | Admin/Anh Huy | Review on model update |
| Price | List price, effective date, source | Anh Huy | Review when changed |
| Promotion | Offers, gifts, conditions | Anh Huy | Review by campaign expiry |
| Fees | Registration, insurance assumptions | Admin/Anh Huy | Review quarterly or when policy changes |
| Loan assumptions | Rate, term, bank note | Anh Huy | Review when program changes |
| FAQ | Common questions and answers | Anh Huy/Admin | Review monthly |
| AI documents | Catalogue, policy, scripts | Admin | Review before indexing |
| Leads | Customer contact and need | Anh Huy | Daily |
| Media | Portrait, showroom, vehicle images, catalogue PDFs | Anh Huy/Admin | Review permission before public use |

## Confirmed Sales Profile

| Field | Value |
| --- | --- |
| Name | Huỳnh Đang Huy |
| Role | Tư Vấn Bán Hàng |
| Unit | Đồng Tháp Ford |
| Phone | 0766994952 |
| Zalo | 0818655369 |
| Email | hh753741@gmail.com |
| Facebook | https://www.facebook.com/share/1X2vMYQ3T4/?mibextid=wwXIfr |
| Temporary URL | https://huy-ford-dong-thap.pages.dev |
| Portrait | `assets/images/people/huy-dang-huy.jpg` |

## Local Assets

| File | Intended use | Status |
| --- | --- | --- |
| `assets/images/people/huy-dang-huy.jpg` | Portrait/showroom hero image | Approved for MVP use by project owner request on 2026-06-07 |

## Approval Status

Use these statuses:

- `draft`
- `pending_review`
- `approved`
- `expired`
- `archived`

Only `approved` content should appear on public pages or in AI RAG.

## Source Record Rules

Each imported source record needs:

- `source_url`
- `source_title`
- `source_type`
- `source_lastmod`
- `fetched_at`
- `content_hash`
- `verified_by`
- `verified_at`
- `effective_from`
- `effective_to` if known
- `review_due_at`
- `approval_status`

Imported source content should be normalized into structured fields, then rewritten for the MVP. Do not publish raw copied paragraphs as final public content unless usage rights and editorial approval are recorded.

## Freshness Rules

- Price and promotions must show update date.
- Expired promotions must not be shown as active.
- AI must avoid using expired documents.
- When freshness is uncertain, show a "cần xác nhận với anh Huy" note.
- Every freshness-sensitive record should have `review_due_at`.
- High-traffic pages must be reviewed first after a price/promotion change.
- Sitemap `<lastmod>` should change only when page content meaningfully changes.
- Source sitemap changes should create review tasks, not automatically publish public changes.

## Freshness Automation

Daily job:

- Fetch tracked source sitemaps.
- Compare `lastmod` and `content_hash`.
- Flag changed vehicle, price, promotion, article, policy and calculator pages.
- Mark records past `effective_to` as `expired`.
- Hide expired promotions from active promotion blocks.
- Remove expired AI documents from retrieval.
- Revalidate affected public pages after approved updates.
- Notify anh Huy/admin about expired or changed records.

Weekly job:

- Find records with `review_due_at` in the next 7 days.
- Generate freshness report.
- List pages that have not been reviewed in the expected window.
- List AI documents due for review.
- List source URLs that changed since the last report.

After any admin update:

- Write audit log.
- Update `verified_by`, `verified_at`, `review_due_at`.
- Trigger page revalidation.
- Trigger RAG re-index if AI source changed.
- Update sitemap `lastmod` only for affected canonical URLs.

## Public Freshness UI

Every price/promotion/fee-sensitive UI should show:

- Last verified date.
- Source or source label.
- Whether the value is "tham khảo".
- Contact CTA when final confirmation is needed.

If a record is `review_due`, public UI may still show it with a softer note. If a record is `expired`, public UI should hide it from active offers or show "cần xác nhận lại với anh Huy" instead of a number.

## Media Rules

Allowed immediately for MVP:

- Custom personal mark in `assets/brand/huy-dang-huy-logo.svg`.
- Anh Huy portrait in `assets/images/people/huy-dang-huy.jpg`.
- Text-only dealer/unit display: Đồng Tháp Ford.
- Anh Huy contact information that has been confirmed.

Allowed after permission record:

- Official Ford/dealership logo.
- Anh Huy portrait with consent.
- Showroom photos with permission.
- Official/approved vehicle images.
- Catalogue PDFs or screenshots.
- Customer delivery photos with written or recorded consent.

Not allowed:

- Ford-like logo created to look similar to the official Ford oval/script.
- Scraped images without permission.
- Customer faces/license plates without consent.
- Images implying official Ford endorsement when not approved.
- Hotlinking source images in production without approval.

## Content Voice

Use clear Vietnamese:

- "Giá tham khảo"
- "Cập nhật ngày"
- "Cần anh Huy xác nhận"
- "Ước tính dựa trên giả định"

Avoid:

- "Cam kết"
- "Chắc chắn"
- "Giá tốt nhất"
- "Duyệt vay"
- "Giao ngay" unless inventory is verified.

## Content Checklist For Anh Huy

- [x] Họ tên, chức danh, branch.
- [x] Hotline.
- [x] Zalo number.
- [x] Email/Facebook if used.
- [x] Temporary URL.
- [x] MVP logo policy.
- [x] Primary source site and sitemap list.
- [x] Phase 1 discovery seed: `docs/PHASE_1_DISCOVERY_AND_CONTENT.md`.
- [ ] Zalo QR/link.
- [x] Work hours fallback policy.
- [x] Service area seed.
- [x] Portrait moved and approved for MVP: `assets/images/people/huy-dang-huy.jpg`.
- [ ] Additional approved showroom photos.
- [x] Vehicle list and variants seed.
- [x] Price table seed.
- [x] Promotion seed.
- [x] Fee assumptions seed.
- [x] Loan assumptions seed.
- [x] FAQ seed.
- [ ] Legal/brand permission notes for official media.

## Data Retention

Suggested default:

- Public lead data retained for 12 months unless customer asks removal.
- AI chat logs retained for 90 days for QA unless linked to active lead.
- Admin audit logs retained for 12 months.

Confirm retention with owner before launch.
