from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Media Generation Service Configuration."""
    
    # Service
    service_name: str = "media-generation-service"
    service_version: str = "1.0.0"
    port: int = 8018
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_database: str = "media_generation"
    
    # RabbitMQ
    rabbitmq_url: str = "amqp://localhost:5672"
    rabbitmq_exchange: str = "autonomy.events"
    rabbitmq_exchange_type: str = "topic"
    
    # Media Generation APIs
    openai_api_key: Optional[str] = None
    stability_api_key: Optional[str] = None
    leonardo_api_key: Optional[str] = None
    replicate_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    
    # Media Settings
    max_retries: int = 3
    retry_backoff_base: int = 2  # seconds
    default_image_size: str = "1024x1024"
    supported_formats: list = ["png", "jpg", "webp"]
    max_file_size_mb: int = 10
    
    # Governance
    enforce_governance: bool = True
    require_governance_approval: bool = False
    
    # Brand Rules
    enforce_brand_rules: bool = True
    brand_colors: list = []
    brand_fonts: list = []
    
    # Compliance
    enforce_compliance: bool = True
    require_alt_text: bool = True
    require_licensing: bool = True
    
    # Event Consumers
    consumer_prefetch_count: int = 10
    consumer_auto_ack: bool = False
    dlq_enabled: bool = True
    
    # OpenTelemetry
    otel_enabled: bool = True
    otel_endpoint: str = "http://localhost:4318"
    otel_service_name: str = "media-generation-service"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # this .env is shared with the divergent app/config.py Settings class


settings = Settings()
