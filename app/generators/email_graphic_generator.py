from typing import Dict, Any, Optional, List
import structlog
from ..services.api_engine import APIEngine


logger = structlog.get_logger()


class EmailGraphicGenerator:
    """Generator for email graphic media."""
    
    def __init__(self):
        self.api_engine = APIEngine()
    
    async def generate(
        self,
        prompt: str,
        style: Optional[str] = None,
        format: str = "png",
        size: str = "600x400",
        aspect_ratio: Optional[str] = None,
        brand_colors: Optional[List[str]] = None,
        brand_fonts: Optional[List[str]] = None,
        platform_requirements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate an email graphic."""
        enhanced_prompt = self._enhance_prompt(prompt, style, brand_colors)
        
        # Use email-optimized size
        email_size = size if size else "600x400"
        
        result = await self.api_engine.generate_image(
            prompt=enhanced_prompt,
            size=email_size,
            format=format,
            style=style,
            trace_id=trace_id
        )
        
        return result
    
    def _enhance_prompt(self, prompt: str, style: Optional[str], brand_colors: Optional[List[str]]) -> str:
        """Enhance prompt for email graphic generation."""
        base_prompt = f"Email marketing graphic: {prompt}"
        
        if style:
            base_prompt += f", {style} style"
        
        if brand_colors:
            base_prompt += f", color palette: {', '.join(brand_colors)}"
        
        base_prompt += ", email optimized, high quality, professional, clean"
        
        return base_prompt
