# JWT Authentication Handler for Partner System
# Secure authentication with tiered access control

import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import boto3
from botocore.exceptions import ClientError

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token
security = HTTPBearer()


class JWTHandler:
    """JWT Authentication and Authorization Handler"""

    def __init__(self):
        self.secret_key = self._get_jwt_secret()
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7

    def _get_jwt_secret(self) -> str:
        """Get JWT secret from AWS Secrets Manager"""
        try:
            # Try to get from environment first (for local development)
            if os.getenv("JWT_SECRET"):
                return os.getenv("JWT_SECRET")

            # Get from AWS Secrets Manager
            session = boto3.session.Session()
            client = session.client(
                service_name="secretsmanager",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )

            secret_name = "goliath-jwt-secret"
            response = client.get_secret_value(SecretId=secret_name)
            secret = response["SecretString"]

            # Parse JSON response
            import json

            secret_data = json.loads(secret)
            return secret_data.get("secret", "fallback-secret")

        except Exception as e:
            print(f"⚠️  Failed to get JWT secret: {e}")
            return "fallback-secret-for-development"

    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)


# Global JWT handler instance
jwt_handler = JWTHandler()


class PartnerAuth:
    """Partner Authentication and Authorization"""

    def __init__(self):
        self.jwt_handler = jwt_handler

    async def authenticate_partner(
        self, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """Authenticate partner with email and password"""
        # This would typically query your database
        # For now, using mock data
        mock_partners = {
            "admin@goliath.com": {
                "partner_id": "admin_001",
                "email": "admin@goliath.com",
                "password_hash": jwt_handler.hash_password("admin123"),
                "tier": "platinum",
                "company": "Goliath Omniedge",
                "is_active": True,
            }
        }

        if email not in mock_partners:
            return None

        partner = mock_partners[email]

        if not jwt_handler.verify_password(password, partner["password_hash"]):
            return None

        if not partner["is_active"]:
            return None

        return partner

    def create_partner_tokens(self, partner: Dict[str, Any]) -> Dict[str, str]:
        """Create access and refresh tokens for partner"""
        token_data = {
            "sub": partner["partner_id"],
            "email": partner["email"],
            "tier": partner["tier"],
            "company": partner["company"],
        }

        access_token = jwt_handler.create_access_token(token_data)
        refresh_token = jwt_handler.create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def get_current_partner(
        self, credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> Dict[str, Any]:
        """Get current authenticated partner from token"""
        token = credentials.credentials
        payload = jwt_handler.verify_token(token)

        partner_id = payload.get("sub")
        if partner_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        # This would typically query your database
        # For now, returning payload data
        return {
            "partner_id": partner_id,
            "email": payload.get("email"),
            "tier": payload.get("tier"),
            "company": payload.get("company"),
        }

    def require_tier(self, required_tier: str):
        """Decorator to require specific partner tier"""

        def tier_checker(
            current_partner: Dict[str, Any] = Depends(self.get_current_partner)
        ):
            tier_hierarchy = {"bronze": 1, "silver": 2, "gold": 3, "platinum": 4}

            current_tier_level = tier_hierarchy.get(current_partner["tier"], 0)
            required_tier_level = tier_hierarchy.get(required_tier, 0)

            if current_tier_level < required_tier_level:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Tier {required_tier} required. Current tier: {current_partner['tier']}",
                )

            return current_partner

        return tier_checker


# Global auth instance
partner_auth = PartnerAuth()


# Dependency functions
async def get_current_partner(
    current_partner: Dict[str, Any] = Depends(partner_auth.get_current_partner)
):
    """Get current authenticated partner"""
    return current_partner


def require_bronze_tier():
    """Require at least bronze tier"""
    return partner_auth.require_tier("bronze")


def require_silver_tier():
    """Require at least silver tier"""
    return partner_auth.require_tier("silver")


def require_gold_tier():
    """Require at least gold tier"""
    return partner_auth.require_tier("gold")


def require_platinum_tier():
    """Require at least platinum tier"""
    return partner_auth.require_tier("platinum")
