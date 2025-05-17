from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from contextlib import asynccontextmanager
from api import router as api_router
from core import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
main_app.include_router(api_router)
