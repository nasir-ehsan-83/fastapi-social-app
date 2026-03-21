from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user

router = APIRouter(
    prefix = '/users',
    tags = ["Users"]
)

@router.post('/', response_model = UserOut)
def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # call create_user() from user_service.py to performe operations in user_service
    return create_user(user_in, db)