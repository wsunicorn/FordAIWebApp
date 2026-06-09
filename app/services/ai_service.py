from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time
from uuid import uuid4

import httpx
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.data.site_content import (
    FAQS,
    ON_ROAD_ASSUMPTIONS,
    PRICE_SOURCE_URL,
    PROMOTIONS,
    SOURCE_CHECKED_AT,
    SOURCE_PERIOD,
    VEHICLES,
    format_vnd,
)
from app.models import AIConversation, AIDocument, AIFeedback, AIMessage
from app.schemas import AIChatRequest, AIChatResponse, AISourceRead, LeadCreate
from app.services.audit_service import write_audit_log
from app.services.i18n_service import normalize_locale
from app.services.lead_service import create_lead

SYSTEM_PROMPT = """Bạn là trợ lý AI tư vấn tham khảo cho anh Huỳnh Đang Huy tại Đồng Tháp Ford.
Chỉ trả lời từ tài liệu đã duyệt, dữ liệu có nguồn hoặc công cụ tính toán nội bộ.
Không chốt giá, không xác nhận tồn kho, không hứa ưu đãi, không nhận đặt cọc,
không cam kết duyệt vay và không thay mặt đại lý xử lý khiếu nại.
Khi câu hỏi cần quyết định mua bán chính thức, hãy giải thích ngắn gọn và chuyển sang anh Huy."""

RISK_KEYWORDS = {
    "final_price": ("giá chốt", "chốt giá", "giá cuối", "bớt thêm", "giảm thêm"),
    "stock": ("còn xe", "tồn kho", "có sẵn", "màu nào còn", "giao ngay"),
    "deposit": ("đặt cọc", "giữ xe", "chuyển khoản", "thanh toán"),
    "loan_approval": ("duyệt vay", "chắc chắn vay", "bao đậu", "nợ xấu"),
    "complaint": ("khiếu nại", "bảo hành lỗi", "tranh chấp", "đền bù"),
}

ASCII_RISK_KEYWORDS = {
    "final_price": ("gia chot", "chot gia", "gia cuoi", "bot them", "giam them"),
    "stock": ("con xe", "ton kho", "co san", "mau nao con", "giao ngay"),
    "deposit": ("dat coc", "giu xe", "chuyen khoan", "thanh toan"),
    "loan_approval": ("duyet vay", "chac chan vay", "bao dau", "no xau"),
    "complaint": ("khieu nai", "bao hanh loi", "tranh chap", "den bu"),
}

STOP_WORDS = {
    "anh",
    "cho",
    "cua",
    "của",
    "toi",
    "tôi",
    "minh",
    "mình",
    "hoi",
    "hỏi",
    "ve",
    "về",
    "xe",
    "ford",
    "la",
    "là",
    "co",
    "có",
    "khong",
    "không",
    "bao",
    "bao nhiêu",
}


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_MAX_CONTEXT_CHARS = 5_600
GEMINI_UNSAFE_PATTERNS = (
    "gia chot la",
    "chot gia la",
    "con xe giao ngay",
    "co san tai dai ly",
    "dat coc ngay",
    "giu xe cho",
    "chac chan duyet",
    "bao dau",
    "giá chốt là",
    "chốt giá là",
    "còn xe giao ngay",
    "có sẵn tại đại lý",
    "đặt cọc ngay",
    "giữ xe cho",
    "chắc chắn duyệt",
)


@dataclass(frozen=True)
class RetrievedDocument:
    document: AIDocument
    score: int


def normalize_text(value: str) -> str:
    return value.lower()


def tokenize(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[\wÀ-ỹ]+", normalize_text(value))
        if len(token) >= 3 and token not in STOP_WORDS
    }


def detect_risk_flags(message: str) -> list[str]:
    normalized = normalize_text(message)
    return [
        flag
        for flag, keywords in RISK_KEYWORDS.items()
        if any(
            keyword in normalized for keyword in keywords + ASCII_RISK_KEYWORDS.get(flag, ())
        )
    ]


def infer_vehicle_name(message: str) -> str | None:
    normalized = normalize_text(message)
    for vehicle in VEHICLES:
        short_name = vehicle.name.lower().replace("ford ", "")
        full_name = vehicle.name.lower()
        if short_name in normalized or full_name in normalized:
            return vehicle.name
    return None


