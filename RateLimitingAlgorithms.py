import threading
from collections import Counter
from datetime import datetime, timedelta
from math import floor

from fastapi import HTTPException


class RateLimit:
    def __init__(self):
        self.lock = threading.Lock()
        self.interval = 60  # seconds window
        self.limit_per_interval = 100  # max number request threshold


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


class FixedCounterWindow(RateLimit):
    def __init__(self):
        super().__init__()
        self.token = 0
        self.current_time = datetime.now().time().replace(second=0, microsecond=0)

    def allow_request(self):
        with self.lock:
            current_request_time = datetime.now().time().replace(second=0, microsecond=0)
            if current_request_time != self.current_time:
                self.token = 0
                self.current_time = current_request_time

            if self.token >= self.limit_per_interval:
                raise RateLimitExceeded()

            self.token += 1
            return True


class SlidingWindow(RateLimit):
    def __init__(self):
        super().__init__()
        self.logs = []

    def allow_request(self):
        with self.lock:
            curr = datetime.now()
            while len(self.logs) > 0 and (curr - self.logs[0]).total_seconds() > self.interval:
                self.logs.pop(0)

            if len(self.logs) > self.limit_per_interval:
                raise RateLimitExceeded()

            self.logs.append(curr)
            return True


class SlidingWindowCounter(RateLimit):
    """
    This method uses a sliding window algorithm for rate limiting, which allows a smoother transition
    of request counts across time windows. By considering a portion of the previous window's request count,
    it avoids abrupt resets of the limit at the boundary of each time window.

    Time-based Keys: The use of time-based keys (current_window_key and previous_window_key) allows the rate limiter
    to segment and track requests by the second.

    Weighted Previous Window: The previous_window_weight ensures that only the appropriate fraction of the previous
    window's request count is considered, based on how much of the current second has elapsed. This contributes to
    the smooth transition between windows.
    """
    def __init__(self):
        super().__init__()
        self.counter = Counter()
        self.token = 10

    def allow_request(self):
        with self.lock:
            current = datetime.now()
            current_window_key = f'{current:%H%M%S}'
            previous_window_key = f'{current - timedelta(seconds=1):%H%M%S}'
            previous_window_weight = (1000000 - current.microsecond)/1000000

            request_count = floor(self.counter[previous_window_key] * previous_window_weight +
                                  self.counter[current_window_key])

            if request_count >= self.token:
                raise RateLimitExceeded()
            self.counter[current_window_key] += 1
            return True
