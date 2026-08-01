"""
Templates router
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from loguru import logger

from app.database import get_db
from app.models.template import Template
from app.utils.serializers import model_to_dict

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

        existing = await db.execute(select(Template).where(Template.name == request.name))
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail=f"Template already exists: {request.name}")

        template = Template(
            name=request.name,
            description=request.description,
            template_type=request.template_type,
            config=request.config,
            default_params=request.default_params,
        )

        db.add(template)
        await db.commit()
        await db.refresh(template)

        logger.info(f"Template created: {template.id}")
        return model_to_dict(template)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{template_id}")
async def get_template(
    template_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get template details"""
    try:
        logger.info(f"Getting template details for {template_id}")

        template = await db.get(Template, uuid.UUID(template_id))
        if template is None:
            raise HTTPException(status_code=404, detail=f"Template not found: {template_id}")

        return model_to_dict(template)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get template: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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

        query = select(Template)
        if template_type is not None:
            query = query.where(Template.template_type == template_type)

        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()

        query = query.order_by(Template.created_at.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        templates = [model_to_dict(t) for t in result.scalars().all()]

        return {
            "total": total,
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
        raise HTTPException(status_code=500, detail=str(e))
