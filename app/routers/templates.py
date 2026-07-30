"""
Templates router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from loguru import logger

from app.database import get_db

router = APIRouter()


class CreateTemplateRequest(BaseModel):
    """Request to create template"""
    name: str
    description: Optional[str] = None
    template_type: str
    config: dict
    default_params: Optional[dict] = None


@router.post("/create")
async def create_template(
    request: CreateTemplateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a media template"""
    try:
        logger.info(f"Creating template: {request.name}")
        
        # In production, this would save to database
        # For now, return a mock response
        template = {
            "id": "template_123",
            "name": request.name,
            "description": request.description,
            "template_type": request.template_type,
            "config": request.config,
            "default_params": request.default_params,
            "is_active": True,
            "usage_count": 0,
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Template created: {template['id']}")
        return template
        
    except Exception as e:
        logger.error(f"Failed to create template: {e}")
        raise HTTPException(status_code=500, detail(str(e))


@router.get("/{template_id}")
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get template details"""
    try:
        logger.info(f"Getting template details for {template_id}")
        
        # In production, this would query from database
        # For now, return a mock response
        template = {
            "id": template_id,
            "name": "Product Image Template",
            "description": "Template for product showcase images",
            "template_type": "image",
            "config": {
                "style": "professional",
                "lighting": "studio",
                "background": "white"
            },
            "default_params": {
                "size": "1024x1024",
                "format": "png"
            },
            "usage_count": 45
        }
        
        return template
        
    except Exception as e:
        logger.error(f"Failed to get template: {e}")
        raise HTTPException(status_code=500, detail(str(e))


@router.get("/")
async def list_templates(
    template_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List templates"""
    try:
        logger.info("Listing templates")
        
        # In production, this would query from database with filters
        # For now, return a mock response
        templates = [
            {
                "id": "template_001",
                "name": "Product Image Template",
                "template_type": "image",
                "usage_count": 45
            },
            {
                "id": "template_002",
                "name": "Social Media Video Template",
                "template_type": "video",
                "usage_count": 32
            }
        ]
        
        return {
            "total": len(templates),
            "templates": templates,
            "filters": {
                "template_type": template_type
            },
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to list templates: {e}")
        raise HTTPException(status_code=500, detail(str(e))