def get_vehicle_by_name(vehicle_name: str | None):
    if not vehicle_name:
        return None
    normalized = vehicle_name.lower()
    return next((vehicle for vehicle in VEHICLES if vehicle.name.lower() == normalized), None)


def monthly_payment(principal: int, annual_rate: float, months: int) -> int:
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate <= 0:
        return round(principal / months)
    payment = principal * monthly_rate * (1 + monthly_rate) ** months
    payment /= (1 + monthly_rate) ** months - 1
    return round(payment)


def maybe_run_tool(
    message: str,
    vehicle_interest: str | None = None,
    locale: str = "vi",
) -> tuple[str | None, str | None]:
    normalized = normalize_text(message)
    inferred_vehicle = infer_vehicle_name(message)
    vehicle = get_vehicle_by_name(vehicle_interest) or get_vehicle_by_name(inferred_vehicle)
    if not vehicle:
        return None, None

    is_english = normalize_locale(locale) == "en"
    price = vehicle.price_from
    if any(
        keyword in normalized
        for keyword in ("lăn bánh", "lan banh", "ra biển", "ra bien", "on-road", "on road")
    ):
        registration_fee = round(price * ON_ROAD_ASSUMPTIONS["registration_rate"])
        total = (
            price
            + registration_fee
            + ON_ROAD_ASSUMPTIONS["inspection_fee"]
            + ON_ROAD_ASSUMPTIONS["road_fee"]
            + ON_ROAD_ASSUMPTIONS["civil_insurance"]
        )
        if is_english:
            answer = (
                f"Reference on-road estimate for {vehicle.name} from {format_vnd(price)} is "
                f"around {format_vnd(total)}. This uses the reference area fee group and is "
                "not an official quote. Huy needs to reconfirm fees, color availability and "
                "current offers."
            )
        else:
            answer = (
                f"Ước tính lăn bánh tham khảo cho {vehicle.name} từ {format_vnd(price)} là "
                f"khoảng {format_vnd(total)}. Con số này dùng nhóm phí khu vực tham khảo, "
                "chưa phải báo giá chính thức. Anh Huy cần xác nhận lại phí, màu xe "
                "và ưu đãi hiện hành."
            )
        return "on_road_calculator", answer

    if any(
        keyword in normalized
        for keyword in (
            "trả góp",
            "tra gop",
            "vay",
            "ngân hàng",
            "financing",
            "loan",
            "monthly payment",
        )
    ):
        down_payment = round(price * 0.3)
        principal = price - down_payment
        payment = monthly_payment(principal, annual_rate=8.5, months=60)
        if is_english:
            answer = (
                f"For {vehicle.name} from {format_vnd(price)}, a 30% down payment is about "
                f"{format_vnd(down_payment)}, leaving around {format_vnd(principal)} to finance. "
                f"With an assumed 8.5% annual rate over 60 months, estimated payment is about "
                f"{format_vnd(payment)}/month. The bank reviews the real application, so this "
                "is not a loan approval commitment."
            )
        else:
            answer = (
                f"Nếu tham khảo {vehicle.name} từ {format_vnd(price)}, trả trước 30% khoảng "
                f"{format_vnd(down_payment)}, khoản vay còn lại khoảng {format_vnd(principal)}. "
                f"Với giả định 8,5%/năm trong 60 tháng, trả góp ước tính khoảng "
                f"{format_vnd(payment)}/tháng. "
                "Ngân hàng sẽ xét hồ sơ thực tế, nên đây không phải cam kết duyệt vay."
            )
        return "loan_calculator", answer

    return None, None


