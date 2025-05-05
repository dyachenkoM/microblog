from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas import UserResponse, UserFull
from crud.user import (get_user_by_id,
                       get_user_id_by_api_key,
                       follow_user as follow,
                       unfollow_user as unfollow,
                       )

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
async def get_my_info(request: Request, session: AsyncSession = Depends(db_helper.session_getter)) -> UserResponse:
    api_key = request.headers.get("api-key")
    user_id = await get_user_id_by_api_key(session=session, api_key=api_key)
    return await get_user(user_id=user_id, session=session)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> UserResponse:
    user = await get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(result="true", user=UserFull.model_validate(user))


@router.post("/{target_id}/follow")
async def follow_user(target_id: int, request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
    api_key = request.headers.get("api-key")
    user_id = await get_user_id_by_api_key(session=session, api_key=api_key)

    res = await follow(session=session, follower_id=user_id, following_id=target_id)
    return 201, res


@router.delete("/{target_id}/follow")
async def unfollow_user(target_id: int, request: Request, session: AsyncSession = Depends(db_helper.session_getter)):
    api_key = request.headers.get("api-key")
    user_id = await get_user_id_by_api_key(session=session, api_key=api_key)

    res = await unfollow(session=session, follower_id=user_id, following_id=target_id)
    return 201, res
