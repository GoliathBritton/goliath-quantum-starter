"""Security Middleware for FastAPI with Zero Trust Architecture"""

import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Optional, List, Callable, Any
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import logging

from .auth_service import (
    get_auth_service, ZeroTrustAuthService, SecurityLevel, UserRole,
    AuthToken, SecurityContext, User
)
from .oauth2_provider import get_oauth2_service, OAuth2Provider
from .quantum_crypto import get_encryption_service, get_signature_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Zero Trust Security Middleware"""
    
    def __init__(self, app: FastAPI, auth_service: ZeroTrustAuthService):
        super().__init__(app)
        self.auth_service = auth_service
        self.encryption_service = get_encryption_service()
        self.signature_service = get_signature_service()
        
        # Security configuration
        self.rate_limit_requests = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
        self.rate_limit_window = int(os.getenv('RATE_LIMIT_WINDOW', '3600'))  # 1 hour
        self.request_counts: Dict[str, List[float]] = {}
        
        # Exempt paths from authentication
        self.exempt_paths = {
            '/health',
            '/metrics',
            '/docs',
            '/openapi.json',
            '/auth/login',
            '/auth/register',
            '/auth/oauth2/authorize',
            '/auth/oauth2/callback',
            '/auth/refresh'
        }
        
        # High security paths requiring additional verification
        self.high_security_paths = {
            '/admin',
            '/quantum/jobs/create',
            '/quantum/jobs/delete',
            '/users/admin',
            '/system/config'
        }
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through security pipeline"""
        start_time = time.time()
        
        try:
            # 1. Rate limiting
            if not self._check_rate_limit(request):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            # 2. Request validation
            await self._validate_request(request)
            
            # 3. Authentication (if required)
            security_context = await self._authenticate_request(request)
            
            # 4. Authorization
            if not self._authorize_request(request, security_context):
                raise HTTPException(status_code=403, detail="Access denied")
            
            # 5. Add security context to request
            request.state.security_context = security_context
            
            # 6. Process request
            response = await call_next(request)
            
            # 7. Add security headers
            self._add_security_headers(response)
            
            # 8. Log security event
            self._log_security_event(request, response, security_context, time.time() - start_time)
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Security middleware error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal security error")
    
    def _check_rate_limit(self, request: Request) -> bool:
        """Check rate limiting"""
        client_ip = self._get_client_ip(request)
        current_time = time.time()
        
        # Initialize or clean old requests
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = []
        
        # Remove old requests outside the window
        self.request_counts[client_ip] = [
            req_time for req_time in self.request_counts[client_ip]
            if current_time - req_time < self.rate_limit_window
        ]
        
        # Check if limit exceeded
        if len(self.request_counts[client_ip]) >= self.rate_limit_requests:
            return False
        
        # Add current request
        self.request_counts[client_ip].append(current_time)
        return True
    
    async def _validate_request(self, request: Request):
        """Validate request structure and content"""
        # Check request size
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="Request too large")
        
        # Check for suspicious headers
        suspicious_headers = ['x-forwarded-host', 'x-real-ip']
        for header in suspicious_headers:
            if header in request.headers:
                logger.warning(f"Suspicious header detected: {header}")
        
        # Validate content type for POST/PUT requests
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.headers.get('content-type', '')
            if not content_type.startswith(('application/json', 'multipart/form-data')):
                logger.warning(f"Unusual content type: {content_type}")
    
    async def _authenticate_request(self, request: Request) -> Optional[SecurityContext]:
        """Authenticate request and return security context"""
        path = request.url.path
        
        # Skip authentication for exempt paths
        if any(path.startswith(exempt) for exempt in self.exempt_paths):
            return None
        
        # Extract token from Authorization header
        auth_header = request.headers.get('authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        # Verify token
        try:
            auth_token = self.auth_service.verify_token(token)
            if not auth_token:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            
            # Get user
            user = self.auth_service.get_user(auth_token.user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            
            # Create security context
            security_context = SecurityContext(
                user=user,
                token=auth_token,
                ip_address=self._get_client_ip(request),
                user_agent=request.headers.get('user-agent', ''),
                timestamp=datetime.now(timezone.utc),
                session_id=request.headers.get('x-session-id'),
                device_fingerprint=request.headers.get('x-device-fingerprint')
            )
            
            return security_context
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=401, detail="Authentication failed")
    
    def _authorize_request(self, request: Request, security_context: Optional[SecurityContext]) -> bool:
        """Authorize request based on security context"""
        path = request.url.path
        method = request.method
        
        # Allow unauthenticated access to exempt paths
        if any(path.startswith(exempt) for exempt in self.exempt_paths):
            return True
        
        # Require authentication for all other paths
        if not security_context:
            return False
        
        user = security_context.user
        
        # Admin access
        if user.role == UserRole.ADMIN:
            return True
        
        # High security paths require high security level
        if any(path.startswith(secure) for secure in self.high_security_paths):
            if user.security_level != SecurityLevel.HIGH:
                logger.warning(f"High security path access denied for user {user.id}")
                return False
        
        # Role-based access control
        if path.startswith('/quantum/'):
            if user.role in [UserRole.QUANTUM_ANALYST, UserRole.RESEARCHER]:
                return True
            if user.role == UserRole.VIEWER and method == 'GET':
                return True
            return False
        
        if path.startswith('/users/'):
            if user.role in [UserRole.ADMIN, UserRole.QUANTUM_ANALYST]:
                return True
            # Users can access their own profile
            if path == f'/users/{user.id}' and method in ['GET', 'PUT']:
                return True
            return False
        
        # Default: allow access for authenticated users
        return True
    
    def _add_security_headers(self, response: Response):
        """Add security headers to response"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        # Check for forwarded IP (behind proxy)
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        # Check for real IP
        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            return real_ip
        
        # Default to client host
        return request.client.host if request.client else 'unknown'
    
    def _log_security_event(self, request: Request, response: Response, 
                          security_context: Optional[SecurityContext], duration: float):
        """Log security event"""
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'method': request.method,
            'path': request.url.path,
            'status_code': response.status_code,
            'duration_ms': round(duration * 1000, 2),
            'client_ip': self._get_client_ip(request),
            'user_agent': request.headers.get('user-agent', ''),
            'user_id': security_context.user.id if security_context else None,
            'user_role': security_context.user.role.value if security_context else None,
            'security_level': security_context.user.security_level.value if security_context else None
        }
        
        # Log based on status code
        if response.status_code >= 400:
            logger.warning(f"Security event: {json.dumps(event)}")
        else:
            logger.info(f"Security event: {json.dumps(event)}")

class JWTBearer(HTTPBearer):
    """JWT Bearer token authentication"""
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.auth_service = get_auth_service()
    
    async def __call__(self, request: Request) -> Optional[SecurityContext]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials:
            return None
        
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        # Verify token
        auth_token = self.auth_service.verify_token(credentials.credentials)
        if not auth_token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Get user
        user = self.auth_service.get_user(auth_token.user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Create security context
        security_context = SecurityContext(
            user=user,
            token=auth_token,
            ip_address=request.client.host if request.client else 'unknown',
            user_agent=request.headers.get('user-agent', ''),
            timestamp=datetime.now(timezone.utc),
            session_id=request.headers.get('x-session-id'),
            device_fingerprint=request.headers.get('x-device-fingerprint')
        )
        
        return security_context

def setup_security_middleware(app: FastAPI):
    """Setup security middleware for FastAPI app"""
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
        allow_headers=['*'],
    )
    
    # Session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv('SESSION_SECRET_KEY', 'quantum-nexus-engine-session-key'),
        max_age=3600,  # 1 hour
        same_site='lax',
        https_only=os.getenv('HTTPS_ONLY', 'false').lower() == 'true'
    )
    
    # Security middleware
    auth_service = get_auth_service()
    app.add_middleware(SecurityMiddleware, auth_service=auth_service)

# Dependency for getting current user
jwt_bearer = JWTBearer()

async def get_current_user(security_context: SecurityContext = Depends(jwt_bearer)) -> User:
    """Get current authenticated user"""
    return security_context.user

async def get_current_admin(security_context: SecurityContext = Depends(jwt_bearer)) -> User:
    """Get current user (admin only)"""
    if security_context.user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return security_context.user

async def get_current_analyst(security_context: SecurityContext = Depends(jwt_bearer)) -> User:
    """Get current user (analyst or admin only)"""
    if security_context.user.role not in [UserRole.ADMIN, UserRole.QUANTUM_ANALYST]:
        raise HTTPException(status_code=403, detail="Analyst access required")
    return security_context.user

async def get_high_security_user(security_context: SecurityContext = Depends(jwt_bearer)) -> User:
    """Get current user (high security level required)"""
    if security_context.user.security_level != SecurityLevel.HIGH:
        raise HTTPException(status_code=403, detail="High security clearance required")
    return security_context.user

# Security context dependency
async def get_security_context(security_context: SecurityContext = Depends(jwt_bearer)) -> SecurityContext:
    """Get current security context"""
    return security_context