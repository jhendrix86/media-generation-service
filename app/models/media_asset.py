"""
Media asset models
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class MediaType(str, enum.Enum):
    """Media type enumeration"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class MediaAsset(Base):
    """Media asset model"""
    __tablename__ = "media_assets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Asset details
    name = Column(String(500), nullable=False)
    media_type = Column(Enum(MediaType), nullable=False)
    
    # File details
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=True)
    
    # Storage
    storage_path = Column(String(500), nullable=False)
    storage_type = Column(String(20), default="local")  # local, s3, gcs
    url = Column(String(500), nullable=True)
    
    # Organization
    tags = Column(JSON, nullable=True)
    category = Column(String(100), nullable=True)
    
    # Usage
    usage_count = Column(Integer, default=0)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MediaAsset {self.name} - {self.media_type}>"
