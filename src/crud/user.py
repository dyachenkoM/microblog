from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError

from core.models import User, FollowersTable, UserKey
from core.schemas import SuccessResponse
from core.exception import (
    UserNotFoundError,
    AlreadyFollowingError,
    SelfFollowError,
    SubscriptionNotFoundError,
)


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    try:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return result.all()
    except SQLAlchemyError as e:
        raise Exception(f"Database error: {str(e)}")


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    try:
        stmt = (
            select(User)
            .options(joinedload(User.followers), joinedload(User.following))
            .where(User.id == user_id)
        )
        user = await session.scalar(stmt)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        return user
    except NoResultFound as e:
        raise Exception(f"Database error: {str(e)}")


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> User:
    try:
        stmt = select(UserKey).where(UserKey.api_key == api_key)
        user_key = await session.scalar(stmt)

        if not user_key:
            raise UserNotFoundError("Invalid API key")

        return await get_user_by_id(session, user_key.user_id)
    except NoResultFound as e:
        raise Exception(f"Database error: {str(e)}")


async def follow_user(
    session: AsyncSession, follower_id: int, following_id: int
) -> SuccessResponse:
    try:
        if follower_id == following_id:
            raise SelfFollowError("Cannot follow yourself")

        await get_user_by_id(session, follower_id)
        await get_user_by_id(session, following_id)

        stmt = select(FollowersTable).where(
            FollowersTable.follower_id == follower_id,
            FollowersTable.following_id == following_id,
        )
        if await session.scalar(stmt):
            raise AlreadyFollowingError("Already following this user")

        new_follow = FollowersTable(follower_id=follower_id, following_id=following_id)
        session.add(new_follow)
        await session.commit()

        return SuccessResponse(result=True)

    except IntegrityError as e:
        await session.rollback()
        if "foreign key" in str(e).lower():
            raise UserNotFoundError("User not found")
        raise Exception(f"Database integrity error: {str(e)}")
    except SQLAlchemyError as e:
        await session.rollback()
        raise Exception(f"Database error: {str(e)}")


async def unfollow_user(
    session: AsyncSession, follower_id: int, following_id: int
) -> SuccessResponse:
    try:
        stmt = select(FollowersTable).where(
            FollowersTable.follower_id == follower_id,
            FollowersTable.following_id == following_id,
        )
        follow_relation = await session.scalar(stmt)

        if not follow_relation:
            raise SubscriptionNotFoundError("Subscription not found")

        await session.delete(follow_relation)
        await session.commit()

        return SuccessResponse(result=True)

    except SQLAlchemyError as e:
        await session.rollback()
        raise Exception(f"Database error: {str(e)}")


async def create_user(
        session: AsyncSession, username: str
) -> SuccessResponse:
    try:
        user = User(name=username)
        session.add(user)
        await session.flush()

        key = UserKey(api_key="api-friend", user_id=user.id)
        session.add(key)
        await session.commit()

        return SuccessResponse(result=True)
    except SQLAlchemyError as e:
        await session.rollback()
        raise Exception(f"Database error: {str(e)}")
