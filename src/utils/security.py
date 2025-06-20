from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля и его хэша.
    """
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Возвращает хеш пароля.
    """
    return pwd_context.hash(password)