from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_not_full_invested_objects(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession
) -> List[Union[CharityProject, Donation]]:
    objects = await session.execute(
        select(obj_in).where(obj_in.fully_invested == 0
                             ).order_by(obj_in.create_date)
    )
    return objects.scalars().all()


def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


def invest_money(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> List[Union[CharityProject, Donation]]:
    for source in sources:
        free_amount_target = target.full_amount - target.invested_amount
        free_amount_source = source.full_amount - source.invested_amount
        if free_amount_target >= free_amount_source:
            target.invested_amount += free_amount_source
            close_donation_for_obj(source)
            if free_amount_target == free_amount_source:
                close_donation_for_obj(target)
                break
        else:
            source.invested_amount += free_amount_target
            close_donation_for_obj(target)
            break

    return sources


def investing_process(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]],
) -> List[Union[CharityProject, Donation]]:
    updated_sources = invest_money(target, sources)
    return updated_sources

# Ерунду какую то сделал)