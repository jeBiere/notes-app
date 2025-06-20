import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base
#from src.models.user_model import UserModel
if TYPE_CHECKING:
    from .user_model import UserModel
class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        comment="Уникальный UUID заметки"
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="UUID владельца заметки"
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="",
        comment="Заголовок заметки"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Текст заметки"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Когда заметка была создана"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Когда заметка была обновлена"
    )

    owner: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="notes",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Note id={self.id} title={self.title!r} owner_id={self.owner_id}>"
