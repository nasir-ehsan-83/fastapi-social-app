from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime

from app.schemas.user import UserOut

class PostBase(BaseModel):
    title: str = Field(min_length = 3, max_length = 50)
    content: str = Field(max_length = 250)
    published: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at : datetime
    owner: UserOut

    model_config = ConfigDict(from_attributes = True)
