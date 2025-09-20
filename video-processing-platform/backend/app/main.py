from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.endpoints import videos
from app.core.database import engine
from app.models import Base
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Video Processing API",
    description="A comprehensive video processing platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="storage"), name="static")

app.include_router(videos.router, prefix="/api/v1/videos", tags=["videos"])

@app.get("/")
async def root():
    return {"message": "Video Processing API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}