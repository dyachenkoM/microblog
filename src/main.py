from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from contextlib import asynccontextmanager
from api import router as api_router
from core.config import settings
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


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                )
