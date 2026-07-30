from typing import Dict, Any, Optional
import structlog
import httpx
from ..utils.config import settings


logger = structlog.get_logger()


class LeonardoAI:
    """Leonardo.AI API integration."""
    
    def __init__(self):
        self.api_key = settings.leonardo_api_key
        self.base_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
    
    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        format: str = "png",
        style: Optional[str] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate image using Leonardo.AI."""
        if not self.api_key:
            return {
                "success": False,
                "error": "Leonardo.AI API key not configured"
            }
        
        try:
            # First, initiate generation
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt,
                        "num_images": 1,
                        "width": int(size.split("x")[0]) if "x" in size else 1024,
                        "height": int(size.split("x")[1]) if "x" in size else 1024,
                        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3"  # Default model
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("sdGenerationJob"):
                    generation_id = data["sdGenerationJob"]["generationId"]
                    
                    # Poll for completion
                    image_url = await self._poll_generation(generation_id)
                    
                    if image_url:
                        return {
                            "success": True,
                            "url": image_url,
                            "format": format,
                            "size": size
                        }
                
                return {
                    "success": False,
                    "error": "Generation failed"
                }
        
        except httpx.HTTPStatusError as e:
            logger.error("leonardo_http_error", status_code=e.response.status_code, error=str(e))
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            logger.error("leonardo_generation_error", error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _poll_generation(self, generation_id: str) -> Optional[str]:
        """Poll for generation completion."""
        import asyncio
        
        for _ in range(30):  # Poll for up to 30 seconds
            await asyncio.sleep(1)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{generation_id}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("generations_by_pk"):
                        generation = data["generations_by_pk"]
                        if generation.get("status") == "COMPLETE":
                            images = generation.get("generated_images", [])
                            if images:
                                return images[0].get("url")
        
        return None
