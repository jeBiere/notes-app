# src/schemas/user_schemas.py

from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(title="Email пользователя", max_length=320)
    username: str = Field(
        title="Отображаемое имя пользователя",
        min_length=2,
        max_length=50,
    )

class UserRead(UserBase):
    id: UUID = Field(title="UUID пользователя")
    is_active: bool = Field(title="Статус активности")
    created_at: datetime = Field(title="Дата создания аккаунта")
    updated_at: datetime = Field(title="Дата последнего обновления")

    class Config:
        orm_mode = True

