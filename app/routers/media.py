"""
Media router
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.database import get_db
from app.models.media_asset import MediaAsset, MediaType
from app.utils.serializers import model_to_dict

router = APIRouter()

STORAGE_ROOT = Path(os.getenv("MEDIA_STORAGE_ROOT", "media_storage"))


@router.post("/upload")
async def upload_media(
    file: UploadFile,
    media_type: MediaType,
    db: AsyncSession = Depends(get_db)
):
    """Upload media file to local storage and record it"""
    try:
        logger.info(f"Uploading media file: {file.filename}")

        STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
        asset_id = uuid.uuid4()
        safe_name = f"{asset_id}_{file.filename}"
        storage_path = STORAGE_ROOT / safe_name

        contents = await file.read()
        storage_path.write_bytes(contents)

        media = MediaAsset(
            id=asset_id,
            name=file.filename,
            media_type=media_type,
            file_name=file.filename,
            file_size=len(contents),
            mime_type=file.content_type,
            storage_path=str(storage_path),
            storage_type="local",
        )

        db.add(media)
        await db.commit()
        await db.refresh(media)

        logger.info(f"Media uploaded: {media.id}")
        return model_to_dict(media)

    except Exception as e:
        logger.error(f"Failed to upload media: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{media_id}")
async def get_media(
    media_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get media details"""
    try:
        logger.info(f"Getting media details for {media_id}")

        media = await db.get(MediaAsset, uuid.UUID(media_id))
        if media is None:
            raise HTTPException(status_code=404, detail=f"Media not found: {media_id}")

        return model_to_dict(media)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get media: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_media(
    media_type: Optional[MediaType] = None,
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List media assets"""
    try:
        logger.info("Listing media assets")

        query = select(MediaAsset)
        if media_type is not None:
            query = query.where(MediaAsset.media_type == media_type)
        if category is not None:
            query = query.where(MediaAsset.category == category)

        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()

        query = query.order_by(MediaAsset.created_at.desc()).limit(limit).offset(offset)
        result = await db.execute(query)
        media = [model_to_dict(m) for m in result.scalars().all()]

        return {
            "total": total,
            "media": media,
            "filters": {
                "media_type": media_type.value if media_type else None,
                "category": category
            },
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }

    except Exception as e:
        logger.error(f"Failed to list media: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{media_id}")
async def delete_media(
    media_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete media asset"""
    try:
        logger.info(f"Deleting media {media_id}")

        media = await db.get(MediaAsset, uuid.UUID(media_id))
        if media is None:
            raise HTTPException(status_code=404, detail=f"Media not found: {media_id}")

        storage_path = Path(media.storage_path) if media.storage_path else None

        await db.delete(media)
        await db.commit()

        if storage_path and storage_path.exists():
            storage_path.unlink()

        logger.info(f"Media deleted: {media_id}")
        return {
            "id": media_id,
            "deleted": True,
            "deleted_at": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete media: {e}")
        raise HTTPException(status_code=500, detail=str(e))
