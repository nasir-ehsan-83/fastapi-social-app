from typing import (
    Any, 
    Dict
)
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from jose import (
    jwt, 
    JWTError
)
from datetime import (
    datetime, 
    timedelta,
    timezone
)
from src.modules.auth.schemas import TokenData
from src.config.config import settings

SECRET_KEY = settings.ACCESS_TOKEN_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

async def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Use run_in_threadpool for the CPU-bound encoding
    encoded_jwt = await run_in_threadpool(
        jwt.encode, 
        to_encode, 
        SECRET_KEY, 
        algorithm = ALGORITHM
    )
    
    return encoded_jwt

async def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData | HTTPException:
    try: 
        # Use run_in_threadpool for the CPU-bound decoding
        payload: Dict[str, int | str] = await run_in_threadpool(
            jwt.decode, 
            token, 
            SECRET_KEY, 
            algorithms = [ALGORITHM]
        )

        user_id: int = payload.get("user_id") # type: ignore

        if not user_id:
            raise credentials_exception
        
        token_data = TokenData( id = user_id)

    except JWTError:
        raise credentials_exception
    
    return token_data
