"""API Middleware - Custom middleware for the qdLLM FastAPI server

This module provides middleware for authentication, rate limiting, CORS,
request logging, and other cross-cutting concerns.
"""

import time
import json
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict, deque

from fastapi import Request, Response, HTTPException, status
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint

# Setup logging
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all HTTP requests and responses"""
    
    def __init__(self, app, log_requests: bool = True, log_responses: bool = False):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
        
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generate request ID
        request_id = f"req_{int(time.time() * 1000)}_{id(request)}"
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        if self.log_requests:
            logger.info(
                f"Request {request_id}: {request.method} {request.url.path} "
                f"from {request.client.host if request.client else 'unknown'}"
            )
            
            # Log request headers (excluding sensitive ones)
            headers = dict(request.headers)
            sensitive_headers = {'authorization', 'x-api-key', 'cookie'}
            filtered_headers = {
                k: v if k.lower() not in sensitive_headers else '[REDACTED]'
                for k, v in headers.items()
            }
            logger.debug(f"Request {request_id} headers: {filtered_headers}")
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Log response
            if self.log_responses:
                logger.info(
                    f"Response {request_id}: {response.status_code} "
                    f"in {processing_time:.3f}s"
                )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Processing-Time"] = f"{processing_time:.3f}"
            
            return response
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"Request {request_id} failed after {processing_time:.3f}s: {str(e)}"
            )
            
            # Return error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "error_message": "Internal server error occurred",
                    "request_id": request_id,
                    "timestamp": datetime.now().isoformat()
                },
                headers={"X-Request-ID": request_id}
            )

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests per client"""
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        enabled: bool = True
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.enabled = enabled
        
        # Store request timestamps per client
        self.client_requests: Dict[str, deque] = defaultdict(deque)
        
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier (IP address or API key)"""
        # Try to get API key first
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"api_key:{api_key[:8]}..."
        
        # Fall back to IP address
        if request.client:
            return f"ip:{request.client.host}"
        
        return "unknown"
    
    def _is_rate_limited(self, client_id: str) -> tuple[bool, Dict[str, Any]]:
        """Check if client is rate limited"""
        now = time.time()
        client_requests = self.client_requests[client_id]
        
        # Remove old requests (older than 1 hour)
        while client_requests and client_requests[0] < now - 3600:
            client_requests.popleft()
        
        # Count requests in the last minute and hour
        minute_ago = now - 60
        requests_last_minute = sum(1 for req_time in client_requests if req_time > minute_ago)
        requests_last_hour = len(client_requests)
        
        # Check limits
        minute_exceeded = requests_last_minute >= self.requests_per_minute
        hour_exceeded = requests_last_hour >= self.requests_per_hour
        
        rate_limit_info = {
            "requests_last_minute": requests_last_minute,
            "requests_last_hour": requests_last_hour,
            "limit_per_minute": self.requests_per_minute,
            "limit_per_hour": self.requests_per_hour,
            "reset_time_minute": int(now + 60 - (now % 60)),
            "reset_time_hour": int(now + 3600 - (now % 3600))
        }
        
        return minute_exceeded or hour_exceeded, rate_limit_info
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if not self.enabled:
            return await call_next(request)
        
        client_id = self._get_client_id(request)
        is_limited, rate_info = self._is_rate_limited(client_id)
        
        if is_limited:
            logger.warning(f"Rate limit exceeded for client {client_id}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "error_message": "Rate limit exceeded. Please try again later.",
                    "rate_limit_info": rate_info,
                    "timestamp": datetime.now().isoformat()
                },
                headers={
                    "X-RateLimit-Limit-Minute": str(self.requests_per_minute),
                    "X-RateLimit-Limit-Hour": str(self.requests_per_hour),
                    "X-RateLimit-Remaining-Minute": str(max(0, self.requests_per_minute - rate_info["requests_last_minute"])),
                    "X-RateLimit-Remaining-Hour": str(max(0, self.requests_per_hour - rate_info["requests_last_hour"])),
                    "X-RateLimit-Reset-Minute": str(rate_info["reset_time_minute"]),
                    "X-RateLimit-Reset-Hour": str(rate_info["reset_time_hour"])
                }
            )
        
        # Record this request
        self.client_requests[client_id].append(time.time())
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Minute"] = str(max(0, self.requests_per_minute - rate_info["requests_last_minute"] - 1))
        response.headers["X-RateLimit-Remaining-Hour"] = str(max(0, self.requests_per_hour - rate_info["requests_last_hour"] - 1))
        
        return response

class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """Middleware for API key authentication"""
    
    def __init__(
        self,
        app,
        api_keys: Optional[Dict[str, Dict[str, Any]]] = None,
        required: bool = False,
        exempt_paths: Optional[list] = None
    ):
        super().__init__(app)
        self.api_keys = api_keys or {}
        self.required = required
        self.exempt_paths = exempt_paths or ["/", "/docs", "/redoc", "/openapi.json", "/system/health"]
        
    def _is_path_exempt(self, path: str) -> bool:
        """Check if path is exempt from authentication"""
        return any(path.startswith(exempt_path) for exempt_path in self.exempt_paths)
    
    def _validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return key info"""
        key_info = self.api_keys.get(api_key)
        if not key_info:
            return None
        
        # Check if key is active
        if not key_info.get("active", True):
            return None
        
        # Check expiration
        expires_at = key_info.get("expires_at")
        if expires_at and datetime.fromisoformat(expires_at) < datetime.now():
            return None
        
        return key_info
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skip authentication for exempt paths
        if self._is_path_exempt(request.url.path):
            return await call_next(request)
        
        # Get API key from header
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not api_key:
            if self.required:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "error_code": "MISSING_API_KEY",
                        "error_message": "API key is required",
                        "timestamp": datetime.now().isoformat()
                    },
                    headers={"WWW-Authenticate": "Bearer"}
                )
            else:
                # API key not required, continue without authentication
                return await call_next(request)
        
        # Validate API key
        key_info = self._validate_api_key(api_key)
        if not key_info:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error_code": "INVALID_API_KEY",
                    "error_message": "Invalid or expired API key",
                    "timestamp": datetime.now().isoformat()
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Add key info to request state
        request.state.api_key_info = key_info
        request.state.authenticated = True
        
        # Log successful authentication
        logger.debug(f"Authenticated request with API key: {api_key[:8]}...")
        
        return await call_next(request)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers"""
    
    def __init__(self, app):
        super().__init__(app)
        
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring API performance"""
    
    def __init__(self, app):
        super().__init__(app)
        self.request_metrics = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate metrics
        processing_time = time.time() - start_time
        endpoint = f"{request.method} {request.url.path}"
        
        # Store metrics
        self.request_metrics[endpoint].append({
            "timestamp": datetime.now().isoformat(),
            "processing_time": processing_time,
            "status_code": response.status_code,
            "success": 200 <= response.status_code < 400
        })
        
        # Keep only last 1000 requests per endpoint
        if len(self.request_metrics[endpoint]) > 1000:
            self.request_metrics[endpoint] = self.request_metrics[endpoint][-1000:]
        
        # Add performance headers
        response.headers["X-Processing-Time"] = f"{processing_time:.3f}"
        
        # Log slow requests
        if processing_time > 5.0:  # Log requests taking more than 5 seconds
            logger.warning(
                f"Slow request detected: {endpoint} took {processing_time:.3f}s"
            )
        
        return response
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for all endpoints"""
        metrics = {}
        
        for endpoint, requests in self.request_metrics.items():
            if not requests:
                continue
                
            processing_times = [req["processing_time"] for req in requests]
            success_count = sum(1 for req in requests if req["success"])
            
            metrics[endpoint] = {
                "total_requests": len(requests),
                "successful_requests": success_count,
                "success_rate": success_count / len(requests) if requests else 0,
                "avg_processing_time": sum(processing_times) / len(processing_times),
                "min_processing_time": min(processing_times),
                "max_processing_time": max(processing_times),
                "last_request": requests[-1]["timestamp"]
            }
        
        return metrics

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling"""
    
    def __init__(self, app, debug: bool = False):
        super().__init__(app)
        self.debug = debug
        
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except HTTPException:
            # Re-raise HTTP exceptions (they're handled by FastAPI)
            raise
        except Exception as e:
            # Log the error
            request_id = getattr(request.state, 'request_id', 'unknown')
            logger.error(
                f"Unhandled exception in request {request_id}: {str(e)}",
                exc_info=True
            )
            
            # Prepare error response
            error_response = {
                "error_code": "INTERNAL_SERVER_ERROR",
                "error_message": "An internal server error occurred",
                "request_id": request_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Only add minimal debug info in debug mode
            if self.debug:
                error_response["debug_info"] = {
                    "exception_type": type(e).__name__
                }
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=error_response,
                headers={"X-Request-ID": request_id}
            )

