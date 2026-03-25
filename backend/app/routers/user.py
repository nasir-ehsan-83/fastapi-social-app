from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, get_user_by_email, update_user_by_id

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
@router.get('/', response_model = UserOut)
def get_user_email(email: str, db: Session = Depends(get_db)) -> User:
    # call get_user_by_email() from user_service.py
    return get_user_by_email(email, db)

# update user by id
@router.put('/{id}', response_model = UserOut)
def update_user(id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    # call update_user() from user_service 
    return update_user_by_id(id, updated_user, db)