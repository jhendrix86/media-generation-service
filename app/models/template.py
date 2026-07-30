"""
Template models
"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base


class Template(Base):
    """Template model"""
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template details
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    template_type = Column(String(50), nullable=False)  # image, video, audio
    
    # Configuration
    config = Column(JSON, nullable=False)
    
    # Default parameters
    default_params = Column(JSON, nullable=True)
    
    # Usage
    usage_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Template {self.name} - {self.template_type}>"
