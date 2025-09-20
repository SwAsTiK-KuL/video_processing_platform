import pytest
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_concurrent_uploads():
    def upload_video():
        with open("test_video.mp4", "rb") as f:
            response = client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        return response.status_code == 200
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(upload_video) for _ in range(10)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    assert all(results)
    assert end_time - start_time < 30  # Should complete within 30 seconds

def test_large_file_upload():
    # Test with larger file (if available)
    pass