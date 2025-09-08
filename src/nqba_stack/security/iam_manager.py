"""
IAM Manager for NQBA Ecosystem
Handles identity and access management with org/user roles, API keys, and SSO
"""

import os
import json
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


class RoleLevel(Enum):
    """Role hierarchy levels"""

    OWNER = "owner"
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    BOT = "bot"


class Permission(Enum):
    """System permissions"""

    # Organization management
    ORG_CREATE = "org_create"
    ORG_DELETE = "org_delete"
    ORG_UPDATE = "org_update"
    ORG_VIEW = "org_view"

    # User management
    USER_CREATE = "user_create"
    USER_DELETE = "user_delete"
    USER_UPDATE = "user_update"
    USER_VIEW = "user_view"

    # API management
    API_KEY_CREATE = "api_key_create"
    API_KEY_DELETE = "api_key_delete"
    API_KEY_UPDATE = "api_key_update"
    API_KEY_VIEW = "api_key_view"

    # Data access
    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_DELETE = "data_delete"

    # Quantum operations
    QUANTUM_ACCESS = "quantum_access"
    QUANTUM_ADMIN = "quantum_admin"

    # Business unit operations
    BU_ACCESS = "bu_access"
    BU_ADMIN = "bu_admin"

    # Monitoring and analytics
    MONITORING_VIEW = "monitoring_view"
    ANALYTICS_ACCESS = "analytics_access"


@dataclass
class Organization:
    """Organization entity"""

    org_id: str
    name: str
    domain: str
    created_at: datetime
    owner_id: str
    settings: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True


@dataclass
class User:
    """User entity"""

    user_id: str
    org_id: str
    email: str
    username: str
    role: RoleLevel
    permissions: Set[Permission] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class APIKey:
    """API key with scopes and rate limits"""

    key_id: str
    user_id: str
    org_id: str
    name: str
    key_hash: str
    scopes: Set[Permission] = field(default_factory=set)
    rate_limit_per_minute: int = 100
    rate_limit_per_hour: int = 1000
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    is_active: bool = True
    usage_count: int = 0


@dataclass
class RateLimitTracker:
    """Rate limiting for API keys"""

    key_id: str
    requests_per_minute: List[datetime] = field(default_factory=list)
    requests_per_hour: List[datetime] = field(default_factory=list)


