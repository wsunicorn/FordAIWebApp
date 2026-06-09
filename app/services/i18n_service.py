from __future__ import annotations

# ruff: noqa: E501
from collections.abc import Mapping
from urllib.parse import parse_qsl, urlencode

from fastapi import Request

from app.data.site_content import Variant, Vehicle

SUPPORTED_LOCALES = ("vi", "en")
DEFAULT_LOCALE = "vi"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "vi": {
        "language.label": "Ngôn ngữ",
        "language.vi": "VI",
        "language.en": "EN",
        "nav.vehicles": "Xe Ford",
        "nav.prices": "Bảng giá",
        "nav.on_road": "Lăn bánh",
        "nav.loan": "Trả góp",
        "nav.ai": "AI tư vấn",
        "nav.promotions": "Ưu đãi",
        "nav.faq": "FAQ",
        "nav.home": "Trang chủ",
        "nav.choose_vehicle": "Chọn xe",
        "nav.ask_ai": "Hỏi AI",
        "action.call_huy": "Gọi anh Huy",
        "action.call": "Gọi điện",
        "action.quote": "Nhận báo giá",
        "action.view_detail": "Xem chi tiết",
        "action.chat_zalo": "Chat Zalo",
        "action.open_ai": "Mở Trợ Lý AI",
        "brand.home_aria": "Trang chủ Huỳnh Đang Huy Ford",
        "footer.contact": "Liên hệ tư vấn",
        "footer.reference_title": "Về thông tin tham khảo",
        "footer.reference_body": "Giá bán, thông số và ưu đãi mang tính chất tham khảo. Được cập nhật từ",
        "footer.reference_notice": "Vui lòng liên hệ trực tiếp anh Huy để xác nhận giá chốt, tồn kho và lịch lái thử thực tế.",
        "footer.about": "Kênh tư vấn cá nhân để khách tham khảo thông tin xe Ford và liên hệ trực tiếp anh Huy tại Đồng Tháp Ford. Mọi thông tin giá, ưu đãi và tình trạng xe cần được xác nhận lại trước khi quyết định.",
        "form.intro": "Điền thông tin ngắn, anh Huy sẽ kiểm tra giá lăn bánh, ưu đãi và phản hồi lại cho anh/chị.",
        "form.full_name": "Họ tên",
        "form.full_name_placeholder": "Tên của anh/chị",
        "form.phone": "Số điện thoại",
        "form.phone_placeholder": "Số để anh Huy gọi lại",
        "form.vehicle": "Xe quan tâm",
        "form.vehicle_placeholder": "Chọn xe nếu đã biết",
        "form.area": "Khu vực",
        "form.area_placeholder": "Đồng Tháp, Cần Thơ...",
        "form.note": "Ghi chú",
        "form.note_placeholder": "Ví dụ: Quan tâm bản Titanium+, muốn tư vấn trả góp, lịch hẹn lái thử...",
        "form.default_button": "Gửi yêu cầu",
        "form.disclaimer": "Website không nhận đặt cọc hoặc thanh toán. Mọi thủ tục sẽ làm việc trực tiếp sau khi tư vấn.",
        "form.success": "Đã nhận yêu cầu. Anh Huy sẽ liên hệ lại sớm.",
        "vehicle.price_from": "Giá từ (tham khảo)",
        "vehicle.no_image": "Chưa có ảnh cho",
        "vehicle.has_promotion": "Có ưu đãi",
        "home.badge": "Kênh tư vấn cá nhân của anh Huy",
        "home.hero_title": "Tư Vấn Tận Tâm.<br>Đồng Hành Dài Lâu.",
        "home.hero_body": "Xin chào, tôi là Huỳnh Đang Huy, tư vấn bán hàng tại Đồng Tháp Ford. Tôi hỗ trợ anh/chị chọn xe phù hợp nhu cầu, dự toán chi phí và kết nối trực tiếp khi cần xác nhận giá, ưu đãi hoặc lịch lái thử.",
        "home.source_note": "Giá tham khảo từ nguồn {source_period}, kiểm tra {source_checked_at}. Không phải giá chốt.",
        "home.featured_title": "Dòng Xe Nổi Bật",
        "home.featured_body": "Tham khảo các dòng xe Ford đang được khách hàng hỏi nhiều. Mỗi giá đều là tham khảo và có nguồn để kiểm tra lại.",
        "home.ai_kicker": "Trợ lý thông minh",
        "home.ai_title": "Hỏi AI về xe Ford",
        "home.ai_body": "Hỏi nhanh về dòng xe, phiên bản hoặc chi phí dự kiến. AI chỉ trả lời trong phạm vi dữ liệu đã duyệt và chuyển sang anh Huy khi cần xác nhận trực tiếp.",
        "home.ai_start": "Bắt đầu trò chuyện",
        "home.on_road": "Dự toán lăn bánh",
        "home.process_title": "Quy Trình Mua Xe Đơn Giản",
        "home.process_body": "Các bước được trình bày rõ để anh/chị biết khi nào đang tham khảo, khi nào cần anh Huy xác nhận trực tiếp.",
        "home.step1_title": "1. Tư Vấn",
        "home.step1_body": "Lắng nghe nhu cầu và đề xuất dòng xe phù hợp nhất với ngân sách.",
        "home.step2_title": "2. Lái Thử",
        "home.step2_body": "Trải nghiệm thực tế xe tại nhà hoặc tại showroom Đồng Tháp Ford.",
        "home.step3_title": "3. Báo Giá & Trả Góp",
        "home.step3_body": "Phương án tài chính minh bạch, chi tiết lăn bánh và lãi suất ưu đãi.",
        "home.step4_title": "4. Giao Xe",
        "home.step4_body": "Giao xe tận nơi, hỗ trợ thủ tục đăng ký trọn gói và nhanh chóng.",
        "home.lead_title": "Nhận tư vấn từ anh Huy",
        "home.lead_button": "Gửi thông tin",
        "vehicles.badge": "Danh sách xe",
        "vehicles.title": "Khám phá các dòng xe Ford.",
        "vehicles.body": "Lọc nhanh theo tên hoặc nhóm xe. Giá hiển thị là giá tham khảo theo nguồn đã ghi nhận.",
        "vehicles.search_label": "Tìm xe Ford theo tên hoặc nhóm xe",
        "vehicles.all": "Tất cả",
        "vehicles.pickup": "Bán tải",
        "vehicles.commercial": "Thương mại",
        "vehicles.empty_title": "Không thấy xe phù hợp",
        "vehicles.empty_body": "Bộ lọc không khớp với dòng xe nào. Hãy gọi anh Huy để được tư vấn trực tiếp.",
        "prices.badge": "Bảng giá tham khảo",
        "prices.title": "Giá bán các dòng xe Ford.",
        "prices.body": "Cập nhật theo nguồn {source_period} (kiểm tra {source_checked_at}). Giá có thể thay đổi theo khu vực, phiên bản, ưu đãi hiện hành và thời điểm giao xe.",
        "prices.source": "Xem nguồn dữ liệu",
        "prices.final_title": "Cần giá chốt tốt nhất?",
        "prices.final_body": "Gọi ngay cho anh Huy để nhận thông tin về ưu đãi tiền mặt, tặng phụ kiện và lịch xe về.",
        "quote.badge": "Báo giá",
        "quote.title": "Nhận báo giá trực tiếp từ anh Huy.",
        "quote.body": "Gửi dòng xe anh/chị quan tâm và số điện thoại. Anh Huy sẽ kiểm tra giá chốt, ưu đãi hiện hành, tồn kho và gọi lại ngay.",
        "quote.form_title": "Yêu cầu báo giá lăn bánh",
        "quote.button": "Gửi yêu cầu báo giá",
        "meta.home.title": "Huỳnh Đang Huy - Tư vấn Ford Đồng Tháp",
        "meta.home.description": "Tham khảo xe Ford, dự toán chi phí và liên hệ anh Huỳnh Đang Huy tại Đồng Tháp Ford để nhận tư vấn trực tiếp.",
        "meta.vehicles.title": "Danh sách xe Ford tham khảo",
        "meta.vehicles.description": "Xem các dòng xe Ford, giá tham khảo và gửi yêu cầu báo giá cho anh Huy.",
        "meta.prices.title": "Bảng giá Ford tham khảo",
        "meta.prices.description": "Bảng giá Ford tham khảo có nguồn và ngày kiểm tra, cần anh Huy xác nhận trước khi chốt.",
        "meta.quote.title": "Nhận báo giá Ford từ anh Huy",
        "meta.quote.description": "Gửi xe quan tâm và số điện thoại để anh Huy kiểm tra giá, ưu đãi và gọi lại.",
    },
    "en": {
        "language.label": "Language",
        "language.vi": "VI",
        "language.en": "EN",
        "nav.vehicles": "Ford models",
        "nav.prices": "Prices",
        "nav.on_road": "On-road cost",
        "nav.loan": "Financing",
        "nav.ai": "AI advisor",
        "nav.promotions": "Offers",
        "nav.faq": "FAQ",
        "nav.home": "Home",
        "nav.choose_vehicle": "Choose car",
        "nav.ask_ai": "Ask AI",
        "action.call_huy": "Call Huy",
        "action.call": "Call",
        "action.quote": "Get quote",
        "action.view_detail": "View details",
        "action.chat_zalo": "Chat on Zalo",
        "action.open_ai": "Open AI Assistant",
        "brand.home_aria": "Huynh Dang Huy Ford home",
        "footer.contact": "Contact",
        "footer.reference_title": "Reference information",
        "footer.reference_body": "Prices, specifications and offers are for reference only. Updated from",
        "footer.reference_notice": "Please contact Huy directly to confirm final price, stock status and actual test-drive schedule.",
        "footer.about": "A personal consultation channel for customers to review Ford vehicle information and contact Huy directly at Dong Thap Ford. Prices, offers and vehicle availability must be confirmed before making a decision.",
        "form.intro": "Leave a short request and Huy will check on-road pricing, offers and reply to you.",
        "form.full_name": "Full name",
        "form.full_name_placeholder": "Your name",
        "form.phone": "Phone number",
        "form.phone_placeholder": "Number for Huy to call back",
        "form.vehicle": "Vehicle of interest",
        "form.vehicle_placeholder": "Choose a vehicle if known",
        "form.area": "Area",
        "form.area_placeholder": "Dong Thap, Can Tho...",
        "form.note": "Note",
        "form.note_placeholder": "Example: Interested in Platinum +, financing advice, test-drive appointment...",
        "form.default_button": "Send request",
        "form.disclaimer": "This website does not take deposits or payments. All procedures are handled directly after consultation.",
        "form.success": "Request received. Huy will contact you soon.",
        "vehicle.price_from": "From (reference)",
        "vehicle.no_image": "No image for",
        "vehicle.has_promotion": "Offer available",
        "home.badge": "Huy's personal consultation channel",
        "home.hero_title": "Careful Advice.<br>Long-Term Support.",
        "home.hero_body": "Hello, I am Huynh Dang Huy, sales consultant at Dong Thap Ford. I help you choose the right Ford, estimate ownership costs and connect directly when final price, offers or test-drive schedules need confirmation.",
        "home.source_note": "Reference prices from {source_period}, checked {source_checked_at}. Not a final quote.",
        "home.featured_title": "Featured Ford Models",
        "home.featured_body": "Browse Ford models customers ask about most. Every displayed price is a reference price with a source for verification.",
        "home.ai_kicker": "Smart assistant",
        "home.ai_title": "Ask AI about Ford vehicles",
        "home.ai_body": "Ask quickly about models, variants or estimated costs. AI answers only from approved data and hands off to Huy when direct confirmation is required.",
        "home.ai_start": "Start chat",
        "home.on_road": "Estimate on-road cost",
        "home.process_title": "A Simple Buying Process",
        "home.process_body": "Clear steps help you know when information is only for reference and when Huy should confirm directly.",
        "home.step1_title": "1. Consultation",
        "home.step1_body": "Understand your needs and suggest the Ford model that best fits your budget.",
        "home.step2_title": "2. Test Drive",
        "home.step2_body": "Experience the vehicle at home or at Dong Thap Ford showroom.",
        "home.step3_title": "3. Quote & Financing",
        "home.step3_body": "Transparent financial options, on-road cost details and financing estimates.",
        "home.step4_title": "4. Delivery",
        "home.step4_body": "Vehicle delivery with registration support and clear handover steps.",
        "home.lead_title": "Get advice from Huy",
        "home.lead_button": "Send information",
        "vehicles.badge": "Vehicle list",
        "vehicles.title": "Explore Ford models.",
        "vehicles.body": "Filter quickly by name or vehicle group. Displayed prices are reference prices from recorded sources.",
        "vehicles.search_label": "Search Ford by name or group",
        "vehicles.all": "All",
        "vehicles.pickup": "Pickup",
        "vehicles.commercial": "Commercial",
        "vehicles.empty_title": "No matching vehicle",
        "vehicles.empty_body": "The filter does not match any vehicle. Call Huy for direct advice.",
        "prices.badge": "Reference price list",
        "prices.title": "Ford vehicle prices.",
        "prices.body": "Updated from source {source_period} (checked {source_checked_at}). Prices may change by area, variant, active offer and delivery timing.",
        "prices.source": "View data source",
        "prices.final_title": "Need the best final quote?",
        "prices.final_body": "Call Huy to check cash offers, accessories and incoming vehicle schedule.",
        "quote.badge": "Quote",
        "quote.title": "Get a direct quote from Huy.",
        "quote.body": "Send the Ford model you are interested in and your phone number. Huy will check final pricing, current offers, stock and call you back.",
        "quote.form_title": "Request an on-road quote",
        "quote.button": "Send quote request",
        "meta.home.title": "Huynh Dang Huy - Ford Dong Thap consultant",
        "meta.home.description": "Browse Ford models, estimate costs and contact Huynh Dang Huy at Dong Thap Ford for direct consultation.",
        "meta.vehicles.title": "Reference Ford model list",
        "meta.vehicles.description": "View Ford models, reference prices and send a quote request to Huy.",
        "meta.prices.title": "Reference Ford price list",
        "meta.prices.description": "Reference Ford prices with source and checked date. Huy should confirm before any final decision.",
        "meta.quote.title": "Get a Ford quote from Huy",
        "meta.quote.description": "Send your vehicle of interest and phone number so Huy can check pricing, offers and call back.",
    },
}

