from fastapi import Request
from fastapi.responses import JSONResponse

from app.organisations.errors import OrganisationNotFoundError
from app.users.errors import EmailAlreadyExistsError, UserNotFoundError

async def email_conflict_handler(_: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "email": exc.email},
    )

async def user_not_found_handler(_: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "user_id": exc.user_id},
    )

async def organisation_not_found_handler(_: Request, exc: OrganisationNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "organisation_id": exc.org_id},
    )

def register_exception_handlers(app):
    app.add_exception_handler(EmailAlreadyExistsError, email_conflict_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
    app.add_exception_handler(OrganisationNotFoundError, organisation_not_found_handler)