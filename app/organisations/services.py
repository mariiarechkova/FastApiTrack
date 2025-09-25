
from app.organisations.repositories import OrganisationRepository
from app.organisations.schemas import OrganisationRead, OrganisationAndUserCreate, OrganisationWithAdminRead
from app.users.schemas import UserCreate, UserRead
from app.users.services import UserService


class OrganisationService:
    def __init__(self, repo: OrganisationRepository, user_service: UserService):
        self._repo = repo
        self._users = user_service

    async def get_all(self):
        return await self._repo.get_all()

    async def get_by_id(self, org_id: int):
        return await self._repo.get_by_id(org_id)

    async def create(self, data: OrganisationAndUserCreate):
        org = await self._repo.create(
            name=data.name,
        )
        await self._repo.session.flush()

        user_data = data.user.model_dump()
        user_data["is_admin"] = True
        user = await self._users.create_user(org_id=org.id, dto=UserCreate(**user_data))
        return OrganisationWithAdminRead(
            id=org.id,
            name=org.name,
            created_at=org.created_at,
            admin=UserRead.model_validate(user)
        )

    async def update(self, org_id, org_in):
        return await self._repo.update(org_id, org_in)

    async def delete(self, org_id):
        ok =  await self._repo.delete(org_id)
        if not ok:
            raise ValueError("Organisation not found")
        return True
