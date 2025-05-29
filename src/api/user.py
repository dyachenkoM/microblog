import logging

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core import db_helper
from core.schemas import UserResponse, SuccessResponse, UserFull
from core.exception import UserNotFoundError, handle_error

from crud.user import (
    get_user_by_id,
    get_user_by_api_key,
    follow_user as follow,
    unfollow_user as unfollow,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

logger = logging.getLogger("route_user")


async def get_current_user_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    api_key: Optional[str] = Header(default="test"),
) -> int:
    try:
        if not api_key:
            raise UserNotFoundError("API key is required")

        user = await get_user_by_api_key(session=session, api_key=api_key)
        return user.id
    except Exception as e:
        raise handle_error(e, logger)


@router.get("/me", response_model=UserResponse)
async def get_my_info(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse | JSONResponse:
    try:
        user = await get_user_by_id(session=session, user_id=user_id)
        return UserResponse(result="true", user=UserFull.model_validate(user))
    except Exception as e:
        return handle_error(e, logger)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse | JSONResponse:
    try:
        user = await get_user_by_id(session=session, user_id=user_id)
        return UserResponse(result="true", user=UserFull.model_validate(user))
    except Exception as e:
        return handle_error(e, logger)


@router.post("/{target_id}/follow", response_model=SuccessResponse)
async def follow_user(
    target_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> SuccessResponse | JSONResponse:
    try:
        return await follow(
            session=session, follower_id=user_id, following_id=target_id
        )
    except Exception as e:
        return handle_error(e, logger)


@router.delete("/{target_id}/follow", response_model=SuccessResponse)
async def unfollow_user(
    target_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> SuccessResponse | JSONResponse:
    try:
        return await unfollow(
            session=session, follower_id=user_id, following_id=target_id
        )
    except Exception as e:
        return handle_error(e, logger)
