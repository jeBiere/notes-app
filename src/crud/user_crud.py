from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from src.models.user_model import UserModel
from src.schemas.user_schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

async def create_user(db: AsyncSession, user_in: UserCreate) -> UserModel:
    """
    Создать нового пользователя: проверка на существование, хэширование пароля, сохранение в БД.
    """

    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")

    hashed = pwd_context.hash(user_in.password)

    user = UserModel(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля и его хэша.
    """
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserModel | None:
    """
    Аутентифицирует пользователя: проверяет email и пароль.
    Возвращает пользователя, если всё верно, иначе None.
    """
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user
