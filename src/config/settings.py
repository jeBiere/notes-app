from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # DATABASE
    database_url: str
    alembic_database_url: str

    # JWT
    jwt_algorithm: str = "RS256"
    jwt_private_key_path: str
    jwt_public_key_path: str
    access_token_expire_minutes: int = 30

    @property
    def private_key(self) -> bytes:
        return Path(self.jwt_private_key_path).read_bytes()

    @property
    def public_key(self) -> bytes:
        return Path(self.jwt_public_key_path).read_bytes()

    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_reload: bool = True

    class Config:
        env_file = ".env"

settings = Settings() # type: ignore
