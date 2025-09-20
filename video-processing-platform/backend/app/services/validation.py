import magic
import subprocess
from fastapi import UploadFile, HTTPException

class FileValidator:
    ALLOWED_TYPES = [
        'video/mp4', 'video/avi', 'video/mov', 
        'video/mkv', 'video/webm', 'video/flv'
    ]
    MAX_SIZE = 500 * 1024 * 1024  
    
    @classmethod
    async def validate_video_file(cls, file: UploadFile) -> bool:
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        
        if size > cls.MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {cls.MAX_SIZE // (1024*1024)}MB"
            )
        
        file_content = await file.read(1024)
        await file.seek(0)
        
        mime_type = magic.from_buffer(file_content, mime=True)
        
        if mime_type not in cls.ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {mime_type}. Allowed: {cls.ALLOWED_TYPES}"
            )
        
        return True
    
    @classmethod
    def validate_video_integrity(cls, file_path: str) -> bool:
        try:
            cmd = ['ffprobe', '-v', 'error', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False