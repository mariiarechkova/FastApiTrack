from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

from .repositories import OrganisationRepository
from .services import OrganisationService
from ..users.repositories import UserRepository
from ..users.services import UserService


async def get_organisation_service(
    session: AsyncSession = Depends(get_session),
) -> OrganisationService:
    repo = OrganisationRepository(session)
    user_repo = UserRepository(session)
    user_service = UserService(repo=user_repo)


    return OrganisationService(repo, user_service= user_service)

