#!/usr/bin/env python3
"""
🔐 JWT Token Handler

Handles JWT token generation, validation, and management for secure
authentication in the NQBA ecosystem.
"""

import jwt
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from ..core.settings import get_settings


class JWTHandler:
    """JWT token management and validation"""

    def __init__(self):
        self.settings = get_settings()
        self.secret_key = self.settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create an access token

        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time

        Returns:
            JWT access token
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )

        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a refresh token

        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time

        Returns:
            JWT refresh token
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)

        to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(
        self, token: str, token_type: str = "access"
    ) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token

        Args:
            token: JWT token to verify
            token_type: Expected token type ("access" or "refresh")

        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Verify token type
            if payload.get("type") != token_type:
                return None

            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
                return None

            return payload

        except jwt.PyJWTError:
            return None

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode a JWT token without verification (for debugging)

        Args:
            token: JWT token to decode

        Returns:
            Decoded token data or None if invalid
        """
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except jwt.PyJWTError:
            return None

    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Get token expiration time

        Args:
            token: JWT token

        Returns:
            Expiration datetime or None if invalid
        """
        payload = self.decode_token(token)
        if payload and "exp" in payload:
            return datetime.fromtimestamp(payload["exp"])
        return None

    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired

        Args:
            token: JWT token

        Returns:
            True if expired, False otherwise
        """
        payload = self.decode_token(token)
        if payload and "exp" in payload:
            return datetime.utcnow() > datetime.fromtimestamp(payload["exp"])
        return True

    def generate_session_token(self) -> str:
        """
        Generate a secure session token

        Returns:
            Secure random session token
        """
        return secrets.token_urlsafe(32)

    def create_user_tokens(
        self, user_id: str, username: str, roles: list
    ) -> Dict[str, Any]:
        """
        Create both access and refresh tokens for a user

        Args:
            user_id: User ID
            username: Username
            roles: User roles

        Returns:
            Dictionary with access_token, refresh_token, and expires_in
        """
        token_data = {"sub": user_id, "username": username, "roles": roles}

        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
        }
