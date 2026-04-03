from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional

from app.schemas.user import UserOut

class PostBase(BaseModel):
    title: str = Field(min_length = 3, max_length = 50)
    content: str = Field(max_length = 250)
    published: bool

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at : datetime
    owner: UserOut

    model_config = ConfigDict(from_attributes = True)

class PostUpdate(BaseModel):
    title: Optional[str] = Field(default = None, min_length = 3, max_length = 50)
    content: Optional[str] = Field(default = None, max_length = 250)
    published: Optional[bool] = None