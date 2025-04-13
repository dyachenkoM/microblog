from pydantic import BaseModel
from typing import List


class UserShort(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class UserFull(BaseModel):
    id: int
    name: str
    followers: List[UserShort]
    following: List[UserShort]

    model_config = {
        "from_attributes": True
    }


class UserResponse(BaseModel):
    result: str
    user: UserFull

    model_config = {
        "from_attributes": True
    }