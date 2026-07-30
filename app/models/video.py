"""
Video models
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class VideoStatus(str, enum.Enum):
    """Video status enumeration"""
    GENERATING = "generating"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Video(Base):
    """Video model"""
    __tablename__ = "videos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Generation details
    prompt = Column(String(2000), nullable=False)
    model = Column(String(50), nullable=False)
    
    # Video properties
    duration = Column(Integer, nullable=False)  # seconds
    resolution = Column(String(20), nullable=False)  # 1080p, 4k
    format = Column(String(10), nullable=False)  # mp4, mov
    style = Column(String(50), nullable=True)
    
    # Status
    status = Column(Enum(VideoStatus), default=VideoStatus.GENERATING)
    
    # Output
    url = Column(String(500), nullable=True)
    storage_path = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    
    # Quality
    quality_score = Column(Integer, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Video {self.id} - {self.status}>"
