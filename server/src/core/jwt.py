from typing import Any, Dict
from uuid import uuid4

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError

from src.modules.auth.schemas import TokenData
from src.config import settings
from src.db import redis_client




async def create_access_token(
    data: Dict[str, Any]
) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    jti = str(uuid4())

    to_encode.update({
        "exp": expire,
        "type": "access",
        "jti": jti
    })


    token = jwt.encode(
        to_encode,
        settings.ACCESS_TOKEN_SECRET_KEY,
        algorithm = settings.ALGORITHM
    )


    return token



async def verify_access_token(
    token: str,
    credentials_exception: HTTPException
) -> TokenData:


    try:

        payload = jwt.decode(
            token,
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithms = [
                settings.ALGORITHM
            ]
        )


        if payload.get("type") != "access":
            raise credentials_exception


        user_id = payload.get("id")
        user_role = payload.get("role")
        jti = payload.get("jti")


        if not user_id or not jti:
            raise credentials_exception



        # check blacklist
        is_revoked = await redis_client.exists(
            f"blacklist:access:{jti}"
        )


        if is_revoked:
            raise credentials_exception



        return TokenData(
            id = user_id,
            role = user_role
        )


    except JWTError:
        raise credentials_exception



async def create_refresh_token(
    data: Dict[str, Any]
):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )


    jti = str(uuid4())


    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": jti
    })


    token = jwt.encode(
        to_encode,
        settings.REFRESH_TOKEN_SECRET_KEY,
        algorithm = settings.ALGORITHM
    )


    return token, jti



async def verify_refresh_token(
    token:str,
    credentials_exception:HTTPException
):

    try:

        payload = jwt.decode(
            token,
            settings.REFRESH_TOKEN_SECRET_KEY,
            algorithms = [
                settings.ALGORITHM
            ]
        )


        if payload.get("type") != "refresh":
            raise credentials_exception



        user_id = payload.get("id")
        user_role = payload.get("role")
        jti = payload.get("jti")


        if not user_id or not jti:
            raise credentials_exception



        exists = await redis_client.exists(
            f"refresh:{user_id}:{jti}"
        )


        if not exists:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Refresh token revoked"
            )


        return payload



    except ExpiredSignatureError:

        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Refresh token expired"
        )


    except JWTError:

        raise credentials_exception
    