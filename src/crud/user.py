from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = (
        select(User).
        options(
            joinedload(User.followers), joinedload(User.following)
        )
        .where(User.id == user_id)
    )
    result = await session.scalar(stmt)
    return result
