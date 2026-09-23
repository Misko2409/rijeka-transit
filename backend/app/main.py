from fastapi import FastAPI

from backend.app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Rijeka Transit platform.",
    version=settings.app_version,
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
