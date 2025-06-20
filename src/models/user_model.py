from typing import List, TYPE_CHECKING
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from src.db import Base
#from src.models.note_model import NoteModel


if TYPE_CHECKING:
    from .note_model import NoteModel
    

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        comment="Уникальный UUID пользователя"
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        nullable=False,
        index=True,
        comment="Email пользователя, используется как логин"
    )

    username: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
        comment="Отображаемое имя пользователя"
    )

    hashed_password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        comment="Bcrypt-хэш пароля"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Аккаунт активен/заблокирован"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Когда аккаунт был создан"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Когда аккаунт последний раз обновлялся"
    )

    notes: Mapped[List["NoteModel"]] = relationship(
        "NoteModel",
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
