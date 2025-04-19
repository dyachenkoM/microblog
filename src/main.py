from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from core.models import User
from contextlib import asynccontextmanager
from api import router as api_router
from core.config import settings
from core.models import db_helper, Base
from core.schemas import UserResponse, UserFull


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(api_router,
                        prefix=settings.api.prefix,
                        )


@main_app.get('/api/users/me')
async def main():
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "Maksim",
            "followers": [],
            "followings": []
        }
    }


@main_app.get('/api/users/{user_id}')
async def get_user(user_id: int, session: AsyncSession = Depends(db_helper.session_getter)) -> UserResponse:
    result = await session.execute(
        select(User)
        .options(
            joinedload(User.followers),
            joinedload(User.following),
        )
        .where(User.id == user_id)
    )
    user = result.unique().scalar_one()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(result='true', user=UserFull.model_validate(user))


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                )
