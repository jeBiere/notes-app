from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.db import get_async_db
from src.crud.user_crud import get_users, get_user_by_email, get_user_by_id
from src.dependencies.auth import get_current_user
from src.models.user_model import UserModel
from src.schemas.user_schemas import UserRead
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/users", response_model = List[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    
    result = await get_users(db)
    return result

@router.get("/users/email/", response_model=UserRead)
async def read_user_by_email(
    user_email: str,
    db: AsyncSession = Depends(get_async_db)
):
    
    result = await get_user_by_email(db, email=user_email)
    return result
    
@router.get("/users/id/{user_id}", response_model=UserRead)
async def read_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_async_db)
):
    result = await get_user_by_id(db, user_id=user_id)
    return result
    

    
    

