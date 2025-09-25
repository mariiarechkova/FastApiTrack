from datetime import datetime

from pydantic import EmailStr, BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=100)
    last_name: str  = Field(..., max_length=100)
    password: str   = Field(..., min_length=6)
    is_admin: bool = False


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    is_admin: bool = False
    organisation_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"