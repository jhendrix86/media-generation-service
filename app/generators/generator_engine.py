from typing import Dict, Any, Optional
import structlog
from ..schemas.media_schemas import MediaType
from .thumbnail_generator import ThumbnailGenerator
from .cover_generator import CoverGenerator
from .banner_generator import BannerGenerator
from .product_image_generator import ProductImageGenerator
from .ad_creative_generator import AdCreativeGenerator
from .social_graphic_generator import SocialGraphicGenerator
from .email_graphic_generator import EmailGraphicGenerator
from .landing_visual_generator import LandingVisualGenerator
from .video_thumbnail_generator import VideoThumbnailGenerator


logger = structlog.get_logger()


class GeneratorEngine:
    """Main generator engine coordinating all media generators."""
    
    def __init__(self):
        self._generators = {
            MediaType.THUMBNAIL: ThumbnailGenerator(),
            MediaType.COVER: CoverGenerator(),
            MediaType.BANNER: BannerGenerator(),
            MediaType.PRODUCT_IMAGE: ProductImageGenerator(),
            MediaType.AD_CREATIVE: AdCreativeGenerator(),
            MediaType.SOCIAL_GRAPHIC: SocialGraphicGenerator(),
            MediaType.EMAIL_GRAPHIC: EmailGraphicGenerator(),
            MediaType.LANDING_VISUAL: LandingVisualGenerator(),
            MediaType.VIDEO_THUMBNAIL: VideoThumbnailGenerator(),
        }
    
    async def generate(
        self,
        media_type: MediaType,
        prompt: str,
        style: Optional[str] = None,
        format: str = "png",
        size: str = "1024x1024",
        aspect_ratio: Optional[str] = None,
        brand_colors: Optional[list] = None,
        brand_fonts: Optional[list] = None,
        platform_requirements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate media using the appropriate generator + API."""
        generator = self._generators.get(media_type)
        
        if not generator:
            logger.error("unknown_media_type", media_type=media_type)
            raise ValueError(f"Unknown media type: {media_type}")
        
        result = await generator.generate(
            prompt=prompt,
            style=style,
            format=format,
            size=size,
            aspect_ratio=aspect_ratio,
            brand_colors=brand_colors,
            brand_fonts=brand_fonts,
            platform_requirements=platform_requirements,
            metadata=metadata,
            trace_id=trace_id
        )
        
        logger.info(
            "media_generated",
            media_type=media_type,
            success=result.get("success", False),
            api_used=result.get("api_used")
        )
        
        return result
    
    def get_generator(self, media_type: MediaType):
        """Get a specific generator instance."""
        return self._generators.get(media_type)
