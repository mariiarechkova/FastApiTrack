from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm

from app.organisations.dependencies import get_organisation_service
from app.organisations.services import OrganisationService
from app.users import schemas
from app.users.dependencies import get_auth_service, get_user_service


from app.users.services import AuthService, UserService

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=schemas.UserRead)
async def register(
    data: schemas.UserCreate,
    user_service: UserService = Depends(get_user_service),
    org_id: int = Query(..., gt=0),
    org_service: OrganisationService = Depends(get_organisation_service),
):
    org = await org_service.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")

    try:
        return await user_service.create_user(org_id, data)
    except ValueError as e:
        msg = str(e).lower()
        if "already" in msg or "exists" in msg:
            raise HTTPException(status_code=409, detail="Email already registered")
        raise HTTPException(status_code=400, detail=str(e))
