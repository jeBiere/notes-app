from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.db import get_async_db
from src.schemas.auth_schemas import AuthRegistration, AuthLogin, TokenPayload, MessageResponse
from src.schemas.user_schemas import UserRead
from src.crud.auth_crud import authenticate_user
from src.crud.user_crud import get_user_by_email
from src.crud.auth_crud import register_user
from src.utils.jwt_utils import InvalidToken, TokenExpired, create_token, decode_token
from src.config.settings import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logout successful"}


@router.post("/registration", response_model=UserRead)
async def registration(user_in: AuthRegistration, db: AsyncSession = Depends(get_async_db)):
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email уже зарегистрирован",
        )
    try:
        user = await register_user(db, user_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(str(e))
        )
    return user

@router.post("/login", response_model=MessageResponse)
async def login(user_in: AuthLogin, response: Response, db: AsyncSession = Depends(get_async_db)):
    user = await authenticate_user(db=db, email=user_in.email, password=user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    payload = TokenPayload(sub=str(user.id), email=user.email)

    access_token = create_token(
        payload=payload,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access"
    )
    refresh_token = create_token(
        payload=payload,
        expires_delta=timedelta(minutes=settings.refresh_token_expire_minutes),
        token_type="refresh"
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=60 * settings.access_token_expire_minutes,
        samesite="lax",
        secure=False,  # В проде обязательно True
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=60 * settings.refresh_token_expire_minutes,
        samesite="lax",
        secure=False,
    )

    return {"message": "Login successful"}


@router.post("/refresh", response_model=MessageResponse)
async def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = decode_token(token, expected_type="refresh")
    except TokenExpired:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_token(
        payload=TokenPayload(sub=payload.sub, email=payload.email),
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access"
    )

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=60 * settings.access_token_expire_minutes,
        samesite="lax",
        secure=False,
    )

    return {"message": "Access token refreshed"}


