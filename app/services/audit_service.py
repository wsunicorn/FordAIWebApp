from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog


async def write_audit_log(
    session: AsyncSession,
    *,
    action: str,
    entity_table: str,
    entity_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    log = AuditLog(
        action=action,
        entity_table=entity_table,
        entity_id=entity_id,
        metadata_json=metadata or {},
    )
    session.add(log)
    await session.commit()
    await session.refresh(log)
    return log
