from typing import Optional
import structlog


logger = structlog.get_logger()


class CaptionGenerator:
    """Generator for image captions."""
    
    async def generate(self, prompt: str, media_type: str) -> str:
        """Generate caption from prompt."""
        # Create engaging caption based on media type
        if media_type == "thumbnail":
            caption = f"A compelling thumbnail featuring {prompt}"
        elif media_type == "cover":
            caption = f"Professional cover design showcasing {prompt}"
        elif media_type == "banner":
            caption = f"Eye-catching banner displaying {prompt}"
        elif media_type == "product_image":
            caption = f"High-quality product image highlighting {prompt}"
        elif media_type == "ad_creative":
            caption = f"Engaging advertisement creative for {prompt}"
        elif media_type == "social_graphic":
            caption = f"Share-worthy social media graphic about {prompt}"
        elif media_type == "email_graphic":
            caption = f"Professional email graphic featuring {prompt}"
        elif media_type == "landing_visual":
            caption = f"Conversion-focused landing page visual for {prompt}"
        elif media_type == "video_thumbnail":
            caption = f"Compelling video thumbnail representing {prompt}"
        else:
            caption = f"Professional image of {prompt}"
        
        return caption