async def seed_ai_documents(session: AsyncSession) -> int:
    source_date = date.fromisoformat(SOURCE_CHECKED_AT)
    documents: list[dict[str, str | date | None]] = [
        {
            "title": "Nguyên tắc trả lời của AI",
            "body": SYSTEM_PROMPT,
            "source_url": None,
            "source_updated_at": source_date,
            "risk_level": "high",
        },
        {
            "title": "Chính sách handoff sang anh Huy",
            "body": (
                "AI phải chuyển sang anh Huy khi khách hỏi giá chốt, tồn kho, màu xe còn sẵn, "
                "đặt cọc, giữ xe, duyệt vay chắc chắn, khiếu nại hoặc tình huống "
                "cần cam kết chính thức."
            ),
            "source_url": None,
            "source_updated_at": source_date,
            "risk_level": "high",
        },
        {
            "title": "Thông tin liên hệ anh Huỳnh Đang Huy",
            "body": (
                "Anh Huỳnh Đang Huy là tư vấn bán hàng tại Đồng Tháp Ford. "
                "Khách có thể gọi 0766994952, Zalo 0818655369 hoặc gửi form trên website."
            ),
            "source_url": None,
            "source_updated_at": source_date,
            "risk_level": "normal",
        },
    ]

    for vehicle in VEHICLES:
        variants = "; ".join(
            f"{variant.name}: {format_vnd(variant.price_vnd)}" for variant in vehicle.variants
        )
        documents.append(
            {
                "title": f"{vehicle.name} tham khảo",
                "body": (
                    f"{vehicle.name} thuộc nhóm {vehicle.category}. {vehicle.summary} "
                    f"Phù hợp: {vehicle.fit}. Giá tham khảo kỳ {SOURCE_PERIOD}: {variants}. "
                    "Giá, ưu đãi, tồn kho và thời gian giao xe cần anh Huy xác nhận."
                ),
                "source_url": vehicle.source_url,
                "source_updated_at": source_date,
                "risk_level": "medium",
            }
        )

    for item in PROMOTIONS:
        documents.append(
            {
                "title": item["title"],
                "body": (
                    f"{item['summary']} Trạng thái: {item['status']}. "
                    "Ưu đãi thực tế cần anh Huy xác nhận tại thời điểm tư vấn."
                ),
                "source_url": item.get("source_url") or PRICE_SOURCE_URL,
                "source_updated_at": source_date,
                "risk_level": "high",
            }
        )

    for item in FAQS:
        documents.append(
            {
                "title": item["question"],
                "body": item["answer"],
                "source_url": PRICE_SOURCE_URL,
                "source_updated_at": source_date,
                "risk_level": "medium",
            }
        )

    touched = 0
    for item in documents:
        result = await session.execute(select(AIDocument).where(AIDocument.title == item["title"]))
        document = result.scalars().first()
        if not document:
            document = AIDocument(title=str(item["title"]), body=str(item["body"]))
            session.add(document)
        document.body = str(item["body"])
        document.source_url = item["source_url"] if isinstance(item["source_url"], str) else None
        document.source_updated_at = item["source_updated_at"]
        document.owner = "Anh Huy + Dev"
        document.approval_status = "approved"
        document.freshness_status = "fresh"
        document.risk_level = str(item["risk_level"])
        touched += 1

    await session.commit()
    await write_audit_log(
        session,
        action="ai_documents.seeded",
        entity_table="ai_documents",
        metadata={"count": touched, "source_period": SOURCE_PERIOD},
    )
    return touched


async def retrieve_documents(
    session: AsyncSession,
    message: str,
    *,
    limit: int = 4,
) -> list[RetrievedDocument]:
    result = await session.execute(
        select(AIDocument).where(
            AIDocument.approval_status == "approved",
            AIDocument.freshness_status == "fresh",
        )
    )
    documents = result.scalars().all()
    query_tokens = tokenize(message)
    scored: list[RetrievedDocument] = []
    for document in documents:
        haystack = tokenize(f"{document.title} {document.body}")
        score = len(query_tokens & haystack)
        if score:
            scored.append(RetrievedDocument(document=document, score=score))
    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:limit]


async def get_or_create_conversation(
    session: AsyncSession,
    *,
    session_id: str | None,
    vehicle_interest: str | None = None,
) -> AIConversation:
    actual_session_id = session_id or str(uuid4())
    result = await session.execute(
        select(AIConversation).where(AIConversation.session_id == actual_session_id)
    )
    conversation = result.scalars().first()
    if conversation:
        if vehicle_interest:
            conversation.vehicle_interest = vehicle_interest
        return conversation

    conversation = AIConversation(
        session_id=actual_session_id,
        vehicle_interest=vehicle_interest,
    )
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


