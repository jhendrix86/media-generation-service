from typing import Dict, Any, Optional, List
import structlog
from ..services.api_engine import APIEngine


logger = structlog.get_logger()


class ProductImageGenerator:
    """Generator for product image media."""
    
    def __init__(self):
        self.api_engine = APIEngine()
    
    async def generate(
        self,
        prompt: str,
        style: Optional[str] = None,
        format: str = "png",
        size: str = "1024x1024",
        aspect_ratio: Optional[str] = None,
        brand_colors: Optional[List[str]] = None,
        brand_fonts: Optional[List[str]] = None,
        platform_requirements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate a product image."""
        enhanced_prompt = self._enhance_prompt(prompt, style, brand_colors)
        
        result = await self.api_engine.generate_image(
            prompt=enhanced_prompt,
            size=size,
            format=format,
            style=style,
            trace_id=trace_id
        )
        
        return result
    
    def _enhance_prompt(self, prompt: str, style: Optional[str], brand_colors: Optional[List[str]]) -> str:
        """Enhance prompt for product image generation."""
        base_prompt = f"Professional product photography: {prompt}"
        
        if style:
            base_prompt += f", {style} style"
        
        if brand_colors:
            base_prompt += f", color palette: {', '.join(brand_colors)}"
        
        base_prompt += ", high quality, professional lighting, clean background"
        
        return base_prompt
