from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import decode_access_token
from app.organisations.reader import OrganisationQueryReader
from app.users.repositories import UserRepository
from app.users.schemas import CurrentUser
from app.users.services.auth_service import AuthService
from app.users.services.user_service import UserService


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    repo = UserRepository(session)
    org_reader = OrganisationQueryReader(session)
    return UserService(repo, org_reader)


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    repo = UserRepository(session)
    return AuthService(repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> CurrentUser:
    try:
        payload = decode_access_token(token)
    except (ExpiredSignatureError, InvalidTokenError):
        raise UNAUTHORIZED

    user_id = payload.get("user_id")
    org_id = payload.get("organisation_id")

    if user_id is None or org_id is None:
        raise UNAUTHORIZED

    return CurrentUser(
        id=int(user_id),
        organisation_id=int(org_id),
        email=payload.get("email"),
    )


async def require_admin_user(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> CurrentUser:
    repo = UserRepository(session)
    is_admin = await repo.is_admin(current_user.id)

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have admin access",
        )

    return current_user