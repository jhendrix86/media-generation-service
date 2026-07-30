from typing import Dict, Any, Optional, List
import structlog
from ..services.api_engine import APIEngine


logger = structlog.get_logger()


class AdCreativeGenerator:
    """Generator for ad creative media."""
    
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
        """Generate an ad creative."""
        enhanced_prompt = self._enhance_prompt(prompt, style, brand_colors, platform_requirements)
        
        # Determine size based on platform requirements
        ad_size = self._determine_size(platform_requirements, size)
        
        result = await self.api_engine.generate_image(
            prompt=enhanced_prompt,
            size=ad_size,
            format=format,
            style=style,
            trace_id=trace_id
        )
        
        return result
    
    def _enhance_prompt(self, prompt: str, style: Optional[str], brand_colors: Optional[List[str]], platform_requirements: Optional[Dict[str, Any]]) -> str:
        """Enhance prompt for ad creative generation."""
        base_prompt = f"Professional advertisement creative: {prompt}"
        
        if style:
            base_prompt += f", {style} style"
        
        if brand_colors:
            base_prompt += f", color palette: {', '.join(brand_colors)}"
        
        if platform_requirements:
            platform = platform_requirements.get("platform", "general")
            base_prompt += f", optimized for {platform}"
        
        base_prompt += ", high conversion, eye-catching, professional"
        
        return base_prompt
    
    def _determine_size(self, platform_requirements: Optional[Dict[str, Any]], default_size: str) -> str:
        """Determine image size based on platform requirements."""
        if platform_requirements:
            platform = platform_requirements.get("platform")
            if platform == "instagram":
                return "1080x1080"
            elif platform == "facebook":
                return "1200x630"
            elif platform == "twitter":
                return "1600x900"
            elif platform == "linkedin":
                return "1200x627"
        
        return default_size
