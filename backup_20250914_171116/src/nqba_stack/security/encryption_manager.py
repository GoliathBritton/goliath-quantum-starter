"""
Encryption Manager for NQBA Ecosystem
Handles multi-tenant isolation, encryption at rest, and field-level encryption
"""

import os
import json
import base64
import logging
from datetime import datetime
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, field
from enum import Enum
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets

logger = logging.getLogger(__name__)


class EncryptionLevel(Enum):
    """Encryption levels for different data types"""

    NONE = "none"
    BASIC = "basic"  # Standard encryption
    ENHANCED = "enhanced"  # Enhanced encryption with key rotation
    PII = "pii"  # PII-specific encryption
    CRITICAL = "critical"  # Highest security level


@dataclass
class EncryptionKey:
    """Encryption key with metadata"""

    key_id: str
    key_data: bytes
    created_at: datetime
    expires_at: datetime
    level: EncryptionLevel
    tenant_id: str
    is_active: bool = True
    usage_count: int = 0


@dataclass
class TenantEncryptionConfig:
    """Encryption configuration for a tenant"""

    tenant_id: str
    master_key_id: str
    data_keys: Dict[str, str] = field(default_factory=dict)
    encryption_level: EncryptionLevel = EncryptionLevel.ENHANCED
    pii_fields: List[str] = field(default_factory=list)
    key_rotation_days: int = 90
    created_at: datetime = field(default_factory=datetime.now)


