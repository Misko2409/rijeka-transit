from fastapi import FastAPI

app = FastAPI(
    title="Rijeka Transit API",
    description="Backend API for the Rijeka Transit platform.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}