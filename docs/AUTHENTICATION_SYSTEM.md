# 🔐 NQBA Authentication System

## Overview

The NQBA Authentication System provides comprehensive user management, role-based access control (RBAC), and secure authentication for the entire NQBA ecosystem. Built with enterprise-grade security, it ensures absolute control for the founding team while providing granular permissions for all users.

## 🏗️ Architecture

### Core Components

1. **AuthManager** - Central orchestrator for all authentication operations
2. **PasswordManager** - Secure password hashing and validation using bcrypt
3. **JWTHandler** - JWT token generation, validation, and management
4. **RoleBasedAccessControl** - Hierarchical role and permission management
5. **User Models** - Comprehensive user data structures

### Security Features

- **bcrypt Password Hashing** - Industry-standard password security
- **JWT Tokens** - Secure stateless authentication
- **Role Hierarchy** - Clear permission inheritance structure
- **Account Locking** - Protection against brute force attacks
- **Session Management** - Secure session tracking and invalidation

## 👥 User Roles & Permissions

### Role Hierarchy

```
Founder (Absolute Control)
├── Executive (High Council)
├── Architect (Technical)
├── Admin (System)
├── Manager (Business Units)
├── User (Regular)
└── Guest (Limited)
```

### Permission Categories

- **SYSTEM** - System-level operations
- **BUSINESS** - Business unit operations
- **ECOSYSTEM** - Ecosystem layer operations
- **DATA** - Data access and manipulation
- **USER** - User management
- **FINANCIAL** - Financial operations
- **QUANTUM** - Quantum operations

### Default System Roles

#### Founder Role
- **Description**: Absolute control over the entire NQBA ecosystem
- **Permissions**: All system permissions
- **Access**: Complete administrative control

#### Executive Role
- **Description**: High council member with strategic oversight
- **Permissions**: All permissions except system-level
- **Access**: Strategic decision-making and oversight

#### Architect Role
- **Description**: Technical architect with system design authority
- **Permissions**: Business, ecosystem, and quantum operations
- **Access**: Technical architecture and quantum operations

#### Admin Role
- **Description**: System administrator with operational control
- **Permissions**: User management, business operations, data access
- **Access**: System administration and user management

#### Manager Role
- **Description**: Business unit manager with operational oversight
- **Permissions**: Business operations and data access
- **Access**: Business unit management

#### User Role
- **Description**: Regular user with basic access
- **Permissions**: Data access only
- **Access**: Basic system functionality

#### Guest Role
- **Description**: Limited access user
- **Permissions**: None
- **Access**: Public endpoints only

## 🚀 Getting Started

### Founder Account

The system automatically creates a founder account with absolute control:

```
Username: founder
Email: founder@nqba.com
Password: Founder@2024!
Status: Active
Role: Founder
```

**⚠️ IMPORTANT**: Change the default password immediately after first login!

### First Login

1. **Access the API**: Navigate to `/api/v1/auth/login`
2. **Use Founder Credentials**:
   ```json
   {
     "username": "founder",
     "password": "Founder@2024!",
     "remember_me": false
   }
   ```
3. **Receive Tokens**: The system returns access and refresh tokens
4. **Change Password**: Use the change password endpoint immediately

## 📡 API Endpoints

### Authentication Endpoints

#### POST `/api/v1/auth/login`
Authenticate user and receive JWT tokens.

**Request Body**:
```json
{
  "username": "your_username",
  "password": "your_password",
  "remember_me": false
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "user_id",
    "username": "your_username",
    "email": "your_email@example.com",
    "first_name": "Your",
    "last_name": "Name",
    "roles": ["role_id"],
    "status": "active"
  }
}
```

#### POST `/api/v1/auth/refresh`
Refresh access token using refresh token.

**Request Body**:
```json
{
  "refresh_token": "your_refresh_token"
}
```

#### POST `/api/v1/auth/logout`
Logout user and invalidate session.

**Headers**: `Authorization: Bearer <access_token>`

#### GET `/api/v1/auth/me`
Get current user information.

**Headers**: `Authorization: Bearer <access_token>`

#### GET `/api/v1/auth/permissions`
Get current user's permissions.

**Headers**: `Authorization: Bearer <access_token>`

### User Management Endpoints

#### POST `/api/v1/auth/users`
Create a new user (requires user creation permission).

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "first_name": "New",
  "last_name": "User",
  "password": "StrongPass123!",
  "roles": ["role_id"],
  "metadata": {
    "department": "engineering",
    "location": "HQ"
  }
}
```

#### GET `/api/v1/auth/users`
Get all users (requires user read permission).

**Headers**: `Authorization: Bearer <access_token>`

#### GET `/api/v1/auth/users/{user_id}`
Get user by ID (requires user read permission).

**Headers**: `Authorization: Bearer <access_token>`

#### PUT `/api/v1/auth/users/{user_id}`
Update user information (requires user update permission).

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "email": "updated@example.com",
  "status": "active"
}
```

#### DELETE `/api/v1/auth/users/{user_id}`
Delete user (requires user delete permission).

**Headers**: `Authorization: Bearer <access_token>`

