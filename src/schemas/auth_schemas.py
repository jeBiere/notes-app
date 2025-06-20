# src/schemas/auth_shemas.py

from typing import Optional, Literal
from src.schemas.user_schemas import UserBase
from pydantic import BaseModel, EmailStr, Field

class AuthRegistration(UserBase):
    password: str = Field(
        title="Пароль (строка от 8 до 128 символов)",
        min_length=8,
        max_length=128,
    )

class AuthLogin(BaseModel):
    email: EmailStr = Field(
        title="Email пользователя для авторизации",
        max_length=320,
    )
    password: str = Field(
        title="Пароль (строка от 8 до 128 символов)",
        min_length=8,
        max_length=128,
    )


class MessageResponse(BaseModel):
    message: str

class TokenPayload(BaseModel):
    sub: str  # user_id
    email: EmailStr
