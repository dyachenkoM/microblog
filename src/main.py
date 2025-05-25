import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from typing import AsyncIterator
from api import router as api_router
from core import db_helper


class AppState:
    def __init__(self):
        self.logger: logging.Logger | None = None


def setup_logging() -> logging.Logger:
    """Настройка логгера для всего приложения"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    return logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state = AppState()
    app.state.logger = setup_logging()

    app.state.logger.info("Application starting...")
    yield
    app.state.logger.info("Application shutting down...")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
main_app.include_router(api_router)
