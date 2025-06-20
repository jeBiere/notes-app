import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from fastapi import HTTPException, status
from datetime import datetime, timedelta

from src.schemas.auth_schemas import TokenPayload
from src.config.settings import settings

class TokenExpired(Exception):
    pass

class InvalidToken(Exception):
    pass


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


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            key=settings.public_key,  # тоже bytes
            algorithms=[settings.jwt_algorithm],
        )
        return TokenPayload(**payload)
    except ExpiredSignatureError:
        raise TokenExpired("JWT token has expired")
    except InvalidTokenError:
        raise InvalidToken("JWT token is invalid")