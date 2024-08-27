from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import get_not_full_invested_objects, investing_process
from app.api.validators import (check_charity_project_already_invested,
                                check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_invested_sum,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

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
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    not_full_invested_donations = await get_not_full_invested_objects(Donation, session)
    updated_donations = investing_process(
        new_project, not_full_invested_donations)
    for donation in updated_donations:
        session.add(donation)
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)

    return new_project



@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


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
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_closed(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_charity_project_invested_sum(project, obj_in.full_amount)

    charity_project = await charity_project_crud.update(
        project, obj_in, session
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
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_already_invested(project)
    charity_project = await charity_project_crud.remove(
        project, session
    )
    return charity_project