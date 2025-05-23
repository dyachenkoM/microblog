from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.attachment import Attachment


async def create_attachment(
    session: AsyncSession,
    url: str,
) -> Attachment:
    try:
        new_attachment = Attachment(link=url)

        session.add(new_attachment)
        await session.commit()

        return new_attachment

    except SQLAlchemyError as e:
        raise Exception(f"Database error: {str(e)}")
