"""
KMS Manager for NQBA Ecosystem
Handles cloud-based secrets management with automatic rotation
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

logger = logging.getLogger(__name__)


class KMSProvider(Enum):
    """Supported KMS providers"""
    AWS_KMS = "aws_kms"
    GCP_KMS = "gcp_kms"
    AZURE_KEYVAULT = "azure_keyvault"
    HCP_VAULT = "hcp_vault"
    LOCAL = "local"  # For development/testing


@dataclass
class SecretMetadata:
    """Metadata for a secret"""
    secret_id: str
    name: str
    description: str
    created_at: datetime
    expires_at: datetime
    rotation_interval_days: int
    last_rotated: datetime
    tags: Dict[str, str]
    version: int


@dataclass
class RotationPolicy:
    """Policy for secret rotation"""
    rotation_interval_days: int = 90
    grace_period_days: int = 7
    auto_rotation: bool = True
    require_approval: bool = False
    notification_channels: List[str] = None


class KMSManager:
    """
    Centralized KMS manager for secrets management
    Supports multiple cloud providers with automatic rotation
    """
    
    def __init__(self, provider: KMSProvider = KMSProvider.LOCAL):
        self.provider = provider
        self.secrets_cache: Dict[str, Any] = {}
        self.rotation_policies: Dict[str, RotationPolicy] = {}
        self.metadata_store: Dict[str, SecretMetadata] = {}
        self._setup_provider()
        self._start_rotation_monitor()
    
    def _setup_provider(self):
        """Initialize the selected KMS provider"""
        if self.provider == KMSProvider.AWS_KMS:
            self._setup_aws_kms()
        elif self.provider == KMSProvider.GCP_KMS:
            self._setup_gcp_kms()
        elif self.provider == KMSProvider.AZURE_KEYVAULT:
            self._setup_azure_keyvault()
        elif self.provider == KMSProvider.HCP_VAULT:
            self._setup_hcp_vault()
        else:
            self._setup_local_kms()
    
    def _setup_aws_kms(self):
        """Setup AWS KMS integration"""
        try:
            import boto3
            self.kms_client = boto3.client('kms')
            self.key_id = os.getenv('AWS_KMS_KEY_ID')
            logger.info("AWS KMS initialized successfully")
        except ImportError:
            logger.warning("boto3 not available, falling back to local KMS")
            self.provider = KMSProvider.LOCAL
            self._setup_local_kms()
    
    def _setup_gcp_kms(self):
        """Setup GCP KMS integration"""
        try:
            from google.cloud import kms_v1
            self.kms_client = kms_v1.KeyManagementServiceClient()
            self.project_id = os.getenv('GCP_PROJECT_ID')
            self.location_id = os.getenv('GCP_LOCATION_ID', 'global')
            self.key_ring_id = os.getenv('GCP_KEY_RING_ID')
            logger.info("GCP KMS initialized successfully")
        except ImportError:
            logger.warning("google-cloud-kms not available, falling back to local KMS")
            self.provider = KMSProvider.LOCAL
            self._setup_local_kms()
    
    def _setup_azure_keyvault(self):
        """Setup Azure Key Vault integration"""
        try:
            from azure.keyvault.secrets import SecretClient
            from azure.identity import DefaultAzureCredential
            credential = DefaultAzureCredential()
            vault_url = os.getenv('AZURE_KEYVAULT_URL')
            self.kms_client = SecretClient(vault_url=vault_url, credential=credential)
            logger.info("Azure Key Vault initialized successfully")
        except ImportError:
            logger.warning("azure-keyvault-secrets not available, falling back to local KMS")
            self.provider = KMSProvider.LOCAL
            self._setup_local_kms()
    
    def _setup_hcp_vault(self):
        """Setup HCP Vault integration"""
        try:
            import hvac
            vault_url = os.getenv('HCP_VAULT_URL')
            token = os.getenv('HCP_VAULT_TOKEN')
            self.kms_client = hvac.Client(url=vault_url, token=token)
            logger.info("HCP Vault initialized successfully")
        except ImportError:
            logger.warning("hvac not available, falling back to local KMS")
            self.provider = KMSProvider.LOCAL
            self._setup_local_kms()
    
    def _setup_local_kms(self):
        """Setup local KMS for development/testing"""
        self.master_key = os.getenv('LOCAL_MASTER_KEY')
        if not self.master_key:
            self.master_key = Fernet.generate_key()
            logger.warning("Generated new local master key - not suitable for production")
        
        self.fernet = Fernet(self.master_key)
        logger.info("Local KMS initialized for development")
    
    async def create_secret(
        self,
        name: str,
        value: str,
        description: str = "",
        tags: Dict[str, str] = None,
        rotation_policy: RotationPolicy = None
    ) -> str:
        """Create a new secret with rotation policy"""
        secret_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Set default rotation policy if none provided
        if rotation_policy is None:
            rotation_policy = RotationPolicy()
        
        # Encrypt and store the secret
        encrypted_value = await self._encrypt_secret(value)
        
        # Store metadata
        metadata = SecretMetadata(
            secret_id=secret_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=rotation_policy.rotation_interval_days),
            rotation_interval_days=rotation_policy.rotation_interval_days,
            last_rotated=datetime.now(),
            tags=tags or {},
            version=1
        )
        
        self.metadata_store[secret_id] = metadata
        self.rotation_policies[secret_id] = rotation_policy
        self.secrets_cache[secret_id] = encrypted_value
        
        logger.info(f"Created secret {name} with ID {secret_id}")
        return secret_id
    
    async def get_secret(self, secret_id: str) -> str:
        """Retrieve a secret value"""
        if secret_id not in self.secrets_cache:
            raise ValueError(f"Secret {secret_id} not found")
        
        # Check if secret needs rotation
        metadata = self.metadata_store[secret_id]
        if self._should_rotate(metadata):
            await self._rotate_secret(secret_id)
        
        encrypted_value = self.secrets_cache[secret_id]
        return await self._decrypt_secret(encrypted_value)
    
    async def update_secret(self, secret_id: str, new_value: str) -> bool:
        """Update an existing secret value"""
        if secret_id not in self.metadata_store:
            raise ValueError(f"Secret {secret_id} not found")
        
        encrypted_value = await self._encrypt_secret(new_value)
        self.secrets_cache[secret_id] = encrypted_value
        
        # Update metadata
        metadata = self.metadata_store[secret_id]
        metadata.last_rotated = datetime.now()
        metadata.expires_at = datetime.now() + timedelta(days=metadata.rotation_interval_days)
        metadata.version += 1
        
        logger.info(f"Updated secret {secret_id} to version {metadata.version}")
        return True
    
    async def delete_secret(self, secret_id: str) -> bool:
        """Delete a secret and its metadata"""
        if secret_id in self.secrets_cache:
            del self.secrets_cache[secret_id]
        if secret_id in self.metadata_store:
            del self.metadata_store[secret_id]
        if secret_id in self.rotation_policies:
            del self.rotation_policies[secret_id]
        
        logger.info(f"Deleted secret {secret_id}")
        return True
    
    async def list_secrets(self) -> List[SecretMetadata]:
        """List all secrets with metadata"""
        return list(self.metadata_store.values())
    
    async def get_secret_metadata(self, secret_id: str) -> Optional[SecretMetadata]:
        """Get metadata for a specific secret"""
        return self.metadata_store.get(secret_id)
    
    def _should_rotate(self, metadata: SecretMetadata) -> bool:
        """Check if a secret should be rotated"""
        if not metadata:
            return False
        
        days_until_expiry = (metadata.expires_at - datetime.now()).days
        return days_until_expiry <= 0
    
    async def _rotate_secret(self, secret_id: str) -> bool:
        """Rotate a secret automatically"""
        metadata = self.metadata_store[secret_id]
        policy = self.rotation_policies[secret_id]
        
        if not policy.auto_rotation:
            logger.warning(f"Auto-rotation disabled for secret {secret_id}")
            return False
        
        try:
            # For now, we'll just update the expiry
            # In production, you'd generate a new secret value
            metadata.expires_at = datetime.now() + timedelta(days=policy.rotation_interval_days)
            metadata.last_rotated = datetime.now()
            metadata.version += 1
            
            logger.info(f"Rotated secret {secret_id} to version {metadata.version}")
            return True
        except Exception as e:
            logger.error(f"Failed to rotate secret {secret_id}: {e}")
            return False
    
    async def _encrypt_secret(self, value: str) -> bytes:
        """Encrypt a secret value"""
        if self.provider == KMSProvider.LOCAL:
            return self.fernet.encrypt(value.encode())
        else:
            # For cloud KMS, you'd use the provider's encryption
            # For now, fall back to local encryption
            return self.fernet.encrypt(value.encode())
    
    async def _decrypt_secret(self, encrypted_value: bytes) -> str:
        """Decrypt a secret value"""
        if self.provider == KMSProvider.LOCAL:
            return self.fernet.decrypt(encrypted_value).decode()
        else:
            # For cloud KMS, you'd use the provider's decryption
            # For now, fall back to local decryption
            return self.fernet.decrypt(encrypted_value).decode()
    
    def _start_rotation_monitor(self):
        """Start background task to monitor secret rotation"""
        async def monitor_rotation():
            while True:
                try:
                    await self._check_expiring_secrets()
                    await asyncio.sleep(3600)  # Check every hour
                except Exception as e:
                    logger.error(f"Error in rotation monitor: {e}")
                    await asyncio.sleep(300)  # Wait 5 minutes on error
        
        # Start the background task
        asyncio.create_task(monitor_rotation())
    
    async def _check_expiring_secrets(self):
        """Check for secrets that need rotation"""
        now = datetime.now()
        for secret_id, metadata in self.metadata_store.items():
            if self._should_rotate(metadata):
                logger.info(f"Secret {secret_id} needs rotation")
                await self._rotate_secret(secret_id)
    
    async def get_rotation_status(self) -> Dict[str, Any]:
        """Get status of all secrets and rotation policies"""
        status = {
            "total_secrets": len(self.metadata_store),
            "secrets_needing_rotation": 0,
            "secrets_expired": 0,
            "rotation_policies": {}
        }
        
        now = datetime.now()
        for secret_id, metadata in self.metadata_store.items():
            if self._should_rotate(metadata):
                status["secrets_needing_rotation"] += 1
            
            if metadata.expires_at < now:
                status["secrets_expired"] += 1
            
            policy = self.rotation_policies.get(secret_id)
            if policy:
                status["rotation_policies"][secret_id] = {
                    "auto_rotation": policy.auto_rotation,
                    "next_rotation": metadata.expires_at.isoformat(),
                    "days_until_rotation": (metadata.expires_at - now).days
                }
        
        return status


# Global KMS manager instance
kms_manager = KMSManager()
