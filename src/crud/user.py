from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import User, FollowersTable, UserKey


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


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> User:
    stmt = select(UserKey).where(UserKey.api_key == api_key)

    user_id = await session.scalar(stmt)
    user = await get_user_by_id(session=session, user_id=user_id.user_id)
    return user


async def follow_user(session: AsyncSession, follower_id: int, following_id: int) -> dict:
    new_follow = FollowersTable(follower_id=follower_id, following_id=following_id)
    session.add(new_follow)
    await session.commit()

    return {"result": "true"}


async def unfollow_user(session: AsyncSession, follower_id: int, following_id: int) -> dict:
    stmt = select(FollowersTable).where(
        FollowersTable.follower_id == follower_id,
        FollowersTable.following_id == following_id
    )
    follow_relation = await session.scalar(stmt)

    if not follow_relation:
        return {"result": "false", "message": "Subscription not found"}

    await session.delete(follow_relation)
    await session.commit()

    return {"result": "true"}
