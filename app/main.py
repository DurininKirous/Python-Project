import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .api.v1.routes import router as checks_router
from .config import get_settings
from .models import Base
from .database import get_engine

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    logging.basicConfig(level=settings.log_level)

    app = FastAPI(title=settings.app_name)
    include_routes(app)
    register_metrics(app, settings.prometheus_metrics_path)

    @app.on_event("startup")
    async def on_startup() -> None:
        engine = get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    return app


def include_routes(app: FastAPI) -> None:
    app.include_router(checks_router, prefix="/api/v1")


def register_metrics(app: FastAPI, metrics_path: str) -> None:
    Instrumentator().instrument(app).expose(app, endpoint=metrics_path)


app = create_app()
