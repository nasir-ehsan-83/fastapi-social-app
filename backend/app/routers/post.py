from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.dependency.current_user import get_current_user
from app.services.post_service import (create_new_post, get_one_post, get_all_posts, update_data, delete_data)


router = APIRouter(
    prefix = '/posts',
    tags = ["Post"]
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = PostOut)
async def create_post(post_in: PostCreate, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Post:
    # send the data to the post_service.py to performe operations 
    return await create_new_post(post_in, current_user, db)

# get a post
@router.get('/{id}', response_model = PostOut)
async def get_post(id: int, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Optional[Post]:
    # send the data to the post_service.py to performe operations 
    return await get_one_post(id, current_user, db)

# get all posts
@router.get('/', response_model = List[PostOut])
async def get_posts(current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Optional[List[Post]]:
    # send the data to the post_service.py to performe operations 
    return await get_all_posts(current_user, db)

# update post
@router.put('/{id}', response_model = PostOut)
async def update_post(id: int, update_post: PostUpdate, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> Post:
    # send the data to the post_service.py to performe operations 
    return await update_data(id, update_post, current_user, db)

# delete post
@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)) :
    return await delete_data(id, current_user, db)