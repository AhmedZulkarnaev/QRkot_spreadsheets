from typing import Optional

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_charity_project_by_id(
        self,
        project_id: int,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        db_project = db_project.scalars().first()
        return db_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        completion_rate = extract(
            'epoch', CharityProject.close_date
        ) - extract('epoch', CharityProject.create_date)
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        ).order_by(completion_rate)

        return projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)