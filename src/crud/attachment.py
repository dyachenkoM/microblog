from sqlalchemy.ext.asyncio import AsyncSession

from core.models.attachment import Attachment


async def create_attachment(
        session: AsyncSession,
        url: str,
) -> Attachment:

    new_attachment = Attachment(
        link=url
    )

    session.add(new_attachment)
    await session.commit()

    return new_attachment
