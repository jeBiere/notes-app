import jwt
from datetime import datetime, timedelta
from typing import Any
from src.schemas.auth_schemas import TokenPayload

from src.config.settings import settings

def create_access_token(payload: TokenPayload) -> str:
    """
    Генерирует JWT токен из TokenPayload. Подписывается приватным ключом.
    """
    to_encode = payload.dict()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode["exp"] = expire

    token = jwt.encode(
        payload=to_encode,
        key=settings.private_key,
        algorithm=settings.jwt_algorithm,
    )

    return token