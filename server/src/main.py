from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.errors import init_error_handlers
from src.db import database
from src.core import cosr_config
from src.modules import (
    auth_routes,
    users_routes,
    posts_routes,
    votes_routes
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    await database.engine.dispose()

app: FastAPI = FastAPI(lifespan = lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = cosr_config["origins"],
    allow_credentials = cosr_config["is_credentials_allowed"],
    allow_methods = cosr_config["methods"],
    allow_headers = cosr_config["headers"]
)

init_error_handlers(app)

app.include_router(auth_routes)
app.include_router(users_routes)
app.include_router(posts_routes)
app.include_router(votes_routes)