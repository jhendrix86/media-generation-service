"""
audio.py and videos.py have no real TTS/video-generation backend anywhere in
this codebase (confirmed 2026-08-01). These tests lock in the honest
contract: requests are persisted for real, but reported as a real failure
with a clear reason -- never faked as a successful generation.
"""

import uuid


async def test_tts_is_recorded_but_honestly_reported_as_failed(client):
    r = await client.post("/audio/tts", json={"text": "hello world"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "failed"
    assert "No text-to-speech" in body["error"]


async def test_voice_clone_is_recorded_but_honestly_reported_as_failed(client):
    r = await client.post("/audio/clone", params={"voice_id": "v1", "text": "hi"})
    assert r.status_code == 200
    assert r.json()["status"] == "failed"


async def test_audio_enhance_on_unknown_id_returns_404(client):
    r = await client.post("/audio/enhance", params={"audio_id": str(uuid.uuid4())}, json={})
    assert r.status_code == 404


async def test_video_generate_is_recorded_but_honestly_reported_as_failed(client):
    r = await client.post("/videos/generate", json={"prompt": "a rocket launch"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "failed"
    assert "No video-generation" in body["error"]


async def test_video_get_roundtrip(client):
    created = await client.post("/videos/generate", json={"prompt": "a rocket launch"})
    video_id = created.json()["id"]

    r = await client.get(f"/videos/{video_id}")
    assert r.status_code == 200
    assert r.json()["id"] == video_id


async def test_video_edit_on_unknown_id_returns_404(client):
    r = await client.post("/videos/edit", params={"video_id": str(uuid.uuid4())}, json={})
    assert r.status_code == 404
