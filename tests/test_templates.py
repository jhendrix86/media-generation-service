import uuid


async def test_create_template(client):
    r = await client.post("/templates/create", json={
        "name": "Product Image Template",
        "template_type": "image",
        "config": {"style": "professional"},
    })
    assert r.status_code == 200
    assert r.json()["is_active"] is True
    assert r.json()["usage_count"] == 0


async def test_duplicate_template_name_rejected(client):
    payload = {"name": "Dup", "template_type": "image", "config": {}}
    r1 = await client.post("/templates/create", json=payload)
    assert r1.status_code == 200

    r2 = await client.post("/templates/create", json=payload)
    assert r2.status_code == 409


async def test_get_template_roundtrip(client):
    created = await client.post("/templates/create", json={
        "name": "A", "template_type": "video", "config": {},
    })
    template_id = created.json()["id"]

    r = await client.get(f"/templates/{template_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "A"


async def test_get_nonexistent_template_returns_404(client):
    r = await client.get(f"/templates/{uuid.uuid4()}")
    assert r.status_code == 404


async def test_list_templates_filters_by_type(client):
    await client.post("/templates/create", json={"name": "A", "template_type": "image", "config": {}})
    await client.post("/templates/create", json={"name": "B", "template_type": "video", "config": {}})

    r = await client.get("/templates/", params={"template_type": "image"})
    assert r.json()["total"] == 1
