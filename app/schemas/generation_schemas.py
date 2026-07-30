from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from .media_schemas import MediaType


class MediaGenerationRequest(BaseModel):
    """Request to generate media."""
    entity_id: str = Field(..., description="Associated entity ID")
    entity_type: str = Field(..., description="Entity type (product, funnel, content, campaign)")
    media_type: MediaType = Field(..., description="Type of media to generate")
    prompt: str = Field(..., description="Generation prompt")
    style: Optional[str] = Field(None, description="Style preference")
    format: str = Field(default="png", description="Output format (png, jpg, webp)")
    size: str = Field(default="1024x1024", description="Image size (e.g., 1024x1024)")
    aspect_ratio: Optional[str] = Field(None, description="Aspect ratio")
    api_preference: Optional[str] = Field(None, description="Preferred API (openai, stability, leonardo, replicate, huggingface)")
    brand_colors: Optional[List[str]] = Field(None, description="Brand colors to use")
    brand_fonts: Optional[List[str]] = Field(None, description="Brand fonts to use")
    platform_requirements: Optional[Dict[str, Any]] = Field(None, description="Platform-specific requirements")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    trace_id: Optional[str] = Field(None, description="Trace ID")
    correlation_id: Optional[str] = Field(None, description="Correlation ID")


class MediaGenerationResult(BaseModel):
    """Result of media generation."""
    media_id: str
    success: bool
    url: Optional[str] = None
    format: Optional[str] = None
    size_bytes: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    api_used: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    trace_id: str
