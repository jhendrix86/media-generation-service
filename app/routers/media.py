"""
Media router
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from loguru import logger

from app.database import get_db

router = APIRouter()


@router.post("/upload")
async def upload_media(
    file: UploadFile,
    media_type: str,
    db: AsyncSession = Depends(get_db)
):
    """Upload media file"""
    try:
        logger.info(f"Uploading media file: {file.filename}")
        
        # In production, this would save to storage and create database record
        # For now, return a mock response
        media = {
            "id": "media_123",
            "name": file.filename,
            "media_type": media_type,
            "file_size": 1024000,
            "storage_path": f"/media/{file.filename}",
            "url": f"https://example.com/{file.filename}",
            "uploaded_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Media uploaded: {media['id']}")
        return media
        
    except Exception as e:
        logger.error(f"Failed to upload media: {e}")
        raise HTTPException(status_code=500, detail(str(e))


@router.get("/{media_id}")
async def get_media(
    media_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get media details"""
    try:
        logger.info(f"Getting media details for {media_id}")
        
        # In production, this would query from database
        # For now, return a mock response
        media = {
            "id": media_id,
            "name": "product-image.png",
            "media_type": "image",
            "file_size": 1024000,
            "url": "https://example.com/product-image.png",
            "tags": ["product", "marketing"],
            "usage_count": 15
        }
        
        return media
        
    except Exception as e:
        logger.error(f"Failed to get media: {e}")
        raise HTTPException(status_code=500, detail(str(e))


@router.get("/")
async def list_media(
    media_type: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List media assets"""
    try:
        logger.info("Listing media assets")
        
        # In production, this would query from database with filters
        # For now, return a mock response
        media = [
            {
                "id": "media_001",
                "name": "product-image.png",
                "media_type": "image",
                "url": "https://example.com/product-image.png",
                "usage_count": 15
            }
        ]
        
        return {
            "total": len(media),
            "media": media,
            "filters": {
                "media_type": media_type,
                "category": category
            },
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to list media: {e}")
        raise HTTPException(status_code=500, detail(str(e))


@router.delete("/{media_id}")
async def delete_media(
    media_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete media asset"""
    try:
        logger.info(f"Deleting media {media_id}")
        
        # In production, this would delete from storage and database
        # For now, return a mock response
        result = {
            "id": media_id,
            "deleted": True,
            "deleted_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Media deleted: {media_id}")
        return result
        
    except Exception as e:
        logger.error(f"Failed to delete media: {e}")
        raise HTTPException(status_code=500, detail(str(e))
