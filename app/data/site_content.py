from __future__ import annotations

from dataclasses import dataclass

PRICE_SOURCE_URL = "https://dongthapford.com/bang-gia-xe/"
SOURCE_PERIOD = "6/2026"
SOURCE_CHECKED_AT = "2026-06-07"


@dataclass(frozen=True)
class Variant:
    name: str
    price_vnd: int
    engine: str = "Đang cập nhật theo nguồn"
    drivetrain: str = "Anh Huy xác nhận theo phiên bản"


@dataclass(frozen=True)
class Vehicle:
    slug: str
    name: str
    category: str
    summary: str
    fit: str
    source_url: str
    variants: tuple[Variant, ...]
    tags: tuple[str, ...]
    image_path: str | None = None
    image_source_url: str | None = None

    @property
    def price_from(self) -> int:
        return min(variant.price_vnd for variant in self.variants)

    @property
    def featured_variant(self) -> Variant:
        return self.variants[0]


VEHICLES: tuple[Vehicle, ...] = (
    Vehicle(
        slug="ford-territory",
        name="Ford Territory",
        category="SUV 5 chỗ",
        summary="SUV đô thị rộng rãi, phù hợp gia đình trẻ cần xe dễ dùng hằng ngày.",
        fit="Gia đình, đi phố, cuối tuần",
        source_url=PRICE_SOURCE_URL,
        tags=("SUV", "5 chỗ", "Gia đình"),
        image_path="/images/vehicles/ford-territory.jpg",
        image_source_url="https://dongthapford.com/gia-xe-territory/",
        variants=(
            Variant("Territory Trend", 739_000_000, "EcoBoost 1.5L", "Cầu trước"),
            Variant("Territory Titanium", 819_000_000, "EcoBoost 1.5L", "Cầu trước"),
            Variant("Territory Titanium X", 875_000_000, "EcoBoost 1.5L", "Cầu trước"),
        ),
    ),
    Vehicle(
        slug="ford-everest",
        name="Ford Everest",
        category="SUV 7 chỗ",
        summary="SUV 7 chỗ cho gia đình cần không gian, an toàn và khả năng đi đường dài.",
        fit="Gia đình 5 đến 7 người, đi tỉnh",
        source_url=PRICE_SOURCE_URL,
        tags=("SUV", "7 chỗ", "Đường dài"),
        image_path="/images/vehicles/ford-everest.jpg",
        image_source_url="https://dongthapford.com/ford-everest-gia-xe-dong-thap/",
        variants=(
            Variant("Everest Ambiente", 1_099_000_000, "Diesel 2.0L", "4x2"),
            Variant("Everest Sport", 1_178_000_000, "Diesel 2.0L", "4x2"),
            Variant("Everest Sport SE", 1_199_000_000, "Diesel 2.0L", "4x2"),
            Variant("Everest Titanium", 1_299_000_000, "Diesel 2.0L", "4x2"),
            Variant("Everest Platinum", 1_545_000_000, "Diesel 2.0L", "Anh Huy xác nhận"),
        ),
    ),
    Vehicle(
        slug="ford-ranger",
        name="Ford Ranger",
        category="Bán tải",
        summary="Bán tải đa dụng cho công việc, gia đình và nhu cầu di chuyển linh hoạt.",
        fit="Kinh doanh, công trình, gia đình",
        source_url=PRICE_SOURCE_URL,
        tags=("Bán tải", "Đa dụng", "Kinh doanh"),
        image_path="/images/vehicles/ford-ranger.jpg",
        image_source_url="https://dongthapford.com/ford-ranger-xls-gia-lan-banh/",
        variants=(
            Variant("Ranger XL 4x4 MT", 669_000_000, "Diesel 2.0L", "4x4"),
            Variant("Ranger XLS 4x2 AT", 707_000_000, "Diesel 2.0L", "4x2"),
            Variant("Ranger XLS 4x4 AT", 776_000_000, "Diesel 2.0L", "4x4"),
            Variant("Ranger Sport", 864_000_000, "Diesel 2.0L", "Anh Huy xác nhận"),
            Variant("Ranger Wildtrak 4x4", 979_000_000, "Diesel 2.0L", "4x4"),
            Variant("Ranger StormTrak", 1_039_000_000, "Diesel 2.0L", "4x4"),
            Variant("Ranger Raptor", 1_299_000_000, "Bi-Turbo 2.0L", "4x4"),
        ),
    ),
    Vehicle(
        slug="ford-transit",
        name="Ford Transit",
        category="Xe thương mại",
        summary="Xe 16 đến 18 chỗ cho doanh nghiệp, dịch vụ vận tải và đưa đón.",
        fit="Doanh nghiệp, dịch vụ, đưa đón",
        source_url=PRICE_SOURCE_URL,
        tags=("16 chỗ", "18 chỗ", "Dịch vụ"),
        image_path="/images/vehicles/ford-transit.jpg",
        image_source_url="https://dongthapford.com/ford-transit-xe-van-tai-da-dung/",
        variants=(
            Variant("Transit Trend 16 chỗ", 907_000_000, "Diesel", "Anh Huy xác nhận"),
            Variant("Transit Premium 16 chỗ", 999_000_000, "Diesel", "Anh Huy xác nhận"),
            Variant("Transit Premium+ 18 chỗ", 1_091_000_000, "Diesel", "Anh Huy xác nhận"),
        ),
    ),
    Vehicle(
        slug="ford-mustang-mach-e",
        name="Ford Mustang Mach-E",
        category="Xe điện",
        summary="Xe điện hiệu năng cao, cần tư vấn kỹ về nhu cầu sạc và chi phí sử dụng.",
        fit="Khách thích xe điện, công nghệ",
        source_url=PRICE_SOURCE_URL,
        tags=("Xe điện", "AWD", "Công nghệ"),
        image_path="/images/vehicles/ford-mustang-mach-e.jpg",
        image_source_url=PRICE_SOURCE_URL,
        variants=(
            Variant("Mustang Mach-E Premium AWD", 2_599_000_000, "Thuần điện", "AWD"),
        ),
    ),
    Vehicle(
        slug="ford-transit-limousine",
        name="Ford Transit Limousine",
        category="Xe dịch vụ cao cấp",
        summary="Cấu hình limousine cho dịch vụ cao cấp, cần xác nhận tùy chọn theo xe thực tế.",
        fit="Dịch vụ cao cấp, hợp đồng",
        source_url=PRICE_SOURCE_URL,
        tags=("Limousine", "Dịch vụ", "Cần xác nhận"),
        image_path="/images/vehicles/ford-transit-limousine.png",
        image_source_url="https://dongthapford.com/ford-transit-xe-van-tai-da-dung/",
        variants=(
            Variant(
                "Transit Limousine 10 chỗ",
                1_388_000_000,
                "Anh Huy xác nhận",
                "Anh Huy xác nhận",
            ),
            Variant(
                "Transit Limousine 12 chỗ",
                1_499_000_000,
                "Anh Huy xác nhận",
                "Anh Huy xác nhận",
            ),
        ),
    ),
)