def compose_answer(
    message: str,
    retrieved: list[RetrievedDocument],
    risk_flags: list[str],
    tool_answer: str | None,
    locale: str = "vi",
) -> tuple[str, bool, bool]:
    if tool_answer:
        return tool_answer, bool(risk_flags), False

    is_english = normalize_locale(locale) == "en"
    if risk_flags:
        if is_english:
            answer = (
                "This question needs direct confirmation from Huy because it involves "
                "information that can change or requires an official commitment. You can "
                "leave your phone number, vehicle of interest and area so AI can hand the "
                "request to Huy for a call or Zalo message."
            )
        else:
            answer = (
                "Câu hỏi này cần anh Huy xác nhận trực tiếp vì liên quan đến "
                "thông tin có thể thay đổi hoặc cần cam kết chính thức. Bạn có "
                "thể để lại số điện thoại, xe quan tâm và khu vực, "
                "AI sẽ chuyển yêu cầu cho anh Huy gọi hoặc nhắn Zalo."
            )
        return answer, True, False

    if not retrieved:
        if is_english:
            answer = (
                "AI does not yet have approved material to answer this confidently. You can "
                "ask about Ford models, reference prices, on-road cost, financing or leave "
                "your information for Huy to advise directly."
            )
        else:
            answer = (
                "Hiện AI chưa có tài liệu đã duyệt để trả lời chắc câu này. "
                "Bạn có thể hỏi về dòng xe, giá tham khảo, lăn bánh, trả góp "
                "hoặc để lại thông tin để anh Huy tư vấn trực tiếp."
            )
        return answer, True, True

    source_lines = [item.document.body for item in retrieved[:2]]
    answer = " ".join(source_lines)
    if len(answer) > 720:
        answer = answer[:700].rsplit(" ", 1)[0] + "."
    if is_english:
        answer += (
            " This information is for reference only. Huy will confirm details "
            "before the customer decides."
        )
    else:
        answer += (
            " Thông tin trên là tham khảo, anh Huy sẽ xác nhận chi tiết "
            "trước khi khách quyết định."
        )
    return answer, False, False


def ai_provider_name() -> str:
    return settings.ai_provider.strip().lower()


def live_ai_key_configured() -> bool:
    api_key = (settings.ai_api_key or "").strip()
    return bool(api_key and "change-me" not in api_key.lower())


def gemini_enabled() -> bool:
    return ai_provider_name() == "gemini" and live_ai_key_configured()


def gemini_model_name() -> str:
    return settings.ai_model.strip().removeprefix("models/")


def build_gemini_context(retrieved: list[RetrievedDocument]) -> str:
    blocks: list[str] = []
    used_chars = 0
    for index, item in enumerate(retrieved, start=1):
        document = item.document
        updated_at = (
            document.source_updated_at.isoformat() if document.source_updated_at else "unknown"
        )
        source_url = document.source_url or "internal"
        body = re.sub(r"\s+", " ", document.body).strip()
        block = (
            f"[{index}] {document.title}\n"
            f"Updated: {updated_at}\n"
            f"Source: {source_url}\n"
            f"Content: {body}"
        )
        remaining_chars = GEMINI_MAX_CONTEXT_CHARS - used_chars
        if remaining_chars <= 0:
            break
        if len(block) > remaining_chars:
            block = block[:remaining_chars].rsplit(" ", 1)[0]
        if block:
            blocks.append(block)
            used_chars += len(block)
    return "\n\n".join(blocks)


def build_gemini_prompt(
    message: str,
    retrieved: list[RetrievedDocument],
    locale: str = "vi",
) -> str:
    context = build_gemini_context(retrieved)
    reply_language = "natural English" if normalize_locale(locale) == "en" else "natural Vietnamese"
    return (
        "Customer question:\n"
        f"{message.strip()}\n\n"
        "Approved knowledge base context:\n"
        f"{context}\n\n"
        "Answer requirements:\n"
        f"- Reply in {reply_language}.\n"
        "- Use only the approved context above and the system rules.\n"
        "- Keep the answer concise, practical and consultation-oriented.\n"
        "- Do not finalize price, stock, color availability, deposit, delivery or loan approval.\n"
        "- If official confirmation is needed, ask the customer to contact anh Huy."
    )


