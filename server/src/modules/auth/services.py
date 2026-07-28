from typing import (
    Any, 
    Dict
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    HTTPException,
    Request,
    Response,
    status
)
from src.config import settings
from src.modules.users.repository import (
    get_user_by_id, 
    get_user_by_username
)
from src.modules.users.model import User
from src.core import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    verify_password
)
from src.modules.auth.session import (
    revoke_refresh_token, 
    save_refresh_token
)



async def handle_login(
    response: Response,
    user_credential: OAuth2PasswordRequestForm,
    db: AsyncSession
) -> Dict[str, str]:

    user: User = await get_user_by_username(
        user_credential.username,
        db
    )


    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )


    if not await verify_password(
        user_credential.password,
        str(user.password)
    ):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )


    access_token = await create_access_token(
        {
            "id": user.id,
            "role": user.role
        }
    )


    refresh_token, refresh_jti = await create_refresh_token(
        {
            "id": user.id,
            "role": user.role
        }
    )


    await save_refresh_token(
        user.id,
        refresh_jti
    )

    response.set_cookie(
        key = "jwt",
        value = refresh_token,
        httponly = True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
        # secure = True, samesite = "lax"  <-  for production security
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }



