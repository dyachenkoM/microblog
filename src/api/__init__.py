from fastapi import APIRouter
from core.config import settings
from .user import router as user_router
from .tweet import router as tweet_router
from .media import router as media_router


router = APIRouter(
    prefix=settings.api.prefix,
)

router.include_router(user_router)
router.include_router(tweet_router)
router.include_router(media_router)
