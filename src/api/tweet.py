from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.schemas import TweetResponse
from crud.tweet import (get_all_tweets as crud_get_all_tweets,
                        like_tweet as crud_like_tweet,
                        dislike_tweet as crud_dislike_tweet)


router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)


@router.get("")
async def get_all_tweets(session: AsyncSession = Depends(db_helper.session_getter),
                         api_key: str | None = Header(default="api-alice")
                         ) -> TweetResponse:
    tweets = await crud_get_all_tweets(session=session, api_key=api_key)
    return TweetResponse(result=True, tweets=tweets)


@router.post("/{tweet_id}/likes")
async def like_tweet(tweet_id: int,
                     session: AsyncSession = Depends(db_helper.session_getter),
                     api_key: str | None = Header(default="api-alice")
                     ):
    return await crud_like_tweet(session=session, tweet_id=tweet_id, api_key=api_key)


@router.delete("/{tweet_id}/likes")
async def dislike_tweet(tweet_id: int,
                        session: AsyncSession = Depends(db_helper.session_getter),
                        api_key: str | None = Header(default="api-alice")
                        ):
    return await crud_dislike_tweet(session=session, tweet_id=tweet_id, api_key=api_key)
