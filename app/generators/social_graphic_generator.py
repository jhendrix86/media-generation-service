from typing import Dict, Any, Optional, List
import structlog
from ..services.api_engine import APIEngine


logger = structlog.get_logger()


class SocialGraphicGenerator:
    """Generator for social graphic media."""
    
    def __init__(self):
        self.api_engine = APIEngine()
    
    async def generate(
        self,
        prompt: str,
        style: Optional[str] = None,
        format: str = "png",
        size: str = "1080x1080",
        aspect_ratio: Optional[str] = None,
        brand_colors: Optional[List[str]] = None,
        brand_fonts: Optional[List[str]] = None,
        platform_requirements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate a social graphic."""
        enhanced_prompt = self._enhance_prompt(prompt, style, brand_colors, platform_requirements)
        
        # Determine size based on platform
        social_size = self._determine_size(platform_requirements, aspect_ratio, size)
        
        result = await self.api_engine.generate_image(
            prompt=enhanced_prompt,
            size=social_size,
            format=format,
            style=style,
            trace_id=trace_id
        )
        
        return result
    
    def _enhance_prompt(self, prompt: str, style: Optional[str], brand_colors: Optional[List[str]], platform_requirements: Optional[Dict[str, Any]]) -> str:
        """Enhance prompt for social graphic generation."""
        base_prompt = f"Social media graphic: {prompt}"
        
        if style:
            base_prompt += f", {style} style"
        
        if brand_colors:
            base_prompt += f", color palette: {', '.join(brand_colors)}"
        
        if platform_requirements:
            platform = platform_requirements.get("platform", "instagram")
            base_prompt += f", optimized for {platform}"
        
        base_prompt += ", engaging, shareable, high quality"
        
        return base_prompt
    
    def _determine_size(self, platform_requirements: Optional[Dict[str, Any]], aspect_ratio: Optional[str], default_size: str) -> str:
        """Determine image size based on platform and aspect ratio."""
        if aspect_ratio:
            if aspect_ratio == "1:1":
                return "1080x1080"
            elif aspect_ratio == "9:16":
                return "1080x1920"
            elif aspect_ratio == "16:9":
                return "1920x1080"
        
        if platform_requirements:
            platform = platform_requirements.get("platform")
            if platform == "instagram":
                return "1080x1080"
            elif platform == "instagram_story":
                return "1080x1920"
            elif platform == "twitter":
                return "1600x900"
            elif platform == "linkedin":
                return "1200x627"
        
        return default_size
