from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MediaStatus(str, Enum):
    """Media generation status."""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class MediaType(str, Enum):
    """Media types."""
    THUMBNAIL = "thumbnail"
    COVER = "cover"
    BANNER = "banner"
    PRODUCT_IMAGE = "product_image"
    AD_CREATIVE = "ad_creative"
    SOCIAL_GRAPHIC = "social_graphic"
    EMAIL_GRAPHIC = "email_graphic"
    LANDING_VISUAL = "landing_visual"
    VIDEO_THUMBNAIL = "video_thumbnail"


class MediaState(BaseModel):
    """Media state model."""
    media_id: str = Field(..., description="Unique media identifier")
    entity_id: str = Field(..., description="Associated entity ID")
    entity_type: str = Field(..., description="Entity type (product, funnel, content, campaign)")
    media_type: MediaType = Field(..., description="Type of media")
    status: MediaStatus = Field(default=MediaStatus.PENDING, description="Generation status")
    version: str = Field(default="1.0.0", description="Media version")
    url: Optional[str] = Field(None, description="Generated media URL")
    format: Optional[str] = Field(None, description="Media format (png, jpg, webp)")
    size_bytes: Optional[int] = Field(None, description="File size in bytes")
    width: Optional[int] = Field(None, description="Image width")
    height: Optional[int] = Field(None, description="Image height")
    retries: int = Field(default=0, description="Number of retries")
    last_error: Optional[str] = Field(None, description="Last error message")
    api_used: Optional[str] = Field(None, description="API used for generation")
    prompt: Optional[str] = Field(None, description="Generation prompt")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Media metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
