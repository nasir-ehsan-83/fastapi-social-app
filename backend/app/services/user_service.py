from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.crud.user_crud import add_new_user, get_user_with_email
from app.core.security import hash

def create_user(user_in: UserCreate, db: Session) -> User:
    # hash the user_in.password before storing in the database
    hashed_password = hash(user_in.password)
    user_in.password = hashed_password

    return add_new_user(user_in, db)

def get_user_by_email(email: str, db: Session) -> User:
    user = get_user_with_email(email, db)

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with email: {email} does not exist!")
    
    return user