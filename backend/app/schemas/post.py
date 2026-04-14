from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional

from app.schemas.user import UserOut

class PostBase(BaseModel):
    title: str = Field(min_length = 3, max_length = 50)
    content: str = Field(max_length = 250)
    post_status: str
    post_type: str
    post_visibility: str
    post_media_url: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int
    created_at : datetime
    updated_at: datetime
    owner: UserOut

    model_config = ConfigDict(from_attributes = True)

class PostUpdate(BaseModel):
    title: Optional[str] = Field(default = None, min_length = 3, max_length = 50)
    content: Optional[str] = Field(default = None, max_length = 250)
    post_status: Optional[str] = None
    post_type: Optional[str] = None
    post_visibility: Optional[str] = None
    post_media_url: Optional[str] = None
    updated_at: datetime = Field(default_factory = datetime.utcnow)