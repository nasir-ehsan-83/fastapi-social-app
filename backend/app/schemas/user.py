from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length = 3, max_length = 30, strip_whitespace=True)


    @field_validator("username", mode="before")
    def normalize_username(cls, v):
        return v.strip().lower()

    @field_validator("email")
    def normalize_email(cls, v):
        return v.strip().lower()

class UserCreate(UserBase):
    password: str = Field(min_length = 8)

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(default = None, min_length = 3, max_length = 30, strip_whitespace=True)
    password: Optional[str] = Field(default = None, min_length = 8)