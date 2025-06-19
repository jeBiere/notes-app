from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db import Base
import uuid


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        comment="Уникальный UUID пользователя"
    )

    email = Column(
        String(320),   # максимальная длина RFC-совместимого email
        unique=True,
        nullable=False,
        index=True,
        comment="Email пользователя, используется как логин"
    )

    username = Column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
        comment="Отображаемое имя пользователя"
    )

    hashed_password = Column(
        String(128),
        nullable=False,
        comment="Bcrypt-хэш пароля"
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Аккаунт активен/заблокирован"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Когда аккаунт был создан"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Когда аккаунт последний раз обновлялся"
    )

    notes = relationship(
        "NoteModel",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
    