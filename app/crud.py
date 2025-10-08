from datetime import datetime, timezone
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .enums import CheckStatus


async def list_checks(
    session: AsyncSession, *, status: CheckStatus | None = None
) -> Sequence[models.ServiceCheck]:
    stmt = select(models.ServiceCheck).order_by(models.ServiceCheck.id)
    if status is not None:
        status_enum = CheckStatus(status)
        stmt = stmt.where(models.ServiceCheck.status == status_enum)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_check(session: AsyncSession, check_id: int) -> models.ServiceCheck | None:
    return await session.get(models.ServiceCheck, check_id)


async def create_check(
    session: AsyncSession, check_in: schemas.ServiceCheckCreate
) -> models.ServiceCheck:
    data = check_in.model_dump()
    if "status" in data:
        data["status"] = CheckStatus(data["status"])
    check = models.ServiceCheck(**data)
    session.add(check)
    await session.commit()
    await session.refresh(check)
    return check


async def update_check(
    session: AsyncSession, check: models.ServiceCheck, update_in: schemas.ServiceCheckUpdate
) -> models.ServiceCheck:
    data = update_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        if field == "status" and value is not None:
            value = CheckStatus(value)
        setattr(check, field, value)
    if "status" in data:
        check.last_checked_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(check)
    return check


async def delete_check(session: AsyncSession, check: models.ServiceCheck) -> None:
    await session.delete(check)
    await session.commit()


async def summarize_checks(session: AsyncSession) -> schemas.ServiceCheckSummary:
    counts_result = await session.execute(
        select(models.ServiceCheck.status, func.count(models.ServiceCheck.id)).group_by(
            models.ServiceCheck.status
        )
    )
    by_status: dict[CheckStatus, int] = {status: 0 for status in CheckStatus}
    for status, count in counts_result.all():
        by_status[CheckStatus(status)] = count
    total = sum(by_status.values())
    latest_check = None
    if total:
        latest_check = await session.scalar(select(func.max(models.ServiceCheck.last_checked_at)))
    return schemas.ServiceCheckSummary(total=total, by_status=by_status, latest_check=latest_check)
