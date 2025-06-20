from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_db
from src.schemas.auth_schemas import AuthRegistration, AuthLogin
from src.crud.auth_crud import authenticate_user
from src.crud.user_crud import get_user_by_email
from src.crud.auth_crud import register_user

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
async def login(user_in: AuthLogin, db: AsyncSession = Depends(get_async_db)):
    user = await authenticate_user(db=db, email=user_in.email, password=user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    return user