def extract_gemini_text(data: dict[str, object]) -> str | None:
    candidates = data.get("candidates")
    if not isinstance(candidates, list):
        return None

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        content = candidate.get("content")
        if not isinstance(content, dict):
            continue
        parts = content.get("parts")
        if not isinstance(parts, list):
            continue
        text_parts = [
            part.get("text", "")
            for part in parts
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        ]
        text = "\n".join(text_parts).strip()
        if text:
            return text
    return None


def clean_gemini_answer(answer: str, locale: str = "vi") -> str | None:
    cleaned = re.sub(r"[ \t]+", " ", answer).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    if not cleaned:
        return None
    normalized = normalize_text(cleaned)
    if any(pattern in normalized for pattern in GEMINI_UNSAFE_PATTERNS):
        return None
    if len(cleaned) > 1_200:
        cleaned = cleaned[:1_180].rsplit(" ", 1)[0].rstrip(".,;:") + "."
    if normalize_locale(locale) == "en":
        if "reference" not in normalized:
            cleaned += (
                "\n\nNote: This information is for reference only; Huy will reconfirm "
                "price, offers, stock and delivery time before the customer decides."
            )
    elif "thông tin trên là tham khảo" not in normalized:
        cleaned += (
            "\n\nLưu ý: Thông tin trên là tham khảo; anh Huy sẽ xác nhận lại giá, "
            "ưu đãi, tồn kho và thời gian giao xe trước khi khách quyết định."
        )
    return cleaned


