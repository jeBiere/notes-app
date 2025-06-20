from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies.db import get_async_db
from src.crud.user_crud import get_users, get_user_by_email, get_user_by_id


router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/users")
async def read_users(db: AsyncSession = Depends(get_async_db)):
    result = await get_users(db)
    return result

@router.get("/users/email/")
async def read_user_by_email(user_email: str, db: AsyncSession = Depends(get_async_db)):
    result = await get_user_by_email(db, email=user_email)
    return result
    
@router.get("/users/id/{user_id}")
async def read_user_by_id(user_id: str, db: AsyncSession = Depends(get_async_db)):
    result = await get_user_by_id(db, user_id=user_id)
    return result
    

    
    

