import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from typing import AsyncIterator
from api import router as api_router
from core import db_helper
from core.logger import configure_logging


logger = logging.getLogger("main_app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging(level=logging.DEBUG)
    logger.info("Application starting...")
    yield
    logger.info("Application shutting down...")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
main_app.include_router(api_router)
