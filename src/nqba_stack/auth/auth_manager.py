#!/usr/bin/env python3
"""
🔐 Authentication Manager

Central orchestrator for user management, authentication, and authorization
in the NQBA ecosystem with absolute control for the founding team.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from .models import (
    User, Role, UserSession, UserCreate, UserUpdate, 
    UserStatus, RoleLevel, LoginRequest, LoginResponse
)
from .password_manager import PasswordManager
from .jwt_handler import JWTHandler
from .rbac import RoleBasedAccessControl
from ..core.ltc_automation import LTCLogger

class AuthManager:
    """Central authentication and authorization manager"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, UserSession] = {}
        self.password_manager = PasswordManager()
        self.jwt_handler = JWTHandler()
        self.rbac = RoleBasedAccessControl()
        self.logger = LTCLogger("auth_manager")
        
        # Initialize with founder account
        self._initialize_founder_account()
    
    def _initialize_founder_account(self):
        """Initialize the founder account with absolute control"""
        founder_role = self.rbac.get_role_by_name("Founder")
        if not founder_role:
            self.logger.error("Founder role not found during initialization")
            return
        
        # Create founder user (you)
        founder_user = User(
            username="founder",
            email="founder@nqba.com",
            first_name="Founder",
            last_name="NQBA",
            roles=[founder_role.id],
            status=UserStatus.ACTIVE,
            is_verified=True
        )
        
        # Set founder password (you'll change this)
        password_hash, salt = self.password_manager.hash_password("Founder@2024!")
        founder_user.password_hash = password_hash
        founder_user.salt = salt
        
        self.users[founder_user.id] = founder_user
        self.logger.info(f"Founder account initialized: {founder_user.username}")
    
    def create_user(self, user_data: UserCreate, creator_roles: List[str]) -> Tuple[bool, str, Optional[User]]:
        """
        Create a new user
        
        Args:
            user_data: User creation data
            creator_roles: Roles of the user creating this account
            
        Returns:
            Tuple of (success, message, user_object)
        """
        # Check if creator has permission to create users
        if not self.rbac.check_permission(creator_roles, "users", "create"):
            return False, "Insufficient permissions to create users", None
        
        # Validate username uniqueness
        if any(user.username == user_data.username for user in self.users.values()):
            return False, "Username already exists", None
        
        # Validate email uniqueness
        if any(user.email == user_data.email for user in self.users.values()):
            return False, "Email already exists", None
        
        # Validate password strength
        is_valid, message = self.password_manager.validate_password_strength(user_data.password)
        if not is_valid:
            return False, f"Password validation failed: {message}", None
        
        # Hash password
        password_hash, salt = self.password_manager.hash_password(user_data.password)
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=password_hash,
            salt=salt,
            roles=user_data.roles,
            metadata=user_data.metadata
        )
        
        # Validate roles
        for role_id in user.roles:
            if not self.rbac.get_role(role_id):
                return False, f"Invalid role ID: {role_id}", None
        
        self.users[user.id] = user
        self.logger.info(f"User created: {user.username} by user with roles: {creator_roles}")
        
        return True, "User created successfully", user
    
    def authenticate_user(self, login_data: LoginRequest) -> Tuple[bool, str, Optional[LoginResponse]]:
        """
        Authenticate user login
        
        Args:
            login_data: Login credentials
            
        Returns:
            Tuple of (success, message, login_response)
        """
        # Find user by username
        user = None
        for u in self.users.values():
            if u.username == login_data.username:
                user = u
                break
        
        if not user:
            return False, "Invalid username or password", None
        
        # Check if account is locked
        if user.status == UserStatus.LOCKED:
            if user.locked_until and datetime.utcnow() < user.locked_until:
                return False, "Account is temporarily locked", None
            else:
                # Unlock account
                user.status = UserStatus.ACTIVE
                user.login_attempts = 0
                user.locked_until = None
        
        # Check if account is active
        if user.status != UserStatus.ACTIVE:
            return False, "Account is not active", None
        
        # Verify password
        if not self.password_manager.verify_password(login_data.password, user.password_hash):
            user.login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.login_attempts >= 5:
                user.status = UserStatus.LOCKED
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                self.logger.warning(f"Account locked for user: {user.username}")
                return False, "Account locked due to multiple failed login attempts", None
            
            return False, "Invalid username or password", None
        
        # Reset login attempts on successful login
        user.login_attempts = 0
        user.last_login = datetime.utcnow()
        
        # Create session
        session_token = self.jwt_handler.generate_session_token()
        session = UserSession(
            user_id=user.id,
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(days=1 if login_data.remember_me else 1)
        )
        
        self.sessions[session.id] = session
        
        # Generate JWT tokens
        tokens = self.jwt_handler.create_user_tokens(
            user_id=user.id,
            username=user.username,
            roles=user.roles
        )
        
        # Create login response
        response = LoginResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=tokens["expires_in"],
            user=user
        )
        
        self.logger.info(f"User authenticated successfully: {user.username}")
        return True, "Authentication successful", response
    
    def refresh_token(self, refresh_token: str) -> Tuple[bool, str, Optional[Dict[str, str]]]:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Tuple of (success, message, new_tokens)
        """
        # Verify refresh token
        payload = self.jwt_handler.verify_token(refresh_token, "refresh")
        if not payload:
            return False, "Invalid or expired refresh token", None
        
        # Get user
        user_id = payload.get("sub")
        user = self.users.get(user_id)
        if not user or user.status != UserStatus.ACTIVE:
            return False, "User not found or inactive", None
        
        # Generate new tokens
        tokens = self.jwt_handler.create_user_tokens(
            user_id=user.id,
            username=user.username,
            roles=user.roles
        )
        
        return True, "Token refreshed successfully", tokens
    
    def validate_token(self, token: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Validate JWT token and return user info
        
        Args:
            token: JWT token to validate
            
        Returns:
            Tuple of (success, message, user_payload)
        """
        payload = self.jwt_handler.verify_token(token, "access")
        if not payload:
            return False, "Invalid or expired token", None
        
        # Get user
        user_id = payload.get("sub")
        user = self.users.get(user_id)
        if not user or user.status != UserStatus.ACTIVE:
            return False, "User not found or inactive", None
        
        return True, "Token valid", payload
    
    def check_permission(self, token: str, resource: str, action: str) -> Tuple[bool, str]:
        """
        Check if user has permission for a specific resource and action
        
        Args:
            token: JWT token
            resource: Resource to access
            action: Action to perform
            
        Returns:
            Tuple of (has_permission, message)
        """
        # Validate token
        success, message, payload = self.validate_token(token)
        if not success:
            return False, message
        
        # Get user roles
        user_id = payload.get("sub")
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"
        
        # Check permission
        has_permission = self.rbac.check_permission(user.roles, resource, action)
        
        if has_permission:
            return True, "Permission granted"
        else:
            return False, "Insufficient permissions"
    
    def update_user(self, user_id: str, updates: UserUpdate, updater_roles: List[str]) -> Tuple[bool, str]:
        """
        Update user information
        
        Args:
            user_id: ID of user to update
            updates: Update data
            updater_roles: Roles of the user making the update
            
        Returns:
            Tuple of (success, message)
        """
        # Check if updater has permission
        if not self.rbac.check_permission(updater_roles, "users", "update"):
            return False, "Insufficient permissions to update users"
        
        # Get user to update
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"
        
        # Check if updater can manage this user's roles
        if updates.roles and not self.rbac.can_manage_role(updater_roles, user_id):
            return False, "Cannot modify user roles"
        
        # Apply updates
        for field, value in updates.dict(exclude_unset=True).items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        
        self.logger.info(f"User updated: {user.username} by user with roles: {updater_roles}")
        return True, "User updated successfully"
    
    def delete_user(self, user_id: str, deleter_roles: List[str]) -> Tuple[bool, str]:
        """
        Delete a user
        
        Args:
            user_id: ID of user to delete
            deleter_roles: Roles of the user making the deletion
            
        Returns:
            Tuple of (success, message)
        """
        # Check if deleter has permission
        if not self.rbac.check_permission(deleter_roles, "users", "delete"):
            return False, "Insufficient permissions to delete users"
        
        # Get user to delete
        user = self.users.get(user_id)
        if not user:
            return False, "User not found"
        
        # Cannot delete founder account
        if "founder" in user.username.lower():
            return False, "Cannot delete founder account"
        
        # Check if deleter can manage this user
        if not self.rbac.can_manage_role(deleter_roles, user_id):
            return False, "Cannot delete user with higher role level"
        
        # Delete user
        del self.users[user_id]
        
        # Clean up sessions
        sessions_to_remove = [s_id for s_id, session in self.sessions.items() if session.user_id == user_id]
        for s_id in sessions_to_remove:
            del self.sessions[s_id]
        
        self.logger.info(f"User deleted: {user.username} by user with roles: {deleter_roles}")
        return True, "User deleted successfully"
    
    def get_user_by_id(self, user_id: str, requester_roles: List[str]) -> Tuple[bool, str, Optional[User]]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            requester_roles: Roles of the user making the request
            
        Returns:
            Tuple of (success, message, user)
        """
        # Check if requester has permission
        if not self.rbac.check_permission(requester_roles, "users", "read"):
            return False, "Insufficient permissions to view users", None
        
        user = self.users.get(user_id)
        if not user:
            return False, "User not found", None
        
        return True, "User retrieved successfully", user
    
    def get_all_users(self, requester_roles: List[str]) -> Tuple[bool, str, List[User]]:
        """
        Get all users
        
        Args:
            requester_roles: Roles of the user making the request
            
        Returns:
            Tuple of (success, message, users)
        """
        # Check if requester has permission
        if not self.rbac.check_permission(requester_roles, "users", "read"):
            return False, "Insufficient permissions to view users", []
        
        users = list(self.users.values())
        return True, "Users retrieved successfully", users
    
    def logout(self, token: str) -> Tuple[bool, str]:
        """
        Logout user and invalidate session
        
        Args:
            token: JWT token
            
        Returns:
            Tuple of (success, message)
        """
        # Validate token
        success, message, payload = self.validate_token(token)
        if not success:
            return False, message
        
        # Invalidate all sessions for user
        user_id = payload.get("sub")
        sessions_to_remove = [s_id for s_id, session in self.sessions.items() if session.user_id == user_id]
        
        for s_id in sessions_to_remove:
            del self.sessions[s_id]
        
        self.logger.info(f"User logged out: {user_id}")
        return True, "Logout successful"
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get system authentication status
        
        Returns:
            System status information
        """
        return {
            "total_users": len(self.users),
            "active_users": len([u for u in self.users.values() if u.status == UserStatus.ACTIVE]),
            "total_sessions": len(self.sessions),
            "total_roles": len(self.rbac.roles),
            "total_permissions": len(self.rbac.permissions),
            "system_roles": [role.name for role in self.rbac.roles.values() if role.is_system_role]
        }
