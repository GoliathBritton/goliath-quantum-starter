"""API Utils - Utility functions for the qdLLM FastAPI server

This module provides utility functions for validation, caching,
response formatting, and other common operations.
"""

import hashlib
import json
import time
import asyncio
from typing import Dict, Any, Optional, List, Union, Callable
from datetime import datetime, timedelta
from functools import wraps
import logging

# Setup logging
logger = logging.getLogger(__name__)

class ResponseCache:
    """Simple in-memory cache for API responses"""
    
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if cache entry is expired"""
        return time.time() > entry["expires_at"]
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if current_time > entry["expires_at"]
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def _enforce_size_limit(self):
        """Enforce maximum cache size by removing oldest entries"""
        if len(self.cache) <= self.max_size:
            return
            
        # Sort by creation time and remove oldest entries
        sorted_entries = sorted(
            self.cache.items(),
            key=lambda x: x[1]["created_at"]
        )
        
        entries_to_remove = len(self.cache) - self.max_size
        for i in range(entries_to_remove):
            key = sorted_entries[i][0]
            del self.cache[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self.cache:
            return None
            
        entry = self.cache[key]
        if self._is_expired(entry):
            del self.cache[key]
            return None
            
        # Update access time
        entry["last_accessed"] = time.time()
        return entry["value"]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        ttl = ttl or self.default_ttl
        current_time = time.time()
        
        self.cache[key] = {
            "value": value,
            "created_at": current_time,
            "last_accessed": current_time,
            "expires_at": current_time + ttl
        }
        
        # Cleanup and enforce limits
        self._cleanup_expired()
        self._enforce_size_limit()
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        expired_count = sum(
            1 for entry in self.cache.values()
            if current_time > entry["expires_at"]
        )
        
        return {
            "total_entries": len(self.cache),
            "expired_entries": expired_count,
            "active_entries": len(self.cache) - expired_count,
            "max_size": self.max_size,
            "default_ttl": self.default_ttl
        }

# Global cache instance
response_cache = ResponseCache()

def cache_response(ttl: Optional[int] = None, key_func: Optional[Callable] = None):
    """Decorator for caching function responses"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = response_cache._generate_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_result = response_cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for {func.__name__}: {cache_key}")
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            response_cache.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator

class RequestValidator:
    """Utility class for request validation"""
    
    @staticmethod
    def validate_text_length(text: str, max_length: int = 10000, field_name: str = "text") -> str:
        """Validate text length"""
        if not text or not text.strip():
            raise ValueError(f"{field_name} cannot be empty")
        
        if len(text) > max_length:
            raise ValueError(f"{field_name} too long (max {max_length} characters)")
        
        return text.strip()
    
    @staticmethod
    def validate_numeric_range(
        value: Union[int, float],
        min_val: Optional[Union[int, float]] = None,
        max_val: Optional[Union[int, float]] = None,
        field_name: str = "value"
    ) -> Union[int, float]:
        """Validate numeric value is within range"""
        if min_val is not None and value < min_val:
            raise ValueError(f"{field_name} must be >= {min_val}")
        
        if max_val is not None and value > max_val:
            raise ValueError(f"{field_name} must be <= {max_val}")
        
        return value
    
    @staticmethod
    def validate_list_length(
        items: List[Any],
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        field_name: str = "list"
    ) -> List[Any]:
        """Validate list length"""
        if min_length is not None and len(items) < min_length:
            raise ValueError(f"{field_name} must have at least {min_length} items")
        
        if max_length is not None and len(items) > max_length:
            raise ValueError(f"{field_name} must have at most {max_length} items")
        
        return items
    
    @staticmethod
    def validate_enum_value(value: str, allowed_values: List[str], field_name: str = "value") -> str:
        """Validate enum value"""
        if value not in allowed_values:
            raise ValueError(f"{field_name} must be one of: {', '.join(allowed_values)}")
        
        return value

