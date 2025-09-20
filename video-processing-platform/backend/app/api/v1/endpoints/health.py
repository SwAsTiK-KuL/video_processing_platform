from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import redis
import subprocess
from app.core.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "checks": {
            "database": False,
            "redis": False,
            "ffmpeg": False,
            "storage": False
        }
    }
    
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = True
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = str(e)
    
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        health_status["checks"]["redis"] = True
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["redis"] = str(e)
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        health_status["checks"]["ffmpeg"] = result.returncode == 0
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["ffmpeg"] = str(e)
    
    try:
        import os
        storage_dirs = ['storage/uploads', 'storage/processed']
        for dir_path in storage_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        health_status["checks"]["storage"] = True
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["storage"] = str(e)
    
    if health_status["status"] != "healthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status