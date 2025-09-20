import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_upload_video():
    with open("test_video.mp4", "rb") as f:
        response = client.post(
            "/api/v1/videos/upload",
            files={"file": ("test_video.mp4", f, "video/mp4")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["original_filename"] == "test_video.mp4"

def test_list_videos():
    response = client.get("/api/v1/videos/")
    assert response.status_code == 200
    data = response.json()
    assert "videos" in data
    assert "total" in data

def test_trim_video():
    # First upload a video
    with open("test_video.mp4", "rb") as f:
        upload_response = client.post(
            "/api/v1/videos/upload",
            files={"file": ("test_video.mp4", f, "video/mp4")}
        )
    video_id = upload_response.json()["id"]
    
    # Test trimming
    response = client.post(
        f"/api/v1/videos/{video_id}/trim",
        params={"start_time": 0, "end_time": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data