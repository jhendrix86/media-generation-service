from typing import Optional
import structlog


logger = structlog.get_logger()


class AltTextGenerator:
    """Generator for alt text (accessibility)."""
    
    async def generate(self, prompt: str, media_type: str) -> str:
        """Generate alt text from prompt."""
        # Extract key elements from prompt
        words = prompt.split()
        
        # Create descriptive alt text
        if media_type == "thumbnail":
            alt_text = f"Thumbnail image showing {prompt}"
        elif media_type == "cover":
            alt_text = f"Cover image featuring {prompt}"
        elif media_type == "banner":
            alt_text = f"Banner displaying {prompt}"
        elif media_type == "product_image":
            alt_text = f"Product photograph of {prompt}"
        elif media_type == "ad_creative":
            alt_text = f"Advertisement creative depicting {prompt}"
        elif media_type == "social_graphic":
            alt_text = f"Social media graphic with {prompt}"
        elif media_type == "email_graphic":
            alt_text = f"Email marketing graphic showing {prompt}"
        elif media_type == "landing_visual":
            alt_text = f"Landing page visual featuring {prompt}"
        elif media_type == "video_thumbnail":
            alt_text = f"Video thumbnail for {prompt}"
        else:
            alt_text = f"Image of {prompt}"
        
        # Ensure alt text is concise but descriptive
        if len(alt_text) > 125:
            alt_text = alt_text[:122] + "..."
        
        return alt_text
