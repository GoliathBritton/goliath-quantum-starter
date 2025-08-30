#!/usr/bin/env python3
"""
🔐 Authentication API Router

Provides secure endpoints for user authentication, authorization,
and management in the NQBA ecosystem.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

from ..auth import (
    AuthManager,
    User,
    UserCreate,
    UserUpdate,
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
)
from ..core.ltc_automation import LTCLogger

# Initialize router and dependencies
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()
logger = LTCLogger("auth_api")

# Global auth manager instance
auth_manager = AuthManager()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Dependency to get current authenticated user from JWT token

    Args:
        credentials: HTTP authorization credentials

    Returns:
        User payload from JWT token

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    success, message, payload = auth_manager.validate_token(token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def require_permission(resource: str, action: str):
    """
    Decorator to require specific permission for endpoint access

    Args:
        resource: Resource to access
        action: Action to perform

    Returns:
        Permission check function
    """

    def permission_checker(current_user: dict = Depends(get_current_user)):
        token = current_user.get("token", "")
        success, message = auth_manager.check_permission(token, resource, action)

        if not success:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

        return current_user

    return permission_checker


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """
    Authenticate user and return JWT tokens

    Args:
        login_data: Login credentials

    Returns:
        Login response with access and refresh tokens
    """
    try:
        success, message, response = auth_manager.authenticate_user(login_data)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=message
            )

        logger.info(f"User login successful: {login_data.username}")
        return response

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication",
        )


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token

    Args:
        refresh_token: Refresh token

    Returns:
        New access and refresh tokens
    """
    try:
        success, message, tokens = auth_manager.refresh_token(refresh_token)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=message
            )

        logger.info("Token refreshed successfully")
        return {"message": message, "tokens": tokens}

    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh",
        )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout user and invalidate session

    Args:
        current_user: Current authenticated user

    Returns:
        Logout confirmation
    """
    try:
        # Extract token from current user context
        token = current_user.get("token", "")
        success, message = auth_manager.logout(token)

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        logger.info(f"User logout successful: {current_user.get('username')}")
        return {"message": message}

    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout",
        )


@router.post("/users", response_model=User)
async def create_user(
    user_data: UserCreate,
    current_user: dict = Depends(require_permission("users", "create")),
):
    """
    Create a new user (requires user creation permission)

    Args:
        user_data: User creation data
        current_user: Current authenticated user with permissions

    Returns:
        Created user object
    """
    try:
        success, message, user = auth_manager.create_user(
            user_data, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        logger.info(f"User created successfully: {user.username}")
        return user

    except Exception as e:
        logger.error(f"User creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user creation",
        )


@router.get("/users", response_model=List[User])
async def get_users(current_user: dict = Depends(require_permission("users", "read"))):
    """
    Get all users (requires user read permission)

    Args:
        current_user: Current authenticated user with permissions

    Returns:
        List of all users
    """
    try:
        success, message, users = auth_manager.get_all_users(
            current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        return users

    except Exception as e:
        logger.error(f"Get users error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving users",
        )


@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str, current_user: dict = Depends(require_permission("users", "read"))
):
    """
    Get user by ID (requires user read permission)

    Args:
        user_id: User ID to retrieve
        current_user: Current authenticated user with permissions

    Returns:
        User object
    """
    try:
        success, message, user = auth_manager.get_user_by_id(
            user_id, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

        return user

    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving user",
        )


@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_updates: UserUpdate,
    current_user: dict = Depends(require_permission("users", "update")),
):
    """
    Update user information (requires user update permission)

    Args:
        user_id: User ID to update
        user_updates: User update data
        current_user: Current authenticated user with permissions

    Returns:
        Updated user object
    """
    try:
        success, message = auth_manager.update_user(
            user_id, user_updates, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        # Get updated user
        success, message, user = auth_manager.get_user_by_id(
            user_id, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found after update",
            )

        logger.info(f"User updated successfully: {user_id}")
        return user

    except Exception as e:
        logger.error(f"Update user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating user",
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str, current_user: dict = Depends(require_permission("users", "delete"))
):
    """
    Delete user (requires user delete permission)

    Args:
        user_id: User ID to delete
        current_user: Current authenticated user with permissions

    Returns:
        Deletion confirmation
    """
    try:
        success, message = auth_manager.delete_user(
            user_id, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        logger.info(f"User deleted successfully: {user_id}")
        return {"message": message}

    except Exception as e:
        logger.error(f"Delete user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting user",
        )


@router.post("/users/{user_id}/change-password")
async def change_password(
    user_id: str,
    password_data: PasswordChangeRequest,
    current_user: dict = Depends(get_current_user),
):
    """
    Change user password (users can only change their own password)

    Args:
        user_id: User ID to change password for
        password_data: Password change data
        current_user: Current authenticated user

    Returns:
        Password change confirmation
    """
    try:
        # Users can only change their own password
        if current_user.get("sub") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only change your own password",
            )

        # Get user to verify current password
        success, message, user = auth_manager.get_user_by_id(
            user_id, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

        # Verify current password
        if not auth_manager.password_manager.verify_password(
            password_data.current_password, user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )

        # Validate new password strength
        is_valid, validation_message = (
            auth_manager.password_manager.validate_password_strength(
                password_data.new_password
            )
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"New password validation failed: {validation_message}",
            )

        # Hash new password
        new_password_hash, new_salt = auth_manager.password_manager.hash_password(
            password_data.new_password
        )

        # Update user password
        user_updates = UserUpdate()
        user_updates.password_hash = new_password_hash
        user_updates.salt = new_salt

        success, message = auth_manager.update_user(
            user_id, user_updates, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

        logger.info(f"Password changed successfully for user: {user_id}")
        return {"message": "Password changed successfully"}

    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while changing password",
        )


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information

    Args:
        current_user: Current authenticated user

    Returns:
        Current user object
    """
    try:
        user_id = current_user.get("sub")
        success, message, user = auth_manager.get_user_by_id(
            user_id, current_user.get("roles", [])
        )

        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

        return user

    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving user information",
        )


@router.get("/permissions")
async def get_user_permissions(current_user: dict = Depends(get_current_user)):
    """
    Get current user's permissions

    Args:
        current_user: Current authenticated user

    Returns:
        User permissions
    """
    try:
        user_id = current_user.get("sub")
        user = auth_manager.users.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        permissions = auth_manager.rbac.get_user_permissions(user.roles)

        return {
            "user_id": user_id,
            "username": user.username,
            "roles": user.roles,
            "permissions": list(permissions),
        }

    except Exception as e:
        logger.error(f"Get permissions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving permissions",
        )


@router.get("/status")
async def get_auth_status():
    """
    Get authentication system status (public endpoint)

    Returns:
        Authentication system status
    """
    try:
        status_info = auth_manager.get_system_status()
        return status_info

    except Exception as e:
        logger.error(f"Get auth status error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving system status",
        )
