from typing import List

from pydantic import BaseModel, Field
from .user import UserShort


class Tweet(BaseModel):
    id: int
    content: str
    attachments: list[str]
    author: UserShort
    likes: list[UserShort]

    model_config = {
        "from_attributes": True
    }


class TweetResponse(BaseModel):
    result: bool
    tweets: list[Tweet]


class TweetCreateRequest(BaseModel):
    tweet_data: str = Field(..., min_length=1, max_length=280)
    tweet_media_ids: List[int] | None


class TweetCreateResponse(BaseModel):
    result: bool
    tweet_id: int
