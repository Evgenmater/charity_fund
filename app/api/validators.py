from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import MAX_LENGTH
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка, существует ли запрашиваемый ID(проект)."""
    charity_project = await charity_project_crud.get(
        obj_id=project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Благотворительный проект не найдет!'
        )
    return charity_project


async def check_name_empty_and_length(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка, на пустое и максимальное значение имени."""
    deleting_empty_string = project_name.strip()
    if not deleting_empty_string or len(project_name) > MAX_LENGTH:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='name не должен быть пустым или более 100 символов!',
        )


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """
    Проверка имени на уникальность.
    Если имя уже занято, то поднимаем исключение.
    """
    charity_project = await charity_project_crud.get_charity_project_id_by_name(
        project_name=project_name, session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_cash_in_project(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверка на внесённые средства в проект.
    Если в проекте есть внесённые средства, то удалять нельзя.
    """
    charity_project = await check_charity_project_exists(
        project_id=project_id, session=session
    )
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return charity_project


async def check_closed_project(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверка закрытого проекта.
    Если данный проект закрыт, то нельзя редактировать.
    """
    charity_project = await check_charity_project_exists(
        project_id=project_id, session=session
    )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    return charity_project


async def check_full_amount_cash(
    project_full_amount: CharityProject,
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    """
    Проверка на изменение требуемой суммы проекта.
    """
    if project_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Запрещено изменять сумму меньше внесённой суммы на проекте!',
        )
