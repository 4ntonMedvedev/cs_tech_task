import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response, status
from prometheus_fastapi_instrumentator import Instrumentator

from app.database import Base, check_database_connectivity, engine
from app.logging_config import setup_logging
from app.routers import incidents

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup complete")
    yield


app = FastAPI(title="Incident Tracker", version="1.0.0", lifespan=lifespan)
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

app.include_router(incidents.router)


@app.get("/health")
def health_check() -> Response:
    if check_database_connectivity():
        return Response(content='{"status":"ok"}', media_type="application/json")
    return Response(
        content='{"status":"unavailable","detail":"database unreachable"}',
        media_type="application/json",
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


@app.get("/error")
def trigger_error() -> None:
    raise ValueError("Intentional error for observability testing")
