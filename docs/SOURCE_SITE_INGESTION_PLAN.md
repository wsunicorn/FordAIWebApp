# Source Site Ingestion Plan

## Phase 0 Decision

Primary official source for initial content study: https://dongthapford.com/

Last checked: 2026-06-07.

This source is used to learn site structure, vehicle categories, public pages, price/promotion patterns, contact flows, service content and available media references. It must not be copied verbatim into the MVP. Public copy should be rewritten for anh Huỳnh Đang Huy's consultation flow, with source URL and update date preserved.

Current Phase 1 seed: [PHASE_1_DISCOVERY_AND_CONTENT.md](PHASE_1_DISCOVERY_AND_CONTENT.md).

## Source Snapshot

| Source | Lastmod from sitemap | Use |
| --- | --- | --- |
| https://dongthapford.com/sitemap_index.xml | 2026-06-06T01:26:49+00:00 | Discover all source sitemaps. |
| https://dongthapford.com/page-sitemap.xml | 2026-05-14T06:45:16+00:00 | Discover static pages, calculators, contact, local SEO pages. |
| https://dongthapford.com/product-sitemap.xml | 2026-04-06T15:28:19+00:00 | Discover product/vehicle detail URLs and media references. |
| https://dongthapford.com/post-sitemap.xml | 2026-06-06T01:26:49+00:00 | Discover news, promotion and article content. |

Homepage observations from 2026-06-07:

- Dealer display: An Giang Ford - CN Đồng Tháp.
- Address shown on source site: QL 30, An Định, phường Mỹ Trà, Tỉnh Đồng Tháp.
- Source site hotline shown: 0915 617 776.
- Main public flows: bảng giá xe, sản phẩm, dịch vụ, dự toán trả góp, dự toán lăn bánh, tin tức, khuyến mãi, liên hệ, báo giá ưu đãi, đặt hẹn dịch vụ, đăng ký lái thử.
- Vehicle groups shown: Territory, Transit, Ranger, Everest, Mustang Mach-E, Ranger Raptor, Explorer.
- Source site has price/promotion content for 6/2026, but MVP must still show "giá tham khảo" and route final confirmation to anh Huy.
- Post sitemap contains news, promotions, service articles, mobile-service events, used-car posts, recruitment posts and local SEO articles.

## Initial URL Groups

Important: the URL lists below are seed examples for humans. The crawler/importer must read every `<url>` node from the tracked sitemaps on each scheduled run and store metadata for every discovered URL. Do not manually maintain the full source inventory in Markdown.

Core pages to study:

- https://dongthapford.com/
- https://dongthapford.com/bang-gia-xe/
- https://dongthapford.com/bang-gia-xe-ford-moi-nhat-xe-co-san-giao-ngay/
- https://dongthapford.com/chi-phi-lan-banh/
- https://dongthapford.com/chi-phi-tra-gop/
- https://dongthapford.com/dang-ky-lai-thu/
- https://dongthapford.com/lien-he/
- https://dongthapford.com/gioi-thieu-ve-an-giang-ford/
- https://dongthapford.com/chinh-sach-bao-hanh/
- https://dongthapford.com/chinh-sach-bao-mat-thong-tin/

Vehicle/product URLs from product sitemap:

- https://dongthapford.com/product/ford-explorer/
- https://dongthapford.com/product/ford-mustang-mach-e/
- https://dongthapford.com/product/ranger-raptor/
- https://dongthapford.com/product/ford-ranger-xl-2-0l-4x4-mt/
- https://dongthapford.com/product/ford-ranger-sport/
- https://dongthapford.com/product/ford-ranger-xls-2-0l-4x2-at/
- https://dongthapford.com/product/ford-ranger-xls-2-0l-4x4-at/
- https://dongthapford.com/product/ford-ranger-wildtrak-the-he-moi-2-0l-at-4x4/
- https://dongthapford.com/product/ford-ranger-stormtrak/
- https://dongthapford.com/product/ford-everest-ambiente/
- https://dongthapford.com/product/ford-everest-sport-2-0l-at-4x2/
- https://dongthapford.com/product/ford-everest-sport-se/
- https://dongthapford.com/product/ford-everest-titatium-2-0l-at-4x2/
- https://dongthapford.com/product/ford-everest-titatium-2-0l-at-4wd/
- https://dongthapford.com/product/ford-everest-platinum/
- https://dongthapford.com/product/territory-trend/
- https://dongthapford.com/product/ford-territory-sport-1-5l-at/
- https://dongthapford.com/product/ford-territory-titanium-1-5l-at/
- https://dongthapford.com/product/ford-territory-titanium-x-1-5l-at/
- https://dongthapford.com/product/transit/
- https://dongthapford.com/product/ford-transit-premium-16-cho/
- https://dongthapford.com/product/ford-transit-premium-18-cho/
- https://dongthapford.com/product/ford-transit-limousine/
- https://dongthapford.com/product/ford-transit-cuu-thuong-dau/
- https://dongthapford.com/product/ford-transit-cuu-thuong-xang/

Post/article examples from post sitemap:

- https://dongthapford.com/khuyen-mai-ford-territory-thang-6-2026-ruoc-xe-chi-voi-79-trieu-dong/
- https://dongthapford.com/ford-territory-2026-cap-nhat-gia-moi-chi-tu-739-trieu-dong/
- https://dongthapford.com/chuong-trinh-khuyen-mai-mua-xe-ford-thang-10-2025/
- https://dongthapford.com/lai-thu-sa-dec-dong-thap/
- https://dongthapford.com/sua-chua-luu-dong-dong-thap-07-3/
- https://dongthapford.com/dich-vu-luu-dong-nhanh-chong-thuan-tien/
- https://dongthapford.com/xe-qua-su/
- https://dongthapford.com/bao-hanh-tieu-chuan/
- https://dongthapford.com/bao-hanh-mo-rong/
- https://dongthapford.com/phu-tung-chinh-hang-ford/

## Ingestion Rules

For each imported source record, store:

- `source_url`
- `source_title`
- `source_type`
- `source_lastmod`
- `fetched_at`
- `content_hash`
- `approval_status`
- `verified_by`
- `verified_at`
- `review_due_at`

For media, store references first:

- `source_image_url`
- `alt_candidate`
- `related_page_url`
- `permission_status`
- `approved_for_public_use`

Do not hotlink source images in production unless explicitly approved. Prefer approved uploads to project storage with optimized AVIF/WebP derivatives.

## Rewrite Policy

- Keep facts such as model names, variant names, published prices and technical specifications tied to source URLs.
- Rewrite descriptions in the MVP voice: clear, concise, consultation-focused and local.
- Do not copy long paragraphs, campaign copy, page layout or image sets directly.
- Every price/promotion block must show update date and "giá tham khảo".
- AI can cite the source and summarize, but must hand off final price, inventory, delivery time, special promotions and loan approval to anh Huy.

## Freshness Plan

Daily:

- Fetch source sitemaps.
- Compare `lastmod` and content hash for tracked URLs.
- Flag changed price, promotion, vehicle and policy pages.
- Remove expired source documents from AI retrieval until reviewed.

Weekly:

- Generate a source freshness report for anh Huy/admin.
- Review high-traffic vehicle pages first.
- Revalidate affected public pages after approved updates.

Before public launch:

- Confirm permission for official logo, showroom photos, catalogue PDFs and vehicle media.
- Replace any unapproved media with custom wordmark, placeholders or approved assets.
- Confirm whether the source-site hotline should appear anywhere. MVP default uses anh Huy's phone/Zalo as primary contact.
