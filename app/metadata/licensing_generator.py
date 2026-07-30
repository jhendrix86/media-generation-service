from typing import Optional
import structlog
from ..schemas.metadata_schemas import LicensingType


logger = structlog.get_logger()


class LicensingGenerator:
    """Generator for licensing information."""
    
    async def generate(self, entity_type: str) -> LicensingType:
        """Generate licensing type based on entity type."""
        # Determine appropriate licensing based on entity type
        if entity_type == "product":
            # Product images typically need commercial licensing
            return LicensingType.COMMERCIAL
        elif entity_type == "funnel":
            # Funnel media is for marketing/commercial use
            return LicensingType.COMMERCIAL
        elif entity_type == "content":
            # Content could be editorial or commercial
            return LicensingType.ROYALTY_FREE
        elif entity_type == "campaign":
            # Campaign media is commercial
            return LicensingType.COMMERCIAL
        else:
            # Default to commercial
            return LicensingType.COMMERCIAL
