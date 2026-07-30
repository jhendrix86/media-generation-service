from typing import Dict, Any, Optional
import structlog
from .alt_text_generator import AltTextGenerator
from .caption_generator import CaptionGenerator
from .tag_generator import TagGenerator
from .category_generator import CategoryGenerator
from .aspect_ratio_generator import AspectRatioGenerator
from .licensing_generator import LicensingGenerator
from ..schemas.metadata_schemas import MediaMetadata


logger = structlog.get_logger()


class MetadataEngine:
    """Main metadata engine coordinating all metadata generators."""
    
    def __init__(self):
        self.alt_text_generator = AltTextGenerator()
        self.caption_generator = CaptionGenerator()
        self.tag_generator = TagGenerator()
        self.category_generator = CategoryGenerator()
        self.aspect_ratio_generator = AspectRatioGenerator()
        self.licensing_generator = LicensingGenerator()
    
    async def generate_metadata(
        self,
        prompt: str,
        media_type: str,
        entity_type: str,
        platform_requirements: Optional[Dict[str, Any]] = None,
        brand_colors: Optional[list] = None
    ) -> MediaMetadata:
        """Generate complete metadata for media."""
        # Generate all metadata components
        alt_text = await self.alt_text_generator.generate(prompt, media_type)
        caption = await self.caption_generator.generate(prompt, media_type)
        tags = await self.tag_generator.generate(prompt, media_type, entity_type)
        category = await self.category_generator.generate(media_type, entity_type)
        aspect_ratio = await self.aspect_ratio_generator.generate(platform_requirements)
        licensing = await self.licensing_generator.generate(entity_type)
        
        from datetime import datetime
        
        metadata = MediaMetadata(
            alt_text=alt_text,
            caption=caption,
            tags=tags,
            category=category,
            aspect_ratio=aspect_ratio,
            platform_requirements=platform_requirements or {},
            licensing=licensing,
            generated_at=datetime.utcnow().isoformat()
        )
        
        logger.info("metadata_generated", media_type=media_type, category=category)
        
        return metadata
