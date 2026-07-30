import structlog
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncpg
from ..utils.config import settings
from ..schemas.media_schemas import MediaState, MediaStatus


logger = structlog.get_logger()


class PostgresMediaStore:
    """PostgreSQL-based media state store for persistent storage and versioning."""
    
    def __init__(self):
        self.host = settings.postgres_host
        self.port = settings.postgres_port
        self.user = settings.postgres_user
        self.password = settings.postgres_password
        self.database = settings.postgres_database
        self._pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Connect to PostgreSQL and create connection pool."""
        self._pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            min_size=5,
            max_size=20
        )
        
        await self._init_schema()
        logger.info("postgres_media_store_connected")
    
    async def disconnect(self):
        """Disconnect from PostgreSQL."""
        if self._pool:
            await self._pool.close()
        logger.info("postgres_media_store_disconnected")
    
    async def _init_schema(self):
        """Initialize database schema."""
        async with self._pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS media_state (
                    media_id VARCHAR(255) PRIMARY KEY,
                    entity_id VARCHAR(255) NOT NULL,
                    entity_type VARCHAR(100) NOT NULL,
                    media_type VARCHAR(100) NOT NULL,
                    status VARCHAR(50) NOT NULL,
                    version VARCHAR(50) DEFAULT '1.0.0',
                    url TEXT,
                    format VARCHAR(20),
                    size_bytes BIGINT,
                    width INTEGER,
                    height INTEGER,
                    retries INTEGER DEFAULT 0,
                    last_error TEXT,
                    api_used VARCHAR(100),
                    prompt TEXT,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW(),
                    completed_at TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_media_entity ON media_state(entity_type, entity_id);
                CREATE INDEX IF NOT EXISTS idx_media_status ON media_state(status);
                CREATE INDEX IF NOT EXISTS idx_media_type ON media_state(media_type);
                
                CREATE TABLE IF NOT EXISTS media_history (
                    id SERIAL PRIMARY KEY,
                    media_id VARCHAR(255) NOT NULL,
                    previous_state JSONB,
                    new_state JSONB,
                    changed_at TIMESTAMP DEFAULT NOW(),
                    change_reason VARCHAR(255)
                );
                
                CREATE INDEX IF NOT EXISTS idx_media_history_id ON media_history(media_id);
            """)
    
    async def save_media_state(self, state: MediaState) -> bool:
        """Save media state to PostgreSQL."""
        try:
            async with self._pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO media_state (
                        media_id, entity_id, entity_type, media_type, status,
                        version, url, format, size_bytes, width, height,
                        retries, last_error, api_used, prompt, created_at, updated_at, completed_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
                    ON CONFLICT (media_id) DO UPDATE SET
                        status = EXCLUDED.status,
                        url = EXCLUDED.url,
                        format = EXCLUDED.format,
                        size_bytes = EXCLUDED.size_bytes,
                        width = EXCLUDED.width,
                        height = EXCLUDED.height,
                        retries = EXCLUDED.retries,
                        last_error = EXCLUDED.last_error,
                        api_used = EXCLUDED.api_used,
                        updated_at = NOW(),
                        completed_at = EXCLUDED.completed_at
                """,
                    state.media_id, state.entity_id, state.entity_type, state.media_type.value,
                    state.status.value, state.version, state.url, state.format,
                    state.size_bytes, state.width, state.height, state.retries,
                    state.last_error, state.api_used, state.prompt, state.created_at,
                    state.updated_at, state.completed_at
                )
            
            logger.info("media_state_saved_postgres", media_id=state.media_id)
            return True
        
        except Exception as e:
            logger.error("save_media_state_postgres_error", error=str(e))
            return False
    
    async def get_media_state(self, media_id: str) -> Optional[MediaState]:
        """Get media state from PostgreSQL."""
        try:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM media_state WHERE media_id = $1",
                    media_id
                )
                
                if row:
                    return MediaState(
                        media_id=row["media_id"],
                        entity_id=row["entity_id"],
                        entity_type=row["entity_type"],
                        media_type=row["media_type"],
                        status=row["status"],
                        version=row["version"],
                        url=row["url"],
                        format=row["format"],
                        size_bytes=row["size_bytes"],
                        width=row["width"],
                        height=row["height"],
                        retries=row["retries"],
                        last_error=row["last_error"],
                        api_used=row["api_used"],
                        prompt=row["prompt"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                        completed_at=row["completed_at"]
                    )
                
                return None
        
        except Exception as e:
            logger.error("get_media_state_postgres_error", error=str(e))
            return None
    
    async def get_entity_media_history(self, entity_type: str, entity_id: str) -> List[MediaState]:
        """Get all media for an entity."""
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT * FROM media_state WHERE entity_type = $1 AND entity_id = $2 ORDER BY created_at DESC",
                    entity_type, entity_id
                )
                
                return [
                    MediaState(
                        media_id=row["media_id"],
                        entity_id=row["entity_id"],
                        entity_type=row["entity_type"],
                        media_type=row["media_type"],
                        status=row["status"],
                        version=row["version"],
                        url=row["url"],
                        format=row["format"],
                        size_bytes=row["size_bytes"],
                        width=row["width"],
                        height=row["height"],
                        retries=row["retries"],
                        last_error=row["last_error"],
                        api_used=row["api_used"],
                        prompt=row["prompt"],
                        created_at=row["created_at"],
                        updated_at=row["updated_at"],
                        completed_at=row["completed_at"]
                    )
                    for row in rows
                ]
        
        except Exception as e:
            logger.error("get_entity_media_history_error", error=str(e))
            return []
    
    async def save_media_history(self, media_id: str, previous_state: Dict, new_state: Dict, reason: str):
        """Save media state change to history."""
        try:
            async with self._pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO media_history (media_id, previous_state, new_state, change_reason)
                    VALUES ($1, $2, $3, $4)
                """, media_id, previous_state, new_state, reason)
        
        except Exception as e:
            logger.error("save_media_history_error", error=str(e))
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
