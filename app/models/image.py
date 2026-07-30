"""
Image models
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class ImageStatus(str, enum.Enum):
    """Image status enumeration"""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    PROCESSING = "processing"


class Image(Base):
    """Image model"""
    __tablename__ = "images"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Generation details
    prompt = Column(String(2000), nullable=False)
    negative_prompt = Column(String(2000), nullable=True)
    model = Column(String(50), nullable=False)  # dall-e-3, stable-diffusion
    
    # Image properties
    size = Column(String(20), nullable=False)  # 1024x1024
    format = Column(String(10), nullable=False)  # png, jpg, webp
    style = Column(String(50), nullable=True)
    
    # Status
    status = Column(Enum(ImageStatus), default=ImageStatus.GENERATING)
    
    # Output
    url = Column(String(500), nullable=True)
    storage_path = Column(String(500), nullable=True)
    
    # Quality
    quality_score = Column(Integer, nullable=True)
    
    # Metadata
    extra_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Image {self.id} - {self.status}>"
