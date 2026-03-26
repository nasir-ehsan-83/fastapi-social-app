from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import create_user, get_user_by_email, update_user_by_id, get_user_by_username

router = APIRouter(
    prefix = '/users',
    tags = ["Users"]
)

# post user
@router.post('/', response_model = UserOut)
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)) -> User:
    # call create_user() from user_service.py to performe operations in user_service
    return create_user(user_in, db)

# get user by email
@router.get('/email/{email}', response_model = UserOut)
def get_user_email(email: str, db: Session = Depends(get_db)) -> User:
    # call get_user_by_email() from user_service.py
    return get_user_by_email(email, db)

# get user by username
@router.get('/username/{username}', response_model = UserOut)
def get_user_username(username: str, db: Session = Depends(get_db)) -> User:
    return get_user_by_username(username, db)

# update user by id
@router.put('/id/{id}', response_model = UserOut)
def update_user(id: int, updated_user: UserUpdate, db: Session = Depends(get_db)) -> User:
    # call update_user() from user_service 
    return update_user_by_id(id, updated_user, db)