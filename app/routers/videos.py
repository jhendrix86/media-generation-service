"""
Video router

Note: unlike images (backed by app/services/api_engine.py + 5 real image
providers), this service has no real video-generation backend implemented
anywhere in the codebase (no Runway/Pika/etc. wrapper exists). These
endpoints persist real Video records so history/listing is truthful, but
report status="failed" rather than faking a successful generation, since
there is no real provider to call. Wiring a real video provider is a
separate feature-build task, not something to invent silently here.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from loguru import logger

from app.database import get_db
from app.models.video import Video, VideoStatus
from app.utils.serializers import model_to_dict

router = APIRouter()

_NO_PROVIDER_MESSAGE = "No video-generation provider is configured for this service yet."


class GenerateVideoRequest(BaseModel):
    """Request to generate video"""
    prompt: str
    duration: int = 30
    resolution: str = "1080p"
    format: str = "mp4"
    style: Optional[str] = None
    model: str = "runway"


@router.post("/generate")
async def generate_video(
    request: GenerateVideoRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate a video"""
    try:
        logger.info(f"Generating video with prompt: {request.prompt[:50]}...")

        video = Video(
            prompt=request.prompt,
            model=request.model,
            duration=request.duration,
            resolution=request.resolution,
            format=request.format,
            style=request.style,
            status=VideoStatus.FAILED,
            extra_metadata={"error": _NO_PROVIDER_MESSAGE},
        )
        db.add(video)
        await db.commit()
        await db.refresh(video)

        logger.warning(f"Video request recorded but not generated (no provider): {video.id}")
        result = model_to_dict(video)
        result["error"] = _NO_PROVIDER_MESSAGE
        return result

    except Exception as e:
        logger.error(f"Failed to record video request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/edit")
async def edit_video(
    video_id: str,
    edits: dict,
    db: AsyncSession = Depends(get_db)
):
    """Edit a video"""
    try:
        logger.info(f"Editing video {video_id}")

        video = await db.get(Video, uuid.UUID(video_id))
        if video is None:
            raise HTTPException(status_code=404, detail=f"Video not found: {video_id}")

        video.extra_metadata = {
            **(video.extra_metadata or {}),
            "requested_edits": edits,
            "error": _NO_PROVIDER_MESSAGE,
        }
        video.status = VideoStatus.FAILED
        await db.commit()
        await db.refresh(video)

        logger.warning(f"Video edit requested but not available (no provider): {video_id}")
        result = model_to_dict(video)
        result["error"] = _NO_PROVIDER_MESSAGE
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to edit video: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}")
async def get_video(
    video_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get video details"""
    try:
        logger.info(f"Getting video details for {video_id}")

        video = await db.get(Video, uuid.UUID(video_id))
        if video is None:
            raise HTTPException(status_code=404, detail=f"Video not found: {video_id}")

        return model_to_dict(video)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get video: {e}")
        raise HTTPException(status_code=500, detail=str(e))
