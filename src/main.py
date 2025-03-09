from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import CORS_WHITELIST

app = FastAPI(
    title="GitHub Stats API Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_WHITELIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"], summary="Health check endpoint")
async def health_check():
    return {"status": "ok"}
