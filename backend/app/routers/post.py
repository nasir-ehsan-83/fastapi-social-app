from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import database, models, schemas, oauth2

router = APIRouter(
    prefix = '/posts',
    tags = ["Posts"]
)

@router.get('/', response_model = List[schemas.Post])
def get_posts(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

"""
@router.get('/recent', response_model = List[schemas.Post])
def recent_post(db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post)

    return post.all()
"""

@router.get('/{id}', response_model = schemas.Post)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The post with id {id} not found")
    
    if post.user_id != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "NOt authorized to perform requested action")
    
    return post 

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db : Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.put('/{id}', response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The post whit id {id} not found")

    if post.first().user_id != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Not authorized to perform requested action")
    
    post.update(updated_post.dict(), synchronize_session = False)
    db.commit()

    return post.first()

@router.patch('/{id}/{update_parameter}', response_model = schemas.Post)
def  update_one(id: int, update_parameter: str, update_value: str, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"the post whit id {id} not found")
    
    if post.first().user_id != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Not authorized to perform requested action")
    
    post.update({update_parameter : update_value}, synchronize_session = False)
    db.commit()

    return post.first()
    
@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"the post whit id {id} not found")
    
    if int(post.first().user_id) != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")
    
    post.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

