"""FastAPI Security Endpoints"""

import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, List
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, validator
import logging

from .auth_service import (
    get_auth_service, ZeroTrustAuthService, User, UserRole, SecurityLevel
)
from .oauth2_provider import get_oauth2_service, OAuth2Provider
from .middleware import get_current_user, get_security_context, SecurityContext

# Configure logging
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.VIEWER
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError('Username must be between 3 and 50 characters')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserLogin(BaseModel):
    username: str
    password: str
    remember_me: bool = False
    device_fingerprint: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str]
    role: UserRole
    security_level: SecurityLevel
    mfa_enabled: bool
    created_at: datetime
    last_login: Optional[datetime]

class OAuth2AuthorizeRequest(BaseModel):
    provider: OAuth2Provider
    redirect_uri: Optional[str] = None

class OAuth2CallbackRequest(BaseModel):
    provider: OAuth2Provider
    code: str
    state: str

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserRegistration, request: Request):
    """Register new user"""
    auth_service = get_auth_service()
    
    try:
        # Check if user already exists
        existing_user = auth_service.get_user_by_username(user_data.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        existing_email = auth_service.get_user_by_email(user_data.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        user = auth_service.register_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            role=user_data.role
        )
        
        # Generate tokens
        access_token = auth_service.generate_access_token(user)
        refresh_token = auth_service.generate_refresh_token(user)
        
        # Log registration
        logger.info(f"User registered: {user.username} ({user.email})")
        
        return TokenResponse(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
            expires_in=access_token.expires_in,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "security_level": user.security_level.value
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=TokenResponse)
async def login_user(user_data: UserLogin, request: Request):
    """Authenticate user and return tokens"""
    auth_service = get_auth_service()
    
    try:
        # Authenticate user
        user = auth_service.authenticate_user(
            username=user_data.username,
            password=user_data.password,
            ip_address=request.client.host if request.client else 'unknown',
            user_agent=request.headers.get('user-agent', ''),
            device_fingerprint=user_data.device_fingerprint
        )
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate tokens
        expires_in = 86400 if user_data.remember_me else 3600  # 24h or 1h
        access_token = auth_service.generate_access_token(user, expires_in=expires_in)
        refresh_token = auth_service.generate_refresh_token(user)
        
        # Log successful login
        logger.info(f"User logged in: {user.username} from {request.client.host if request.client else 'unknown'}")
        
        return TokenResponse(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
            expires_in=access_token.expires_in,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "security_level": user.security_level.value,
                "mfa_enabled": user.mfa_enabled
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: RefreshTokenRequest, request: Request):
    """Refresh access token using refresh token"""
    auth_service = get_auth_service()
    
    try:
        # Verify refresh token
        refresh_token = auth_service.verify_refresh_token(token_data.refresh_token)
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        # Get user
        user = auth_service.get_user(refresh_token.user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Generate new access token
        access_token = auth_service.generate_access_token(user)
        
        # Optionally rotate refresh token
        new_refresh_token = refresh_token
        if datetime.now(timezone.utc) > refresh_token.expires_at - timedelta(days=7):
            # Rotate refresh token if it expires within 7 days
            new_refresh_token = auth_service.generate_refresh_token(user)
            auth_service.revoke_token(refresh_token.token)
        
        return TokenResponse(
            access_token=access_token.token,
            refresh_token=new_refresh_token.token,
            expires_in=access_token.expires_in,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "security_level": user.security_level.value
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@router.post("/logout")
async def logout_user(security_context: SecurityContext = Depends(get_security_context)):
    """Logout user and revoke tokens"""
    auth_service = get_auth_service()
    
    try:
        # Revoke current token
        auth_service.revoke_token(security_context.token.token)
        
        # Log logout
        logger.info(f"User logged out: {security_context.user.username}")
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(status_code=500, detail="Logout failed")

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return UserProfile(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        security_level=current_user.security_level,
        mfa_enabled=current_user.mfa_enabled,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )

@router.put("/profile")
async def update_user_profile(
    full_name: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    auth_service = get_auth_service()
    
    try:
        # Update user profile
        updated_user = auth_service.update_user_profile(
            user_id=current_user.id,
            full_name=full_name
        )
        
        return {"message": "Profile updated successfully"}
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(status_code=500, detail="Profile update failed")

@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user)
):
    """Change user password"""
    auth_service = get_auth_service()
    
    try:
        # Verify current password
        if not auth_service.verify_password(password_data.current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Update password
        auth_service.update_password(current_user.id, password_data.new_password)
        
        # Log password change
        logger.info(f"Password changed for user: {current_user.username}")
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        raise HTTPException(status_code=500, detail="Password change failed")

# OAuth2 endpoints
@router.post("/oauth2/authorize")
async def oauth2_authorize(auth_request: OAuth2AuthorizeRequest):
    """Initiate OAuth2 authorization flow"""
    oauth2_service = get_oauth2_service()
    
    try:
        auth_data = oauth2_service.generate_authorization_url(
            provider=auth_request.provider,
            redirect_uri=auth_request.redirect_uri
        )
        
        return {
            "authorization_url": auth_data["authorization_url"],
            "state": auth_data["state"]
        }
        
    except Exception as e:
        logger.error(f"OAuth2 authorization error: {str(e)}")
        raise HTTPException(status_code=500, detail="OAuth2 authorization failed")

@router.post("/oauth2/callback", response_model=TokenResponse)
async def oauth2_callback(callback_data: OAuth2CallbackRequest, request: Request):
    """Handle OAuth2 callback and create/login user"""
    oauth2_service = get_oauth2_service()
    auth_service = get_auth_service()
    
    try:
        # Exchange code for token
        oauth_token = oauth2_service.exchange_code_for_token(
            provider=callback_data.provider,
            authorization_code=callback_data.code,
            state=callback_data.state
        )
        
        # Get user info from OAuth2 provider
        oauth_user = oauth2_service.get_user_info(callback_data.provider, oauth_token)
        
        # Create or update user
        user = oauth2_service.create_or_update_user(oauth_user)
        
        # Check if user exists in our system
        existing_user = auth_service.get_user_by_email(user.email)
        if existing_user:
            user = existing_user
        else:
            # Register new user
            user = auth_service.register_oauth_user(
                username=user.username,
                email=user.email,
                full_name=oauth_user.name,
                role=user.role,
                oauth_provider=callback_data.provider.value,
                oauth_id=oauth_user.provider_id
            )
        
        # Generate tokens
        access_token = auth_service.generate_access_token(user)
        refresh_token = auth_service.generate_refresh_token(user)
        
        # Log OAuth2 login
        logger.info(f"OAuth2 login: {user.username} via {callback_data.provider.value}")
        
        return TokenResponse(
            access_token=access_token.token,
            refresh_token=refresh_token.token,
            expires_in=access_token.expires_in,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value,
                "security_level": user.security_level.value
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth2 callback error: {str(e)}")
        raise HTTPException(status_code=500, detail="OAuth2 authentication failed")

@router.get("/oauth2/providers")
async def get_oauth2_providers():
    """Get available OAuth2 providers"""
    oauth2_service = get_oauth2_service()
    
    providers = []
    for provider in OAuth2Provider:
        if provider in oauth2_service.providers:
            providers.append({
                "name": provider.value,
                "display_name": provider.value.title(),
                "available": True
            })
    
    return {"providers": providers}

@router.get("/verify")
async def verify_token(current_user: User = Depends(get_current_user)):
    """Verify current token and return user info"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "role": current_user.role.value,
            "security_level": current_user.security_level.value
        }
    }

# Health check endpoint
@router.get("/health")
async def auth_health_check():
    """Authentication service health check"""
    return {
        "status": "healthy",
        "service": "authentication",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }