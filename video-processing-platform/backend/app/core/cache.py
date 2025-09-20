import redis
import json
from typing import Optional, Any
import os

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379/1")
        )
    
    async def get(self, key: str) -> Optional[Any]:
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600):
        try:
            self.redis_client.setex(key, expire, json.dumps(value))
        except Exception:
            pass
    
    async def delete(self, key: str):
        try:
            self.redis_client.delete(key)
        except Exception:
            pass

cache_service = CacheService()