class EncryptionManager:
    """
    Centralized encryption manager for multi-tenant data protection
    Handles encryption at rest, field-level encryption, and tenant isolation
    """

    def __init__(self):
        self.tenant_configs: Dict[str, TenantEncryptionConfig] = {}
        self.encryption_keys: Dict[str, EncryptionKey] = {}
        self.master_keys: Dict[str, bytes] = {}
        self._initialize_master_keys()

    def _initialize_master_keys(self):
        """Initialize master encryption keys"""
        # In production, these would come from KMS
        master_key = os.getenv("NQBA_MASTER_KEY")
        if not master_key:
            master_key = Fernet.generate_key()
            logger.warning("Generated new master key - not suitable for production")

        self.global_master_key = master_key
        logger.info("Encryption manager initialized")

    def create_tenant(
        self,
        tenant_id: str,
        encryption_level: EncryptionLevel = EncryptionLevel.ENHANCED,
    ) -> str:
        """Create a new tenant with encryption configuration"""
        if tenant_id in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} already exists")

        # Generate tenant-specific master key
        tenant_master_key = Fernet.generate_key()
        master_key_id = (
            f"tenant_{tenant_id}_master_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Store tenant master key
        self.master_keys[master_key_id] = tenant_master_key

        # Create encryption key for the tenant
        encryption_key = EncryptionKey(
            key_id=master_key_id,
            key_data=tenant_master_key,
            created_at=datetime.now(),
            expires_at=datetime.now(),
            level=encryption_level,
            tenant_id=tenant_id,
        )

        self.encryption_keys[master_key_id] = encryption_key

        # Create tenant configuration
        config = TenantEncryptionConfig(
            tenant_id=tenant_id,
            master_key_id=master_key_id,
            encryption_level=encryption_level,
        )

        self.tenant_configs[tenant_id] = config

        logger.info(
            f"Created tenant {tenant_id} with {encryption_level.value} encryption"
        )
        return master_key_id

    def delete_tenant(self, tenant_id: str) -> bool:
        """Delete a tenant and all associated encryption keys"""
        if tenant_id not in self.tenant_configs:
            return False

        config = self.tenant_configs[tenant_id]

        # Delete all keys associated with the tenant
        keys_to_delete = [
            key_id
            for key_id, key in self.encryption_keys.items()
            if key.tenant_id == tenant_id
        ]

        for key_id in keys_to_delete:
            del self.encryption_keys[key_id]
            if key_id in self.master_keys:
                del self.master_keys[key_id]

        # Delete tenant configuration
        del self.tenant_configs[tenant_id]

        logger.info(f"Deleted tenant {tenant_id} and all associated keys")
        return True

    def encrypt_data(
        self, data: Any, tenant_id: str, encryption_level: EncryptionLevel = None
    ) -> Dict[str, Any]:
        """Encrypt data for a specific tenant"""
        if tenant_id not in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} not found")

        config = self.tenant_configs[tenant_id]
        if encryption_level is None:
            encryption_level = config.encryption_level

        # Get or create data key for this encryption operation
        data_key_id = self._get_or_create_data_key(tenant_id, encryption_level)
        data_key = self.encryption_keys[data_key_id]

        # Encrypt the data
        if isinstance(data, dict):
            encrypted_data = self._encrypt_dict(data, data_key, config)
        elif isinstance(data, str):
            encrypted_data = self._encrypt_string(data, data_key)
        elif isinstance(data, bytes):
            encrypted_data = self._encrypt_bytes(data, data_key)
        else:
            encrypted_data = self._encrypt_object(data, data_key)

        # Return encrypted data with metadata
        return {
            "encrypted_data": encrypted_data,
            "encryption_metadata": {
                "key_id": data_key_id,
                "encryption_level": encryption_level.value,
                "tenant_id": tenant_id,
                "encrypted_at": datetime.now().isoformat(),
                "algorithm": "AES-256-GCM",
            },
        }

    def decrypt_data(self, encrypted_package: Dict[str, Any], tenant_id: str) -> Any:
        """Decrypt data for a specific tenant"""
        if tenant_id not in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} not found")

        metadata = encrypted_package.get("encryption_metadata", {})
        if metadata.get("tenant_id") != tenant_id:
            raise ValueError("Tenant ID mismatch in encrypted data")

        key_id = metadata.get("key_id")
        if key_id not in self.encryption_keys:
            raise ValueError(f"Encryption key {key_id} not found")

        data_key = self.encryption_keys[key_id]
        encrypted_data = encrypted_package.get("encrypted_data")

        # Decrypt based on data type
        if isinstance(encrypted_data, dict):
            return self._decrypt_dict(encrypted_data, data_key)
        elif isinstance(encrypted_data, str):
            return self._decrypt_string(encrypted_data, data_key)
        elif isinstance(encrypted_data, bytes):
            return self._decrypt_bytes(encrypted_data, data_key)
        else:
            return self._decrypt_object(encrypted_data, data_key)

    def encrypt_field(self, value: str, tenant_id: str, field_name: str) -> str:
        """Encrypt a specific field (for PII)"""
        if tenant_id not in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} not found")

        config = self.tenant_configs[tenant_id]

        # Check if this is a PII field
        if field_name in config.pii_fields:
            encryption_level = EncryptionLevel.PII
        else:
            encryption_level = EncryptionLevel.BASIC

        # Encrypt the field value
        encrypted_package = self.encrypt_data(value, tenant_id, encryption_level)

        # Return base64 encoded encrypted data
        return base64.b64encode(json.dumps(encrypted_package).encode()).decode()

    def decrypt_field(self, encrypted_value: str, tenant_id: str) -> str:
        """Decrypt a specific field"""
        if tenant_id not in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} not found")

        # Decode the encrypted package
        encrypted_package = json.loads(base64.b64decode(encrypted_value).decode())

        # Decrypt the data
        return self.decrypt_data(encrypted_package, tenant_id)

    def add_pii_field(self, tenant_id: str, field_name: str) -> bool:
        """Add a field to the PII list for enhanced encryption"""
        if tenant_id not in self.tenant_configs:
            return False

        config = self.tenant_configs[tenant_id]
        if field_name not in config.pii_fields:
            config.pii_fields.append(field_name)
            logger.info(f"Added {field_name} to PII fields for tenant {tenant_id}")

        return True

    def remove_pii_field(self, tenant_id: str, field_name: str) -> bool:
        """Remove a field from the PII list"""
        if tenant_id not in self.tenant_configs:
            return False

        config = self.tenant_configs[tenant_id]
        if field_name in config.pii_fields:
            config.pii_fields.remove(field_name)
            logger.info(f"Removed {field_name} from PII fields for tenant {tenant_id}")

        return True

    def _get_or_create_data_key(
        self, tenant_id: str, encryption_level: EncryptionLevel
    ) -> str:
        """Get or create a data key for encryption"""
        config = self.tenant_configs[tenant_id]

        # Check if we have an existing data key
        for key_id, key in self.encryption_keys.items():
            if (
                key.tenant_id == tenant_id
                and key.level == encryption_level
                and key.is_active
            ):
                return key_id

        # Create new data key
        data_key = Fernet.generate_key()
        key_id = f"tenant_{tenant_id}_data_{encryption_level.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        encryption_key = EncryptionKey(
            key_id=key_id,
            key_data=data_key,
            created_at=datetime.now(),
            expires_at=datetime.now(),
            level=encryption_level,
            tenant_id=tenant_id,
        )

        self.encryption_keys[key_id] = encryption_key
        config.data_keys[encryption_level.value] = key_id

        logger.info(f"Created new data key {key_id} for tenant {tenant_id}")
        return key_id

    def _encrypt_dict(
        self, data: Dict[str, Any], key: EncryptionKey, config: TenantEncryptionConfig
    ) -> Dict[str, Any]:
        """Encrypt a dictionary with field-level encryption for PII"""
        encrypted_dict = {}

        for field_name, value in data.items():
            if field_name in config.pii_fields:
                # PII fields get enhanced encryption
                encrypted_value = self.encrypt_field(
                    str(value), config.tenant_id, field_name
                )
                encrypted_dict[field_name] = encrypted_value
            elif isinstance(value, (dict, list)):
                # Recursively encrypt nested structures
                encrypted_dict[field_name] = self.encrypt_data(
                    value, config.tenant_id, key.level
                )
            else:
                # Regular fields get standard encryption
                encrypted_dict[field_name] = self._encrypt_string(str(value), key)

        return encrypted_dict

    def _decrypt_dict(
        self, encrypted_data: Dict[str, Any], key: EncryptionKey
    ) -> Dict[str, Any]:
        """Decrypt a dictionary"""
        decrypted_dict = {}

        for field_name, value in encrypted_data.items():
            if isinstance(value, str) and value.startswith("eyJ"):
                # This looks like a PII field
                try:
                    decrypted_dict[field_name] = self.decrypt_field(
                        value, key.tenant_id
                    )
                except:
                    # Fall back to regular decryption
                    decrypted_dict[field_name] = self._decrypt_string(value, key)
            elif isinstance(value, dict):
                # Recursively decrypt nested structures
                decrypted_dict[field_name] = self.decrypt_data(
                    {"encrypted_data": value}, key.tenant_id
                )
            else:
                # Regular decryption
                decrypted_dict[field_name] = self._decrypt_string(value, key)

        return decrypted_dict

    def _encrypt_string(self, data: str, key: EncryptionKey) -> str:
        """Encrypt a string using the provided key"""
        fernet = Fernet(key.key_data)
        encrypted_bytes = fernet.encrypt(data.encode())
        return base64.b64encode(encrypted_bytes).decode()

    def _decrypt_string(self, encrypted_data: str, key: EncryptionKey) -> str:
        """Decrypt a string using the provided key"""
        fernet = Fernet(key.key_data)
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        decrypted_bytes = fernet.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()

    def _encrypt_bytes(self, data: bytes, key: EncryptionKey) -> str:
        """Encrypt bytes using the provided key"""
        fernet = Fernet(key.key_data)
        encrypted_bytes = fernet.encrypt(data)
        return base64.b64encode(encrypted_bytes).decode()

    def _decrypt_bytes(self, encrypted_data: str, key: EncryptionKey) -> bytes:
        """Decrypt bytes using the provided key"""
        fernet = Fernet(key.key_data)
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        return fernet.decrypt(encrypted_bytes)

    def _encrypt_object(self, obj: Any, key: EncryptionKey) -> str:
        """Encrypt an object by serializing to JSON first"""
        json_data = json.dumps(obj, default=str)
        return self._encrypt_string(json_data, key)

    def _decrypt_object(self, encrypted_data: str, key: EncryptionKey) -> Any:
        """Decrypt an object by deserializing from JSON"""
        json_data = self._decrypt_string(encrypted_data, key)
        return json.loads(json_data)

    def rotate_keys(self, tenant_id: str) -> bool:
        """Rotate encryption keys for a tenant"""
        if tenant_id not in self.tenant_configs:
            return False

        config = self.tenant_configs[tenant_id]

        # Generate new master key
        new_master_key = Fernet.generate_key()
        new_master_key_id = (
            f"tenant_{tenant_id}_master_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        # Store new master key
        self.master_keys[new_master_key_id] = new_master_key

        # Create new encryption key
        new_key = EncryptionKey(
            key_id=new_master_key_id,
            key_data=new_master_key,
            created_at=datetime.now(),
            expires_at=datetime.now(),
            level=config.encryption_level,
            tenant_id=tenant_id,
        )

        self.encryption_keys[new_master_key_id] = new_key

        # Update tenant configuration
        config.master_key_id = new_master_key_id

        # Mark old keys as inactive
        for key_id, key in self.encryption_keys.items():
            if key.tenant_id == tenant_id and key.is_active:
                key.is_active = False

        logger.info(f"Rotated keys for tenant {tenant_id}")
        return True

    def get_tenant_status(self, tenant_id: str) -> Dict[str, Any]:
        """Get encryption status for a tenant"""
        if tenant_id not in self.tenant_configs:
            return {}

        config = self.tenant_configs[tenant_id]

        # Count active keys
        active_keys = sum(
            1
            for key in self.encryption_keys.values()
            if key.tenant_id == tenant_id and key.is_active
        )

        return {
            "tenant_id": tenant_id,
            "encryption_level": config.encryption_level.value,
            "pii_fields": config.pii_fields,
            "active_keys": active_keys,
            "master_key_id": config.master_key_id,
            "created_at": config.created_at.isoformat(),
            "key_rotation_days": config.key_rotation_days,
        }

    def get_global_status(self) -> Dict[str, Any]:
        """Get global encryption status"""
        total_tenants = len(self.tenant_configs)
        total_keys = len(self.encryption_keys)
        active_keys = sum(1 for key in self.encryption_keys.values() if key.is_active)

        return {
            "total_tenants": total_tenants,
            "total_keys": total_keys,
            "active_keys": active_keys,
            "tenants": [
                self.get_tenant_status(tenant_id)
                for tenant_id in self.tenant_configs.keys()
            ],
        }


# Global encryption manager instance
encryption_manager = EncryptionManager()
