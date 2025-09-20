# Video Processing Platform

## Overview

A FastAPI-based backend service for comprehensive video processing including upload, trimming, overlay management, watermarking, and multi-quality output generation with asynchronous job processing.

**Key Features:**
- Video upload with metadata extraction
- Precise trimming with FFmpeg integration
- Text/image/video overlays with positioning
- Watermark application
- Async background processing with job tracking
- Multiple quality outputs (1080p, 720p, 480p)

## Technology Stack

- **Backend**: FastAPI 0.104.1
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Queue**: Celery + Redis
- **Video Processing**: FFmpeg
- **Deployment**: Docker + Docker Compose
- **API Docs**: Auto-generated OpenAPI/Swagger

## Installation

### Quick Setup (Docker)
```bash
git clone https://github.com/yourusername/video-processing-platform.git
cd video-processing-platform
docker-compose up -d
```

### Manual Setup

**Prerequisites**: Python 3.10+, PostgreSQL 15+, Redis 6+, FFmpeg

```bash
# 1. Clone repository
git clone https://github.com/yourusername/video-processing-platform.git
cd video-processing-platform/backend

# 2. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Database setup
psql -U postgres -c "CREATE DATABASE video_processing;"
psql -U postgres -c "CREATE USER video_user WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE video_processing TO video_user;"

# 4. Environment configuration
cp .env.example .env
# Edit .env with your database credentials

# 5. Run migrations
alembic upgrade head

# 6. Start services
# Terminal 1: API
uvicorn app.main:app --reload

# Terminal 2: Worker
celery -A app.core.celery_app worker --loglevel=info
```

**Access**: http://localhost:8000/docs

### System Dependencies

**Windows (Chocolatey):**
```powershell
choco install python postgresql redis-64 ffmpeg -y
```

**macOS (Homebrew):**
```bash
brew install python@3.11 postgresql redis ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install python3.11 postgresql redis-server ffmpeg python3-dev libpq-dev
```

## Quick Test
```bash
# Upload video
curl -X POST "http://localhost:8000/api/v1/videos/upload" -F "file=@video.mp4"

# Check health
curl http://localhost:8000/health
```
