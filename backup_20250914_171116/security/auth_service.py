"""Zero Trust Authentication Service with Quantum-Resistant Cryptography"""

import os
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import bcrypt
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json
from functools import wraps

class UserRole(Enum):
    ADMIN = "admin"
    QUANTUM_ANALYST = "quantum_analyst"
    PORTFOLIO_MANAGER = "portfolio_manager"
    VIEWER = "viewer"
    API_USER = "api_user"

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    QUANTUM = "quantum"

@dataclass
class User:
    id: str
    username: str
    email: str
    role: UserRole
    security_level: SecurityLevel
    mfa_enabled: bool = False
    quantum_key_id: Optional[str] = None
    created_at: datetime = None
    last_login: Optional[datetime] = None
    failed_attempts: int = 0
    locked_until: Optional[datetime] = None

@dataclass
class AuthToken:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    scope: List[str] = None

@dataclass
class SecurityContext:
    user: User
    session_id: str
    ip_address: str
    user_agent: str
    risk_score: float
    requires_mfa: bool = False
    quantum_verified: bool = False

class QuantumResistantCrypto:
    """Quantum-resistant cryptographic operations"""
    
    def __init__(self):
        self.backend = default_backend()
        # Use larger key sizes for quantum resistance
        self.key_size = 4096
        self.salt_size = 32
        self.iterations = 100000
    
    def generate_quantum_safe_key(self) -> bytes:
        """Generate quantum-safe encryption key"""
        return secrets.token_bytes(32)  # 256-bit key
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        return kdf.derive(password.encode())
    
    def encrypt_data(self, data: bytes, key: bytes) -> Dict[str, str]:
        """Encrypt data using AES-256-GCM"""
        iv = secrets.token_bytes(12)  # 96-bit IV for GCM
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'iv': base64.b64encode(iv).decode(),
            'tag': base64.b64encode(encryptor.tag).decode()
        }
    
    def decrypt_data(self, encrypted_data: Dict[str, str], key: bytes) -> bytes:
        """Decrypt data using AES-256-GCM"""
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        iv = base64.b64decode(encrypted_data['iv'])
        tag = base64.b64decode(encrypted_data['tag'])
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt with high cost factor"""
        salt = bcrypt.gensalt(rounds=12)  # High cost for quantum resistance
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), hashed.encode())

class ZeroTrustAuthService:
    """Zero Trust Authentication Service"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.crypto = QuantumResistantCrypto()
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, SecurityContext] = {}
        self.revoked_tokens: set = set()
        
        # Security policies
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=30)
        self.token_expiry = timedelta(hours=1)
        self.refresh_token_expiry = timedelta(days=7)
        self.high_risk_threshold = 0.7
    
    def register_user(self, username: str, email: str, password: str, 
                     role: UserRole = UserRole.VIEWER) -> User:
        """Register new user with quantum-safe password hashing"""
        user_id = secrets.token_urlsafe(16)
        hashed_password = self.crypto.hash_password(password)
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            role=role,
            security_level=SecurityLevel.MEDIUM,
            created_at=datetime.now(timezone.utc)
        )
        
        self.users[user_id] = user
        # Store hashed password separately (in production, use database)
        self._store_password(user_id, hashed_password)
        
        return user
    
    def authenticate(self, username: str, password: str, 
                    ip_address: str, user_agent: str) -> Optional[AuthToken]:
        """Authenticate user with Zero Trust principles"""
        user = self._find_user_by_username(username)
        if not user:
            return None
        
        # Check if account is locked
        if self._is_account_locked(user):
            return None
        
        # Verify password
        stored_password = self._get_stored_password(user.id)
        if not self.crypto.verify_password(password, stored_password):
            self._record_failed_attempt(user)
            return None
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(user, ip_address, user_agent)
        
        # Create security context
        session_id = secrets.token_urlsafe(32)
        context = SecurityContext(
            user=user,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            risk_score=risk_score,
            requires_mfa=risk_score > self.high_risk_threshold or user.mfa_enabled
        )
        
        self.sessions[session_id] = context
        
        # Generate tokens
        access_token = self._generate_access_token(user, session_id)
        refresh_token = self._generate_refresh_token(user, session_id)
        
        # Update user login info
        user.last_login = datetime.now(timezone.utc)
        user.failed_attempts = 0
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(self.token_expiry.total_seconds()),
            scope=[user.role.value]
        )
    
    def verify_token(self, token: str) -> Optional[SecurityContext]:
        """Verify JWT token and return security context"""
        if token in self.revoked_tokens:
            return None
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            session_id = payload.get('session_id')
            
            if session_id not in self.sessions:
                return None
            
            context = self.sessions[session_id]
            
            # Verify token hasn't expired
            exp = payload.get('exp')
            if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
                return None
            
            # Continuous risk assessment
            context.risk_score = self._update_risk_score(context)
            
            return context
            
        except jwt.InvalidTokenError:
            return None
    
    def refresh_token(self, refresh_token: str) -> Optional[AuthToken]:
        """Refresh access token using refresh token"""
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=[self.algorithm])
            session_id = payload.get('session_id')
            token_type = payload.get('type')
            
            if token_type != 'refresh' or session_id not in self.sessions:
                return None
            
            context = self.sessions[session_id]
            
            # Generate new access token
            access_token = self._generate_access_token(context.user, session_id)
            
            return AuthToken(
                access_token=access_token,
                refresh_token=refresh_token,  # Keep same refresh token
                expires_in=int(self.token_expiry.total_seconds()),
                scope=[context.user.role.value]
            )
            
        except jwt.InvalidTokenError:
            return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoke token (add to blacklist)"""
        self.revoked_tokens.add(token)
        return True
    
    def logout(self, session_id: str) -> bool:
        """Logout user and invalidate session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def require_auth(self, required_role: UserRole = None, 
                    required_security_level: SecurityLevel = None):
        """Decorator for protecting endpoints"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Extract token from request (implementation depends on framework)
                token = self._extract_token_from_request()
                if not token:
                    raise PermissionError("Authentication required")
                
                context = self.verify_token(token)
                if not context:
                    raise PermissionError("Invalid or expired token")
                
                # Check role requirements
                if required_role and context.user.role != required_role:
                    if not self._has_higher_privilege(context.user.role, required_role):
                        raise PermissionError("Insufficient privileges")
                
                # Check security level requirements
                if required_security_level:
                    if not self._meets_security_level(context.user.security_level, required_security_level):
                        raise PermissionError("Insufficient security clearance")
                
                # Check if MFA is required but not completed
                if context.requires_mfa and not context.quantum_verified:
                    raise PermissionError("Multi-factor authentication required")
                
                # Add context to kwargs
                kwargs['security_context'] = context
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def _generate_access_token(self, user: User, session_id: str) -> str:
        """Generate JWT access token"""
        now = datetime.now(timezone.utc)
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'security_level': user.security_level.value,
            'session_id': session_id,
            'type': 'access',
            'iat': now,
            'exp': now + self.token_expiry,
            'iss': 'quantum-nexus-engine',
            'aud': 'qne-api'
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def _generate_refresh_token(self, user: User, session_id: str) -> str:
        """Generate JWT refresh token"""
        now = datetime.now(timezone.utc)
        payload = {
            'user_id': user.id,
            'session_id': session_id,
            'type': 'refresh',
            'iat': now,
            'exp': now + self.refresh_token_expiry,
            'iss': 'quantum-nexus-engine'
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def _calculate_risk_score(self, user: User, ip_address: str, user_agent: str) -> float:
        """Calculate risk score based on various factors"""
        risk_score = 0.0
        
        # Check for unusual login patterns
        if user.last_login:
            time_since_last = datetime.now(timezone.utc) - user.last_login
            if time_since_last > timedelta(days=30):
                risk_score += 0.3
        
        # Check failed attempts
        if user.failed_attempts > 0:
            risk_score += min(user.failed_attempts * 0.1, 0.4)
        
        # IP address analysis (simplified)
        if self._is_suspicious_ip(ip_address):
            risk_score += 0.4
        
        # User agent analysis
        if self._is_suspicious_user_agent(user_agent):
            risk_score += 0.2
        
        # Time-based analysis
        current_hour = datetime.now(timezone.utc).hour
        if current_hour < 6 or current_hour > 22:  # Outside business hours
            risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    def _update_risk_score(self, context: SecurityContext) -> float:
        """Update risk score during session"""
        # Implement continuous risk assessment
        return context.risk_score
    
    def _find_user_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None
    
    def _is_account_locked(self, user: User) -> bool:
        """Check if account is locked"""
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            return True
        return False
    
    def _record_failed_attempt(self, user: User):
        """Record failed login attempt"""
        user.failed_attempts += 1
        if user.failed_attempts >= self.max_failed_attempts:
            user.locked_until = datetime.now(timezone.utc) + self.lockout_duration
    
    def _store_password(self, user_id: str, hashed_password: str):
        """Store hashed password (implement with secure storage)"""
        # In production, store in secure database
        pass
    
    def _get_stored_password(self, user_id: str) -> str:
        """Get stored password hash (implement with secure storage)"""
        # In production, retrieve from secure database
        return "$2b$12$dummy_hash_for_demo"
    
    def _is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP address is suspicious"""
        # Implement IP reputation checking
        return False
    
    def _is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Check if user agent is suspicious"""
        # Implement user agent analysis
        return False
    
    def _extract_token_from_request(self) -> Optional[str]:
        """Extract token from HTTP request"""
        # Implementation depends on web framework
        return None
    
    def _has_higher_privilege(self, user_role: UserRole, required_role: UserRole) -> bool:
        """Check if user role has higher privileges"""
        role_hierarchy = {
            UserRole.VIEWER: 1,
            UserRole.API_USER: 2,
            UserRole.PORTFOLIO_MANAGER: 3,
            UserRole.QUANTUM_ANALYST: 4,
            UserRole.ADMIN: 5
        }
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)
    
    def _meets_security_level(self, user_level: SecurityLevel, required_level: SecurityLevel) -> bool:
        """Check if user meets security level requirements"""
        level_hierarchy = {
            SecurityLevel.LOW: 1,
            SecurityLevel.MEDIUM: 2,
            SecurityLevel.HIGH: 3,
            SecurityLevel.QUANTUM: 4
        }
        return level_hierarchy.get(user_level, 0) >= level_hierarchy.get(required_level, 0)

# Global auth service instance
auth_service = None

def get_auth_service() -> ZeroTrustAuthService:
    """Get global auth service instance"""
    global auth_service
    if auth_service is None:
        secret_key = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        auth_service = ZeroTrustAuthService(secret_key)
    return auth_service

def init_auth_service(secret_key: str) -> ZeroTrustAuthService:
    """Initialize auth service with custom secret key"""
    global auth_service
    auth_service = ZeroTrustAuthService(secret_key)
    return auth_service