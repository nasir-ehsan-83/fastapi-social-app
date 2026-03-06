from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix = '/votes',
    tags = ["Votes"]
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # does post exist? or note
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    # if post does not exist
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {vote.post_id} does not exist")
    
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    # get the specified vote 
    found_vote = vote_query.first()
    # if the vote's dir is 1, means that want to vote
    if vote.dir == 1:
        # if the specified vote exists 
        if found_vote:
           raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"User with id: {current_user.id} has already voted on post {vote.post_id}")

        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message" : "succesfully added vote"}
    # if the vote's dir is 0 means that want to devote 
    else:
        # if the specified vote does not exist
        if not found_vote:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote does not exist")
        
        vote_query.delete(synchronize_session = False)
        db.commit()

        return {"message" : "Successfully deleted vote"}