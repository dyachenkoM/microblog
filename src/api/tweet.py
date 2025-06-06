import logging

from fastapi import APIRouter, Depends, Header
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.logger import configure_logging
from core.schemas import (
    TweetResponse,
    TweetCreateRequest,
    TweetCreateResponse,
    SuccessResponse,
)
from core.exception import TweetNotFoundError, handle_error, UserNotFoundError
from core.models import Tweet
from crud.tweet import (
    get_all_tweets as crud_get_all_tweets,
    like_tweet as crud_like_tweet,
    dislike_tweet as crud_dislike_tweet,
    create_tweet as crud_create_tweet,
    delete_tweet as crud_delete_tweet,
)


router = APIRouter(prefix="/tweets", tags=["Tweets"])

logger = logging.getLogger("route_tweet")
configure_logging(level=logging.DEBUG)


@router.get("", response_model=TweetResponse)
async def get_all_tweets(
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: str | None = Header(default="test"),
) -> TweetResponse | ORJSONResponse:
    if not api_key:
        logger.warning("User with API-key %s not found", api_key)
        raise UserNotFoundError("API key is required")
    try:
        tweets = await crud_get_all_tweets(session=session, api_key=api_key)
        return TweetResponse(result=True, tweets=tweets)
    except Exception as e:
        logger.error("%s: API-key = %s", e, api_key)
        return handle_error(e)


@router.post("", response_model=TweetCreateResponse)
async def create_tweet(
    tweet_data: TweetCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: str | None = Header(default="test"),
) -> TweetCreateResponse | ORJSONResponse:
    if not api_key:
        logger.warning("User with API-key %s not found", api_key)
        raise UserNotFoundError("API key is required")
    try:
        tweet = await crud_create_tweet(
            session=session,
            api_key=api_key,
            tweet_data=tweet_data.tweet_data,
            tweet_media_ids=tweet_data.tweet_media_ids,
        )
        return TweetCreateResponse(result=True, tweet_id=tweet.id)
    except Exception as e:
        logger.error("%s: API-key = %s; tweet_data = %s", e, api_key, tweet_data)
        return handle_error(e)


@router.delete("/{tweet_id}", response_model=SuccessResponse)
async def delete_tweet(
    tweet_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: str | None = Header(default="test"),
) -> SuccessResponse | ORJSONResponse:
    if not api_key:
        logger.warning("User with API-key %s not found", api_key)
        raise UserNotFoundError("API key is required")
    try:
        tweet = await session.get(Tweet, tweet_id)
        if not tweet:
            raise TweetNotFoundError("Tweet not found")
        return await crud_delete_tweet(
            session=session, tweet_id=tweet_id, api_key=api_key
        )
    except Exception as e:
        logger.error("%s: API-key = %s; tweet_id = %s", e, api_key, tweet_id)
        return handle_error(e)


@router.post("/{tweet_id}/likes", response_model=SuccessResponse)
async def like_tweet(
    tweet_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: str | None = Header(default="test"),
) -> SuccessResponse | ORJSONResponse:
    if not api_key:
        logger.warning("User with API-key %s not found", api_key)
        raise UserNotFoundError("API key is required")
    try:
        tweet = await session.get(Tweet, tweet_id)
        if not tweet:
            raise TweetNotFoundError("Tweet not found")
        return await crud_like_tweet(
            session=session, tweet_id=tweet_id, api_key=api_key
        )
    except Exception as e:
        logger.error("%s: API-key = %s; tweet_id = %s", e, api_key, tweet_id)
        return handle_error(e)


@router.delete("/{tweet_id}/likes", response_model=SuccessResponse)
async def dislike_tweet(
    tweet_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: str | None = Header(default="test"),
) -> SuccessResponse | ORJSONResponse:
    if not api_key:
        logger.warning("User with API-key %s not found", api_key)
        raise UserNotFoundError("API key is required")
    try:
        tweet = await session.get(Tweet, tweet_id)
        if not tweet:
            raise TweetNotFoundError("Tweet not found")
        return await crud_dislike_tweet(
            session=session, tweet_id=tweet_id, api_key=api_key
        )
    except Exception as e:
        logger.error("%s: API-key = %s; tweet_id = %s", e, api_key, tweet_id)
        return handle_error(e)
