from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password, create_access_token
from app.users.models import User
from app.users.repositories import UserRepository
from app.users.schemas import UserCreate, UserUpdate, Token


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def get_all_users(self, org_id):
        return await self._repo.get_all(org_id=org_id)

    async def get_user_by_id(self, user_id):
        user = await self._repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def create_user(self, org_id: int, dto: UserCreate) -> User:
        data = dto.model_dump()
        data["hashed_password"] = hash_password(data.pop("password"))
        data["organisation_id"] = org_id

        try:
            return await self._repo.create_user(**data)
        except IntegrityError as e:
            raise ValueError("User with this email already exists") from e

    async def update_user(self, user_id: int, org_id: int, dto: UserUpdate) -> User:
        changes = dto.model_dump(exclude_unset=True)

        try:
            user = await self._repo.update_user(user_id, org_id, changes)
        except IntegrityError as e:
            raise ValueError("Integrity constraint failed") from e

        if not user:
            raise ValueError("User not found")
        return user

    async def delete_user(self, user_id: int, org_id: int) -> None:
        ok = await self._repo.delete_user(user_id, org_id)
        if not ok:
            raise ValueError("User not found")


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def login(self, email: str, password: str) -> Token:
        user = await self.repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        token = create_access_token(user)
        return Token(access_token=token)