class ResponseFormatter:
    """Utility class for formatting API responses"""
    
    @staticmethod
    def success_response(
        data: Any,
        message: str = "Success",
        request_id: Optional[str] = None,
        processing_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """Format successful response"""
        response = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        if request_id:
            response["request_id"] = request_id
        
        if processing_time is not None:
            response["processing_time"] = processing_time
        
        return response
    
    @staticmethod
    def error_response(
        error_code: str,
        error_message: str,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format error response"""
        response = {
            "success": False,
            "error_code": error_code,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            response["details"] = details
        
        if request_id:
            response["request_id"] = request_id
        
        return response
    
    @staticmethod
    def paginated_response(
        items: List[Any],
        page: int,
        page_size: int,
        total_items: int,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Format paginated response"""
        total_pages = (total_items + page_size - 1) // page_size
        
        response = {
            "success": True,
            "data": {
                "items": items,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_items": total_items,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_previous": page > 1
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
        if request_id:
            response["request_id"] = request_id
        
        return response

class MetricsCollector:
    """Utility class for collecting and aggregating metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Any]]] = {}
        self.counters: Dict[str, int] = {}
        
    def record_metric(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a metric value"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        self.metrics[metric_name].append({
            "value": value,
            "timestamp": time.time(),
            "tags": tags or {}
        })
        
        # Keep only last 1000 values per metric
        if len(self.metrics[metric_name]) > 1000:
            self.metrics[metric_name] = self.metrics[metric_name][-1000:]
    
    def increment_counter(self, counter_name: str, increment: int = 1):
        """Increment a counter"""
        self.counters[counter_name] = self.counters.get(counter_name, 0) + increment
    
    def get_metric_stats(self, metric_name: str, time_window: Optional[int] = None) -> Dict[str, float]:
        """Get statistics for a metric"""
        if metric_name not in self.metrics:
            return {}
        
        values = self.metrics[metric_name]
        
        # Filter by time window if specified
        if time_window:
            cutoff_time = time.time() - time_window
            values = [v for v in values if v["timestamp"] > cutoff_time]
        
        if not values:
            return {}
        
        metric_values = [v["value"] for v in values]
        
        return {
            "count": len(metric_values),
            "min": min(metric_values),
            "max": max(metric_values),
            "avg": sum(metric_values) / len(metric_values),
            "sum": sum(metric_values)
        }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics and counters"""
        return {
            "metrics": {
                name: self.get_metric_stats(name, time_window=3600)  # Last hour
                for name in self.metrics.keys()
            },
            "counters": self.counters.copy(),
            "timestamp": datetime.now().isoformat()
        }

# Global metrics collector
metrics_collector = MetricsCollector()

class ConfigManager:
    """Utility class for managing configuration"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values"""
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.config, updates)
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return self.config.copy()

class AsyncBatchProcessor:
    """Utility class for processing items in batches asynchronously"""
    
    def __init__(self, batch_size: int = 10, max_concurrency: int = 5):
        self.batch_size = batch_size
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
    
    async def process_batch(self, items: List[Any], processor_func: Callable) -> List[Any]:
        """Process a batch of items"""
        async with self.semaphore:
            if asyncio.iscoroutinefunction(processor_func):
                tasks = [processor_func(item) for item in items]
                return await asyncio.gather(*tasks, return_exceptions=True)
            else:
                return [processor_func(item) for item in items]
    
    async def process_all(self, items: List[Any], processor_func: Callable) -> List[Any]:
        """Process all items in batches"""
        results = []
        
        # Split items into batches
        batches = [
            items[i:i + self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]
        
        # Process batches
        for batch in batches:
            batch_results = await self.process_batch(batch, processor_func)
            results.extend(batch_results)
        
        return results

def timing_decorator(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            metrics_collector.record_metric(
                f"function_execution_time",
                execution_time,
                {"function": func.__name__}
            )
            logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            execution_time = time.time() - start_time
            metrics_collector.record_metric(
                f"function_execution_time",
                execution_time,
                {"function": func.__name__}
            )
            logger.debug(f"{func.__name__} executed in {execution_time:.3f}s")
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Sanitize user input"""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Remove null bytes and control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def generate_request_id() -> str:
    """Generate unique request ID"""
    timestamp = int(time.time() * 1000)
    return f"req_{timestamp}_{hash(time.time()) % 10000:04d}"

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

# Export commonly used utilities
__all__ = [
    "ResponseCache",
    "cache_response",
    "RequestValidator",
    "ResponseFormatter",
    "MetricsCollector",
    "ConfigManager",
    "AsyncBatchProcessor",
    "response_cache",
    "metrics_collector",
    "timing_decorator",
    "sanitize_input",
    "generate_request_id",
    "format_file_size",
    "truncate_text"
]