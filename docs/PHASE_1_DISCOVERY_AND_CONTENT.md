# Phase 1 Discovery And Content

## Status

Phase 1 is completed for content discovery and MVP seed data.

Last source check: 2026-06-07.

This file is the working seed for Phase 2/3 implementation. The data below is source-backed and ready to import as draft/approved seed records depending on risk level. Price, promotion, loan and fee data must still be displayed as "tham khảo" and routed to anh Huỳnh Đang Huy for final confirmation.

## Local Asset Moved And Approved

| Asset | New path | Status | Intended use |
| --- | --- | --- | --- |
| `Huy_image.jpg` | `assets/images/people/huy-dang-huy.jpg` | Approved for MVP use by project owner request on 2026-06-07 | Hero portrait, sales profile, contact section |

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

## Dealer And Source Profile

| Field | Source-backed value | MVP use |
| --- | --- | --- |
| Source dealer display | An Giang Ford - CN Đồng Tháp | Use only as source/dealer context, not as official website claim. |
| Public unit text | Đồng Tháp Ford | Use in anh Huy's role line. |
| Source address | QL 30, An Định, phường Mỹ Trà, Tỉnh Đồng Tháp | Can be shown as dealer/source location if approved. |
| Source hotline | 0915 617 776 | Keep as source/dealer reference. MVP primary CTA remains anh Huy's phone/Zalo. |
| Source email | lienhe@dongthapford.com | Keep as source/dealer reference. MVP primary email remains `hh753741@gmail.com`. |

## Work Hours Policy

No personal work-hour window for anh Huy is available from the provided data.

MVP policy:

- Do not publish a fixed personal working-hours claim yet.
- Let quote/test-drive/contact forms receive leads 24/7.
- Keep direct phone/Zalo CTA visible.
- Use copy such as "Anh Huy sẽ kiểm tra và phản hồi sớm" instead of promising exact response time.
- The source site labels its dealer hotline as 24/7, but the MVP should not transfer that claim to anh Huy's personal number unless he confirms it.

## Service Area Seed

Primary area:

- Đồng Tháp.

Source-derived extended area:

- An Giang.
- Vĩnh Long.
- Cần Thơ.
- Cà Mau.
- Phú Quốc.
- Rạch Giá.
- Khu vực đồng bằng sông Cửu Long.

MVP public wording:

```text
Anh Huy tư vấn khách tại Đồng Tháp và có thể hỗ trợ khu vực lân cận. Với lịch lái thử, giao xe hoặc báo giá theo tỉnh, vui lòng để lại thông tin để anh Huy xác nhận trực tiếp.
```

## Vehicle And Price Seed

Source: https://dongthapford.com/bang-gia-xe/

Displayed source period: 6/2026.

Status for MVP: approved as seed/reference data, but public UI must label as "giá tham khảo" and include source/update date.

### Ford Ranger

| Variant | Seed price |
| --- | ---: |
| Ranger XL 4x4 MT | 669.000.000 VNĐ |
| Ranger XLS 4x2 AT | 707.000.000 VNĐ |
| Ranger XLS 4x4 AT | 776.000.000 VNĐ |
| Ranger Sport | 864.000.000 VNĐ |
| Ranger Wildtrak 4x4 | 979.000.000 VNĐ |
| Ranger StormTrak | 1.039.000.000 VNĐ |
| Ranger Raptor | 1.299.000.000 VNĐ |

### Ford Everest

| Variant | Seed price |
| --- | ---: |
| Everest Ambiente | 1.099.000.000 VNĐ |
| Everest Sport | 1.178.000.000 VNĐ |
| Everest Sport SE | 1.199.000.000 VNĐ |
| Everest Titanium | 1.299.000.000 VNĐ |
| Everest Platinum | 1.545.000.000 VNĐ |

### Ford Territory

| Variant | Seed price |
| --- | ---: |
| Territory Trend | 739.000.000 VNĐ |
| Territory Titanium | 819.000.000 VNĐ |
| Territory Titanium X | 875.000.000 VNĐ |

### Ford Transit

| Variant | Seed price |
| --- | ---: |
| Transit Trend 16 chỗ | 907.000.000 VNĐ |
| Transit Premium 16 chỗ | 999.000.000 VNĐ |
| Transit Premium+ 18 chỗ | 1.091.000.000 VNĐ |

### Ford Mustang Mach-E

| Variant | Seed price |
| --- | ---: |
| Mustang Mach-E Premium AWD | 2.599.000.000 VNĐ |

### Ford Transit Limousine

| Variant | Seed price |
| --- | ---: |
| Transit Limousine 10 chỗ | 1.388.000.000 VNĐ |
| Transit Limousine 12 chỗ | 1.499.000.000 VNĐ |

### Tracked But Needs Detail Review

| Model | Reason |
| --- | --- |
| Ford Explorer | Present in navigation/product sitemap, but not in the captured 6/2026 price table segment. |
| Transit cứu thương dầu/xăng | Present in product sitemap, special-use vehicle needs separate content review. |

## Product URL Seed

Source: https://dongthapford.com/product-sitemap.xml

