"""
Audit Logger for NQBA Ecosystem
Handles append-only logs, signed entries, hash chains, and IPFS export
"""

import os
import json
import hashlib
import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import ipfshttpclient

logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of audit events"""

    # Authentication events
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"

    # API events
    API_CALL = "api_call"
    API_KEY_CREATE = "api_key_create"
    API_KEY_REVOKE = "api_key_revoke"

    # Data events
    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_DELETE = "data_delete"
    DATA_EXPORT = "data_export"

    # Quantum events
    QUANTUM_JOB_SUBMIT = "quantum_job_submit"
    QUANTUM_JOB_COMPLETE = "quantum_job_complete"
    QUANTUM_JOB_FAIL = "quantum_job_fail"

    # Business unit events
    BU_ACCESS = "bu_access"
    BU_UPDATE = "bu_update"
    BU_DELETE = "bu_delete"

    # Security events
    PERMISSION_CHANGE = "permission_change"
    ROLE_CHANGE = "role_change"
    ENCRYPTION_KEY_ROTATE = "encryption_key_rotate"

    # Compliance events
    COMPLIANCE_CHECK = "compliance_check"
    AUDIT_EXPORT = "audit_export"
    REGULATORY_REPORT = "regulatory_report"


class AuditSeverity(Enum):
    """Audit event severity levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Audit event record"""

    event_id: str
    timestamp: datetime
    event_type: AuditEventType
    severity: AuditSeverity
    user_id: str
    org_id: str
    session_id: str
    ip_address: str
    user_agent: str
    resource_type: str
    resource_id: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    previous_hash: str = ""
    current_hash: str = ""
    signature: str = ""


@dataclass
class AuditLogEntry:
    """Complete audit log entry with chain verification"""

    event: AuditEvent
    chain_position: int
    merkle_root: str
    block_hash: str
    timestamp: datetime
    is_signed: bool = False
    is_exported_to_ipfs: bool = False
    ipfs_cid: Optional[str] = None


class AuditLogger:
    """
    Comprehensive audit logging system with blockchain-like integrity
    Features append-only logs, signed entries, hash chains, and IPFS export
    """

    def __init__(self, private_key_path: Optional[str] = None):
        self.audit_events: List[AuditEvent] = []
        self.audit_log_entries: List[AuditLogEntry] = []
        self.merkle_tree: Dict[str, str] = {}
        self.previous_hash = ""
        self.private_key = None
        self.public_key = None
        self._initialize_crypto_keys(private_key_path)
        self._start_export_task()

    def _initialize_crypto_keys(self, private_key_path: Optional[str]):
        """Initialize cryptographic keys for signing audit logs"""
        if private_key_path and os.path.exists(private_key_path):
            try:
                with open(private_key_path, "rb") as key_file:
                    self.private_key = load_pem_private_key(
                        key_file.read(), password=None
                    )
                self.public_key = self.private_key.public_key()
                logger.info("Loaded existing private key for audit signing")
            except Exception as e:
                logger.warning(f"Failed to load private key: {e}")

        if not self.private_key:
            # Generate new key pair
            self.private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            )
            self.public_key = self.private_key.public_key()
            logger.info("Generated new key pair for audit signing")

    def log_event(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        user_id: str,
        org_id: str,
        session_id: str,
        ip_address: str,
        user_agent: str,
        resource_type: str,
        resource_id: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log an audit event with automatic chain verification"""
        # Generate event ID
        event_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        # Create audit event
        event = AuditEvent(
            event_id=event_id,
            timestamp=datetime.now(timezone.utc),
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            org_id=org_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            details=details or {},
            metadata=metadata or {},
            previous_hash=self.previous_hash,
        )

        # Calculate current hash
        event.current_hash = self._calculate_event_hash(event)

        # Sign the event
        event.signature = self._sign_event(event)

        # Add to audit events
        self.audit_events.append(event)

        # Create audit log entry
        entry = self._create_audit_log_entry(event)
        self.audit_log_entries.append(entry)

        # Update previous hash for next event
        self.previous_hash = event.current_hash

        # Update merkle tree
        self._update_merkle_tree(entry)

        logger.info(f"Logged audit event {event_id}: {event_type.value}")
        return event_id

    def _calculate_event_hash(self, event: AuditEvent) -> str:
        """Calculate SHA-256 hash of an audit event"""
        # Create a deterministic representation of the event
        event_data = {
            "event_id": event.event_id,
            "timestamp": event.timestamp.isoformat(),
            "event_type": event.event_type.value,
            "severity": event.severity.value,
            "user_id": event.user_id,
            "org_id": event.org_id,
            "session_id": event.session_id,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "action": event.action,
            "details": event.details,
            "metadata": event.metadata,
            "previous_hash": event.previous_hash,
        }

        # Convert to sorted JSON string for deterministic hashing
        json_str = json.dumps(event_data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def _sign_event(self, event: AuditEvent) -> str:
        """Sign an audit event with the private key"""
        if not self.private_key:
            return ""

        try:
            # Sign the event hash
            signature = self.private_key.sign(
                event.current_hash.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return base64.b64encode(signature).decode()
        except Exception as e:
            logger.error(f"Failed to sign audit event: {e}")
            return ""

    def _create_audit_log_entry(self, event: AuditEvent) -> AuditLogEntry:
        """Create a complete audit log entry"""
        chain_position = len(self.audit_log_entries)

        # Calculate merkle root
        merkle_root = self._calculate_merkle_root()

        # Calculate block hash
        block_data = f"{event.current_hash}{merkle_root}{chain_position}"
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()

        return AuditLogEntry(
            event=event,
            chain_position=chain_position,
            merkle_root=merkle_root,
            block_hash=block_hash,
            timestamp=datetime.now(timezone.utc),
            is_signed=bool(event.signature),
        )

    def _update_merkle_tree(self, entry: AuditLogEntry):
        """Update the merkle tree with new entry"""
        # Simple binary merkle tree implementation
        leaf_hash = entry.event.current_hash
        self.merkle_tree[f"leaf_{entry.chain_position}"] = leaf_hash

        # Recalculate internal nodes
        self._recalculate_merkle_tree()

    def _recalculate_merkle_tree(self):
        """Recalculate merkle tree internal nodes"""
        # Get all leaf hashes
        leaf_hashes = []
        for i in range(len(self.audit_log_entries)):
            leaf_key = f"leaf_{i}"
            if leaf_key in self.merkle_tree:
                leaf_hashes.append(self.merkle_tree[leaf_key])

        # Build internal nodes
        level = 0
        current_level = leaf_hashes

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    # Hash two nodes together
                    combined = current_level[i] + current_level[i + 1]
                    node_hash = hashlib.sha256(combined.encode()).hexdigest()
                    next_level.append(node_hash)
                    self.merkle_tree[f"level_{level}_{i//2}"] = node_hash
                else:
                    # Odd number of nodes, promote the last one
                    next_level.append(current_level[i])
                    self.merkle_tree[f"level_{level}_{i//2}"] = current_level[i]

            current_level = next_level
            level += 1

        # Store root
        if current_level:
            self.merkle_tree["root"] = current_level[0]

    def _calculate_merkle_root(self) -> str:
        """Calculate current merkle root"""
        return self.merkle_tree.get("root", "")

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Verify the integrity of the audit log chain"""
        if not self.audit_log_entries:
            return {"valid": True, "message": "No audit entries to verify"}

        issues = []

        # Verify hash chain
        for i, entry in enumerate(self.audit_log_entries):
            if i > 0:
                previous_entry = self.audit_log_entries[i - 1]
                if entry.event.previous_hash != previous_entry.event.current_hash:
                    issues.append(f"Hash chain broken at position {i}")

        # Verify signatures
        unsigned_events = []
        for entry in self.audit_log_entries:
            if not entry.is_signed:
                unsigned_events.append(entry.event.event_id)

        if unsigned_events:
            issues.append(f"Found {len(unsigned_events)} unsigned events")

        # Verify merkle tree
        expected_root = self._calculate_merkle_root()
        for entry in self.audit_log_entries:
            if entry.merkle_root != expected_root:
                issues.append(
                    f"Merkle root mismatch at position {entry.chain_position}"
                )
                break

        return {
            "valid": len(issues) == 0,
            "total_entries": len(self.audit_log_entries),
            "issues": issues,
            "merkle_root": expected_root,
            "last_hash": self.previous_hash,
        }

    def export_audit_log(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Export audit log entries for a date range"""
        entries = []

        for entry in self.audit_log_entries:
            event = entry.event

            # Apply date filter
            if start_date and event.timestamp < start_date:
                continue
            if end_date and event.timestamp > end_date:
                continue

            # Convert to exportable format
            export_entry = {
                "event_id": event.event_id,
                "timestamp": event.timestamp.isoformat(),
                "event_type": event.event_type.value,
                "severity": event.severity.value,
                "user_id": event.user_id,
                "org_id": event.org_id,
                "session_id": event.session_id,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
                "resource_type": event.resource_type,
                "resource_id": event.resource_id,
                "action": event.action,
                "details": event.details,
                "metadata": event.metadata,
                "chain_position": entry.chain_position,
                "merkle_root": entry.merkle_root,
                "block_hash": entry.block_hash,
                "previous_hash": event.previous_hash,
                "current_hash": event.current_hash,
                "signature": event.signature,
                "is_signed": entry.is_signed,
            }

            entries.append(export_entry)

        return entries

    def search_audit_log(
        self,
        user_id: Optional[str] = None,
        org_id: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        severity: Optional[AuditSeverity] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Search audit log with multiple filters"""
        results = []

        for entry in self.audit_log_entries:
            event = entry.event

            # Apply filters
            if user_id and event.user_id != user_id:
                continue
            if org_id and event.org_id != org_id:
                continue
            if event_type and event.event_type != event_type:
                continue
            if severity and event.severity != severity:
                continue
            if resource_type and event.resource_type != resource_type:
                continue
            if resource_id and event.resource_id != resource_id:
                continue
            if start_date and event.timestamp < start_date:
                continue
            if end_date and event.timestamp > end_date:
                continue

            # Add to results
            results.append(self.export_audit_log()[entry.chain_position])

        return results

    async def export_to_ipfs(self, entries: List[Dict[str, Any]]) -> Optional[str]:
        """Export audit log entries to IPFS"""
        try:
            # Connect to IPFS
            client = ipfshttpclient.connect()

            # Create export data
            export_data = {
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "total_entries": len(entries),
                "entries": entries,
                "merkle_root": self._calculate_merkle_root(),
                "chain_verification": self.verify_chain_integrity(),
            }

            # Convert to JSON
            json_data = json.dumps(export_data, default=str, indent=2)

            # Add to IPFS
            result = client.add_str(json_data)
            cid = result["Hash"]

            # Update entries as exported
            for entry in self.audit_log_entries:
                if entry.event.event_id in [e["event_id"] for e in entries]:
                    entry.is_exported_to_ipfs = True
                    entry.ipfs_cid = cid

            logger.info(f"Exported {len(entries)} audit entries to IPFS: {cid}")
            return cid

        except Exception as e:
            logger.error(f"Failed to export to IPFS: {e}")
            return None

    def _start_export_task(self):
        """Start background task for periodic IPFS export"""

        async def export_task():
            while True:
                try:
                    # Export audit logs every 24 hours
                    await asyncio.sleep(86400)

                    # Get entries from last 24 hours
                    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
                    entries = self.export_audit_log(start_date=yesterday)

                    if entries:
                        await self.export_to_ipfs(entries)

                except Exception as e:
                    logger.error(f"Error in export task: {e}")
                    await asyncio.sleep(3600)  # Wait 1 hour on error

        # Start the background task only if there's a running event loop
        try:
            loop = asyncio.get_running_loop()
            self._export_task = loop.create_task(export_task())
        except RuntimeError:
            # No running event loop, skip background task
            logger.debug("No running event loop, skipping export task")
            self._export_task = None

    def get_audit_statistics(self) -> Dict[str, Any]:
        """Get audit log statistics"""
        total_events = len(self.audit_events)
        signed_events = sum(1 for entry in self.audit_log_entries if entry.is_signed)
        exported_events = sum(
            1 for entry in self.audit_log_entries if entry.is_exported_to_ipfs
        )

        # Count by event type
        event_type_counts = {}
        for entry in self.audit_log_entries:
            event_type = entry.event.event_type.value
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1

        # Count by severity
        severity_counts = {}
        for entry in self.audit_log_entries:
            severity = entry.event.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "total_events": total_events,
            "signed_events": signed_events,
            "exported_events": exported_events,
            "chain_integrity": self.verify_chain_integrity(),
            "event_type_counts": event_type_counts,
            "severity_counts": severity_counts,
            "merkle_root": self._calculate_merkle_root(),
            "last_export": datetime.now(timezone.utc).isoformat(),
        }


# Global audit logger instance
audit_logger = AuditLogger()
