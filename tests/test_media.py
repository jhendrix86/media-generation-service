import pathlib
import uuid


async def test_upload_writes_a_real_file_and_persists_a_row(client):
    files = {"file": ("test.png", b"\x89PNG\r\n\x1a\nfake-bytes", "image/png")}
    r = await client.post("/media/upload", files=files, params={"media_type": "image"})
    assert r.status_code == 200
    media = r.json()
    assert media["file_size"] == len(b"\x89PNG\r\n\x1a\nfake-bytes")
    assert pathlib.Path(media["storage_path"]).exists()


async def test_get_media_roundtrip(client):
    files = {"file": ("test.png", b"data", "image/png")}
    created = await client.post("/media/upload", files=files, params={"media_type": "image"})
    media_id = created.json()["id"]

    r = await client.get(f"/media/{media_id}")
    assert r.status_code == 200
    assert r.json()["id"] == media_id


async def test_get_nonexistent_media_returns_404(client):
    r = await client.get(f"/media/{uuid.uuid4()}")
    assert r.status_code == 404


async def test_list_media_filters_by_type(client):
    files = {"file": ("a.png", b"x", "image/png")}
    await client.post("/media/upload", files=files, params={"media_type": "image"})
    files = {"file": ("b.mp4", b"x", "video/mp4")}
    await client.post("/media/upload", files=files, params={"media_type": "video"})

    r = await client.get("/media/", params={"media_type": "image"})
    assert r.json()["total"] == 1


async def test_delete_media_removes_row_and_file(client):
    files = {"file": ("test.png", b"data", "image/png")}
    created = await client.post("/media/upload", files=files, params={"media_type": "image"})
    media = created.json()
    media_id = media["id"]
    storage_path = pathlib.Path(media["storage_path"])

    r = await client.delete(f"/media/{media_id}")
    assert r.status_code == 200
    assert r.json()["deleted"] is True
    assert not storage_path.exists()

    r = await client.get(f"/media/{media_id}")
    assert r.status_code == 404
