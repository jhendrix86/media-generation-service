from typing import Dict, Any, Optional
import structlog
import httpx
from ..utils.config import settings


logger = structlog.get_logger()


class ReplicateAPI:
    """Replicate API integration."""
    
    def __init__(self):
        self.api_key = settings.replicate_api_key
        self.base_url = "https://api.replicate.com/v1/predictions"
    
    async def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        format: str = "png",
        style: Optional[str] = None,
        trace_id: str = None
    ) -> Dict[str, Any]:
        """Generate image using Replicate."""
        if not self.api_key:
            return {
                "success": False,
                "error": "Replicate API key not configured"
            }
        
        try:
            # Start prediction
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "version": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                        "input": {
                            "prompt": prompt,
                            "width": int(size.split("x")[0]) if "x" in size else 1024,
                            "height": int(size.split("x")[1]) if "x" in size else 1024
                        }
                    },
                    timeout=60.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                if data.get("urls") and data["urls"].get("get"):
                    # Poll for completion
                    image_url = await self._poll_prediction(data["urls"]["get"])
                    
                    if image_url:
                        return {
                            "success": True,
                            "url": image_url,
                            "format": format,
                            "size": size
                        }
                
                return {
                    "success": False,
                    "error": "Prediction failed"
                }
        
        except httpx.HTTPStatusError as e:
            logger.error("replicate_http_error", status_code=e.response.status_code, error=str(e))
            return {
                "success": False,
                "error": f"HTTP error: {e.response.status_code}"
            }
        except Exception as e:
            logger.error("replicate_generation_error", error=str(e))
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _poll_prediction(self, get_url: str) -> Optional[str]:
        """Poll for prediction completion."""
        import asyncio
        
        for _ in range(60):  # Poll for up to 60 seconds
            await asyncio.sleep(1)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    get_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    if status == "succeeded":
                        output = data.get("output")
                        if output and isinstance(output, list):
                            return output[0]
                    elif status == "failed":
                        return None
        
        return None
