from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import create_user, get_user_by_email, update_user_by_id, get_user_by_username, get_user_by_id, delete_user_by_id, get_all_users

router = APIRouter(
    prefix = '/users',
    tags = ["Users"]
)

# post user
@router.post('/', response_model = UserOut)
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)) -> User:
    # call create_user() from user_service.py to performe operations in user_service
    return create_user(user_in, db)


# get all user
@router.get('/', response_model = List[UserOut])
def get_all_user(db: Session = Depends(get_db)) -> User:
    return get_all_users(db)

# get user by email
@router.get('/email/{email}', response_model = UserOut)
def get_user_email(email: str, db: Session = Depends(get_db)) -> User:
    # call get_user_by_email() from user_service.py
    return get_user_by_email(email, db)

# get user by username
@router.get('/username/{username}', response_model = UserOut)
def get_user_username(username: str, db: Session = Depends(get_db)) -> User:
    return get_user_by_username(username, db)

# get user by id
@router.get('/id/{id}', response_model = UserOut)
def get_user_id(id: int, db: Session = Depends(get_db)):
    return get_user_by_id(id, db)

# update user by id
@router.put('/id/{id}', response_model = UserOut)
def update_user(id: int, updated_user: UserUpdate, db: Session = Depends(get_db)) -> User:
    # call update_user() from user_service 
    return update_user_by_id(id, updated_user, db)

# delete user by id
@router.delete('/id/{id}')
def delete_user_id(id: int, db: Session = Depends(get_db)):
    return delete_user_by_id(id, db)