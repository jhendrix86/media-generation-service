from typing import Dict, Any, Optional
import structlog
import httpx
from ..utils.config import settings


logger = structlog.get_logger()


class StabilityAI:
    """Stability AI API integration."""
    
    def __init__(self):
        self.api_key = settings.stability_api_key
        self.base_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        format: str = "png",
        style: Optional[str] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate image using Stability AI."""
        if not self.api_key:
            return {
                "success": False,
                "error": "Stability AI API key not configured"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    json={
                        "text_prompts": [{"text": prompt}],
                        "cfg_scale": 7,
                        "height": int(size.split("x")[1]) if "x" in size else 1024,
                        "width": int(size.split("x")[0]) if "x" in size else 1024,
                        "samples": 1,
                        "steps": 30
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("artifacts"):
                    # Stability AI returns base64 encoded images
                    image_base64 = data["artifacts"][0]["base64"]
                    
                    return {
                        "success": True,
                        "url": f"data:image/png;base64,{image_base64}",
                        "format": format,
                        "size": size,
                        "base64": image_base64
                    }
                else:
                    return {
                        "success": False,
                        "error": "No image data in response"
                    }
        
        except httpx.HTTPStatusError as e:
            logger.error("stability_http_error", status_code=e.response.status_code, error=str(e))
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            logger.error("stability_generation_error", error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
