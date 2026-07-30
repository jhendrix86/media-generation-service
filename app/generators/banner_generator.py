from typing import Dict, Any, Optional, List
import structlog
from ..services.api_engine import APIEngine


logger = structlog.get_logger()


class BannerGenerator:
    """Generator for banner media."""
    
    def __init__(self):
        self.api_engine = APIEngine()
    
    async def generate(
        self,
        prompt: str,
        style: Optional[str] = None,
        format: str = "png",
        size: str = "1920x1080",
        aspect_ratio: Optional[str] = None,
        brand_colors: Optional[List[str]] = None,
        brand_fonts: Optional[List[str]] = None,
        platform_requirements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate a banner image."""
        enhanced_prompt = self._enhance_prompt(prompt, style, brand_colors)
        
        # Use landscape size for banners
        banner_size = aspect_ratio if aspect_ratio == "16:9" else "1920x1080"
        
        result = await self.api_engine.generate_image(
            prompt=enhanced_prompt,
            size=banner_size,
            format=format,
            style=style,
            trace_id=trace_id
        )
        
        return result
    
    def _enhance_prompt(self, prompt: str, style: Optional[str], brand_colors: Optional[List[str]]) -> str:
        """Enhance prompt for banner generation."""
        base_prompt = f"Professional banner image: {prompt}"
        
        if style:
            base_prompt += f", {style} style"
        
        if brand_colors:
            base_prompt += f", color palette: {', '.join(brand_colors)}"
        
        base_prompt += ", wide format, high quality, professional, eye-catching"
        
        return base_prompt
