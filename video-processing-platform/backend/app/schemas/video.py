from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VideoBase(BaseModel):
    filename: str
    original_filename: str

class VideoCreate(VideoBase):
    pass

class VideoResponse(VideoBase):
    id: int
    file_path: str
    duration: Optional[float]
    size: int
    format: Optional[str]
    resolution: Optional[str]
    upload_time: datetime
    
    class Config:
        from_attributes = True

class VideoList(BaseModel):
    videos: List[VideoResponse]
    total: int