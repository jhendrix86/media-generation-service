from typing import Optional
import structlog


logger = structlog.get_logger()


class CategoryGenerator:
    """Generator for media categories."""
    
    async def generate(self, media_type: str, entity_type: str) -> str:
        """Generate category from media type and entity type."""
        # Map media types to categories
        media_categories = {
            "thumbnail": "thumbnail",
            "cover": "cover",
            "banner": "banner",
            "product_image": "product",
            "ad_creative": "advertisement",
            "social_graphic": "social_media",
            "email_graphic": "email_marketing",
            "landing_visual": "landing_page",
            "video_thumbnail": "video"
        }
        
        # Map entity types to categories
        entity_categories = {
            "product": "ecommerce",
            "funnel": "marketing",
            "content": "content",
            "campaign": "advertising"
        }
        
        # Combine for more specific category
        media_cat = media_categories.get(media_type, "general")
        entity_cat = entity_categories.get(entity_type, "")
        
        if entity_cat:
            category = f"{entity_cat}_{media_cat}"
        else:
            category = media_cat
        
        return category
