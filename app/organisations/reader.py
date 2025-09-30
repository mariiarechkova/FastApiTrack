from sqlalchemy.ext.asyncio import AsyncSession

from app.organisations.repositories import OrganisationRepository


class OrganisationQueryReader:
    def __init__(self, session: AsyncSession):
        self.repo = OrganisationRepository(session)

    async def exists_by_id(self, org_id: int) -> bool:
        return await self.repo.get_by_id(org_id) is not None