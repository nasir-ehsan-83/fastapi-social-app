from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)

    @field_validator("username", "email", mode="before")
    @classmethod
    def normalize_fields(cls, v: str):
        if isinstance(v, str):
            return v.strip().lower()
        return v

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    password: Optional[str] = Field(None, min_length=8)

    @field_validator("username", "email", mode="before")
    @classmethod
    def normalize_fields(cls, v: str):
        if v is not None and isinstance(v, str):
            return v.strip().lower()
        return v
