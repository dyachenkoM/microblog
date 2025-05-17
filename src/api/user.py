from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.schemas import UserResponse, UserFull
from crud.user import (get_user_by_id,
                       get_user_by_api_key,
                       follow_user as follow,
                       unfollow_user as unfollow,
                       )

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
async def get_my_info(session: AsyncSession = Depends(db_helper.session_getter),
                      api_key: str | None = Header(default="test")
                      ) -> UserResponse:
    user_id = (await get_user_by_api_key(session=session, api_key=api_key)).id
    return await get_user(user_id=user_id, session=session)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int,
                   session: AsyncSession = Depends(db_helper.session_getter),
                   api_key: str | None = Header(default="test")
                   ) -> UserResponse:
    user = await get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(result="true", user=UserFull.model_validate(user))


@router.post("/{target_id}/follow")
async def follow_user(target_id: int,
                      session: AsyncSession = Depends(db_helper.session_getter),
                      api_key: str | None = Header(default="test")
                      ):
    user_id = (await get_user_by_api_key(session=session, api_key=api_key)).id

    res = await follow(session=session, follower_id=user_id, following_id=target_id)
    return res


@router.delete("/{target_id}/follow")
async def unfollow_user(target_id: int,
                        session: AsyncSession = Depends(db_helper.session_getter),
                        api_key: str | None = Header(default="test")
                        ):
    user_id = (await get_user_by_api_key(session=session, api_key=api_key)).id

    res = await unfollow(session=session, follower_id=user_id, following_id=target_id)
    return res