VEHICLE_TRANSLATIONS: dict[str, dict[str, str | tuple[str, ...]]] = {
    "ford-territory": {
        "category": "5-seat SUV",
        "summary": "A spacious urban SUV for young families who need an easy daily vehicle.",
        "fit": "Family, city driving, weekends",
        "tags": ("SUV", "5 seats", "Family"),
    },
    "ford-everest": {
        "category": "7-seat SUV",
        "summary": "A 7-seat SUV for families who need space, safety and long-distance confidence.",
        "fit": "Families of 5 to 7, inter-province travel",
        "tags": ("SUV", "7 seats", "Long trips"),
    },
    "ford-ranger": {
        "category": "Pickup",
        "summary": "A versatile pickup for work, family use and flexible daily mobility.",
        "fit": "Business, construction, family use",
        "tags": ("Pickup", "Versatile", "Business"),
    },
    "ford-transit": {
        "category": "Commercial vehicle",
        "summary": "A 16 to 18-seat vehicle for businesses, transport services and shuttle operations.",
        "fit": "Business, service, shuttle",
        "tags": ("16 seats", "18 seats", "Service"),
    },
    "ford-mustang-mach-e": {
        "category": "Electric vehicle",
        "summary": "A high-performance EV that needs detailed consultation on charging needs and ownership cost.",
        "fit": "EV buyers, technology-focused customers",
        "tags": ("EV", "AWD", "Technology"),
    },
}

