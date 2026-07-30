from typing import List, Optional
import structlog


logger = structlog.get_logger()


class TagGenerator:
    """Generator for image tags."""
    
    async def generate(self, prompt: str, media_type: str, entity_type: str) -> List[str]:
        """Generate tags from prompt and context."""
        # Extract keywords from prompt
        words = prompt.lower().split()
        
        # Base tags from media type
        base_tags = {
            "thumbnail": ["thumbnail", "preview", "small"],
            "cover": ["cover", "header", "featured"],
            "banner": ["banner", "hero", "wide"],
            "product_image": ["product", "photography", "commercial"],
            "ad_creative": ["advertisement", "marketing", "creative"],
            "social_graphic": ["social", "media", "shareable"],
            "email_graphic": ["email", "marketing", "newsletter"],
            "landing_visual": ["landing", "page", "conversion"],
            "video_thumbnail": ["video", "thumbnail", "preview"]
        }
        
        # Base tags from entity type
        entity_tags = {
            "product": ["product", "ecommerce", "sales"],
            "funnel": ["funnel", "marketing", "conversion"],
            "content": ["content", "media", "creative"],
            "campaign": ["campaign", "marketing", "promotion"]
        }
        
        # Combine tags
        tags = []
        
        # Add media type tags
        if media_type in base_tags:
            tags.extend(base_tags[media_type])
        
        # Add entity type tags
        if entity_type in entity_tags:
            tags.extend(entity_tags[entity_type])
        
        # Add keywords from prompt (filter common words)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        tags.extend(keywords[:5])  # Limit to 5 keywords
        
        # Remove duplicates and limit
        tags = list(set(tags))
        tags = tags[:10]  # Limit to 10 tags
        
        return tags
