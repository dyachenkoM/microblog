from pydantic import BaseModel
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
