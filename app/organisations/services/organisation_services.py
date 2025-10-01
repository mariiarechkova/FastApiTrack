from app.core.exceptions import NotFoundError
from app.organisations.repositories import OrganisationRepository
from app.organisations.schemas import OrganisationAndUserCreate, OrganisationWithAdminRead
from app.users.schemas import UserRead
from app.users.services.user_service import UserService


class OrganisationService:
    def __init__(self, repo: OrganisationRepository, user_service: UserService):
        self._repo = repo
        self._users = user_service

    async def get_all(self):
        return await self._repo.get_all()

    async def get_by_id(self, org_id: int):
        org = await self._repo.get_by_id(org_id)
        if not org:
            raise NotFoundError("Organisation", org_id)
        return org

    async def create(self, data: OrganisationAndUserCreate):
        org = await self._repo.create(
            name=data.name,
        )
        user = await self._users.create_admin_user(org_id=org.id, dto=data.user)
        return OrganisationWithAdminRead(
            id=org.id,
            name=org.name,
            created_at=org.created_at,
            admin=UserRead.model_validate(user)
        )

    async def update(self, org_id, org_in):
        org = await self._repo.update(org_id, org_in)
        if not org:
            raise NotFoundError("Organisation", org_id)
        return org

    async def delete(self, org_id):
        ok = await self._repo.delete(org_id)
        if not ok:
            raise NotFoundError("Organisation", org_id)