Use these as initial product records and source URLs:

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

## Promotion Seed

Source examples:

- Homepage and post sitemap show current/near-current promotion content.
- Latest observed post sitemap item: https://dongthapford.com/khuyen-mai-ford-territory-thang-6-2026-ruoc-xe-chi-voi-79-trieu-dong/
- Homepage mentions promotion rules by version/model, loan support and free test drive.

MVP policy:

- Store promotions as draft until anh Huy/admin approves.
- Never present a promotion as active without `effective_from`, `effective_to` or `review_due_at`.
- If a campaign lacks clear expiry, show "cần anh Huy xác nhận".

## On-road Cost Assumptions

Source: https://dongthapford.com/chi-phi-lan-banh/

Seed assumptions:

| Field | Source-backed seed |
| --- | --- |
| Vehicle groups | Ranger, Ranger Raptor, Transit, Mustang Mach-E, Territory, Everest |
| Registration regions | Hà Nội, TP. HCM, Khác |
| Registration fee assumption shown | 7.2% |
| Inspection fee | 340.000 VNĐ |
| Road-use fee per year | 1.560.000 VNĐ |
| Civil liability insurance per year | 480.000 VNĐ |
| Physical insurance | User/configurable field |

MVP note: Đồng Tháp-specific lăn bánh should be calculated as "Khác" unless a separate Đồng Tháp rule table is confirmed.

## Loan Assumptions

Source: https://dongthapford.com/chi-phi-tra-gop/

Seed assumptions:

| Field | Source-backed seed |
| --- | --- |
| Vehicle groups | Ranger, Ranger Raptor, Transit, Mustang Mach-E, Territory, Everest |
| Loan term options | 1 to 10 years |
| First-year interest rate options | 5% to 15%, step 0.5% |
| Following-year interest rate options | 5% to 15%, step 0.5% |

MVP note: loan results are estimates only. AI and UI must not say the loan is approved.

## Lead And Form Flow Seed

Source pages:

- https://dongthapford.com/lien-he/
- https://dongthapford.com/bao-gia-uu-dai-xe-ford/
- https://dongthapford.com/dang-ky-lai-thu/

Useful intent options observed:

- Mua xe.
- Lái thử.
- Bảo hiểm.
- Bảo dưỡng.
- Trả góp.
- Khác.

Useful location/appointment options observed:

- Showroom.
- Tại nhà riêng.
- Chỉ tư vấn trước qua điện thoại.

MVP lead form fields:

- Họ tên.
- Số điện thoại.
- Xe quan tâm.
- Khu vực.
- Nhu cầu.
- Hình thức thanh toán: trả góp/trả thẳng.
- Ghi chú.
- Đồng ý xử lý thông tin.

## FAQ Seed

These are draft FAQ topics for Phase 2 content and AI seed documents:

- Giá xe Ford hiện tại là bao nhiêu và ngày cập nhật là khi nào?
- Giá lăn bánh tại Đồng Tháp tính gồm những khoản nào?
- Tôi muốn trả góp thì cần chuẩn bị gì?
- Lãi suất trả góp trên website có phải lãi suất chính thức không?
- Có thể đăng ký lái thử tại nhà không?
- Xe nào phù hợp cho gia đình 5-7 người?
- Xe nào phù hợp kinh doanh, chở khách hoặc dịch vụ?
- Ranger khác Raptor ở điểm nào?
- Everest Sport, Titanium và Platinum khác nhau thế nào?
- Territory Trend, Titanium và Titanium X khác nhau thế nào?
- Có xe sẵn/màu sẵn không?
- Ưu đãi tháng này còn áp dụng không?
- Bảo hành, bảo dưỡng và phụ tùng chính hãng xử lý ở đâu?
- Anh Huy có hỗ trợ khách ngoài Đồng Tháp không?

## AI Must Handoff

AI must hand off to anh Huy when the user asks about:

- Giá chốt.
- Xe sẵn, màu sẵn, ngày giao xe.
- Ưu đãi riêng, quà tặng, giảm thêm.
- Giữ xe, đặt cọc, ký hợp đồng.
- Duyệt vay, hồ sơ vay, cam kết lãi suất.
- Khiếu nại, tranh chấp, pháp lý.
- Thông tin không có nguồn hoặc nguồn xung đột.
- Dữ liệu khách hàng khác hoặc yêu cầu vượt quyền riêng tư.

## Source Update Process

Daily after app exists:

- Fetch `sitemap_index.xml`.
- Fetch child sitemaps.
- Store URL, `lastmod`, source type and content hash.
- Flag changed records for review.

Weekly:

- Review changed vehicle/price/promotion pages.
- Review top lead/search pages first.
- Generate freshness report.

After approval:

- Update structured records.
- Revalidate affected public pages.
- Re-index approved AI documents.
- Keep old version in audit log.

## Phase 1 Remaining Release Gates

These do not block Phase 1 completion:

- Final custom domain.
- Official Ford/dealer logo and media permissions.
- Exact personal working hours, if anh Huy wants to publish them.
- Additional showroom/delivery/customer photos.
