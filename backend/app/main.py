from fastapi import FastAPI
from app.db import database
from fastapi_offline_docs.offline_docs import setup_offline_docs
from app.routers import user, post


app = FastAPI(docs_url=False, redoc_url=False)
setup_offline_docs(app)

@app.on_event("startup")
async def init_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

app.include_router(user.router)
app.include_router(post.router)