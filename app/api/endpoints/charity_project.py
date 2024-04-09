from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_cash_in_project, check_closed_project,
    check_name_duplicate, check_full_amount_cash, check_name_empty_and_length,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import investment_process
router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Создает благотворительный проект.
    """
    await check_name_empty_and_length(
        project_name=charity_project.name, session=session
    )
    await check_name_duplicate(
        project_name=charity_project.name, session=session
    )
    create_new_project = await charity_project_crud.create(
        obj_in=charity_project, session=session
    )

    await investment_process(
        db_obj=Donation, obj_in=create_new_project, session=session
    )

    return create_new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    all_charity_project = await charity_project_crud.get_multi(session=session)

    return all_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать,
    также нельзя установить требуемую сумму меньше уже вложенной.
    """
    if obj_in.name is not None:
        await check_name_empty_and_length(
            project_name=obj_in.name, session=session
        )
        await check_name_duplicate(
            project_name=obj_in.name, session=session
        )

    charity_project = await check_closed_project(
        project_id=project_id, session=session
    )

    if obj_in.full_amount is not None:
        await check_full_amount_cash(
            project_full_amount=obj_in.full_amount,
            charity_project=charity_project,
            session=session,
        )

    charity_project = await charity_project_crud.update(
        db_obj=charity_project, obj_in=obj_in, session=session
    )

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть.
    """
    check_charity_project = await check_cash_in_project(
        project_id=project_id, session=session
    )

    charity_project = await charity_project_crud.remove(
        db_obj=check_charity_project, session=session
    )

    return charity_project