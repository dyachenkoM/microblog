from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.schemas import TweetResponse, TweetCreateRequest, TweetCreateResponse
from crud.tweet import (get_all_tweets as crud_get_all_tweets,
                        like_tweet as crud_like_tweet,
                        dislike_tweet as crud_dislike_tweet,
                        create_tweet as crud_create_tweet)


router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)


@router.get("")
async def get_all_tweets(session: AsyncSession = Depends(db_helper.session_getter),
                         api_key: str | None = Header(default="test")
                         ) -> TweetResponse:
    tweets = await crud_get_all_tweets(session=session, api_key=api_key)
    return TweetResponse(result=True, tweets=tweets)


@router.post("")
async def create_tweet(tweet_data: TweetCreateRequest,
                       session: AsyncSession = Depends(db_helper.session_getter),
                       api_key: str | None = Header(default="test"),
                       ) -> TweetCreateResponse:
    tweet = await crud_create_tweet(session=session,
                                    api_key=api_key,
                                    tweet_data=tweet_data.tweet_data,
                                    tweet_media_ids=tweet_data.tweet_media_ids
                                    )
    return TweetCreateResponse(result=True, tweet_id=tweet.id)


@router.post("/{tweet_id}/likes")
async def like_tweet(tweet_id: int,
                     session: AsyncSession = Depends(db_helper.session_getter),
                     api_key: str | None = Header(default="test")
                     ):
    return await crud_like_tweet(session=session, tweet_id=tweet_id, api_key=api_key)


@router.delete("/{tweet_id}/likes")
async def dislike_tweet(tweet_id: int,
                        session: AsyncSession = Depends(db_helper.session_getter),
                        api_key: str | None = Header(default="test")
                        ):
    return await crud_dislike_tweet(session=session, tweet_id=tweet_id, api_key=api_key)
