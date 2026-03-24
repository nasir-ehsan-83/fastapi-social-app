from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash

def create_user(user_in: UserCreate, db: Session) -> User:
    # hash the user_in.password before storing in the database
    hashed_password = hash(user_in.password)
    user_in.password = hashed_password

    new_user = User(**user_in)
    # add user into database
    db.add(new_user)
    # commit the changes
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_email(email: str, db: Session) -> User:
    # find the user from database
    user = db.query(User).filter(User.email == email).first()

    # if the user by specific email does not exist return an exception
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with email: {email} does not exist!")
    
    return user