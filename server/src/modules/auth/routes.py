from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Dict
from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response
)
from src.db import get_db
from src.modules.auth.schemas import Token
from src.modules.auth.services import (
    handle_login, 
    handle_refresh_token
)



router = APIRouter(
    prefix = '/api/auth',
    tags = ["Auth"]
)




@router.post('/login', response_model = Token)
async def login(
    response: Response,
    user_credential: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    
    return await handle_login(response, user_credential, db)




@router.post('/refresh')
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:

    return await handle_refresh_token(request, response, db)


