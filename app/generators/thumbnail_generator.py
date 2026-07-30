from typing import Dict, Any, Optional, List
import structlog
from ..services.api_engine import APIEngine


logger = structlog.get_logger()


class ThumbnailGenerator:
    """Generator for thumbnail media."""
    
    def __init__(self):
        self.api_engine = APIEngine()
    
    async def generate(
        self,
        prompt: str,
        style: Optional[str] = None,
        format: str = "png",
        size: str = "512x512",
        aspect_ratio: Optional[str] = None,
        brand_colors: Optional[List[str]] = None,
        brand_fonts: Optional[List[str]] = None,
        platform_requirements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate a thumbnail."""
        # Enhance prompt for thumbnail generation
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        # Use appropriate size for thumbnails
        thumbnail_size = size if size else "512x512"
        
        # Generate using API engine
        result = await self.api_engine.generate_image(
            prompt=enhanced_prompt,
            size=thumbnail_size,
            format=format,
            style=style,
            trace_id=trace_id
        )
        
        return result
    
    def _enhance_prompt(self, prompt: str, style: Optional[str]) -> str:
        """Enhance prompt for thumbnail generation."""
        base_prompt = f"Professional thumbnail image: {prompt}"
        
        if style:
            base_prompt += f", {style} style"
        
        base_prompt += ", clean composition, eye-catching, high quality"
        
        return base_prompt
