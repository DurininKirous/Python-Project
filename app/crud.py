from datetime import datetime, timezone
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def list_checks(session: AsyncSession) -> Sequence[models.ServiceCheck]:
    result = await session.execute(select(models.ServiceCheck))
    return result.scalars().all()


async def get_check(session: AsyncSession, check_id: int) -> models.ServiceCheck | None:
    return await session.get(models.ServiceCheck, check_id)


async def create_check(
    session: AsyncSession, check_in: schemas.ServiceCheckCreate
) -> models.ServiceCheck:
    check = models.ServiceCheck(**check_in.model_dump())
    session.add(check)
    await session.commit()
    await session.refresh(check)
    return check


async def update_check(
    session: AsyncSession, check: models.ServiceCheck, update_in: schemas.ServiceCheckUpdate
) -> models.ServiceCheck:
    data = update_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(check, field, value)
    if "status" in data:
        check.last_checked_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(check)
    return check


async def delete_check(session: AsyncSession, check: models.ServiceCheck) -> None:
    await session.delete(check)
    await session.commit()
