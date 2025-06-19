from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user_schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_async_db
from src.crud.user_crud import get_user_by_email
from src.crud.auth_crud import register_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/registration")
async def registration(user_in: UserCreate, db: AsyncSession = Depends(get_async_db)):
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