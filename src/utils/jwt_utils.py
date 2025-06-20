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


def create_token(payload: TokenPayload, expires_delta: timedelta, token_type: str) -> str:
    """
    Генерирует JWT токен с заданным типом (`access` или `refresh`).
    """
    to_encode = payload.dict()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({
        "exp": expire,
        "token_type": token_type
    })

    token = jwt.encode(
        payload=to_encode,
        key=settings.private_key,
        algorithm=settings.jwt_algorithm,
    )
    return token



def decode_token(token: str, expected_type: str | None = None) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            key=settings.public_key,
            algorithms=[settings.jwt_algorithm],
        )

        if expected_type and payload.get("token_type") != expected_type:
            raise InvalidToken("Invalid token type")

        return TokenPayload(**payload)

    except ExpiredSignatureError:
        raise TokenExpired("JWT token has expired")
    except InvalidTokenError:
        raise InvalidToken("JWT token is invalid")

    
    