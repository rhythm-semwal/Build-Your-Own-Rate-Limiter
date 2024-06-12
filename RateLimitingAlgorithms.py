import threading
from datetime import datetime

from fastapi import HTTPException

class RateLimit:
    def __init__(self):
        self.lock = threading.Lock()


class RateLimitExceeded(HTTPException):
    def __init__(self, detail="Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)


class TokenBucket(RateLimit):
    def __init__(self):
        super().__init__()
        self.total_capacity = 10  # tracks the maximum token in a bucket
        self.tokens = 10  # tracks current available tokens
        self.token_interval = 1  # rate of 1 token per second
        self.last_updated = datetime.now()

    def allow_request(self):
        with self.lock:
            current_time = datetime.now()
            gap = (current_time - self.last_updated).total_seconds()

            tokens_to_add = gap * self.token_interval

            self.tokens = min(self.total_capacity, self.tokens + tokens_to_add)
            self.last_updated = current_time

            if self.tokens >= 1:
                self.tokens -= 1
                return True

            raise RateLimitExceeded()
