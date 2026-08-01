"""
Shared pytest fixtures: boots the real app against an isolated in-memory
SQLite database so every test exercises the real routers and real
SQLAlchemy models end to end. Media uploads go to a temp directory that
gets cleaned up after each test.
"""

import os
import shutil
import tempfile

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite://")
os.environ.setdefault("OPENAI_API_KEY", "")

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import StaticPool

import app.database as database_module

database_module.engine = database_module.create_async_engine(
    "sqlite+aiosqlite://",
    echo=False,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
database_module.AsyncSessionLocal = database_module.async_sessionmaker(
    database_module.engine, class_=database_module.AsyncSession, expire_on_commit=False
)

from app.main import app  # noqa: E402
import app.routers.media as media_router  # noqa: E402


@pytest_asyncio.fixture
async def client():
    """A fresh database schema, an isolated media storage dir, and a live ASGI test client."""
    async with database_module.engine.begin() as conn:
        await conn.run_sync(database_module.Base.metadata.drop_all)

    tmp_storage = tempfile.mkdtemp(prefix="media_gen_test_")
    original_root = media_router.STORAGE_ROOT
    media_router.STORAGE_ROOT = __import__("pathlib").Path(tmp_storage)

    try:
        async with LifespanManager(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
                yield c
    finally:
        media_router.STORAGE_ROOT = original_root
        shutil.rmtree(tmp_storage, ignore_errors=True)
