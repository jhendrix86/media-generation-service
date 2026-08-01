"""
Image router
"""

import uuid
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from loguru import logger

from app.database import get_db
from app.models.image import Image, ImageStatus
from app.services.api_engine import APIEngine
from app.utils.serializers import model_to_dict

router = APIRouter()


def get_api_engine(request: Request) -> APIEngine:
    return request.app.state.api_engine


class GenerateImageRequest(BaseModel):
    """Request to generate image"""
    prompt: str
    negative_prompt: Optional[str] = None
    size: str = "1024x1024"
    format: str = "png"
    style: Optional[str] = None
    model: str = "dall-e-3"
    api_preference: Optional[str] = None


async def _generate_and_persist(request: GenerateImageRequest, api_engine: APIEngine, db: AsyncSession) -> Image:
    result = await api_engine.generate_image(
        prompt=request.prompt,
        size=request.size,
        format=request.format,
        style=request.style,
        api_preference=request.api_preference,
    )

    image = Image(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        model=request.model,
        size=request.size,
        format=request.format,
        style=request.style,
        status=ImageStatus.COMPLETED if result.get("success") else ImageStatus.FAILED,
        url=result.get("url"),
        extra_metadata={"generation_result": result},
        completed_at=datetime.utcnow(),
    )
    db.add(image)
    return image


@router.post("/generate")
async def generate_image(
    request: GenerateImageRequest,
    db: AsyncSession = Depends(get_db),
    api_engine: APIEngine = Depends(get_api_engine)
):
    """Generate an image"""
    try:
        logger.info(f"Generating image with prompt: {request.prompt[:50]}...")

        image = await _generate_and_persist(request, api_engine, db)
        await db.commit()
        await db.refresh(image)

        logger.info(f"Image generated: {image.id}")
        return model_to_dict(image)

    except Exception as e:
        logger.error(f"Failed to generate image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def batch_generate_images(
    prompts: List[str],
    size: str = "1024x1024",
    format: str = "png",
    db: AsyncSession = Depends(get_db),
    api_engine: APIEngine = Depends(get_api_engine)
):
    """Batch generate images"""
    try:
        logger.info(f"Batch generating {len(prompts)} images")

        images = []
        for prompt in prompts:
            req = GenerateImageRequest(prompt=prompt, size=size, format=format)
            image = await _generate_and_persist(req, api_engine, db)
            images.append(image)

        await db.commit()
        for image in images:
            await db.refresh(image)

        logger.info(f"Batch images generated: {len(images)}")
        return {
            "total": len(images),
            "images": [model_to_dict(i) for i in images]
        }

    except Exception as e:
        logger.error(f"Failed to batch generate images: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}")
async def get_image(
    image_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get image details"""
    try:
        logger.info(f"Getting image details for {image_id}")

        image = await db.get(Image, uuid.UUID(image_id))
        if image is None:
            raise HTTPException(status_code=404, detail=f"Image not found: {image_id}")

        return model_to_dict(image)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_images(
    status: Optional[ImageStatus] = None,
    model: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List images"""
    try:
        logger.info("Listing images")

        query = select(Image)
        if status is not None:
            query = query.where(Image.status == status)
        if model is not None:
            query = query.where(Image.model == model)

        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()

        query = query.order_by(Image.created_at.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        images = [model_to_dict(i) for i in result.scalars().all()]

        return {
            "total": total,
            "images": images,
            "filters": {
                "status": status.value if status else None,
                "model": model
            },
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }

    except Exception as e:
        logger.error(f"Failed to list images: {e}")
        raise HTTPException(status_code=500, detail=str(e))