# Middleware configuration function
def setup_middleware(app, config: Dict[str, Any]):
    """Setup all middleware for the FastAPI app"""
    
    # Error handling (should be first)
    app.add_middleware(
        ErrorHandlingMiddleware,
        debug=config.get("debug", False)
    )
    
    # Security headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Performance monitoring
    performance_middleware = PerformanceMonitoringMiddleware(app)
    app.add_middleware(PerformanceMonitoringMiddleware)
    
    # Request logging
    app.add_middleware(
        RequestLoggingMiddleware,
        log_requests=config.get("log_requests", True),
        log_responses=config.get("log_responses", False)
    )
    
    # Rate limiting
    if config.get("rate_limit_enabled", True):
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=config.get("rate_limit_per_minute", 60),
            requests_per_hour=config.get("rate_limit_per_hour", 1000),
            enabled=True
        )
    
    # API key authentication
    if config.get("api_key_required", False):
        app.add_middleware(
            APIKeyAuthMiddleware,
            api_keys=config.get("api_keys", {}),
            required=True,
            exempt_paths=config.get("auth_exempt_paths", [])
        )
    
    # CORS (should be last)
    if config.get("enable_cors", True):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.get("cors_origins", ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    
    # Store performance middleware instance for metrics access
    app.state.performance_middleware = performance_middleware
    
    logger.info("All middleware configured successfully")