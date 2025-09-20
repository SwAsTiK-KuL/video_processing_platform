from fastapi import Request, HTTPException
import time
import redis
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis_client = redis.Redis(host='localhost', port=6379, db=2)
    
    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        current_requests = self.redis_client.get(key)
        
        if current_requests is None:
            self.redis_client.setex(key, self.window_seconds, 1)
            return True
        
        if int(current_requests) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later."
            )
        
        self.redis_client.incr(key)
        return True