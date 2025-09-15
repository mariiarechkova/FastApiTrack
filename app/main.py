from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()

app = FastAPI(title="My API", lifespan=lifespan)