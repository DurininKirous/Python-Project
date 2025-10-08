from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ... import crud, schemas
from ...database import get_session

router = APIRouter(prefix="/checks", tags=["checks"])


@router.get("/", response_model=list[schemas.ServiceCheckRead])
async def list_service_checks(session: AsyncSession = Depends(get_session)):
    return await crud.list_checks(session)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ServiceCheckRead,
)
async def create_service_check(
    check_in: schemas.ServiceCheckCreate, session: AsyncSession = Depends(get_session)
):
    return await crud.create_check(session, check_in)


@router.get("/{check_id}", response_model=schemas.ServiceCheckRead)
async def get_service_check(check_id: int, session: AsyncSession = Depends(get_session)):
    check = await crud.get_check(session, check_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found")
    return check


@router.patch("/{check_id}", response_model=schemas.ServiceCheckRead)
async def update_service_check(
    check_id: int,
    update_in: schemas.ServiceCheckUpdate,
    session: AsyncSession = Depends(get_session),
):
    check = await crud.get_check(session, check_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found")
    return await crud.update_check(session, check, update_in)


@router.delete("/{check_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service_check(check_id: int, session: AsyncSession = Depends(get_session)):
    check = await crud.get_check(session, check_id)
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check not found")
    await crud.delete_check(session, check)
    return None
