from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.organisations.models import Organisation
from app.organisations.schemas import OrganisationUpdate


class OrganisationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all(self) -> List[Organisation]:
        result = await self.session.execute(select(Organisation))
        return result.scalars().all()

    async def get_by_id(self, org_id):
        return await self.session.get(Organisation, org_id)

    async def create(self, name: str) -> Organisation:
        org = Organisation(name=name)

        self.session.add(org)
        await self.session.flush()
        await self.session.refresh(org)
        return org

    async def update(self, org_id: int, org_in: OrganisationUpdate) -> Organisation | None:
        organisation = await self.get_by_id(org_id)
        if not organisation:
            return None

        organisation.name = org_in.name

        await self.session.flush()
        return organisation

    async def delete(self, org_id: int) -> bool:
        organisation = await self.get_by_id(org_id)
        if organisation is None:
            return False
        await self.session.delete(organisation)
        await self.session.flush()
        return True