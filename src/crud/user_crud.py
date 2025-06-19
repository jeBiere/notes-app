from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from typing import Optional, List, Sequence
from src.models.user_model import UserModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_users(db: AsyncSession) -> Optional[Sequence[UserModel]]:
    result = await db.execute(select(UserModel))
    return result.scalars().all()

async def get_user_by_email(db: AsyncSession, email: str) -> UserModel | None:
    """
    Получить пользователя по email.
    """
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalars().first()

async def get_user_by_id(db: AsyncSession, user_id: str) -> UserModel | None:
    """
    Получить пользователя по его UUID.
    """
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    return result.scalars().first()


