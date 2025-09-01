#!/usr/bin/env python3
"""
🔐 NQBA Authentication & Authorization System

Provides secure user management, role-based access control, and authentication
for the NQBA ecosystem with absolute control for the founding team.
"""

from .models import (
    User,
    Role,
    Permission,
    UserSession,
    UserCreate,
    UserUpdate,
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
)
from .auth_manager import AuthManager
from .rbac import RoleBasedAccessControl
from .jwt_handler import JWTHandler
from .password_manager import PasswordManager

__all__ = [
    "User",
    "Role",
    "Permission",
    "UserSession",
    "UserCreate",
    "UserUpdate",
    "LoginRequest",
    "LoginResponse",
    "PasswordChangeRequest",
    "AuthManager",
    "RoleBasedAccessControl",
    "JWTHandler",
    "PasswordManager",
]
