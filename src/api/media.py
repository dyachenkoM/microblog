from fastapi import APIRouter, UploadFile, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.s3 import s3_client
from core.schemas.attachment import AttachmentResponse
from crud.attachment import create_attachment

router = APIRouter(
    prefix="/medias",
    tags=["medias"]
)


@router.post("")
async def file_upload(file: UploadFile,
                      session: AsyncSession = Depends(db_helper.session_getter),
                      api_key: str | None = Header(default="api-alice")
                      ):
    media_url = await s3_client.upload_file(file.file, file.filename)
    media_id = await create_attachment(session=session, url=media_url)
    return AttachmentResponse(result=True, media_id=media_id)
