from fastapi import FastAPI

from fastapi_offline_docs.offline_docs import setup_offline_docs
from app.db import database
from app.routers import user

database.Base.metadata.create_all(bind = database.engine)

app = FastAPI(
    docs_url = False,
    redoc_url = False
)

setup_offline_docs(app)

app.include_router(user.router)