from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.api.exeptions import BadRequest, NotFound


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
):
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise BadRequest(
            detail='Проект с таким именем уже существует!',
        )


def check_charity_project_invested_sum(
        project: CharityProject, new_amount: int
):
    if project.invested_amount > new_amount:
        raise BadRequest(
            detail='Нельзя установить сумму, ниже уже вложенной!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
):
    project = await charity_project_crud.get_charity_project_by_id(
        project_id, session
    )
    if project is None:
        raise NotFound(
            detail='Проект не найден!'
        )
    return project


def check_charity_project_already_invested(charity_project: CharityProject):
    if charity_project.invested_amount > 0:
        raise BadRequest(
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_charity_project_closed(charity_project: CharityProject):
    if charity_project.fully_invested:
        raise BadRequest(
            detail='Закрытый проект нельзя редактировать!'
        )
