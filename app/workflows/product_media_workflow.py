from typing import Dict, Any, Optional
import structlog
import uuid
from datetime import datetime
from ..schemas.media_schemas import MediaType, MediaState, MediaStatus
from ..schemas.generation_schemas import MediaGenerationRequest, MediaGenerationResult
from ..generators import GeneratorEngine
from ..metadata import MetadataEngine


logger = structlog.get_logger()


class ProductMediaWorkflow:
    """Workflow for generating product-related media."""
    
    def __init__(self, generator_engine: GeneratorEngine, metadata_engine: MetadataEngine):
        self.generator_engine = generator_engine
        self.metadata_engine = metadata_engine
    
    async def execute(
        self,
        request: MediaGenerationRequest,
        trace_id: str = None
    ) -> MediaGenerationResult:
        """Execute product media workflow."""
        media_id = str(uuid.uuid4())
        
        try:
            # Determine media types to generate for product
            media_types = self._determine_media_types(request)
            
            results = []
            for media_type in media_types:
                # Generate media
                generation_result = await self.generator_engine.generate(
                    media_type=media_type,
                    prompt=request.prompt,
                    style=request.style,
                    format=request.format,
                    size=request.size,
                    aspect_ratio=request.aspect_ratio,
                    brand_colors=request.brand_colors,
                    brand_fonts=request.brand_fonts,
                    platform_requirements=request.platform_requirements,
                    metadata=request.metadata,
                    trace_id=trace_id
                )
                
                if generation_result.get("success"):
                    # Generate metadata
                    metadata = await self.metadata_engine.generate_metadata(
                        prompt=request.prompt,
                        media_type=media_type.value,
                        entity_type=request.entity_type,
                        platform_requirements=request.platform_requirements,
                        brand_colors=request.brand_colors
                    )
                    
                    results.append({
                        "media_type": media_type.value,
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
            logger.error("product_workflow_error", error=str(e))
            return MediaGenerationResult(
                media_id=media_id,
                success=False,
                error=str(e),
                trace_id=trace_id or ""
            )
    
    def _determine_media_types(self, request: MediaGenerationRequest) -> list[MediaType]:
        """Determine which media types to generate for a product."""
        # For products, typically generate product images and thumbnails
        media_types = [MediaType.PRODUCT_IMAGE]
        
        # Add thumbnail if not specified
        if request.media_type == MediaType.PRODUCT_IMAGE:
            media_types.append(MediaType.THUMBNAIL)
        
        return media_types
