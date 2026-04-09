from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession # تغییر به AsyncSession
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.dependency.current_user import get_current_user
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import (
    create_user, get_user_by_email, update_user_by_id, 
    get_user_by_username, get_user_by_id, delete_user_by_id, get_all_users,
    get_users_by_name
)

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

# post user
@router.post('/', response_model=UserOut)
async def create_new_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    
    return await create_user(user_in, db)


# get all user
@router.get('/', response_model=List[UserOut])
async def get_all_user(db: AsyncSession = Depends(get_db)) -> List[User]:
    
    return await get_all_users(db)

# get user by email
@router.get('/email/{email}', response_model=UserOut)
async def get_user_email(email: str, db: AsyncSession = Depends(get_db)):
    return await get_user_by_email(email, db)

# get user by username
@router.get('/username/{username}', response_model=UserOut)
async def get_user_username(username: str, db: AsyncSession = Depends(get_db)):
    return await get_user_by_username(username, db)

# get user by name
@router.get('/name/{name}', response_model = List[UserOut])
async def get_user_name(name: str, db: AsyncSession = Depends(get_db)) -> List[User]:
    return await get_users_by_name(name, db)

# get user by id
@router.get('/id/{id}', response_model=UserOut)
async def get_user_id(id: int, db: AsyncSession = Depends(get_db)):
    return await get_user_by_id(id, db)

# update user by id
@router.put('/id', response_model=UserOut)
async def update_user( updated_user: UserUpdate, current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_user_by_id(current_user, updated_user, db)

# delete user by id
@router.delete('/id')
async def delete_user_id(current_user: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await delete_user_by_id(current_user, db)
