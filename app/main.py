from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine
from app.core.exception_handlers import register_exception_handlers
from app.organisations.routers import router as organisation_router
from app.users.routers.auth import router as auth_router
from app.users.routers.user_routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()


app = FastAPI(title="My API", lifespan=lifespan)

register_exception_handlers(app)


app.include_router(organisation_router)
app.include_router(user_router)
app.include_router(auth_router)
