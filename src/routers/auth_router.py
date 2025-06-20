from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.db import get_async_db
from src.schemas.auth_schemas import AuthRegistration, AuthLogin, TokenPayload, TokenResponse
from src.crud.auth_crud import authenticate_user
from src.crud.user_crud import get_user_by_email
from src.crud.auth_crud import register_user
from src.utils.jwt_utils import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/registration")
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

@router.post("/login")
async def login(user_in: AuthLogin,response: Response ,db: AsyncSession = Depends(get_async_db)):
    user = await authenticate_user(db=db, email=user_in.email, password=user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )
    payload = TokenPayload(
        sub=str(user.id),
        email=user.email,
    )

    access_token = create_access_token(payload)
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,       # Защищает от XSS
        secure=False,        # В проде ставим True (https)
        samesite="lax",      # или "strict"
        max_age=60 * 30      # столько же, сколько живёт токен
    )
    
    return {"message": "Login successful"}


