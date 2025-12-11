"""
API Usage monitoring for free-tier compliance
"""
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Deque
import threading


class APILimitMonitor:
    def __init__(self, max_requests_per_minute: int = 100, max_requests_per_day: int = 1000):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_requests_per_day = max_requests_per_day
        
        # Track requests per minute (last 60 seconds)
        self.requests_per_minute: Dict[str, Deque[float]] = defaultdict(lambda: deque())
        
        # Track requests per day (last 24 hours)
        self.requests_per_day: Dict[str, Deque[float]] = defaultdict(lambda: deque())
        
        # Lock for thread safety
        self._lock = threading.Lock()
    
    def record_request(self, api_key_hash: str) -> bool:
        """
        Record an API request and check if it's within limits
        Returns True if request is allowed, False if it exceeds limits
        """
        with self._lock:
            current_time = time.time()
            
            # Clean old entries (older than 1 minute)
            while (self.requests_per_minute[api_key_hash] and 
                   current_time - self.requests_per_minute[api_key_hash][0] > 60):
                self.requests_per_minute[api_key_hash].popleft()
            
            # Clean old entries (older than 24 hours)
            while (self.requests_per_day[api_key_hash] and 
                   current_time - self.requests_per_day[api_key_hash][0] > 24 * 3600):
                self.requests_per_day[api_key_hash].popleft()
            
            # Check if limits are exceeded
            if (len(self.requests_per_minute[api_key_hash]) >= self.max_requests_per_minute or
                len(self.requests_per_day[api_key_hash]) >= self.max_requests_per_day):
                return False
            
            # Add the current request
            self.requests_per_minute[api_key_hash].append(current_time)
            self.requests_per_day[api_key_hash].append(current_time)
            
            return True
    
    def get_usage_stats(self, api_key_hash: str) -> Dict:
        """
        Get current usage statistics for an API key
        """
        with self._lock:
            current_time = time.time()
            
            # Clean old entries before getting stats
            while (self.requests_per_minute[api_key_hash] and 
                   current_time - self.requests_per_minute[api_key_hash][0] > 60):
                self.requests_per_minute[api_key_hash].popleft()
            
            while (self.requests_per_day[api_key_hash] and 
                   current_time - self.requests_per_day[api_key_hash][0] > 24 * 3600):
                self.requests_per_day[api_key_hash].popleft()
            
            return {
                "requests_last_minute": len(self.requests_per_minute[api_key_hash]),
                "requests_today": len(self.requests_per_day[api_key_hash]),
                "max_requests_per_minute": self.max_requests_per_minute,
                "max_requests_per_day": self.max_requests_per_day,
                "within_minute_limit": len(self.requests_per_minute[api_key_hash]) < self.max_requests_per_minute,
                "within_daily_limit": len(self.requests_per_day[api_key_hash]) < self.max_requests_per_day
            }


# Global monitor instance
monitor = APILimitMonitor()


def check_api_limits(api_key_hash: str) -> bool:
    """
    Check if an API request is within limits
    """
    return monitor.record_request(api_key_hash)


def get_api_usage_stats(api_key_hash: str) -> Dict:
    """
    Get current usage statistics for an API key
    """
    return monitor.get_usage_stats(api_key_hash)