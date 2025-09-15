from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db, get_async_db
from ..models.user import User
from .jwt_handler import JWTHandler, TokenData

security = HTTPBearer()

class RoleChecker:
    """Dependency class for role-based access control."""
    
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role"
            )
        return current_user

def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """Extract and verify JWT token from Authorization header."""
    token = credentials.credentials
    return JWTHandler.verify_token(token)

def get_current_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(get_current_user_token)
) -> User:
    """Get current user from database using token data."""
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_user_async(
    db: AsyncSession = Depends(get_async_db),
    token_data: TokenData = Depends(get_current_user_token)
) -> User:
    """Get current user from database using token data (async version)."""
    from sqlalchemy import select
    
    result = await db.execute(select(User).filter(User.id == token_data.user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_optional_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[User]:
    """Get current user if token is provided, otherwise return None."""
    if credentials is None:
        return None
    
    try:
        token_data = JWTHandler.verify_token(credentials.credentials)
        user = db.query(User).filter(User.id == token_data.user_id).first()
        
        if user and user.is_active:
            return user
    except HTTPException:
        pass
    
    return None

# Role-based access control dependencies
require_admin = RoleChecker(["admin"])
require_partner = RoleChecker(["partner", "admin"])
require_qhc = RoleChecker(["qhc", "admin"])
require_any_role = RoleChecker(["admin", "partner", "qhc"])

# Type annotations for dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserAsync = Annotated[User, Depends(get_current_user_async)]
OptionalCurrentUser = Annotated[Optional[User], Depends(get_optional_current_user)]
AdminUser = Annotated[User, Depends(require_admin)]
PartnerUser = Annotated[User, Depends(require_partner)]
QHCUser = Annotated[User, Depends(require_qhc)]
AnyRoleUser = Annotated[User, Depends(require_any_role)]