import uuid


async def test_generate_image_calls_real_api_engine(client):
    """No API key is configured in tests, so this proves the router really
    calls APIEngine (real error) rather than faking a successful generation."""
    r = await client.post("/images/generate", json={"prompt": "a red bicycle"})
    assert r.status_code == 200
    image = r.json()
    assert image["status"] == "failed"
    assert "OpenAI API key not configured" in image["extra_metadata"]["generation_result"]["error"]


async def test_get_image_roundtrip(client):
    created = await client.post("/images/generate", json={"prompt": "a cat"})
    image_id = created.json()["id"]

    r = await client.get(f"/images/{image_id}")
    assert r.status_code == 200
    assert r.json()["id"] == image_id


async def test_get_nonexistent_image_returns_404(client):
    r = await client.get(f"/images/{uuid.uuid4()}")
    assert r.status_code == 404


async def test_batch_generate_persists_one_row_per_prompt(client):
    r = await client.post("/images/batch", json=["a cat", "a dog", "a bird"])
    assert r.status_code == 200
    assert r.json()["total"] == 3


async def test_list_images_reflects_the_db(client):
    await client.post("/images/generate", json={"prompt": "a"})
    await client.post("/images/generate", json={"prompt": "b"})

    r = await client.get("/images/")
    assert r.json()["total"] == 2


async def test_list_images_filters_by_status(client):
    await client.post("/images/generate", json={"prompt": "a"})

    r = await client.get("/images/", params={"status": "failed"})
    assert r.json()["total"] == 1

    r = await client.get("/images/", params={"status": "completed"})
    assert r.json()["total"] == 0
