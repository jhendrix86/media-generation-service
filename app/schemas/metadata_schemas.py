from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class AspectRatio(str, Enum):
    """Aspect ratio options."""
    SQUARE = "1:1"
    PORTRAIT = "9:16"
    LANDSCAPE = "16:9"
    WIDE = "21:9"
    INSTAGRAM = "4:5"
    TWITTER = "1.91:1"


class LicensingType(str, Enum):
    """Licensing types."""
    COMMERCIAL = "commercial"
    PERSONAL = "personal"
    EDITORIAL = "editorial"
    ROYALTY_FREE = "royalty_free"
    CREATIVE_COMMONS = "creative_commons"


class MediaMetadata(BaseModel):
    """Media metadata model."""
    alt_text: str = Field(..., description="Alternative text for accessibility")
    caption: str = Field(..., description="Media caption")
    tags: List[str] = Field(default_factory=list, description="Media tags")
    category: str = Field(..., description="Media category")
    aspect_ratio: AspectRatio = Field(default=AspectRatio.SQUARE, description="Aspect ratio")
    platform_requirements: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific requirements")
    licensing: LicensingType = Field(default=LicensingType.COMMERCIAL, description="Licensing type")
    version: str = Field(default="1.0.0", description="Metadata version")
    brand_compliant: bool = Field(default=True, description="Whether media is brand compliant")
    compliance_checked: bool = Field(default=True, description="Whether compliance was checked")
    generated_at: str = Field(..., description="Generation timestamp")
    additional_info: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
