import os
import uuid
import subprocess
import json
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models import Video

class VideoService:
    def __init__(self, upload_dir: str = "storage/uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    async def upload_video(self, file: UploadFile, db: Session) -> Video:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'mp4'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        metadata = self._get_video_metadata(file_path)
        
        video = Video(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            duration=metadata.get('duration'),
            size=len(content),
            format=metadata.get('format'),
            resolution=metadata.get('resolution')
        )
        
        db.add(video)
        db.commit()
        db.refresh(video)
        
        return video
    
    def _get_video_metadata(self, file_path: str) -> dict:
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # Extract relevant metadata
            format_info = data.get('format', {})
            video_stream = next((s for s in data.get('streams', []) if s['codec_type'] == 'video'), {})
            
            return {
                'duration': float(format_info.get('duration', 0)),
                'format': format_info.get('format_name'),
                'resolution': f"{video_stream.get('width', 0)}x{video_stream.get('height', 0)}"
            }
        except Exception as e:
            print(f"Error getting video metadata: {e}")
            return {}