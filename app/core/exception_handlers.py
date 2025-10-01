from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import NotFoundError, EmailAlreadyExistsError


async def email_conflict_handler(_: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "email": exc.email},
    )

async def not_found_handler(_: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "entity": exc.entity,
            "id": exc.entity_id,
        },
    )
def register_exception_handlers(app):
    app.add_exception_handler(EmailAlreadyExistsError, email_conflict_handler)
    app.add_exception_handler(NotFoundError, not_found_handler)