VALUE_TRANSLATIONS = {
    "Anh Huy xác nhận": "Huy will confirm",
    "Anh Huy xác nhận theo phiên bản": "Huy will confirm by variant",
    "Cầu trước": "Front-wheel drive",
    "Thuần điện": "Electric",
}


def normalize_locale(value: str | None) -> str:
    if not value:
        return DEFAULT_LOCALE
    normalized = value.strip().lower()
    return normalized if normalized in SUPPORTED_LOCALES else DEFAULT_LOCALE


def request_locale(request: Request) -> str:
    return normalize_locale(request.query_params.get("lang"))


def t(locale: str, key: str, **kwargs: object) -> str:
    value = TRANSLATIONS.get(normalize_locale(locale), TRANSLATIONS[DEFAULT_LOCALE]).get(
        key,
        TRANSLATIONS[DEFAULT_LOCALE].get(key, key),
    )
    return value.format(**kwargs) if kwargs else value


def localized_url(
    path: str,
    locale: str,
    current_query: Mapping[str, str] | str | None = None,
) -> str:
    pairs: list[tuple[str, str]]
    if isinstance(current_query, str):
        pairs = parse_qsl(current_query, keep_blank_values=True)
    elif current_query:
        pairs = list(current_query.items())
    else:
        pairs = []
    pairs = [(key, value) for key, value in pairs if key != "lang"]
    if normalize_locale(locale) != DEFAULT_LOCALE:
        pairs.append(("lang", normalize_locale(locale)))
    query = urlencode(pairs)
    return f"{path}?{query}" if query else path


