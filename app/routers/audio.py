"""
Audio router

Note: unlike images (backed by app/services/api_engine.py + 5 real image
providers), this service has no real text-to-speech, voice-cloning, or audio
enhancement backend implemented anywhere in the codebase. These endpoints
persist real Audio records so history/listing is truthful, but report
status="failed" rather than faking a successful generation, since there is
no real provider to call. Wiring a real TTS provider (e.g. ElevenLabs) is
a separate feature-build task, not something to invent silently here.
"""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from loguru import logger

from app.database import get_db
from app.models.audio import Audio, AudioStatus
from app.utils.serializers import model_to_dict

router = APIRouter()

_NO_PROVIDER_MESSAGE = "No text-to-speech/voice provider is configured for this service yet."


class TTSRequest(BaseModel):
    """Request for text-to-speech"""
    text: str
    voice: str = "natural"
    language: str = "en-US"
    format: str = "mp3"


@router.post("/tts")
async def text_to_speech(
    request: TTSRequest,
    db: AsyncSession = Depends(get_db)
):
    """Convert text to speech"""
    try:
        logger.info(f"Converting text to speech: {request.text[:50]}...")

        audio = Audio(
            text=request.text,
            audio_type="tts",
            model="none",
            voice=request.voice,
            language=request.language,
            format=request.format,
            status=AudioStatus.FAILED,
            extra_metadata={"error": _NO_PROVIDER_MESSAGE},
        )
        db.add(audio)
        await db.commit()
        await db.refresh(audio)

        logger.warning(f"Audio request recorded but not generated (no provider): {audio.id}")
        result = model_to_dict(audio)
        result["error"] = _NO_PROVIDER_MESSAGE
        return result

    except Exception as e:
        logger.error(f"Failed to record audio request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clone")
async def clone_voice(
    voice_id: str,
    text: str,
    db: AsyncSession = Depends(get_db)
):
    """Clone voice and generate audio"""
    try:
        logger.info(f"Cloning voice {voice_id}")

        audio = Audio(
            text=text,
            audio_type="clone",
            model="none",
            voice=voice_id,
            language="en-US",
            format="mp3",
            status=AudioStatus.FAILED,
            extra_metadata={"voice_id": voice_id, "error": _NO_PROVIDER_MESSAGE},
        )
        db.add(audio)
        await db.commit()
        await db.refresh(audio)

        logger.warning(f"Voice clone request recorded but not generated (no provider): {audio.id}")
        result = model_to_dict(audio)
        result["error"] = _NO_PROVIDER_MESSAGE
        return result

    except Exception as e:
        logger.error(f"Failed to record voice clone request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enhance")
async def enhance_audio(
    audio_id: str,
    enhancements: dict,
    db: AsyncSession = Depends(get_db)
):
    """Enhance audio quality"""
    try:
        logger.info(f"Enhancing audio {audio_id}")

        audio = await db.get(Audio, uuid.UUID(audio_id))
        if audio is None:
            raise HTTPException(status_code=404, detail=f"Audio not found: {audio_id}")

        audio.extra_metadata = {
            **(audio.extra_metadata or {}),
            "requested_enhancements": enhancements,
            "error": _NO_PROVIDER_MESSAGE,
        }
        audio.status = AudioStatus.FAILED
        await db.commit()
        await db.refresh(audio)

        logger.warning(f"Audio enhancement requested but not available (no provider): {audio_id}")
        result = model_to_dict(audio)
        result["error"] = _NO_PROVIDER_MESSAGE
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to enhance audio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