class IAMManager:
    """
    Centralized IAM manager for identity and access management
    Handles organizations, users, roles, permissions, and API keys
    """

    def __init__(self):
        self.organizations: Dict[str, Organization] = {}
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.rate_limit_trackers: Dict[str, RateLimitTracker] = {}
        self.role_permissions: Dict[RoleLevel, Set[Permission]] = {}
        self._initialize_role_permissions()
        self._start_cleanup_task()

    def _initialize_role_permissions(self):
        """Initialize default role permissions"""
        self.role_permissions = {
            RoleLevel.OWNER: {
                Permission.ORG_CREATE,
                Permission.ORG_DELETE,
                Permission.ORG_UPDATE,
                Permission.ORG_VIEW,
                Permission.USER_CREATE,
                Permission.USER_DELETE,
                Permission.USER_UPDATE,
                Permission.USER_VIEW,
                Permission.API_KEY_CREATE,
                Permission.API_KEY_DELETE,
                Permission.API_KEY_UPDATE,
                Permission.API_KEY_VIEW,
                Permission.DATA_READ,
                Permission.DATA_WRITE,
                Permission.DATA_DELETE,
                Permission.QUANTUM_ACCESS,
                Permission.QUANTUM_ADMIN,
                Permission.BU_ACCESS,
                Permission.BU_ADMIN,
                Permission.MONITORING_VIEW,
                Permission.ANALYTICS_ACCESS,
            },
            RoleLevel.ADMIN: {
                Permission.ORG_VIEW,
                Permission.ORG_UPDATE,
                Permission.USER_CREATE,
                Permission.USER_UPDATE,
                Permission.USER_VIEW,
                Permission.API_KEY_CREATE,
                Permission.API_KEY_UPDATE,
                Permission.API_KEY_VIEW,
                Permission.DATA_READ,
                Permission.DATA_WRITE,
                Permission.QUANTUM_ACCESS,
                Permission.BU_ACCESS,
                Permission.BU_ADMIN,
                Permission.MONITORING_VIEW,
                Permission.ANALYTICS_ACCESS,
            },
            RoleLevel.ANALYST: {
                Permission.ORG_VIEW,
                Permission.USER_VIEW,
                Permission.API_KEY_VIEW,
                Permission.DATA_READ,
                Permission.DATA_WRITE,
                Permission.QUANTUM_ACCESS,
                Permission.BU_ACCESS,
                Permission.ANALYTICS_ACCESS,
            },
            RoleLevel.VIEWER: {
                Permission.ORG_VIEW,
                Permission.USER_VIEW,
                Permission.DATA_READ,
                Permission.BU_ACCESS,
            },
            RoleLevel.BOT: {
                Permission.DATA_READ,
                Permission.DATA_WRITE,
                Permission.QUANTUM_ACCESS,
                Permission.BU_ACCESS,
            },
        }

    def create_organization(
        self, name: str, domain: str, owner_email: str, owner_username: str
    ) -> Dict[str, str]:
        """Create a new organization with owner user"""
        # Generate organization ID
        org_id = f"org_{secrets.token_urlsafe(8)}"

        # Create organization
        org = Organization(
            org_id=org_id,
            name=name,
            domain=domain,
            created_at=datetime.now(),
            owner_id="",  # Will be set after user creation
            settings={
                "default_role": RoleLevel.VIEWER.value,
                "require_mfa": True,
                "session_timeout_minutes": 480,
                "max_users": 100,
                "max_api_keys_per_user": 10,
            },
        )

        self.organizations[org_id] = org

        # Create owner user
        owner_user = self.create_user(
            org_id=org_id,
            email=owner_email,
            username=owner_username,
            role=RoleLevel.OWNER,
        )

        # Update organization with owner ID
        org.owner_id = owner_user["user_id"]

        logger.info(f"Created organization {name} with owner {owner_email}")
        return {"org_id": org_id, "user_id": owner_user["user_id"]}

    def create_user(
        self,
        org_id: str,
        email: str,
        username: str,
        role: RoleLevel,
        permissions: Optional[Set[Permission]] = None,
    ) -> Dict[str, str]:
        """Create a new user in an organization"""
        if org_id not in self.organizations:
            raise ValueError(f"Organization {org_id} not found")

        # Check if user already exists
        for user in self.users.values():
            if user.email == email and user.org_id == org_id:
                raise ValueError(
                    f"User {email} already exists in organization {org_id}"
                )

        # Generate user ID
        user_id = f"user_{secrets.token_urlsafe(8)}"

        # Set default permissions based on role
        if permissions is None:
            permissions = self.role_permissions.get(role, set())

        # Create user
        user = User(
            user_id=user_id,
            org_id=org_id,
            email=email,
            username=username,
            role=role,
            permissions=permissions,
        )

        self.users[user_id] = user

        logger.info(
            f"Created user {email} in organization {org_id} with role {role.value}"
        )
        return {"user_id": user_id, "org_id": org_id}

    def update_user_role(self, user_id: str, new_role: RoleLevel) -> bool:
        """Update a user's role and permissions"""
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        old_role = user.role
        user.role = new_role

        # Update permissions based on new role
        user.permissions = self.role_permissions.get(new_role, set())

        logger.info(
            f"Updated user {user_id} role from {old_role.value} to {new_role.value}"
        )
        return True

    def create_api_key(
        self,
        user_id: str,
        name: str,
        scopes: Optional[Set[Permission]] = None,
        rate_limit_per_minute: int = 100,
        rate_limit_per_hour: int = 1000,
        expires_in_days: Optional[int] = None,
    ) -> Dict[str, str]:
        """Create a new API key for a user"""
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")

        user = self.users[user_id]

        # Check if user has permission to create API keys
        if Permission.API_KEY_CREATE not in user.permissions:
            raise PermissionError("User does not have permission to create API keys")

        # Generate API key
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Set default scopes based on user permissions
        if scopes is None:
            scopes = user.permissions.copy()

        # Ensure scopes don't exceed user permissions
        scopes = scopes.intersection(user.permissions)

        # Generate key ID
        key_id = f"key_{secrets.token_urlsafe(8)}"

        # Set expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now() + timedelta(days=expires_in_days)

        # Create API key
        api_key_obj = APIKey(
            key_id=key_id,
            user_id=user_id,
            org_id=user.org_id,
            name=name,
            key_hash=key_hash,
            scopes=scopes,
            rate_limit_per_minute=rate_limit_per_minute,
            rate_limit_per_hour=rate_limit_per_hour,
            expires_at=expires_at,
        )

        self.api_keys[key_id] = api_key_obj

        # Create rate limit tracker
        self.rate_limit_trackers[key_id] = RateLimitTracker(key_id=key_id)

        logger.info(f"Created API key {name} for user {user_id}")
        return {
            "key_id": key_id,
            "api_key": api_key,
            "scopes": [scope.value for scope in scopes],
        }

    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate an API key and return user/org information"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()

        # Find the API key
        for key_id, key_obj in self.api_keys.items():
            if key_obj.key_hash == key_hash and key_obj.is_active:
                # Check expiration
                if key_obj.expires_at and key_obj.expires_at < datetime.now():
                    logger.warning(f"API key {key_id} has expired")
                    continue

                # Update usage
                key_obj.last_used = datetime.now()
                key_obj.usage_count += 1

                # Get user and org info
                user = self.users.get(key_obj.user_id)
                org = self.organizations.get(key_obj.org_id)

                if not user or not org:
                    logger.error(f"Invalid user or org for API key {key_id}")
                    continue

                return {
                    "key_id": key_id,
                    "user_id": key_obj.user_id,
                    "org_id": key_obj.org_id,
                    "scopes": [scope.value for scope in key_obj.scopes],
                    "user_role": user.role.value,
                    "org_name": org.name,
                }

        return None

    def check_rate_limit(self, key_id: str) -> bool:
        """Check if API key is within rate limits"""
        if key_id not in self.rate_limit_trackers:
            return False

        tracker = self.rate_limit_trackers[key_id]
        now = datetime.now()

        # Clean old requests
        tracker.requests_per_minute = [
            req_time
            for req_time in tracker.requests_per_minute
            if now - req_time < timedelta(minutes=1)
        ]

        tracker.requests_per_hour = [
            req_time
            for req_time in tracker.requests_per_hour
            if now - req_time < timedelta(hours=1)
        ]

        # Check limits
        api_key = self.api_keys.get(key_id)
        if not api_key:
            return False

        if (
            len(tracker.requests_per_minute) >= api_key.rate_limit_per_minute
            or len(tracker.requests_per_hour) >= api_key.rate_limit_per_hour
        ):
            return False

        # Add current request
        tracker.requests_per_minute.append(now)
        tracker.requests_per_hour.append(now)

        return True

    def check_permission(self, user_id: str, permission: Permission) -> bool:
        """Check if a user has a specific permission"""
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        return permission in user.permissions

    def get_user_permissions(self, user_id: str) -> Set[Permission]:
        """Get all permissions for a user"""
        if user_id not in self.users:
            return set()

        user = self.users[user_id]
        return user.permissions.copy()

    def get_organization_users(self, org_id: str) -> List[Dict[str, Any]]:
        """Get all users in an organization"""
        if org_id not in self.organizations:
            return []

        users = []
        for user in self.users.values():
            if user.org_id == org_id:
                users.append(
                    {
                        "user_id": user.user_id,
                        "email": user.email,
                        "username": user.username,
                        "role": user.role.value,
                        "permissions": [perm.value for perm in user.permissions],
                        "created_at": user.created_at.isoformat(),
                        "last_login": (
                            user.last_login.isoformat() if user.last_login else None
                        ),
                        "is_active": user.is_active,
                    }
                )

        return users

    def get_user_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all API keys for a user"""
        if user_id not in self.users:
            return []

        keys = []
        for key in self.api_keys.values():
            if key.user_id == user_id:
                keys.append(
                    {
                        "key_id": key.key_id,
                        "name": key.name,
                        "scopes": [scope.value for scope in key.scopes],
                        "rate_limit_per_minute": key.rate_limit_per_minute,
                        "rate_limit_per_hour": key.rate_limit_per_hour,
                        "created_at": key.created_at.isoformat(),
                        "expires_at": (
                            key.expires_at.isoformat() if key.expires_at else None
                        ),
                        "last_used": (
                            key.last_used.isoformat() if key.last_used else None
                        ),
                        "usage_count": key.usage_count,
                        "is_active": key.is_active,
                    }
                )

        return keys

    def revoke_api_key(self, key_id: str, user_id: str) -> bool:
        """Revoke an API key"""
        if key_id not in self.api_keys:
            return False

        key = self.api_keys[key_id]
        if key.user_id != user_id:
            return False

        # Check if user has permission to revoke keys
        user = self.users.get(user_id)
        if not user or Permission.API_KEY_DELETE not in user.permissions:
            return False

        key.is_active = False
        logger.info(f"Revoked API key {key_id} by user {user_id}")
        return True

    def delete_user(self, user_id: str, admin_user_id: str) -> bool:
        """Delete a user (admin only)"""
        if user_id not in self.users:
            return False

        # Check if admin user has permission
        admin_user = self.users.get(admin_user_id)
        if not admin_user or Permission.USER_DELETE not in admin_user.permissions:
            return False

        # Check if trying to delete self
        if user_id == admin_user_id:
            return False

        # Check if trying to delete organization owner
        user = self.users[user_id]
        org = self.organizations.get(user.org_id)
        if org and user.user_id == org.owner_id:
            return False

        # Revoke all API keys for the user
        for key in self.api_keys.values():
            if key.user_id == user_id:
                key.is_active = False

        # Delete user
        del self.users[user_id]

        logger.info(f"Deleted user {user_id} by admin {admin_user_id}")
        return True

    def _start_cleanup_task(self):
        """Start background task to clean up expired API keys and rate limit data"""

        async def cleanup_task():
            while True:
                try:
                    await self._cleanup_expired_keys()
                    await self._cleanup_rate_limit_data()
                    await asyncio.sleep(3600)  # Run every hour
                except Exception as e:
                    logger.error(f"Error in cleanup task: {e}")
                    await asyncio.sleep(300)  # Wait 5 minutes on error

        # Start the background task only if there's a running event loop
        try:
            loop = asyncio.get_running_loop()
            self._cleanup_task = loop.create_task(cleanup_task())
        except RuntimeError:
            # No running event loop, skip background task
            logger.debug("No running event loop, skipping cleanup task")
            self._cleanup_task = None

    async def _cleanup_expired_keys(self):
        """Clean up expired API keys"""
        now = datetime.now()
        expired_keys = []

        for key_id, key in self.api_keys.items():
            if key.expires_at and key.expires_at < now:
                expired_keys.append(key_id)

        for key_id in expired_keys:
            self.api_keys[key_id].is_active = False
            logger.info(f"Deactivated expired API key {key_id}")

    async def _cleanup_rate_limit_data(self):
        """Clean up old rate limit data"""
        now = datetime.now()

        for tracker in self.rate_limit_trackers.values():
            # Keep only last hour of data
            tracker.requests_per_minute = [
                req_time
                for req_time in tracker.requests_per_minute
                if now - req_time < timedelta(hours=1)
            ]
            tracker.requests_per_hour = [
                req_time
                for req_time in tracker.requests_per_hour
                if now - req_time < timedelta(hours=1)
            ]

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        total_orgs = len(self.organizations)
        total_users = len(self.users)
        total_api_keys = len(self.api_keys)
        active_api_keys = sum(1 for key in self.api_keys.values() if key.is_active)

        # Count users by role
        role_counts = {}
        for user in self.users.values():
            role = user.role.value
            role_counts[role] = role_counts.get(role, 0) + 1

        return {
            "total_organizations": total_orgs,
            "total_users": total_users,
            "total_api_keys": total_api_keys,
            "active_api_keys": active_api_keys,
            "users_by_role": role_counts,
            "organizations": [
                {
                    "org_id": org.org_id,
                    "name": org.name,
                    "domain": org.domain,
                    "user_count": sum(
                        1 for user in self.users.values() if user.org_id == org.org_id
                    ),
                }
                for org in self.organizations.values()
            ],
        }


# Global IAM manager instance
iam_manager = IAMManager()