def translate_value(value: str, locale: str) -> str:
    if normalize_locale(locale) == DEFAULT_LOCALE:
        return value
    return VALUE_TRANSLATIONS.get(value, value)


def localize_vehicle(vehicle: Vehicle, locale: str) -> Vehicle:
    if normalize_locale(locale) == DEFAULT_LOCALE:
        return vehicle

    translated = VEHICLE_TRANSLATIONS.get(vehicle.slug, {})
    variants = tuple(
        Variant(
            name=variant.name,
            price_vnd=variant.price_vnd,
            engine=translate_value(variant.engine, locale),
            drivetrain=translate_value(variant.drivetrain, locale),
        )
        for variant in vehicle.variants
    )
    return Vehicle(
        slug=vehicle.slug,
        name=vehicle.name,
        category=str(translated.get("category", vehicle.category)),
        summary=str(translated.get("summary", vehicle.summary)),
        fit=str(translated.get("fit", vehicle.fit)),
        source_url=vehicle.source_url,
        variants=variants,
        tags=tuple(translated.get("tags", vehicle.tags)),
        image_path=vehicle.image_path,
        image_source_url=vehicle.image_source_url,
    )


def localize_vehicles(vehicles: tuple[Vehicle, ...], locale: str) -> tuple[Vehicle, ...]:
    return tuple(localize_vehicle(vehicle, locale) for vehicle in vehicles)
