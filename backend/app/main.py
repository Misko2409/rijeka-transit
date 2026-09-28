from fastapi import FastAPI

from backend.app.api.v1.stops import router as stops_router
from backend.app.api.v1.vehicles import router as vehicles_router
from backend.app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Rijeka Transit platform.",
    version=settings.app_version,
)

app.include_router(
    vehicles_router,
    prefix="/api/v1",
)

app.include_router(
    stops_router,
    prefix="/api/v1",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
