import os
import uuid
import subprocess
from sqlalchemy.orm import Session
from app.models import Video, ProcessingJob

class TrimService:
    def __init__(self, output_dir: str = "storage/processed"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def trim_video(self, video_id: int, start_time: float, end_time: float, db: Session) -> ProcessingJob:
        # Get original video
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            raise ValueError("Video not found")
        
        # Create job record
        job_id = str(uuid.uuid4())
        job = ProcessingJob(
            job_id=job_id,
            video_id=video_id,
            job_type="trim",
            parameters={
                "start_time": start_time,
                "end_time": end_time
            }
        )
        db.add(job)
        db.commit()
        
        # Process video
        self._process_trim(job, video, start_time, end_time, db)
        
        return job
    
    def _process_trim(self, job: ProcessingJob, video: Video, start_time: float, end_time: float, db: Session):
        try:
            job.status = "processing"
            db.commit()
            
            output_filename = f"trimmed_{job.job_id}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            
            cmd = [
                'ffmpeg', '-i', video.file_path,
                '-ss', str(start_time),
                '-to', str(end_time),
                '-c', 'copy',
                '-avoid_negative_ts', 'make_zero',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                job.status = "completed"
                job.result_path = output_path
                job.progress = 100
            else:
                job.status = "failed"
                job.error_message = result.stderr
                
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
        
        finally:
            db.commit()