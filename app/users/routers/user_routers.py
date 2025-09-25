from fastapi import APIRouter, Depends, Path, HTTPException, status

from app.users import schemas
from app.users.dependencies import get_user_service, require_admin_user, get_current_user
from app.users.models import User
from app.users.schemas import UserRead, UserCreate, UserUpdate
from app.users.services import UserService


router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(
    current_user: User = Depends(require_admin_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_all_users(current_user.organisation_id)

@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserRead)
async def get_user(
    user_id: int = Path(..., gt=0),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



@router.post("", response_model=UserRead)
async def create_user(
    dto: UserCreate,
    service: UserService = Depends(get_user_service),
    admin_user: User = Depends(require_admin_user),
):
    try:
        return await service.create_user(admin_user.organisation_id, dto)
    except ValueError as e:
        detail = str(e)
        if "already exists" in detail:
            raise HTTPException(status_code=409, detail=detail)
        raise HTTPException(status_code=400, detail=detail)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
        user_id: int = Path(..., gt=0),
        dto: UserUpdate = ...,
        service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    try:
        return await service.update_user(user_id, current_user.organisation_id, dto)
    except ValueError as e:
        msg = str(e).lower()
        if "not found" in msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if "integrity" in msg or "exists" in msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(..., gt=0),
    service: UserService = Depends(get_user_service),
    admin_user: User = Depends(require_admin_user),
):
    try:
        await service.delete_user(user_id, admin_user.organisation_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
