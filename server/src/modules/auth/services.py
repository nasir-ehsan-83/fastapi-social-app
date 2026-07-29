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



    
async def handle_refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession
) -> Dict[str, str]:

    try:

        refresh_token = request.cookies.get(
            "refresh_token"
        )


        if not refresh_token:

            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Refresh token not found"
            )


        payload: Dict[str, Any] = await verify_refresh_token(
            refresh_token,
            HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Unauthorized"
            )
        )


        user_id = payload.get("user_id")
        jti = payload.get("jti")


        if not user_id or not jti:

            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user: User | None = await get_user_by_id(
            user_id,
            db
        )


        if user is None:

            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "User not found"
            )


        if user.status != "active":

            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "User account is inactive"
            )

        await revoke_refresh_token(
            user_id,
            jti
        )

        access_token = await create_access_token(
            {
                "id": user.id,
                "role": user.role
            }
        )

        new_refresh_token, new_jti = await create_refresh_token(
            {
                "id": user.id,
                "role": user.role
            }
        )

        await save_refresh_token(
            user.id,
            new_jti
        )

        response.set_cookie(
            key = "jwt",
            value = new_refresh_token,
            httponly = True,
            max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400
            # secure = True, samesite = "lax"  <-  for production security
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


    except HTTPException:
        raise


    except Exception as error:

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )
    



async def handle_logout(
        request: Request,
    response: Response
):

    try:

        refresh_token = request.cookies.get("jwt")
        response = Response(status_code = status.HTTP_204_NO_CONTENT)


        if not refresh_token:

            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Refresh token not found"
            )

        payload = await verify_refresh_token(
            refresh_token,
            HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid refresh token"
            )
        )

        user_id = payload.get("id")
        jti = payload.get("jti")


        if not user_id or not jti:

            raise HTTPException(
                status_code = 401,
                detail = "Invalid refresh token"
            )

        await revoke_refresh_token(
            user_id,
            jti
        )

        response.delete_cookie(
            key = "refresh_token"
        )

        return {
            "message": "Successfully logged out"
        }

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )