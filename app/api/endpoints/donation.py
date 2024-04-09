from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationAdminDB, DonationCreate, DonationDB
)
from app.models import User, CharityProject
from app.services.investment import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_user)],
    # Оставлю это здесь для напоминания моего вопроса в Пачке=)
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Сделать пожертвование."""
    create_new_donation = await donation_crud.create(
        obj_in=donation, user=user, session=session
    )

    await investment_process(
        db_obj=CharityProject, obj_in=create_new_donation, session=session
    )

    return create_new_donation


@router.get(
    '/',
    response_model=list[DonationAdminDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Получает список всех пожертвований.
    """
    all_charity_project = await donation_crud.get_multi(session=session)

    return all_charity_project


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получить список моих пожертвований."""
    my_donations = await donation_crud.get_user_donations(
        user=user, session=session
    )

    return my_donations