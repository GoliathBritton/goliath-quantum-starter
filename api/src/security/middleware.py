from fastapi import Request, Response, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Optional, Dict, Any
import time
import json
import logging
from datetime import datetime
import hashlib
import ipaddress

from .compliance import compliance_engine, DataClassification, AuditEvent
from .rate_limiter import rate_limit_manager, RateLimitType, RateLimitExceeded
from src.entitlements import SubscriptionTier
from src.models import User

class SecurityMiddleware(BaseHTTPMiddleware):
    """Comprehensive security middleware integrating all security features"""
    
    def __init__(self, app, enable_rate_limiting: bool = True, enable_audit_logging: bool = True,
                 enable_ip_filtering: bool = True, enable_compliance_checks: bool = True):
        super().__init__(app)
        self.enable_rate_limiting = enable_rate_limiting
        self.enable_audit_logging = enable_audit_logging
        self.enable_ip_filtering = enable_ip_filtering
        self.enable_compliance_checks = enable_compliance_checks
        
        # Security configuration
        self.blocked_ips = set()
        self.suspicious_ips = set()
        self.allowed_ip_ranges = []  # CIDR ranges for IP allowlisting
        self.security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        
        self.logger = logging.getLogger('security_middleware')
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Main middleware dispatch method"""
        start_time = time.time()
        
        try:
            # 1. IP filtering
            if self.enable_ip_filtering:
                ip_check_result = await self._check_ip_address(request)
                if not ip_check_result["allowed"]:
                    return self._create_blocked_response(ip_check_result["reason"])
            
            # 2. Extract user information
            user_info = await self._extract_user_info(request)
            
            # 3. Rate limiting
            if self.enable_rate_limiting and user_info:
                rate_limit_result = await self._check_rate_limits(request, user_info)
                if not rate_limit_result["allowed"]:
                    raise RateLimitExceeded(rate_limit_result["result"], rate_limit_result["limit_type"])
            
            # 4. Compliance checks
            if self.enable_compliance_checks and user_info:
                compliance_result = await self._check_compliance(request, user_info)
                if not compliance_result["allowed"]:
                    return self._create_compliance_blocked_response(compliance_result["reason"])
            
            # 5. Process request
            response = await call_next(request)
            
            # 6. Add security headers
            self._add_security_headers(response)
            
            # 7. Audit logging
            if self.enable_audit_logging:
                await self._log_request(request, response, user_info, time.time() - start_time)
            
            return response
            
        except RateLimitExceeded as e:
            # Handle rate limit exceeded
            if self.enable_audit_logging:
                await self._log_security_event(request, "rate_limit_exceeded", user_info)
            raise e
            
        except Exception as e:
            # Handle other security-related errors
            if self.enable_audit_logging:
                await self._log_security_event(request, "security_error", user_info, str(e))
            
            self.logger.error(f"Security middleware error: {e}")
            return self._create_error_response("Security check failed", 500)
    
    async def _check_ip_address(self, request: Request) -> Dict[str, Any]:
        """Check if IP address is allowed"""
        client_ip = self._get_client_ip(request)
        
        if not client_ip:
            return {"allowed": True, "reason": "No IP address found"}
        
        # Check blocked IPs
        if client_ip in self.blocked_ips:
            return {"allowed": False, "reason": "IP address is blocked"}
        
        # Check IP allowlist if configured
        if self.allowed_ip_ranges:
            ip_allowed = False
            try:
                client_ip_obj = ipaddress.ip_address(client_ip)
                for ip_range in self.allowed_ip_ranges:
                    if client_ip_obj in ipaddress.ip_network(ip_range):
                        ip_allowed = True
                        break
                
                if not ip_allowed:
                    return {"allowed": False, "reason": "IP address not in allowlist"}
            except ValueError:
                return {"allowed": False, "reason": "Invalid IP address format"}
        
        return {"allowed": True, "reason": "IP address allowed"}
    
    def _get_client_ip(self, request: Request) -> Optional[str]:
        """Extract client IP address from request"""
        # Check X-Forwarded-For header (for load balancers/proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP in the chain
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # Fall back to direct client IP
        if request.client:
            return request.client.host
        
        return None
    
    async def _extract_user_info(self, request: Request) -> Optional[Dict[str, Any]]:
        """Extract user information from request"""
        try:
            # Try to get user from request state (set by auth middleware)
            user = getattr(request.state, 'user', None)
            if user:
                return {
                    "user_id": user.id,
                    "subscription_tier": user.subscription_tier,
                    "email": user.email
                }
            
            # Try to extract from Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                # This would typically involve JWT token validation
                # For now, return a placeholder
                return {
                    "user_id": "anonymous",
                    "subscription_tier": SubscriptionTier.BASIC,
                    "email": None
                }
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Failed to extract user info: {e}")
            return None
    
    async def _check_rate_limits(self, request: Request, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check rate limits for the request"""
        try:
            # Determine which rate limits to check based on the endpoint
            limit_types = self._get_applicable_rate_limits(request)
            
            for limit_type in limit_types:
                result = await rate_limit_manager.check_limit(
                    user_info["user_id"],
                    user_info["subscription_tier"],
                    limit_type,
                    request
                )
                
                if not result.allowed:
                    return {
                        "allowed": False,
                        "result": result,
                        "limit_type": limit_type
                    }
            
            return {"allowed": True}
            
        except Exception as e:
            self.logger.error(f"Rate limit check failed: {e}")
            return {"allowed": True}  # Fail open for availability
    
    def _get_applicable_rate_limits(self, request: Request) -> list[RateLimitType]:
        """Determine which rate limits apply to this request"""
        path = request.url.path
        method = request.method
        
        limits = [RateLimitType.REQUESTS_PER_MINUTE, RateLimitType.REQUESTS_PER_HOUR]
        
        # Add specific limits based on endpoint
        if "/api/qnexus" in path:
            limits.append(RateLimitType.QUANTUM_JOBS_PER_DAY)
        
        if method == "POST" and ("upload" in path or "data" in path):
            limits.append(RateLimitType.DATA_UPLOAD_MB_PER_HOUR)
        
        if "/api/" in path:
            limits.append(RateLimitType.API_CALLS_PER_MINUTE)
        
        return limits
    
    async def _check_compliance(self, request: Request, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance requirements"""
        try:
            # Determine data classification for the request
            data_classification = self._classify_request_data(request)
            
            # Check if processing is allowed
            purpose = self._determine_processing_purpose(request)
            
            is_compliant = compliance_engine.validate_data_processing(
                user_info["user_id"],
                data_classification,
                purpose
            )
            
            if not is_compliant:
                return {
                    "allowed": False,
                    "reason": "Data processing not compliant with regulations"
                }
            
            return {"allowed": True}
            
        except Exception as e:
            self.logger.error(f"Compliance check failed: {e}")
            return {"allowed": True}  # Fail open, but log the error
    
    def _classify_request_data(self, request: Request) -> DataClassification:
        """Classify the data being processed in the request"""
        path = request.url.path
        
        # Classify based on endpoint
        if "personal" in path or "profile" in path:
            return DataClassification.PII
        elif "medical" in path or "health" in path:
            return DataClassification.PHI
        elif "confidential" in path or "private" in path:
            return DataClassification.CONFIDENTIAL
        else:
            return DataClassification.INTERNAL
    
    def _determine_processing_purpose(self, request: Request) -> str:
        """Determine the purpose of data processing"""
        path = request.url.path
        method = request.method
        
        if method == "GET":
            return "service_provision"
        elif method == "POST" and "analytics" in path:
            return "legitimate_interest"
        elif method in ["PUT", "PATCH", "DELETE"]:
            return "user_consent"
        else:
            return "service_provision"
    
    def _add_security_headers(self, response: Response):
        """Add security headers to response"""
        for header, value in self.security_headers.items():
            response.headers[header] = value
    
    async def _log_request(self, request: Request, response: Response, 
                          user_info: Optional[Dict[str, Any]], duration: float):
        """Log request for audit purposes"""
        try:
            event = AuditEvent(
                event_id=self._generate_event_id(request),
                timestamp=datetime.utcnow(),
                user_id=user_info.get("user_id") if user_info else None,
                action=f"{request.method} {request.url.path}",
                resource=request.url.path,
                ip_address=self._get_client_ip(request) or "unknown",
                user_agent=request.headers.get("User-Agent", "unknown"),
                result="success" if response.status_code < 400 else "failure",
                risk_score=self._calculate_request_risk_score(request, response),
                metadata={
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                    "content_length": response.headers.get("content-length", "0")
                },
                compliance_frameworks=compliance_engine.config.enabled_frameworks
            )
            
            compliance_engine.audit_logger.log_event(event)
            
        except Exception as e:
            self.logger.error(f"Failed to log audit event: {e}")
    
    async def _log_security_event(self, request: Request, event_type: str, 
                                 user_info: Optional[Dict[str, Any]], details: str = ""):
        """Log security-related events"""
        try:
            event = AuditEvent(
                event_id=self._generate_event_id(request),
                timestamp=datetime.utcnow(),
                user_id=user_info.get("user_id") if user_info else None,
                action=event_type,
                resource=request.url.path,
                ip_address=self._get_client_ip(request) or "unknown",
                user_agent=request.headers.get("User-Agent", "unknown"),
                result="blocked",
                risk_score=0.8,  # High risk for security events
                metadata={
                    "event_type": event_type,
                    "details": details
                },
                compliance_frameworks=compliance_engine.config.enabled_frameworks
            )
            
            compliance_engine.audit_logger.log_event(event)
            
        except Exception as e:
            self.logger.error(f"Failed to log security event: {e}")
    
    def _generate_event_id(self, request: Request) -> str:
        """Generate unique event ID for request"""
        unique_string = f"{datetime.utcnow().isoformat()}{request.url.path}{self._get_client_ip(request)}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def _calculate_request_risk_score(self, request: Request, response: Response) -> float:
        """Calculate risk score for the request"""
        base_score = 0.1
        
        # Higher risk for certain HTTP methods
        if request.method in ["DELETE", "PUT"]:
            base_score += 0.3
        elif request.method == "POST":
            base_score += 0.2
        
        # Higher risk for error responses
        if response.status_code >= 400:
            base_score += 0.2
        
        # Higher risk for sensitive endpoints
        path = request.url.path.lower()
        if any(keyword in path for keyword in ["admin", "delete", "export", "download"]):
            base_score += 0.3
        
        return min(base_score, 1.0)
    
    def _create_blocked_response(self, reason: str) -> Response:
        """Create response for blocked requests"""
        return Response(
            content=json.dumps({"error": "Access denied", "reason": reason}),
            status_code=403,
            headers={"Content-Type": "application/json"}
        )
    
    def _create_compliance_blocked_response(self, reason: str) -> Response:
        """Create response for compliance-blocked requests"""
        return Response(
            content=json.dumps({"error": "Compliance violation", "reason": reason}),
            status_code=451,  # Unavailable For Legal Reasons
            headers={"Content-Type": "application/json"}
        )
    
    def _create_error_response(self, message: str, status_code: int) -> Response:
        """Create error response"""
        return Response(
            content=json.dumps({"error": message}),
            status_code=status_code,
            headers={"Content-Type": "application/json"}
        )
    
    # Configuration methods
    def add_blocked_ip(self, ip_address: str):
        """Add IP address to blocklist"""
        self.blocked_ips.add(ip_address)
    
    def remove_blocked_ip(self, ip_address: str):
        """Remove IP address from blocklist"""
        self.blocked_ips.discard(ip_address)
    
    def add_allowed_ip_range(self, cidr_range: str):
        """Add IP range to allowlist"""
        try:
            ipaddress.ip_network(cidr_range)  # Validate CIDR format
            self.allowed_ip_ranges.append(cidr_range)
        except ValueError as e:
            raise ValueError(f"Invalid CIDR range: {e}")
    
    def update_security_headers(self, headers: Dict[str, str]):
        """Update security headers"""
        self.security_headers.update(headers)

# Create global security middleware instance
security_middleware = SecurityMiddleware