import logging

from fastapi import APIRouter, UploadFile, Depends, Header, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.exception import handle_error
from core.logger import configure_logging
from core.s3 import s3_client
from core.schemas.attachment import AttachmentResponse
from crud.attachment import create_attachment

router = APIRouter(prefix="/medias", tags=["medias"])

logger = logging.getLogger("route_media")
configure_logging(level=logging.DEBUG)


@router.post("", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def file_upload(
    file: UploadFile,
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: str | None = Header(default="test"),
) -> AttachmentResponse | ORJSONResponse:
    try:
        media_url = await s3_client.upload_file(file.file, file.filename)
        media_id = (await create_attachment(session=session, url=media_url)).id
        return AttachmentResponse(result=True, media_id=media_id)

    except Exception as e:
        logger.error("%s: API-key = %s; tweet_id = %s", e, api_key, file)
        return handle_error(e)
