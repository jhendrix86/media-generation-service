from typing import Dict, Any, Optional, List
import structlog
import uuid
from datetime import datetime
from ..schemas.media_schemas import MediaType, MediaState, MediaStatus
from ..schemas.generation_schemas import MediaGenerationRequest, MediaGenerationResult
from ..generators import GeneratorEngine
from ..metadata import MetadataEngine
from .product_media_workflow import ProductMediaWorkflow
from .funnel_media_workflow import FunnelMediaWorkflow
from .content_media_workflow import ContentMediaWorkflow
from .campaign_media_workflow import CampaignMediaWorkflow
from .platform_formatting_workflow import PlatformFormattingWorkflow


logger = structlog.get_logger()


class WorkflowEngine:
    """Main workflow engine coordinating all media workflows."""
    
    def __init__(self):
        self.generator_engine = GeneratorEngine()
        self.metadata_engine = MetadataEngine()
        self._workflows = {
            "product": ProductMediaWorkflow(self.generator_engine, self.metadata_engine),
            "funnel": FunnelMediaWorkflow(self.generator_engine, self.metadata_engine),
            "content": ContentMediaWorkflow(self.generator_engine, self.metadata_engine),
            "campaign": CampaignMediaWorkflow(self.generator_engine, self.metadata_engine),
            "platform_formatting": PlatformFormattingWorkflow(self.generator_engine, self.metadata_engine),
        }
    
    async def execute_workflow(
        self,
        workflow_type: str,
        request: MediaGenerationRequest,
        trace_id: str = None
    ) -> MediaGenerationResult:
        """Execute a media generation workflow."""
        workflow = self._workflows.get(workflow_type)
        
        if not workflow:
            logger.error("unknown_workflow", workflow_type=workflow_type)
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        result = await workflow.execute(request, trace_id)
        
        logger.info(
            "workflow_executed",
            workflow_type=workflow_type,
            success=result.success,
            media_id=result.media_id
        )
        
        return result
    
    def get_workflow(self, workflow_type: str):
        """Get a specific workflow instance."""
        return self._workflows.get(workflow_type)
