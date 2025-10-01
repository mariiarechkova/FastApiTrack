from typing import List

from sqlalchemy.exc import IntegrityError
from app.core.exceptions import NotFoundError, EmailAlreadyExistsError
from app.core.security import hash_password
from app.organisations.services.query_service import OrganisationQueryService
from app.users.models import User
from app.users.repositories import UserRepository
from app.users.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepository, org_query: OrganisationQueryService):
        self._repo = repo
        self.org_query = org_query

    async def get_all_users(self, org_id: int)-> List[User]:
        return await self._repo.get_all(org_id=org_id)

    async def get_user_by_id(self, user_id: int)-> User:
        user = await self._repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User", user_id)
        return user

    async def create_user(self, org_id: int, dto: UserCreate) -> User:
        if not await self.org_query.exists_by_id(org_id):
            raise NotFoundError('Organisation', org_id)

        data = dto.model_dump()
        data["is_admin"] = False
        data["hashed_password"] = hash_password(data.pop("password"))
        data["organisation_id"] = org_id

        try:
            return await self._repo.create_user(**data)
        except IntegrityError as e:
            raise EmailAlreadyExistsError(dto.email) from e

    async def create_admin_user(self, org_id, dto: UserCreate) -> User:
        data = dto.model_dump()
        data["is_admin"] = True
        data["hashed_password"] = hash_password(data.pop("password"))
        data["organisation_id"] = org_id

        try:
            return await self._repo.create_user(**data)
        except IntegrityError as e:
            raise EmailAlreadyExistsError(dto.email) from e

    async def update_user(self, user_id: int, org_id: int, dto: UserUpdate) -> User:
        try:
            user = await self._repo.update_user(user_id, org_id, dto)
        except IntegrityError as e:
            raise EmailAlreadyExistsError(str(dto.email)) from e

        if not user:
            raise NotFoundError("User", user_id)

        return user

    async def delete_user(self, user_id: int, org_id: int) -> None:
        ok = await self._repo.delete_user(user_id, org_id)
        if not ok:
            raise NotFoundError("User", user_id)