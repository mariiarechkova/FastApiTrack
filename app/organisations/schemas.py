from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.users.schemas import UserCreate, UserRead


class OrganisationBase(BaseModel):
    name: str

class OrganisationCreate(OrganisationBase):
    pass

class OrganisationAndUserCreate(OrganisationBase):
    user: UserCreate

class OrganisationUpdate(BaseModel):
    name: str | None = None

class OrganisationRead(OrganisationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OrganisationWithAdminRead(OrganisationRead):
    admin: UserRead