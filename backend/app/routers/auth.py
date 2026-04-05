from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.token import Token
from app.services.auth_service import login

router = APIRouter(
    tags = ["Authentication"]
)

@router.post('/login', response_model = Token)
async def user_login(user_credential: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # perform login logic in auth_service.py
    return await login(user_credential, db)