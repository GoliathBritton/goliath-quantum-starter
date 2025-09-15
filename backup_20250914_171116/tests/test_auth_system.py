#!/usr/bin/env python3
"""
🧪 Authentication System Tests

Comprehensive testing suite for the NQBA authentication system including
user management, role-based access control, and JWT token handling.
"""

import pytest
import pytest_asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.nqba_stack.auth import (
    AuthManager,
    User,
    Role,
    Permission,
    UserSession,
    UserCreate,
    UserUpdate,
    LoginRequest,
    LoginResponse,
    UserStatus,
    RoleLevel,
    PermissionCategory,
)
from src.nqba_stack.auth.password_manager import PasswordManager
from src.nqba_stack.auth.jwt_handler import JWTHandler
from src.nqba_stack.auth.rbac import RoleBasedAccessControl


# Test fixtures
@pytest.fixture
def auth_manager():
    """Create a fresh auth manager for testing"""
    return AuthManager()


@pytest.fixture
def password_manager():
    """Create password manager for testing"""
    return PasswordManager()


@pytest.fixture
def jwt_handler():
    """Create JWT handler for testing"""
    return JWTHandler()


@pytest.fixture
def rbac():
    """Create RBAC instance for testing"""
    return RoleBasedAccessControl()


@pytest.fixture
def sample_user_data():
    """Sample user creation data"""
    return UserCreate(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="TestPass123!",
        roles=[],
        metadata={"department": "engineering"},
    )


@pytest.fixture
def sample_login_data():
    """Sample login data"""
    return LoginRequest(username="testuser", password="TestPass123!", remember_me=False)


# Password Manager Tests
class TestPasswordManager:
    """Test password management functionality"""

    def test_hash_password(self, password_manager):
        """Test password hashing"""
        password = "TestPass123!"
        password_hash, salt = password_manager.hash_password(password)

        assert password_hash is not None
        assert salt is not None
        assert password_hash != password
        assert len(password_hash) > 0
        assert len(salt) > 0

    def test_verify_password(self, password_manager):
        """Test password verification"""
        password = "TestPass123!"
        password_hash, salt = password_manager.hash_password(password)

        # Correct password should verify
        assert password_manager.verify_password(password, password_hash) is True

        # Wrong password should not verify
        assert password_manager.verify_password("WrongPass123!", password_hash) is False

    def test_generate_strong_password(self, password_manager):
        """Test strong password generation"""
        password = password_manager.generate_strong_password()

        assert len(password) == 16
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    def test_validate_password_strength(self, password_manager):
        """Test password strength validation"""
        # Valid password
        is_valid, message = password_manager.validate_password_strength("TestPass123!")
        assert is_valid is True
        assert "meets strength requirements" in message

        # Too short
        is_valid, message = password_manager.validate_password_strength("Test1!")
        assert is_valid is False
        assert "at least 8 characters" in message

        # Missing lowercase
        is_valid, message = password_manager.validate_password_strength("TESTPASS123!")
        assert is_valid is False
        assert "lowercase letter" in message

        # Missing uppercase
        is_valid, message = password_manager.validate_password_strength("testpass123!")
        assert is_valid is False
        assert "uppercase letter" in message

        # Missing digit
        is_valid, message = password_manager.validate_password_strength("TestPass!")
        assert is_valid is False
        assert "digit" in message

        # Missing special character
        is_valid, message = password_manager.validate_password_strength("TestPass123")
        assert is_valid is False
        assert "special character" in message


# JWT Handler Tests
class TestJWTHandler:
    """Test JWT token functionality"""

    @patch("nqba_stack.auth.jwt_handler.get_settings")
    def test_create_access_token(self, mock_settings, jwt_handler):
        """Test access token creation"""
        mock_settings.return_value.SECRET_KEY = "test_secret_key"

        data = {"user_id": "123", "username": "testuser"}
        token = jwt_handler.create_access_token(data)

        assert token is not None
        assert len(token) > 0

    @patch("nqba_stack.auth.jwt_handler.get_settings")
    def test_create_refresh_token(self, mock_settings, jwt_handler):
        """Test refresh token creation"""
        mock_settings.return_value.SECRET_KEY = "test_secret_key"

        data = {"user_id": "123", "username": "testuser"}
        token = jwt_handler.create_refresh_token(data)

        assert token is not None
        assert len(token) > 0

    @patch("nqba_stack.auth.jwt_handler.get_settings")
    def test_create_user_tokens(self, mock_settings, jwt_handler):
        """Test user token creation"""
        mock_settings.return_value.SECRET_KEY = "test_secret_key"

        tokens = jwt_handler.create_user_tokens("123", "testuser", ["user"])

        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert "token_type" in tokens
        assert "expires_in" in tokens
        assert tokens["token_type"] == "bearer"

    def test_generate_session_token(self, jwt_handler):
        """Test session token generation"""
        token = jwt_handler.generate_session_token()

        assert token is not None
        assert len(token) > 0


