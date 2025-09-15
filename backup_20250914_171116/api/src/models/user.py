from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class User(Base):
    """User model for authentication and role-based access control."""
    
    __tablename__ = "users"
    
    # Partner relationship (nullable for system admins)
    partner_id: Mapped[Optional[str]] = mapped_column(ForeignKey("partners.id"), nullable=True, index=True)
    
    # Basic Information
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Authentication
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Nullable for OAuth-only users
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Role & Permissions
    role: Mapped[str] = mapped_column(String(50), default="user", nullable=False)  # admin, partner_admin, user, viewer
    permissions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # Custom permissions array
    
    # Profile Information
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="UTC")
    language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default="en")
    
    # Avatar & Preferences
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # OAuth Integration
    oauth_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # google, microsoft, github
    oauth_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    oauth_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Security & Session Management
    last_login_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv6 support
    failed_login_attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Two-Factor Authentication
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    two_factor_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    backup_codes: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    
    # Email Verification & Password Reset
    email_verification_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email_verification_expires: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    password_reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_reset_expires: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # API Access
    api_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    api_key_expires: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Onboarding & Training
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarding_step: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    training_completed: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # List of completed training modules
    
    # Compliance & Audit
    terms_accepted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    privacy_accepted_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    gdpr_consent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    # partner = relationship("Partner", back_populates="users")
    # oracle_queries = relationship("OracleQuery", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
    
    @property
    def full_name(self) -> str:
        """Get full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role in ["admin", "partner_admin"]
    
    @property
    def is_partner_admin(self) -> bool:
        """Check if user is a partner administrator."""
        return self.role == "partner_admin"
    
    @property
    def is_system_admin(self) -> bool:
        """Check if user is a system administrator."""
        return self.role == "admin"
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is locked."""
        if not self.locked_until:
            return False
        return datetime.utcnow() < self.locked_until
    
    @property
    def can_login(self) -> bool:
        """Check if user can log in."""
        return (
            self.is_active and 
            self.is_verified and 
            not self.is_locked and
            not self.is_deleted
        )
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        if self.is_system_admin:
            return True
        
        if not self.permissions:
            return False
        
        return permission in self.permissions
    
    def add_permission(self, permission: str) -> None:
        """Add permission to user."""
        if not self.permissions:
            self.permissions = []
        
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: str) -> None:
        """Remove permission from user."""
        if self.permissions and permission in self.permissions:
            self.permissions.remove(permission)
    
    def record_login(self, ip_address: str) -> None:
        """Record successful login."""
        self.last_login_at = datetime.utcnow()
        self.last_login_ip = ip_address
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def record_failed_login(self, max_attempts: int = 5, lockout_minutes: int = 30) -> None:
        """Record failed login attempt and lock if necessary."""
        self.failed_login_attempts += 1
        
        if self.failed_login_attempts >= max_attempts:
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=lockout_minutes)
    
    def unlock_account(self) -> None:
        """Unlock user account."""
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.email_verification_token = None
        self.email_verification_expires = None
    
    def set_password_reset_token(self, token: str, expires_hours: int = 24) -> None:
        """Set password reset token."""
        from datetime import timedelta
        self.password_reset_token = token
        self.password_reset_expires = datetime.utcnow() + timedelta(hours=expires_hours)
    
    def clear_password_reset_token(self) -> None:
        """Clear password reset token."""
        self.password_reset_token = None
        self.password_reset_expires = None
    
    def set_email_verification_token(self, token: str, expires_hours: int = 48) -> None:
        """Set email verification token."""
        from datetime import timedelta
        self.email_verification_token = token
        self.email_verification_expires = datetime.utcnow() + timedelta(hours=expires_hours)
    
    def accept_terms(self) -> None:
        """Record terms acceptance."""
        self.terms_accepted_at = datetime.utcnow()
    
    def accept_privacy(self) -> None:
        """Record privacy policy acceptance."""
        self.privacy_accepted_at = datetime.utcnow()
    
    def give_gdpr_consent(self) -> None:
        """Record GDPR consent."""
        self.gdpr_consent = True