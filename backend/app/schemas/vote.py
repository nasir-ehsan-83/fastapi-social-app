from pydantic import BaseModel, ConfigDict

from app.enums.post import ReactionType

class VoteBase(BaseModel):
    post_id: int
    vote_type: ReactionType

class VoteCreate(VoteBase):
    pass

class VoteOut(VoteBase):
    user_id: int

    model_config = ConfigDict(from_attributes=True)