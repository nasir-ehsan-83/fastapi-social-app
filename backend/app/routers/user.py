from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, utils

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

# GET user by ID
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user

# CREATE user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # hash the password (truncate to 72 chars for bcrypt)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# UPDATE user
@router.put('/{id}', response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

# PATCH single field
@router.patch('/{id}', response_model=schemas.UserOut)
def update_one(id: int, updated_parameter: str, updated_value: str, db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    user_query.update({updated_parameter: updated_value}, synchronize_session=False)
    db.commit()
    return user_query.first()

# DELETE user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_users(id: int, db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    if user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
