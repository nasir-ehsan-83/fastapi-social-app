from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.post import Post
from app.schemas.post import PostCreate

async def create_new_post(post_in: PostCreate, owner_id: int, db: AsyncSession) -> Post:
    new_post = Post(owner_id = owner_id, **post_in.model_dump())
    db.add(new_post)

    await db.commit()
    await db.refresh(new_post)

    return new_post
