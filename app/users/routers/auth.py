from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from app.users import schemas
from app.users.dependencies import UNAUTHORIZED, get_auth_service, get_user_service
from app.users.services.auth_service import AuthService
from app.users.services.user_service import UserService

#
router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.login(form_data.username, form_data.password)
    except ValueError:
        raise UNAUTHORIZED


@router.post("/register", response_model=schemas.UserRead)
async def register(
    data: schemas.UserCreate,
    user_service: UserService = Depends(get_user_service),
    org_id: int = Query(..., gt=0),
):
    return await user_service.create_user(org_id, data)