async def generate_gemini_answer(
    message: str,
    retrieved: list[RetrievedDocument],
    locale: str = "vi",
) -> str | None:
    if not gemini_enabled() or not retrieved:
        return None

    model = gemini_model_name()
    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [
            {
                "role": "user",
                "parts": [{"text": build_gemini_prompt(message, retrieved, locale)}],
            }
        ],
        "generationConfig": {
            "temperature": settings.ai_temperature,
            "maxOutputTokens": settings.ai_max_output_tokens,
        },
    }
    headers = {"x-goog-api-key": settings.ai_api_key or ""}

    try:
        async with httpx.AsyncClient(timeout=settings.ai_request_timeout_seconds) as client:
            response = await client.post(
                GEMINI_API_URL.format(model=model),
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPError:
        return None

    raw_answer = extract_gemini_text(response.json())
    if not raw_answer:
        return None
    return clean_gemini_answer(raw_answer, locale)


async def answer_chat(session: AsyncSession, payload: AIChatRequest) -> AIChatResponse:
    locale = normalize_locale(payload.locale)
    document_count = await session.scalar(select(func.count(AIDocument.id)))
    if not document_count:
        await seed_ai_documents(session)

    conversation = await get_or_create_conversation(
        session,
        session_id=payload.session_id,
        vehicle_interest=payload.vehicle_interest,
    )
    user_message = AIMessage(
        conversation_id=conversation.id,
        role="user",
        content=payload.message,
    )
    session.add(user_message)

    today_start = datetime.combine(date.today(), time.min)
    today_user_messages = await session.scalar(
        select(func.count(AIMessage.id)).where(
            AIMessage.role == "user",
            AIMessage.created_at >= today_start,
        )
    )
    quota_exceeded = bool(today_user_messages and today_user_messages > settings.ai_daily_quota)

    risk_flags = detect_risk_flags(payload.message)
    tool_name, tool_answer = maybe_run_tool(payload.message, payload.vehicle_interest, locale)
    retrieved = [] if quota_exceeded else await retrieve_documents(session, payload.message)
    provider_name = "internal"
    if quota_exceeded:
        if locale == "en":
            answer = (
                "AI has reached the temporary daily processing limit. You can leave your "
                "phone number, vehicle of interest and area so Huy can call or message you "
                "on Zalo directly."
            )
        else:
            answer = (
                "AI đã đạt giới hạn xử lý tạm thời trong ngày. Bạn có thể để lại số điện thoại, "
                "xe quan tâm và khu vực để anh Huy gọi hoặc nhắn Zalo tư vấn trực tiếp."
            )
        handoff_required = True
        fallback_used = True
        risk_flags = [*risk_flags, "quota_exceeded"]
        tool_name = None
    else:
        answer, handoff_required, fallback_used = compose_answer(
            payload.message,
            retrieved,
            risk_flags,
            tool_answer,
            locale,
        )
        if not tool_answer and not risk_flags and retrieved:
            generated_answer = await generate_gemini_answer(payload.message, retrieved, locale)
            if generated_answer:
                answer = generated_answer
                handoff_required = False
                fallback_used = False
                provider_name = f"gemini:{gemini_model_name()}"
            elif gemini_enabled():
                fallback_used = True
    source_ids = ",".join(item.document.id for item in retrieved) or None
    assistant_message = AIMessage(
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
        source_ids=source_ids,
        tool_name=tool_name,
        risk_flags=",".join(risk_flags) or None,
    )
    session.add(assistant_message)
    conversation.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(assistant_message)

    return AIChatResponse(
        conversation_id=conversation.id,
        session_id=conversation.session_id,
        message_id=assistant_message.id,
        answer=answer,
        sources=[
            AISourceRead(
                id=item.document.id,
                title=item.document.title,
                source_url=item.document.source_url,
                source_updated_at=(
                    item.document.source_updated_at.isoformat()
                    if item.document.source_updated_at
                    else None
                ),
            )
            for item in retrieved
        ],
        risk_flags=risk_flags,
        handoff_required=handoff_required,
        provider_name=provider_name,
        tool_name=tool_name,
        fallback_used=fallback_used,
    )


async def handoff_conversation_to_lead(
    session: AsyncSession,
    *,
    conversation_id: str,
    full_name: str,
    phone: str,
    vehicle_interest: str | None,
    area: str | None,
    note: str | None,
):
    conversation = await session.get(AIConversation, conversation_id)
    if not conversation:
        return None

    result = await session.execute(
        select(AIMessage)
        .where(AIMessage.conversation_id == conversation.id)
        .order_by(AIMessage.created_at)
        .limit(8)
    )
    transcript = "\n".join(
        f"{message.role}: {message.content[:240]}" for message in result.scalars().all()
    )
    lead = await create_lead(
        session,
        LeadCreate(
            full_name=full_name,
            phone=phone,
            vehicle_interest=vehicle_interest or conversation.vehicle_interest,
            area=area,
            need_type="ai_handoff",
            note=f"{note or ''}\n\nAI transcript:\n{transcript}".strip(),
        ),
    )
    conversation.customer_name = full_name
    conversation.phone = phone
    conversation.vehicle_interest = vehicle_interest or conversation.vehicle_interest
    conversation.status = "lead_created"
    await session.commit()
    await write_audit_log(
        session,
        action="ai.handoff",
        entity_table="ai_conversations",
        entity_id=conversation.id,
        metadata={"lead_id": lead.id, "phone": phone},
    )
    return lead


async def create_ai_feedback(
    session: AsyncSession,
    *,
    message_id: str,
    rating: int,
    note: str | None = None,
) -> AIFeedback | None:
    message = await session.get(AIMessage, message_id)
    if not message:
        return None
    feedback = AIFeedback(message_id=message_id, rating=rating, note=note)
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)
    return feedback


async def ai_dashboard_stats(session: AsyncSession) -> dict[str, int]:
    documents = await session.scalar(select(func.count(AIDocument.id)))
    conversations = await session.scalar(select(func.count(AIConversation.id)))
    messages = await session.scalar(select(func.count(AIMessage.id)))
    feedback = await session.scalar(select(func.count(AIFeedback.id)))
    return {
        "documents": documents or 0,
        "conversations": conversations or 0,
        "messages": messages or 0,
        "feedback": feedback or 0,
    }


async def list_ai_documents(session: AsyncSession) -> list[AIDocument]:
    result = await session.execute(select(AIDocument).order_by(AIDocument.title))
    return list(result.scalars().all())


async def recent_ai_conversations(
    session: AsyncSession,
    *,
    limit: int = 30,
) -> list[AIConversation]:
    result = await session.execute(
        select(AIConversation).order_by(desc(AIConversation.created_at)).limit(limit)
    )
    return list(result.scalars().all())
