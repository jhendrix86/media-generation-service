"""
Audio models
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from app.database import Base


class AudioStatus(str, enum.Enum):
    """Audio status enumeration"""
    GENERATING = "generating"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Audio(Base):
    """Audio model"""
    __tablename__ = "audio"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Generation details
    text = Column(Text, nullable=False)
    audio_type = Column(String(50), nullable=False)  # tts, clone, enhance
    model = Column(String(50), nullable=False)
    
    # Audio properties
    voice = Column(String(50), nullable=True)
    language = Column(String(10), nullable=False)  # en-US, es-ES
    format = Column(String(10), nullable=False)  # mp3, wav
    duration = Column(Integer, nullable=True)  # seconds
    
    # Status
    status = Column(Enum(AudioStatus), default=AudioStatus.GENERATING)
    
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
        return f"<Audio {self.id} - {self.audio_type} - {self.status}>"
