from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash

def create_user(user_in: UserCreate, db: Session) -> User:
    # hash the user_in.password before storing in the database
    hashed_password = hash(user_in.password)
    user_in.password = hashed_password

    new_user = User(**user_in.dict())
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

def update_user_by_id(id: int, updated_user: UserCreate, db: Session):
    # get user from database
    user_query = db.query(User).filter(User.id == id)

    # if the user by specific id does not exist
    if user_query.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exist")
    
    # hash the password 
    updated_user.password = hash(updated_user.password)
    print(id)
    # save updated user
    user_query.update(updated_user.dict() , synchronize_session = False)
    print(user_query.first())
    # commit changes
    db.commit()

    return user_query.first()