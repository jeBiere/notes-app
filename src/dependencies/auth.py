from fastapi import Depends, Request, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.db import get_async_db
from src.utils.jwt_utils import decode_token, TokenExpired, InvalidToken
from src.crud.user_crud import get_user_by_id
from src.models.user_model import UserModel


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_async_db)
) -> UserModel:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    try:
        payload = decode_token(token)
    except TokenExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await get_user_by_id(db, payload.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user