#### POST `/api/v1/auth/users/{user_id}/change-password`
Change user password (users can only change their own password).

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "current_password": "CurrentPass123!",
  "new_password": "NewStrongPass123!"
}
```

### System Endpoints

#### GET `/api/v1/auth/status`
Get authentication system status (public endpoint).

**Response**:
```json
{
  "total_users": 5,
  "active_users": 3,
  "total_sessions": 2,
  "total_roles": 7,
  "total_permissions": 25,
  "system_roles": ["Founder", "Executive", "Architect", "Admin", "Manager", "User", "Guest"]
}
```

## 🔒 Security Features

### Password Requirements

Passwords must meet the following criteria:
- **Minimum Length**: 8 characters
- **Maximum Length**: 128 characters
- **Character Types Required**:
  - Lowercase letters
  - Uppercase letters
  - Digits
  - Special characters (!@#$%^&*()_+-=[]{}|;:,.<>?)

### Account Protection

- **Failed Login Attempts**: Account locks after 5 failed attempts
- **Lock Duration**: 30 minutes automatic lockout
- **Session Management**: Secure session tokens with expiration
- **Token Refresh**: Automatic token refresh mechanism

### JWT Token Security

- **Access Token Expiry**: 30 minutes
- **Refresh Token Expiry**: 7 days
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Token Types**: Access and refresh tokens with distinct purposes

## 👥 Team Management

### Creating Team Members

1. **Login as Founder**: Use founder credentials to get access token
2. **Create User**: Use the user creation endpoint
3. **Assign Roles**: Choose appropriate role for team member
4. **Activate Account**: Set status to active and verify email

### Role Assignment Examples

#### High Council Member
```json
{
  "username": "executive1",
  "email": "executive@nqba.com",
  "first_name": "Executive",
  "last_name": "Member",
  "password": "ExecPass123!",
  "roles": ["executive_role_id"],
  "metadata": {
    "department": "executive",
    "level": "high_council"
  }
}
```

#### Technical Architect
```json
{
  "username": "architect1",
  "email": "architect@nqba.com",
  "first_name": "Technical",
  "last_name": "Architect",
  "password": "ArchPass123!",
  "roles": ["architect_role_id"],
  "metadata": {
    "department": "engineering",
    "specialization": "quantum_architecture"
  }
}
```

#### Business Unit Manager
```json
{
  "username": "manager1",
  "email": "manager@nqba.com",
  "first_name": "Business",
  "last_name": "Manager",
  "password": "MgrPass123!",
  "roles": ["manager_role_id"],
  "metadata": {
    "department": "operations",
    "business_unit": "flyfox_ai"
  }
}
```

## 🧪 Testing

### Running Authentication Tests

```bash
# Run all authentication tests
pytest tests/test_auth_system.py -v

# Run specific test classes
pytest tests/test_auth_system.py::TestPasswordManager -v
pytest tests/test_auth_system.py::TestJWTHandler -v
pytest tests/test_auth_system.py::TestRoleBasedAccessControl -v
pytest tests/test_auth_system.py::TestAuthManager -v

# Run integration tests
pytest tests/test_auth_system.py::TestAuthIntegration -v
```

### Test Coverage

The authentication system includes comprehensive tests for:
- Password management and validation
- JWT token operations
- Role-based access control
- User lifecycle management
- Security features (account locking, etc.)
- Integration scenarios

## 🚨 Security Best Practices

### For Founders & Administrators

1. **Change Default Password**: Immediately change the founder password
2. **Use Strong Passwords**: Generate strong passwords for all accounts
3. **Regular Role Review**: Periodically review user roles and permissions
4. **Monitor Access**: Regularly check authentication logs
5. **Session Management**: Implement proper session timeout policies

### For Developers

1. **Token Validation**: Always validate JWT tokens on protected endpoints
2. **Permission Checking**: Use permission decorators for endpoint protection
3. **Input Validation**: Validate all user input data
4. **Error Handling**: Don't expose sensitive information in error messages
5. **Logging**: Log all authentication events for audit purposes

### For Users

1. **Password Security**: Use unique, strong passwords
2. **Token Protection**: Keep access tokens secure and don't share them
3. **Regular Updates**: Change passwords regularly
4. **Logout**: Always logout when finished using the system
5. **Report Issues**: Report any suspicious activity immediately

## 🔧 Configuration

### Environment Variables

```bash
# JWT Configuration
SECRET_KEY=your_super_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Security Configuration
PASSWORD_MIN_LENGTH=8
PASSWORD_MAX_LENGTH=128
MAX_LOGIN_ATTEMPTS=5
ACCOUNT_LOCKOUT_DURATION_MINUTES=30

# Session Configuration
SESSION_EXPIRE_DAYS=1
REMEMBER_ME_EXPIRE_DAYS=30
```

### Customization

The authentication system can be customized by:
- Modifying role permissions
- Adding custom permission categories
- Implementing additional security measures
- Customizing password policies
- Adding multi-factor authentication

## 📚 Additional Resources

### API Documentation
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Schema**: `/openapi.json`

### Code Examples
- **Python Client**: See `examples/auth_client.py`
- **JavaScript Client**: See `examples/auth_client.js`
- **cURL Examples**: See `examples/curl_examples.md`

### Support
- **Documentation**: This document and related guides
- **Code Repository**: GitHub repository with source code
- **Issues**: GitHub issues for bug reports and feature requests

## 🎯 Next Steps

1. **Change Founder Password**: Immediately change the default password
2. **Create Team Accounts**: Set up accounts for your team members
3. **Configure Roles**: Assign appropriate roles and permissions
4. **Test Access**: Verify all permissions work correctly
5. **Monitor Usage**: Set up monitoring and alerting

---

**🔐 The NQBA Authentication System gives you absolute control over your platform while maintaining enterprise-grade security for your team and users.**
