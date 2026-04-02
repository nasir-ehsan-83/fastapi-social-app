from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostOut
from app.services.post_service import create_new_post

router = APIRouter(
    prefix = '/posts',
    tags = ["Post"]
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = PostOut)
async def create_post(post_in: PostCreate, owner_id: int, db: AsyncSession = Depends(get_db)) -> Post:
    return await create_new_post(post_in, owner_id, db)

