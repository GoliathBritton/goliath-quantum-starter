from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import uuid

from ..database import get_db
from ..models.user import User
from ..models.partner import Partner
from ..models.audit_log import AuditLog
from ..auth.jwt_handler import JWTHandler, Token
from ..auth.dependencies import CurrentUser, AdminUser

router = APIRouter()

# Request/Response Models
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str = "qhc"  # Default role
    partner_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    partner_id: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None

@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token."""
    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not JWTHandler.verify_password(user_credentials.password, user.password_hash):
        # Log failed login attempt
        audit_log = AuditLog(
            id=str(uuid.uuid4()),
            user_id=user.id,
            action="login_failed",
            resource_type="auth",
            resource_id=user.id,
            event_metadata={"email": user_credentials.email, "reason": "invalid_password"},
            ip_address="unknown",  # TODO: Extract from request
            user_agent="unknown"   # TODO: Extract from request
        )
        db.add(audit_log)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Log successful login
    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=user.id,
        action="login_success",
        resource_type="auth",
        resource_id=user.id,
        event_metadata={"email": user.email},
        ip_address="unknown",  # TODO: Extract from request
        user_agent="unknown"   # TODO: Extract from request
    )
    db.add(audit_log)
    db.commit()
    
    # Create and return token
    return JWTHandler.create_user_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
        partner_id=user.partner_id
    )

@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate partner_id if provided
    if user_data.partner_id:
        partner = db.query(Partner).filter(Partner.id == user_data.partner_id).first()
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid partner ID"
            )
    
    # Validate role
    valid_roles = ["admin", "partner", "qhc"]
    if user_data.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        )
    
    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        password_hash=JWTHandler.get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        partner_id=user_data.partner_id,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Log user registration
    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=user.id,
        action="user_registered",
        resource_type="user",
        resource_id=user.id,
        event_metadata={"email": user.email, "role": user.role},
        ip_address="unknown",  # TODO: Extract from request
        user_agent="unknown"   # TODO: Extract from request
    )
    db.add(audit_log)
    db.commit()
    
    return user

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser):
    """Get current user information."""
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Update current user information."""
    # Only allow users to update their own basic info
    if user_update.first_name is not None:
        current_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        current_user.last_name = user_update.last_name
    
    # Only admins can change role and active status
    if user_update.role is not None or user_update.is_active is not None:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change role or active status"
            )
        
        if user_update.role is not None:
            valid_roles = ["admin", "partner", "qhc"]
            if user_update.role not in valid_roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                )
            current_user.role = user_update.role
        
        if user_update.is_active is not None:
            current_user.is_active = user_update.is_active
    
    db.commit()
    db.refresh(current_user)
    
    # Log user update
    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        action="user_updated",
        resource_type="user",
        resource_id=current_user.id,
        event_metadata=user_update.dict(exclude_unset=True),
        ip_address="unknown",  # TODO: Extract from request
        user_agent="unknown"   # TODO: Extract from request
    )
    db.add(audit_log)
    db.commit()
    
    return current_user

@router.post("/change-password")
def change_password(
    password_change: PasswordChange,
    current_user: CurrentUser,
    db: Session = Depends(get_db)
):
    """Change user password."""
    # Verify current password
    if not JWTHandler.verify_password(password_change.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = JWTHandler.get_password_hash(password_change.new_password)
    db.commit()
    
    # Log password change
    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        action="password_changed",
        resource_type="user",
        resource_id=current_user.id,
        event_metadata={"email": current_user.email},
        ip_address="unknown",  # TODO: Extract from request
        user_agent="unknown"   # TODO: Extract from request
    )
    db.add(audit_log)
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin_user: AdminUser,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all users (admin only)."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    admin_user: AdminUser,
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_update: UserUpdate,
    admin_user: AdminUser,
    db: Session = Depends(get_db)
):
    """Update user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "role":
            valid_roles = ["admin", "partner", "qhc"]
            if value not in valid_roles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                )
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    # Log user update by admin
    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=admin_user.id,
        action="user_updated_by_admin",
        resource_type="user",
        resource_id=user.id,
        event_metadata={"updated_fields": user_update.dict(exclude_unset=True), "target_user": user.email},
        ip_address="unknown",  # TODO: Extract from request
        user_agent="unknown"   # TODO: Extract from request
    )
    db.add(audit_log)
    db.commit()
    
    return user

@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    admin_user: AdminUser,
    db: Session = Depends(get_db)
):
    """Delete user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Log user deletion
    audit_log = AuditLog(
        id=str(uuid.uuid4()),
        user_id=admin_user.id,
        action="user_deleted",
        resource_type="user",
        resource_id=user.id,
        event_metadata={"deleted_user": user.email, "deleted_by": admin_user.email},
        ip_address="unknown",  # TODO: Extract from request
        user_agent="unknown"   # TODO: Extract from request
    )
    db.add(audit_log)
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}