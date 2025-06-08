import logging

from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core import db_helper
from core.logger import configure_logging
from core.schemas import UserResponse, SuccessResponse, UserFull
from core.exception import UserNotFoundError, handle_error

from crud.user import (
    get_user_by_id,
    get_user_by_api_key,
    follow_user as follow,
    unfollow_user as unfollow,
    create_user as create,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger("route_user")
configure_logging(level=logging.DEBUG)


async def get_current_user_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: Optional[str] = Header(default="test"),
) -> int | ORJSONResponse:
    try:
        if not api_key:
            logger.warning("User with API-key %s not found", api_key)
            raise UserNotFoundError("API key is required")

        user = await get_user_by_api_key(session=session, api_key=api_key)
        return user.id
    except Exception as e:
        logger.error("%s: API-key = %s", e, api_key)
        return handle_error(e)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_my_info(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse | ORJSONResponse:
    try:
        user = await get_user_by_id(session=session, user_id=user_id)
        return UserResponse(result="true", user=UserFull.model_validate(user))
    except Exception as e:
        logger.error("%s: user_id = %s", e, user_id)
        return handle_error(e)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse | ORJSONResponse:
    try:
        user = await get_user_by_id(session=session, user_id=user_id)
        return UserResponse(result="true", user=UserFull.model_validate(user))
    except Exception as e:
        logger.error("%s: user_id = %s", e, user_id)
        return handle_error(e)


@router.post(
    "/{target_id}/follow",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def follow_user(
    target_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> SuccessResponse | ORJSONResponse:
    try:
        return await follow(
            session=session, follower_id=user_id, following_id=target_id
        )
    except Exception as e:
        logger.error("%s: user_id = %s; target_id = %s", e, user_id, target_id)
        return handle_error(e)


@router.delete(
    "/{target_id}/follow",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
)
async def unfollow_user(
    target_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> SuccessResponse | ORJSONResponse:
    try:
        return await unfollow(
            session=session, follower_id=user_id, following_id=target_id
        )
    except Exception as e:
        logger.error("%s: user_id = %s; target_id = %s", e, user_id, target_id)
        return handle_error(e)


@router.post(
    "/create/{username}",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    username: str,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> SuccessResponse | ORJSONResponse:
    try:
        return await create(session=session, username=username)
    except Exception as e:
        logger.error("%s: Error while create user", e)
        return handle_error(e)
