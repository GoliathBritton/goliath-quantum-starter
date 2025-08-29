#!/usr/bin/env python3
"""
🔐 User Authentication Models

Defines the core data models for user management, roles, permissions,
and sessions in the NQBA ecosystem.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel, Field

class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"
    LOCKED = "locked"

class RoleLevel(str, Enum):
    """Role hierarchy levels"""
    FOUNDER = "founder"           # Absolute control - you
    EXECUTIVE = "executive"        # High council members
    ARCHITECT = "architect"        # Technical architects
    ADMIN = "admin"               # System administrators
    MANAGER = "manager"           # Business unit managers
    USER = "user"                 # Regular users
    GUEST = "guest"               # Limited access

class PermissionCategory(str, Enum):
    """Permission categories"""
    SYSTEM = "system"             # System-level operations
    BUSINESS = "business"         # Business unit operations
    ECOSYSTEM = "ecosystem"       # Ecosystem layer operations
    DATA = "data"                 # Data access and manipulation
    USER = "user"                 # User management
    FINANCIAL = "financial"       # Financial operations
    QUANTUM = "quantum"           # Quantum operations

class Permission(BaseModel):
    """Individual permission definition"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    category: PermissionCategory
    description: str
    resource: str                  # Resource this permission applies to
    action: str                   # Action allowed (read, write, delete, etc.)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Role(BaseModel):
    """Role definition with permissions"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    level: RoleLevel
    description: str
    permissions: List[str] = Field(default_factory=list)  # Permission IDs
    is_system_role: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserSession(BaseModel):
    """User session tracking"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    session_token: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    is_active: bool = True
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class User(BaseModel):
    """User account model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str
    salt: str
    roles: List[str] = Field(default_factory=list)  # Role IDs
    status: UserStatus = UserStatus.PENDING
    is_verified: bool = False
    is_2fa_enabled: bool = False
    two_fa_secret: Optional[str] = None
    last_login: Optional[datetime] = None
    login_attempts: int = 0
    locked_until: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, str] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserCreate(BaseModel):
    """User creation request"""
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    roles: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)

class UserUpdate(BaseModel):
    """User update request"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[List[str]] = None
    status: Optional[UserStatus] = None
    is_2fa_enabled: Optional[bool] = None
    metadata: Optional[Dict[str, str]] = None

class LoginRequest(BaseModel):
    """Login request"""
    username: str
    password: str
    remember_me: bool = False

class LoginResponse(BaseModel):
    """Login response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: User

class PasswordChangeRequest(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str

class TwoFactorSetup(BaseModel):
    """2FA setup request"""
    secret: str
    code: str
