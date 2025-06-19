# чтобы при импорте app.models у вас сразу появились Base и все модели
from db import Base
from user_model import UserModel
from note_model import NoteModel

__all__ = ["Base", "UserModel", "NoteModel"]
