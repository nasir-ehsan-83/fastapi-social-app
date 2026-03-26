from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import hash

def create_user(user_in: UserCreate, db: Session) -> User:
    # check does the user already exist
    user_by_email = db.query(User).filter(User.email == user_in.email).first()
    user_by_username = db.query(User).filter(User.username == user_in.username).first()
    
    if user_by_email:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User with email: {user_in.email} already exist")

    if user_by_username:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"User whit username: {user_in.username} already exist.")
    
    # hash the user_in.password before storing in the database
    hashed_password = hash(user_in.password)
    user_in.password = hashed_password

    new_user = User(**user_in.model_dump())
    # add user into database
    db.add(new_user)
    # commit the changes
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_by_email(email: str, db: Session) -> User:
    # find the user from database by specific email
    user = db.query(User).filter(User.email == email).first()

    # if the user by specific email does not exist return an exception
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with email: {email} does not exist!")
    
    return user

def get_user_by_username(username: str, db: Session) -> User:
    # find the user by specific username
    user = db.query(User).filter(func.lower(User.username) == func.lower(username)).first()
   
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with username: {username} does not exist.")
    
    return user

def update_user_by_id(id: int, updated_user: UserUpdate, db: Session) -> User:
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    data = updated_user.model_dump(exclude_unset=True)
    if "password" in data:
        data["password"] = hash(data["password"])

    user_query.update(data, synchronize_session=False)
    db.commit()
    db.refresh(user)  # ensure returned object is updated

    return user