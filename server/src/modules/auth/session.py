from src.db import redis_client
from src.config import settings


async def save_refresh_token(
    user_id: int,
    jti: str
):

    await redis_client.setex(

        f"refresh:{user_id}:{jti}",

        settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,

        "active"
    )




async def revoke_refresh_token(
    user_id: int,
    jti: str
):

    await redis_client.delete(
        f"refresh:{user_id}:{jti}"
    )