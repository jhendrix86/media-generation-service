"""
Media Generation Service - Main Application
AI-powered media generation system for the Autonomous Company OS
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import os

from app.config import settings
from app.database import init_db
from app.routers import images, videos, audio, media, templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Media Generation Service...")
    
    # Initialize database
    await init_db()
    
    logger.info("Media Generation Service started successfully")
    yield
    
    logger.info("Shutting down Media Generation Service...")


# Create FastAPI application
app = FastAPI(
    title="Media Generation Service",
    description="AI-powered media generation system for the Autonomous Company OS",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(images.router, prefix="/images", tags=["images"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(audio.router, prefix="/audio", tags=["audio"])
app.include_router(media.router, prefix="/media", tags=["media"])
app.include_router(templates.router, prefix="/templates", tags=["templates"])


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "Media Generation Service",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-powered media generation system",
        "features": [
            "Image generation",
            "Video generation",
            "Audio processing",
            "Media management",
            "Template system",
            "Batch processing",
            "Quality control",
            "Analytics"
        ],
        "endpoints": {
            "images": "/images",
            "videos": "/videos",
            "audio": "/audio",
            "media": "/media",
            "templates": "/templates"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "media-generation-service",
        "timestamp": logger.info("Health check performed")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8045,
        reload=True
    )
