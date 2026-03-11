from backend.fastapi_offline_docs.offline_docs import  setup_offline_docs
from fastapi import FastAPI
from . import models, database
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind = database.engine)

app = FastAPI(
    docs_url=None,
    redoc_url=None
)

setup_offline_docs(app)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
