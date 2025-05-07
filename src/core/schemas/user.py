from pydantic import BaseModel


class UserShort(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class UserFull(BaseModel):
    id: int
    name: str
    followers: list[UserShort]
    following: list[UserShort]

    model_config = {
        "from_attributes": True
    }


class UserResponse(BaseModel):
    result: str
    user: UserFull

    model_config = {
        "from_attributes": True
    }
    