from typing import Dict, Any, Optional
import structlog
from ..schemas.metadata_schemas import AspectRatio


logger = structlog.get_logger()


class AspectRatioGenerator:
    """Generator for aspect ratios based on platform requirements."""
    
    async def generate(self, platform_requirements: Optional[Dict[str, Any]] = None) -> AspectRatio:
        """Generate aspect ratio from platform requirements."""
        if platform_requirements:
            platform = platform_requirements.get("platform")
            
            if platform == "instagram":
                return AspectRatio.SQUARE
            elif platform == "instagram_story":
                return AspectRatio.PORTRAIT
            elif platform == "facebook":
                return AspectRatio.LANDSCAPE
            elif platform == "twitter":
                return AspectRatio.LANDSCAPE
            elif platform == "linkedin":
                return AspectRatio.LANDSCAPE
            elif platform == "youtube":
                return AspectRatio.LANDSCAPE
            elif platform == "tiktok":
                return AspectRatio.PORTRAIT
            elif platform == "pinterest":
                return AspectRatio.PORTRAIT
        
        # Default to square
        return AspectRatio.SQUARE
