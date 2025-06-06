import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_tweets_empty(client: AsyncClient):
    response = await client.get("/api/tweets", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response.json()["tweets"] == []


@pytest.mark.asyncio
async def test_create_tweet_wo_media(client: AsyncClient):
    response = await client.post("/api/tweets", headers={"api-key": "test"}, json={"tweet_data": "string",
                                                                                   "tweet_media_ids": []
                                                                                   })
    assert response.status_code == 201
    assert response.json()["result"] is True
    assert response.json()["tweet_id"] == 1
    tweets = await client.get("/api/tweets", headers={"api-key": "test"})
    assert len(tweets.json()["tweets"]) == 1


@pytest.mark.asyncio
async def test_like_tweet(client: AsyncClient):
    response = await client.post("/api/tweets/1/likes", headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json()["result"] is True
    tweets = await client.get("/api/tweets", headers={"api-key": "test"})
    assert len(tweets.json()["tweets"][0]["likes"]) == 1


@pytest.mark.asyncio
async def test_dislike_tweet(client: AsyncClient):
    response = await client.delete("/api/tweets/1/likes", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    tweets = await client.get("/api/tweets", headers={"api-key": "test"})
    assert len(tweets.json()["tweets"][0]["likes"]) == 0


@pytest.mark.asyncio
async def test_delete_tweet(client: AsyncClient):
    response = await client.delete("/api/tweets/1", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json()["result"] is True
    tweets = await client.get("/api/tweets", headers={"api-key": "test"})
    assert tweets.json()["tweets"] == []
