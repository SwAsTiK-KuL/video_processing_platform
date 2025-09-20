from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.video_service import VideoService
from app.schemas.video import VideoResponse, VideoList
from app.models import Video

router = APIRouter()
video_service = VideoService()

@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    video = await video_service.upload_video(file, db)
    return video

@router.get("/", response_model=VideoList)
async def list_videos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    videos = db.query(Video).offset(skip).limit(limit).all()
    total = db.query(Video).count()
    return VideoList(videos=videos, total=total)

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video