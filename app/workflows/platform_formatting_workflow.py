from typing import Dict, Any, Optional
import structlog
import uuid
from datetime import datetime
from ..schemas.media_schemas import MediaType, MediaState, MediaStatus
from ..schemas.generation_schemas import MediaGenerationRequest, MediaGenerationResult
from ..generators import GeneratorEngine
from ..metadata import MetadataEngine


logger = structlog.get_logger()


class PlatformFormattingWorkflow:
    """Workflow for generating platform-specific formatted media."""
    
    def __init__(self, generator_engine: GeneratorEngine, metadata_engine: MetadataEngine):
        self.generator_engine = generator_engine
        self.metadata_engine = metadata_engine
    
    async def execute(
        self,
        request: MediaGenerationRequest,
        trace_id: str = None
    ) -> MediaGenerationResult:
        """Execute platform formatting workflow."""
        media_id = str(uuid.uuid4())
        
        try:
            # Determine target platforms
            platforms = self._determine_platforms(request)
            
            results = []
            for platform in platforms:
                # Adjust requirements for platform
                platform_requirements = self._get_platform_requirements(platform)
                
                # Generate media for platform
                generation_result = await self.generator_engine.generate(
                    media_type=request.media_type,
                    prompt=request.prompt,
                    style=request.style,
                    format=request.format,
                    size=platform_requirements.get("size", request.size),
                    aspect_ratio=platform_requirements.get("aspect_ratio", request.aspect_ratio),
                    brand_colors=request.brand_colors,
                    brand_fonts=request.brand_fonts,
                    platform_requirements={"platform": platform, **platform_requirements},
                    metadata=request.metadata,
                    trace_id=trace_id
                )
                
                if generation_result.get("success"):
                    # Generate metadata
                    metadata = await self.metadata_engine.generate_metadata(
                        prompt=request.prompt,
                        media_type=request.media_type.value,
                        entity_type=request.entity_type,
                        platform_requirements={"platform": platform},
                        brand_colors=request.brand_colors
                    )
                    
                    results.append({
                        "platform": platform,
                        "url": generation_result.get("url"),
                        "metadata": metadata.dict()
                    })
            
            return MediaGenerationResult(
                media_id=media_id,
                success=len(results) > 0,
                url=results[0]["url"] if results else None,
                metadata={"generated_media": results},
                trace_id=trace_id or ""
            )
        
        except Exception as e:
            logger.error("platform_formatting_workflow_error", error=str(e))
            return MediaGenerationResult(
                media_id=media_id,
                success=False,
                error=str(e),
                trace_id=trace_id or ""
            )
    
    def _determine_platforms(self, request: MediaGenerationRequest) -> list[str]:
        """Determine target platforms from request."""
        if request.platform_requirements:
            platform = request.platform_requirements.get("platform")
            if platform:
                return [platform]
        
        # Default platforms based on media type
        if request.media_type == MediaType.SOCIAL_GRAPHIC:
            return ["instagram", "facebook", "twitter", "linkedin"]
        elif request.media_type == MediaType.AD_CREATIVE:
            return ["facebook", "instagram", "google"]
        elif request.media_type == MediaType.EMAIL_GRAPHIC:
            return ["email"]
        else:
            return ["instagram"]
    
    def _get_platform_requirements(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific requirements."""
        requirements = {
            "instagram": {"size": "1080x1080", "aspect_ratio": "1:1"},
            "instagram_story": {"size": "1080x1920", "aspect_ratio": "9:16"},
            "facebook": {"size": "1200x630", "aspect_ratio": "16:9"},
            "twitter": {"size": "1600x900", "aspect_ratio": "16:9"},
            "linkedin": {"size": "1200x627", "aspect_ratio": "16:9"},
            "email": {"size": "600x400", "aspect_ratio": "3:2"},
            "google": {"size": "1200x628", "aspect_ratio": "16:9"}
        }
        
        return requirements.get(platform, {"size": "1024x1024", "aspect_ratio": "1:1"})
