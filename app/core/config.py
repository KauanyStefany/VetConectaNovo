import os
import secrets
from typing import Optional


class Settings:
    # Database
    DATABASE_URL: str = "dados.db"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SESSION_MAX_AGE: int = 3600  # 1 hora em segundos

    # Upload
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/jpg"]

    # Email (para funcionalidades futuras)
    EMAIL_FROM: Optional[str] = None
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: Optional[int] = None
    EMAIL_USERNAME: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    # Templates
    TEMPLATES_DIR: str = "app/templates"
    STATIC_DIR: str = "static"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100


settings = Settings()