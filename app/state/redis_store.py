import json
import structlog
from typing import Optional, Dict, Any
from datetime import datetime
import redis.asyncio as aioredis
from ..utils.config import settings
from ..schemas.media_schemas import MediaState


logger = structlog.get_logger()


class RedisMediaStore:
    """Redis-based media state store for real-time tracking."""
    
    def __init__(self):
        self.host = settings.redis_host
        self.port = settings.redis_port
        self.db = settings.redis_db
        self.password = settings.redis_password
        self._client: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """Connect to Redis."""
        self._client = aioredis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True
        )
        
        await self._client.ping()
        logger.info("redis_media_store_connected")
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
        logger.info("redis_media_store_disconnected")
    
    async def save_media_state(self, state: MediaState) -> bool:
        """Save media state to Redis."""
        try:
            key = f"media:{state.media_id}"
            await self._client.setex(
                key,
                3600,  # 1 hour TTL
                json.dumps(state.dict())
            )
            
            # Also index by entity
            entity_key = f"media:entity:{state.entity_type}:{state.entity_id}"
            await self._client.sadd(entity_key, state.media_id)
            await self._client.expire(entity_key, 3600)
            
            logger.info("media_state_saved", media_id=state.media_id)
            return True
        
        except Exception as e:
            logger.error("save_media_state_error", error=str(e))
            return False
    
    async def get_media_state(self, media_id: str) -> Optional[MediaState]:
        """Get media state from Redis."""
        try:
            key = f"media:{media_id}"
            data = await self._client.get(key)
            
            if data:
                return MediaState(**json.loads(data))
            
            return None
        
        except Exception as e:
            logger.error("get_media_state_error", error=str(e))
            return None
    
    async def update_media_status(self, media_id: str, status: str) -> bool:
        """Update media status."""
        try:
            state = await self.get_media_state(media_id)
            if state:
                state.status = status
                state.updated_at = datetime.utcnow()
                return await self.save_media_state(state)
            return False
        
        except Exception as e:
            logger.error("update_media_status_error", error=str(e))
            return False
    
    async def delete_media_state(self, media_id: str) -> bool:
        """Delete media state from Redis."""
        try:
            key = f"media:{media_id}"
            await self._client.delete(key)
            logger.info("media_state_deleted", media_id=media_id)
            return True
        
        except Exception as e:
            logger.error("delete_media_state_error", error=str(e))
            return False
    
    async def get_entity_media(self, entity_type: str, entity_id: str) -> list[str]:
        """Get all media IDs for an entity."""
        try:
            entity_key = f"media:entity:{entity_type}:{entity_id}"
            media_ids = await self._client.smembers(entity_key)
            return list(media_ids)
        
        except Exception as e:
            logger.error("get_entity_media_error", error=str(e))
            return []
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