PROMOTIONS = (
    {
        "title": "Khuyến mãi áp dụng theo từng phiên bản",
        "summary": "Nguồn site ghi nhận ưu đãi thay đổi theo dòng xe, phiên bản và thời điểm.",
        "status": "Cần anh Huy xác nhận",
        "source_url": "https://dongthapford.com/bao-gia-uu-dai-xe-ford/",
    },
    {
        "title": "Hỗ trợ trả góp và tư vấn hồ sơ",
        "summary": (
            "Kết quả vay phụ thuộc ngân hàng, hồ sơ và chương trình "
            "tại thời điểm làm thủ tục."
        ),
        "status": "Tham khảo",
        "source_url": "https://dongthapford.com/chi-phi-tra-gop/",
    },
    {
        "title": "Đăng ký lái thử",
        "summary": "Có thể để lại thông tin để anh Huy kiểm tra lịch và khu vực hỗ trợ.",
        "status": "Cần xác nhận lịch",
        "source_url": "https://dongthapford.com/dang-ky-lai-thu/",
    },
)


FAQS = (
    {
        "question": "Giá xe trên website có phải giá chốt không?",
        "answer": (
            "Không. Đây là giá tham khảo theo nguồn đã ghi nhận. Giá chốt, "
            "ưu đãi, màu xe và thời gian giao xe cần anh Huy xác nhận trực tiếp."
        ),
    },
    {
        "question": "Có thể tính lăn bánh tại Đồng Tháp không?",
        "answer": (
            "Có thể ước tính theo nhóm khu vực Khác trong nguồn hiện tại. "
            "Phí thực tế theo thời điểm đăng ký cần được xác nhận lại."
        ),
    },
    {
        "question": "Trả góp có được duyệt chắc chắn không?",
        "answer": (
            "Không thể cam kết trên website. Công cụ chỉ ước tính số tiền "
            "theo lãi suất giả định, hồ sơ vay do ngân hàng xét duyệt."
        ),
    },
    {
        "question": "Anh Huy có hỗ trợ ngoài Đồng Tháp không?",
        "answer": (
            "Có thể tư vấn khu vực lân cận tùy trường hợp. Vui lòng để lại "
            "thông tin để anh Huy kiểm tra cách hỗ trợ phù hợp."
        ),
    },
)


ON_ROAD_ASSUMPTIONS = {
    "registration_rate": 0.072,
    "inspection_fee": 340_000,
    "road_fee": 1_560_000,
    "civil_insurance": 480_000,
}


PUBLIC_ROUTES = (
    "/",
    "/anh-huy",
    "/xe",
    "/so-sanh",
    "/bang-gia",
    "/du-toan-lan-banh",
    "/du-toan-tra-gop",
    "/uu-dai",
    "/faq",
    "/tro-ly-ai",
    "/lien-he",
    "/lai-thu",
    "/bao-gia",
)


def format_vnd(value: int) -> str:
    return f"{value:,}".replace(",", ".") + " VNĐ"


def vehicle_options() -> list[dict[str, str | int]]:
    return [
        {
            "slug": vehicle.slug,
            "name": vehicle.name,
            "price": vehicle.price_from,
            "price_label": format_vnd(vehicle.price_from),
        }
        for vehicle in VEHICLES
    ]


def get_vehicle(slug: str) -> Vehicle | None:
    return next((vehicle for vehicle in VEHICLES if vehicle.slug == slug), None)
