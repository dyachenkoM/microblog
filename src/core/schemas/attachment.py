from pydantic import BaseModel


class AttachmentResponse(BaseModel):
    result: bool
    media_id: int
