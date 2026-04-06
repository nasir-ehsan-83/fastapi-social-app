from fastapi import HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.models.user import User
from app.core.security import hash, verify # to verfiry is the password hashed
from app.core.oauth2 import create_access_token

async def login(user_credential: OAuth2PasswordRequestForm, db: AsyncSession):
    print(user_credential.password, user_credential.username)
    
    user_query = await db.execute(select(User).filter(User.username == user_credential.username))
    user = user_query.scalars().first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid credential")
    
    if not await verify(user_credential.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid credential")
    
    access_token = await create_access_token(data = {"user_id" : user.id})

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }