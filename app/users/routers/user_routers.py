from fastapi import APIRouter, Depends, Path, status

from app.users import schemas
from app.users.dependencies import get_current_user, get_user_service, require_admin_user
from app.users.models import User
from app.users.schemas import UserCreate, UserRead, UserUpdate
from app.users.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(
    admin_user: User = Depends(require_admin_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all_users(admin_user.organisation_id)


@router.get("/me", response_model=schemas.CurrentUser)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserRead)
async def get_user(
    user_id: int = Path(..., gt=0),
    service: UserService = Depends(get_user_service),
):
    return await service.get_user_by_id(user_id)


@router.post("", response_model=UserRead)
async def create_user(
    dto: UserCreate,
    service: UserService = Depends(get_user_service),
    admin_user: User = Depends(require_admin_user),
):
    return await service.create_user(admin_user.organisation_id, dto)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int = Path(..., gt=0),
    dto: UserUpdate = ...,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return await service.update_user(user_id, current_user.organisation_id, dto)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(..., gt=0),
    service: UserService = Depends(get_user_service),
    admin_user: User = Depends(require_admin_user),
):
    await service.delete_user(user_id, admin_user.organisation_id)
