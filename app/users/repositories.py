from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemas import UserUpdate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, org_id: int):
        stmt = select(User).where(User.organisation_id == org_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def is_admin(self, user_id: int) -> bool:
        result = await self.session.execute(select(User.is_admin).where(User.id == user_id))
        return bool(result.scalar())

    async def create_user(self, **kwargs) -> User:
        user = User(**kwargs)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, org_id: int, changes: UserUpdate) -> User | None:
        res = await self.session.execute(select(User).where(User.id == user_id, User.organisation_id == org_id))
        user = res.scalar_one_or_none()
        if user is None:
            return None

        data = changes.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(user, key, value)

        await self.session.flush()
        return user

    async def delete_user(self, user_id: int, org_id: int) -> bool:
        result = await self.session.execute(delete(User).where(User.id == user_id, User.organisation_id == org_id))
        await self.session.flush()
        return result.rowcount > 0
