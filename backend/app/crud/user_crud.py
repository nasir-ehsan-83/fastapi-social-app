from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

def add_new_user(user_in: UserCreate, db: Session) -> User:
    new_user = User(**user_in.dict())
    # save new_user to database
    db.add(new_user)
    db.commit()
    # refresh database
    db.refresh(new_user)

    return new_user

def get_user_with_email(email: str, db: Session) -> User:
    # get user from database by email
    return db.query(User).filter(User.email == email).first()