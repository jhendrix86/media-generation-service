"""
Configuration management for Media Generation Service
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost/media")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # AI Services
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    stability_api_key: str = os.getenv("STABILITY_API_KEY", "")
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    
    # Storage
    aws_access_key: str = os.getenv("AWS_ACCESS_KEY", "")
    aws_secret_key: str = os.getenv("AWS_SECRET_KEY", "")
    s3_bucket: str = os.getenv("S3_BUCKET", "")
    storage_type: str = os.getenv("STORAGE_TYPE", "local")  # local, s3, gcs
    
    # Generation Settings
    default_image_size: str = os.getenv("DEFAULT_IMAGE_SIZE", "1024x1024")
    default_image_format: str = os.getenv("DEFAULT_IMAGE_FORMAT", "png")
    max_video_duration: int = int(os.getenv("MAX_VIDEO_DURATION", "60"))
    
    # Application
    app_name: str = "Media Generation Service"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Integration
    content_engine_url: str = os.getenv("CONTENT_ENGINE_URL", "http://localhost:8040")
    marketing_automation_url: str = os.getenv("MARKETING_AUTOMATION_URL", "http://localhost:8039")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # tolerate env vars owned by other libs/fields declared in app/utils/config.py's separate Settings class


settings = Settings()
