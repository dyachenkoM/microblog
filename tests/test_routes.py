import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_tweets_empty(client: AsyncClient):
    response = await client.get("/api/tweets", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response.json()["tweets"] == []
