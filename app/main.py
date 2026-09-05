"""
Media Generation Service - Main Application
AI-powered media generation system for the Autonomous Company OS
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import os

from datetime import datetime

from app.config import settings
from app.database import init_db
from app.services.api_engine import APIEngine
from app.routers import images, videos, audio, media, templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting Media Generation Service...")

    # Initialize database
    await init_db()

    # Single shared API engine instance for the app's lifetime
    app.state.api_engine = APIEngine()

    logger.info("Media Generation Service started successfully")
    yield

    logger.info("Shutting down Media Generation Service...")


# Create FastAPI application
app = FastAPI(
    title="Media Generation Service",
    description="AI-powered media generation system for the Autonomous Company OS",
    version="1.0.0",
    lifespan=lifespan,
    # SECURITY_REVIEW.md finding: /docs, /redoc, /openapi.json were reachable
    # unauthenticated on every engine (dynamic-pentest-confirmed) - a full
    # interactive API browser plus every unauth write path. Disabled unless
    # DEBUG=true.
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Configure CORS
def _cors_allowed_origins() -> list:
    # SECURITY_REVIEW.md #1 - no wildcard with credentials. Set
    # ALLOWED_ORIGINS (comma-separated) when a browser client exists.
    import os
    return [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allowed_origins(),
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
    logger.info("Health check performed")
    return {
        "status": "healthy",
        "service": "media-generation-service",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8045,
        reload=True
    )
