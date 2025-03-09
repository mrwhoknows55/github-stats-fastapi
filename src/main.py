from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.github_endpoints import router as github_router
from src.core.config import CORS_WHITELIST

app = FastAPI(
    title="GitHub Stats API Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_WHITELIST,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"], summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}


app.include_router(github_router)
