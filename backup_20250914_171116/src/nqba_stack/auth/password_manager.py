#!/usr/bin/env python3
"""
🔐 Password Management System

Handles secure password hashing, verification, and salt generation
using industry-standard bcrypt for the NQBA ecosystem.
"""

import bcrypt
import secrets
import string
from typing import Tuple


class PasswordManager:
    """Secure password management using bcrypt"""

    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        """
        Hash a password with a random salt

        Args:
            password: Plain text password

        Returns:
            Tuple of (password_hash, salt)
        """
        # Generate a random salt
        salt = bcrypt.gensalt()

        # Hash the password with the salt
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        return password_hash.decode("utf-8"), salt.decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash

        Args:
            password: Plain text password to verify
            password_hash: Stored password hash

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), password_hash.encode("utf-8")
            )
        except Exception:
            return False

    @staticmethod
    def generate_strong_password(length: int = 16) -> str:
        """
        Generate a strong random password

        Args:
            length: Password length (default: 16)

        Returns:
            Strong random password
        """
        # Character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        # Ensure at least one character from each set
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(symbols),
        ]

        # Fill remaining length with random characters
        all_chars = lowercase + uppercase + digits + symbols
        password.extend(secrets.choice(all_chars) for _ in range(length - 4))

        # Shuffle the password
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)

        return "".join(password_list)

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """
        Validate password strength requirements

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if len(password) > 128:
            return False, "Password must be less than 128 characters"

        # Check for at least one lowercase letter
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"

        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"

        # Check for at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"

        # Check for at least one special character
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, "Password must contain at least one special character"

        return True, "Password meets strength requirements"
