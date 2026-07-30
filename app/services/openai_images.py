from typing import Dict, Any, Optional
import structlog
import httpx
from ..utils.config import settings


logger = structlog.get_logger()


class OpenAIImages:
    """OpenAI Images API integration."""
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        self.base_url = "https://api.openai.com/v1/images/generations"
    
    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        format: str = "png",
        style: Optional[str] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate image using OpenAI DALL-E."""
        if not self.api_key:
            return {
                "success": False,
                "error": "OpenAI API key not configured"
            }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt,
                        "n": 1,
                        "size": size,
                        "response_format": "url"
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("data"):
                    image_url = data["data"][0]["url"]
                    
                    return {
                        "success": True,
                        "url": image_url,
                        "format": format,
                        "size": size
                    }
                else:
                    return {
                        "success": False,
                        "error": "No image data in response"
                    }
        
        except httpx.HTTPStatusError as e:
            logger.error("openai_http_error", status_code=e.response.status_code, error=str(e))
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            logger.error("openai_generation_error", error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
