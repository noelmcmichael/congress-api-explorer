"""
Rate limiting for Congress API requests.
"""

import time
import asyncio
from typing import Dict, Optional
from collections import deque
from dataclasses import dataclass, field

from ..utils.config import settings
from ..utils.logging import logger


@dataclass
class RateLimitWindow:
    """Rate limit tracking window."""
    requests: deque = field(default_factory=deque)
    max_requests: int = 0
    window_seconds: int = 0
    
    def __post_init__(self):
        """Initialize with empty deque."""
        self.requests = deque()
    
    def add_request(self, timestamp: float) -> None:
        """Add a request timestamp."""
        self.requests.append(timestamp)
        self._cleanup_old_requests(timestamp)
    
    def _cleanup_old_requests(self, current_time: float) -> None:
        """Remove requests outside the current window."""
        cutoff_time = current_time - self.window_seconds
        while self.requests and self.requests[0] < cutoff_time:
            self.requests.popleft()
    
    def can_make_request(self, current_time: float) -> bool:
        """Check if we can make a request within rate limits."""
        self._cleanup_old_requests(current_time)
        return len(self.requests) < self.max_requests
    
    def time_until_next_request(self, current_time: float) -> float:
        """Calculate time until next request is allowed."""
        self._cleanup_old_requests(current_time)
        if len(self.requests) < self.max_requests:
            return 0.0
        
        # Calculate when the oldest request will expire
        oldest_request = self.requests[0]
        return (oldest_request + self.window_seconds) - current_time


class RateLimiter:
    """Rate limiter for Congress API requests."""
    
    def __init__(self):
        self.windows: Dict[str, RateLimitWindow] = {
            "hour": RateLimitWindow(
                max_requests=settings.rate_limit_requests_per_hour,
                window_seconds=3600
            ),
            "minute": RateLimitWindow(
                max_requests=settings.rate_limit_requests_per_minute,
                window_seconds=60
            )
        }
        self._lock = asyncio.Lock()
    
    async def wait_if_needed(self) -> None:
        """Wait if rate limit would be exceeded."""
        async with self._lock:
            current_time = time.time()
            
            # Check all windows
            max_wait_time = 0.0
            for window_name, window in self.windows.items():
                if not window.can_make_request(current_time):
                    wait_time = window.time_until_next_request(current_time)
                    max_wait_time = max(max_wait_time, wait_time)
                    logger.warning(
                        f"Rate limit reached for {window_name} window. "
                        f"Waiting {wait_time:.2f} seconds."
                    )
            
            if max_wait_time > 0:
                await asyncio.sleep(max_wait_time)
                current_time = time.time()
            
            # Record the request
            for window in self.windows.values():
                window.add_request(current_time)
    
    async def can_make_request(self) -> bool:
        """Check if we can make a request without waiting."""
        async with self._lock:
            current_time = time.time()
            return all(
                window.can_make_request(current_time) 
                for window in self.windows.values()
            )
    
    def get_rate_limit_status(self) -> Dict[str, Dict[str, int]]:
        """Get current rate limit status."""
        current_time = time.time()
        status = {}
        
        for window_name, window in self.windows.items():
            window._cleanup_old_requests(current_time)
            status[window_name] = {
                "used": len(window.requests),
                "limit": window.max_requests,
                "remaining": window.max_requests - len(window.requests),
                "reset_in": int(window.time_until_next_request(current_time))
            }
        
        return status
    
    def reset(self) -> None:
        """Reset all rate limit counters."""
        for window in self.windows.values():
            window.requests.clear()
        logger.info("Rate limit counters reset")


# Global rate limiter instance
rate_limiter = RateLimiter()