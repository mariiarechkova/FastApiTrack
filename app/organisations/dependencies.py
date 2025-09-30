from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from .repositories import OrganisationRepository
from .services import OrganisationService
from ..users.dependencies import get_user_service
from ..users.services.user_service import UserService


async def get_organisation_service(
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service)
) -> OrganisationService:
    repo = OrganisationRepository(session)
    return OrganisationService(repo=repo, user_service = user_service)