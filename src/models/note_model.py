# app/models/note.py

import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base  # или app.database: Base

class NoteModel(Base):
    __tablename__ = "notes"

    # UUID — уникальный ключ заметки
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
        comment="Уникальный UUID заметки"
    )

    # Внешний ключ на пользователя
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="UUID владельца заметки"
    )

    # Заголовок заметки
    title = Column(
        String(200),
        nullable=False,
        default="",
        comment="Заголовок заметки"
    )

    # Основное содержимое
    content = Column(
        Text,
        nullable=False,
        comment="Текст заметки"
    )

    # Метки времени
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Когда заметка была создана"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Когда заметка была обновлена"
    )

    owner = relationship(
        "UserModel",               
        back_populates="notes",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Note id={self.id} title={self.title!r} owner_id={self.owner_id}>"
