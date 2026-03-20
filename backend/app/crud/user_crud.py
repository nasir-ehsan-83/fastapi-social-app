from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate

def add_new_user(user_in: UserCreate, db: Session):
    new_user = User(**user_in.dict())
    # save new_user to database
    db.add(new_user)
    db.commit()
    # refresh database
    db.refresh(new_user)

    return new_user