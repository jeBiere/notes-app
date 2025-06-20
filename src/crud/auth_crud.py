from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth_schemas import AuthRegistration
from src.models.user_model import UserModel
from src.crud.user_crud import get_user_by_email
from src.utils.security import  verify_password, hash_password

async def register_user(db: AsyncSession, user_in: AuthRegistration) -> UserModel:
    """
    Регистрация нового пользователя: проверка на существование, хэширование пароля, сохранение в БД.
    """

    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    hashed = hash_password(user_in.password)

    user = UserModel(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user



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