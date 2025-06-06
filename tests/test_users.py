import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_my_info(client: AsyncClient):
    response = await client.get("/api/users/me", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] == "true"
    assert response.json()["user"] == {
        "id": 1,
        "name": "TestUser",
        "followers": [],
        "following": [],
    }


@pytest.mark.asyncio
async def test_get_user_info(client: AsyncClient):
    response = await client.get("/api/users/1", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] == "true"
    assert response.json()["user"] == {
        "id": 1,
        "name": "TestUser",
        "followers": [],
        "following": [],
    }


@pytest.mark.asyncio
async def test_follow_user(client: AsyncClient, db_session):
    await client.post("/api/users/create/friend")
    response = await client.post("/api/users/2/follow", headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json()["result"] is True
    user_info = await client.get("/api/users/me", headers={"api-key": "test"})
    assert user_info.json()["user"] == {
        "id": 1,
        "name": "TestUser",
        "followers": [],
        "following": [{"id": 2, "name": "friend"}],
    }


@pytest.mark.asyncio
async def test_unfollow_user(client: AsyncClient, db_session):
    response = await client.delete("/api/users/2/follow", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    user_info = await client.get("/api/users/me", headers={"api-key": "test"})
    assert user_info.json()["user"] == {
        "id": 1,
        "name": "TestUser",
        "followers": [],
        "following": [],
    }
