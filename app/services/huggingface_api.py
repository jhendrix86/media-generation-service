from typing import Dict, Any, Optional
import structlog
import httpx
from ..utils.config import settings


logger = structlog.get_logger()


class HuggingFaceAPI:
    """HuggingFace Inference API integration."""
    
    def __init__(self):
        self.api_key = settings.huggingface_api_key
        self.base_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        format: str = "png",
        style: Optional[str] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate image using HuggingFace Inference API."""
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "width": int(size.split("x")[0]) if "x" in size else 1024,
                            "height": int(size.split("x")[1]) if "x" in size else 1024
                        }
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                
                # HuggingFace returns raw image bytes
                image_bytes = response.content
                
                # In production, you'd upload this to storage and return a URL
                # For now, return base64
                import base64
                image_base64 = base64.b64encode(image_bytes).decode()
                
                return {
                    "success": True,
                    "url": f"data:image/png;base64,{image_base64}",
                    "format": format,
                    "size": size,
                    "base64": image_base64
                }
        
        except httpx.HTTPStatusError as e:
            logger.error("huggingface_http_error", status_code=e.response.status_code, error=str(e))
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            logger.error("huggingface_generation_error", error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