# RBAC Tests
class TestRoleBasedAccessControl:
    """Test role-based access control functionality"""

    def test_initialize_system_roles(self, rbac):
        """Test system role initialization"""
        assert len(rbac.roles) > 0
        assert len(rbac.permissions) > 0

        # Check for founder role
        founder_role = rbac.get_role_by_name("Founder")
        assert founder_role is not None
        assert founder_role.level == RoleLevel.FOUNDER
        assert founder_role.is_system_role is True

        # Check for executive role
        executive_role = rbac.get_role_by_name("Executive")
        assert executive_role is not None
        assert executive_role.level == RoleLevel.EXECUTIVE

    def test_add_role(self, rbac):
        """Test role addition"""
        new_role = Role(
            name="TestRole",
            level=RoleLevel.USER,
            description="Test role for testing",
            permissions=[],
            is_system_role=False,
        )

        success = rbac.add_role(new_role)
        assert success is True
        assert new_role.id in rbac.roles

        # Try to add duplicate role
        success = rbac.add_role(new_role)
        assert success is False

    def test_get_role(self, rbac):
        """Test role retrieval"""
        # Get existing role
        founder_role = rbac.get_role_by_name("Founder")
        assert founder_role is not None

        retrieved_role = rbac.get_role(founder_role.id)
        assert retrieved_role is not None
        assert retrieved_role.id == founder_role.id

        # Get non-existent role
        non_existent = rbac.get_role("non-existent-id")
        assert non_existent is None

    def test_check_permission(self, rbac):
        """Test permission checking"""
        # Get founder role
        founder_role = rbac.get_role_by_name("Founder")
        assert founder_role is not None

        # Founder should have system admin permission
        has_permission = rbac.check_permission([founder_role.id], "system", "all")
        assert has_permission is True

        # Guest role should not have system admin permission
        guest_role = rbac.get_role_by_name("Guest")
        assert guest_role is not None

        has_permission = rbac.check_permission([guest_role.id], "system", "all")
        assert has_permission is False

    def test_get_user_permissions(self, rbac):
        """Test user permission retrieval"""
        founder_role = rbac.get_role_by_name("Founder")
        assert founder_role is not None

        permissions = rbac.get_user_permissions([founder_role.id])
        assert len(permissions) > 0

        # Check for system admin permission
        system_perms = [p for p in permissions if "system" in p]
        assert len(system_perms) > 0

    def test_can_manage_role(self, rbac):
        """Test role management permissions"""
        founder_role = rbac.get_role_by_name("Founder")
        executive_role = rbac.get_role_by_name("Executive")
        user_role = rbac.get_role_by_name("User")

        assert founder_role is not None
        assert executive_role is not None
        assert user_role is not None

        # Founder can manage executive
        can_manage = rbac.can_manage_role([founder_role.id], executive_role.id)
        assert can_manage is True

        # Executive cannot manage founder
        can_manage = rbac.can_manage_role([executive_role.id], founder_role.id)
        assert can_manage is False

        # User cannot manage executive
        can_manage = rbac.can_manage_role([user_role.id], executive_role.id)
        assert can_manage is False


