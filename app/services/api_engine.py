from typing import Dict, Any, Optional
import structlog
from .openai_images import OpenAIImages
from .stability_ai import StabilityAI
from .leonardo_ai import LeonardoAI
from .replicate_api import ReplicateAPI
from .huggingface_api import HuggingFaceAPI
from ..utils.config import settings


logger = structlog.get_logger()


class APIEngine:
    """Main API engine coordinating all media generation APIs."""
    
    def __init__(self):
        self._apis = {
            "openai": OpenAIImages(),
            "stability": StabilityAI(),
            "leonardo": LeonardoAI(),
            "replicate": ReplicateAPI(),
            "huggingface": HuggingFaceAPI(),
        }
        self.default_api = "openai"
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        format: str = "png",
        style: Optional[str] = None,
        api_preference: Optional[str] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate image using the specified or default API."""
        api_name = api_preference or self.default_api
        api = self._apis.get(api_name)
        
        if not api:
            logger.warning("api_not_found", api=api_name, using_default=self.default_api)
            api = self._apis[self.default_api]
            api_name = self.default_api
        
        try:
            result = await api.generate(
                prompt=prompt,
                size=size,
                format=format,
                style=style,
                trace_id=trace_id
            )
            
            result["api_used"] = api_name
            
            logger.info(
                "image_generated",
                api=api_name,
                success=result.get("success", False)
            )
            
            return result
        
        except Exception as e:
            logger.error("api_generation_failed", api=api_name, error=str(e))
            return {
                "success": False,
                "error": str(e),
                "api_used": api_name
            }
    
    def get_api(self, api_name: str):
        """Get a specific API instance."""
        return self._apis.get(api_name)
