from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(min_length = 1, length = 30)
    lastname: Optional[str] = Field(length = 30)
    username: str = Field(min_length=3, max_length=30)
    biography: Optional[str] = Field(max_length = 250)
    email: EmailStr
    role: str
    status: str
    visibility: str

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
    updated_at: datetime
     
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length = 1, max_length = 50)
    lastname: Optional[str] = Field(None, length = 30)
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length = 20)
    biography: Optional[str] = Field(max_length = 250)

    @field_validator("username", "email", mode="before")
    @classmethod
    def normalize_fields(cls, v: str):
        if v is not None and isinstance(v, str):
            return v.strip().lower()
        return v
