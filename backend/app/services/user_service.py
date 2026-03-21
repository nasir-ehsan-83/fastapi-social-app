from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.crud.user_crud import add_new_user
from app.core.security import hash

def create_user(user_in: UserCreate, db: Session):
    # hash the user_in.password before storing in the database
    hashed_password = hash(user_in.password)
    user_in.password = hashed_password

    return add_new_user(user_in, db)