# Auth Manager Tests
class TestAuthManager:
    """Test authentication manager functionality"""

    def test_initialize_founder_account(self, auth_manager):
        """Test founder account initialization"""
        # Check if founder account exists
        founder_user = None
        for user in auth_manager.users.values():
            if user.username == "founder":
                founder_user = user
                break

        assert founder_user is not None
        assert founder_user.username == "founder"
        assert founder_user.email == "founder@nqba.com"
        assert founder_user.status == UserStatus.ACTIVE
        assert founder_user.is_verified is True

        # Check founder role
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None
        assert founder_role.id in founder_user.roles

    def test_create_user(self, auth_manager):
        """Test user creation"""
        # Get founder role for permissions
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None

        user_data = UserCreate(
            username="newuser",
            email="newuser@example.com",
            first_name="New",
            last_name="User",
            password="NewPass123!",
            roles=[founder_role.id],
            metadata={"department": "engineering"},
        )

        success, message, user = auth_manager.create_user(user_data, [founder_role.id])

        assert success is True
        assert user is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.status == UserStatus.PENDING  # New users start as pending

    def test_create_user_duplicate_username(self, auth_manager):
        """Test user creation with duplicate username"""
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None

        # Create first user
        user_data1 = UserCreate(
            username="duplicate",
            email="user1@example.com",
            first_name="User",
            last_name="One",
            password="Pass123!",
            roles=[founder_role.id],
        )

        success1, message1, user1 = auth_manager.create_user(
            user_data1, [founder_role.id]
        )
        assert success1 is True

        # Try to create second user with same username
        user_data2 = UserCreate(
            username="duplicate",
            email="user2@example.com",
            first_name="User",
            last_name="Two",
            password="Pass123!",
            roles=[founder_role.id],
        )

        success2, message2, user2 = auth_manager.create_user(
            user_data2, [founder_role.id]
        )
        assert success2 is False
        assert "Username already exists" in message2

    def test_authenticate_user(self, auth_manager):
        """Test user authentication"""
        # Get founder role
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None

        # Create a test user
        user_data = UserCreate(
            username="authuser",
            email="authuser@example.com",
            first_name="Auth",
            last_name="User",
            password="AuthPass123!",
            roles=[founder_role.id],
        )

        success, message, user = auth_manager.create_user(user_data, [founder_role.id])
        assert success is True

        # Activate the user
        user.status = UserStatus.ACTIVE
        user.is_verified = True

        # Test login
        login_data = LoginRequest(
            username="authuser", password="AuthPass123!", remember_me=False
        )

        success, message, response = auth_manager.authenticate_user(login_data)
        assert success is True
        assert response is not None
        assert response.access_token is not None
        assert response.refresh_token is not None
        assert response.user.username == "authuser"

    def test_authenticate_user_invalid_password(self, auth_manager):
        """Test authentication with invalid password"""
        # Get founder role
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None

        # Create a test user
        user_data = UserCreate(
            username="invalidpass",
            email="invalidpass@example.com",
            first_name="Invalid",
            last_name="Pass",
            password="ValidPass123!",
            roles=[founder_role.id],
        )

        success, message, user = auth_manager.create_user(user_data, [founder_role.id])
        assert success is True

        # Activate the user
        user.status = UserStatus.ACTIVE
        user.is_verified = True

        # Test login with wrong password
        login_data = LoginRequest(
            username="invalidpass", password="WrongPass123!", remember_me=False
        )

        success, message, response = auth_manager.authenticate_user(login_data)
        assert success is False
        assert "Invalid username or password" in message
        assert response is None

    def test_account_locking(self, auth_manager):
        """Test account locking after failed attempts"""
        # Get founder role
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None

        # Create a test user
        user_data = UserCreate(
            username="lockuser",
            email="lockuser@example.com",
            first_name="Lock",
            last_name="User",
            password="LockPass123!",
            roles=[founder_role.id],
        )

        success, message, user = auth_manager.create_user(user_data, [founder_role.id])
        assert success is True

        # Activate the user
        user.status = UserStatus.ACTIVE
        user.is_verified = True

        # Try to login with wrong password multiple times
        login_data = LoginRequest(
            username="lockuser", password="WrongPass123!", remember_me=False
        )

        # First 4 attempts should fail but not lock
        for i in range(4):
            success, message, response = auth_manager.authenticate_user(login_data)
            assert success is False
            assert user.login_attempts == i + 1
            assert user.status == UserStatus.ACTIVE

        # 5th attempt should lock the account
        success, message, response = auth_manager.authenticate_user(login_data)
        assert success is False
        assert "Account locked" in message
        assert user.status == UserStatus.LOCKED
        assert user.locked_until is not None

    def test_get_system_status(self, auth_manager):
        """Test system status retrieval"""
        status_info = auth_manager.get_system_status()

        assert "total_users" in status_info
        assert "active_users" in status_info
        assert "total_sessions" in status_info
        assert "total_roles" in status_info
        assert "total_permissions" in status_info
        assert "system_roles" in status_info

        assert status_info["total_users"] > 0  # At least founder account
        assert status_info["total_roles"] > 0
        assert status_info["total_permissions"] > 0
        assert len(status_info["system_roles"]) > 0


# Integration Tests
class TestAuthIntegration:
    """Test authentication system integration"""

    def test_full_user_lifecycle(self, auth_manager):
        """Test complete user lifecycle from creation to deletion"""
        # Get founder role
        founder_role = auth_manager.rbac.get_role_by_name("Founder")
        assert founder_role is not None

        # 1. Create user
        user_data = UserCreate(
            username="lifecycle",
            email="lifecycle@example.com",
            first_name="Life",
            last_name="Cycle",
            password="LifePass123!",
            roles=[founder_role.id],
        )

        success, message, user = auth_manager.create_user(user_data, [founder_role.id])
        assert success is True
        assert user.username == "lifecycle"

        # 2. Activate user
        user.status = UserStatus.ACTIVE
        user.is_verified = True

        # 3. Login user
        login_data = LoginRequest(
            username="lifecycle", password="LifePass123!", remember_me=False
        )

        success, message, response = auth_manager.authenticate_user(login_data)
        assert success is True
        assert response.access_token is not None

        # 4. Update user
        updates = UserUpdate(first_name="Updated", last_name="Name")
        success, message = auth_manager.update_user(user.id, updates, [founder_role.id])
        assert success is True

        # 5. Verify update
        success, message, updated_user = auth_manager.get_user_by_id(
            user.id, [founder_role.id]
        )
        assert success is True
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"

        # 6. Delete user
        success, message = auth_manager.delete_user(user.id, [founder_role.id])
        assert success is True

        # 7. Verify deletion
        success, message, deleted_user = auth_manager.get_user_by_id(
            user.id, [founder_role.id]
        )
        assert success is False
        assert "User not found" in message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
