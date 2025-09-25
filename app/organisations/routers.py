
from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status

from app.organisations import schemas
from app.organisations.dependencies import get_organisation_service
from app.organisations.schemas import OrganisationCreate, OrganisationAndUserCreate
from app.organisations.services import OrganisationService

router = APIRouter(prefix="/api/organisations", tags=["Organisations"])


@router.get("/", response_model=list[schemas.OrganisationRead])
async def list_organisations(
    service: OrganisationService = Depends(get_organisation_service),
):
    return await service.get_all()

@router.get("/{org_id}", response_model=schemas.OrganisationRead)
async def get_organisation(
    org_id: int = Path(..., gt=0),
    service: OrganisationService = Depends(get_organisation_service),
):
    return await service.get_by_id(org_id)

@router.post(
    "/",
    response_model=schemas.OrganisationWithAdminRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_organisation(
    data: OrganisationAndUserCreate,
    service: OrganisationService = Depends(get_organisation_service),
):
    return await service.create(data)

@router.patch(
    "/{org_id}",
    response_model=schemas.OrganisationRead,
)
async def update_organisation(
    data: schemas.OrganisationUpdate,
    org_id: int = Path(..., gt=0),
    service: OrganisationService = Depends(get_organisation_service),
):
    organisation = await service.update(org_id, data)
    if not organisation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return organisation


@router.delete(
    "/{org_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_organisation(
    org_id: int = Path(..., gt=0),
    service: OrganisationService = Depends(get_organisation_service),
):
    deleted = await service.delete(org_id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    return None



