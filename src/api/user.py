from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas import UserResponse, UserFull
from crud.user import get_user_by_id

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> UserResponse:
    user = await get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(result='true', user=UserFull.model_validate(user))

