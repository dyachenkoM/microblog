from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Tweet, Attachment, TweetLikes
from crud.user import get_user_by_api_key


async def get_all_tweets(session: AsyncSession, api_key: str) -> [Tweet, ]:
    user = await get_user_by_api_key(session=session, api_key=api_key)

    following_ids = [u.id for u in user.following]

    stmt = (
        select(Tweet)
        .where(Tweet.author_id.in_(following_ids))
        .options(
            joinedload(Tweet.author),
            joinedload(Tweet.attachments),
            joinedload(Tweet.likes)
        )
        .order_by(Tweet.likes_count.desc())
    )

    result = await session.execute(stmt)
    tweets = result.unique().scalars().all()

    return tweets


async def create_tweet(
        session: AsyncSession,
        api_key: str,
        tweet_data: str,
        tweet_media_ids: Optional[List[int]] = None
) -> Tweet:

    stmt = select(Attachment).where(Attachment.id.in_(tweet_media_ids))
    result = await session.execute(stmt)
    existing_media = result.scalars().all()

    new_tweet = Tweet(
        content=tweet_data,
        author_id=(await get_user_by_api_key(session=session, api_key=api_key)).id,
        attachments=existing_media
    )

    session.add(new_tweet)
    await session.commit()
    await session.refresh(new_tweet)

    return new_tweet


async def delete_tweet(session: AsyncSession, tweet_id: int, api_key: str):
    user_id = (await get_user_by_api_key(session=session, api_key=api_key)).id
    stmt = select(Tweet).where(Tweet.id == tweet_id)

    tweet = await session.scalar(stmt)
    if user_id == tweet.author_id:
        await session.delete(tweet)
        await session.commit()

        return {"result": "true"}


async def like_tweet(session: AsyncSession, tweet_id: int, api_key: str):
    user_id = (await get_user_by_api_key(session=session, api_key=api_key)).id
    new_like = TweetLikes(user_id=user_id, tweet_id=tweet_id)

    session.add(new_like)
    await session.commit()

    return {"result": "true"}


async def dislike_tweet(session: AsyncSession, tweet_id: int, api_key: str):
    user_id = (await get_user_by_api_key(session=session, api_key=api_key)).id
    stmt = select(TweetLikes).where(TweetLikes.tweet_id == tweet_id,
                                    TweetLikes.user_id == user_id
                                    )
    like_relation = await session.scalar(stmt)

    await session.delete(like_relation)
    await session.commit()

    return {"result": "true"}
