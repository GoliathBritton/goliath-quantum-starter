"""
Comprehensive test suite for NQBA Security System
Tests KMS, encryption, IAM, audit logging, and compliance management
"""

import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, MagicMock
import json
import base64

# Import security components
from src.nqba_stack.security.kms_manager import (
    KMSManager,
    KMSProvider,
    SecretMetadata,
    RotationPolicy,
)
from src.nqba_stack.security.encryption_manager import (
    EncryptionManager,
    EncryptionLevel,
    EncryptionKey,
    TenantEncryptionConfig,
)
from src.nqba_stack.security.iam_manager import (
    IAMManager,
    RoleLevel,
    Permission,
    Organization,
    User,
    APIKey,
)
from src.nqba_stack.security.audit_logger import (
    AuditLogger,
    AuditEventType,
    AuditSeverity,
    AuditEvent,
    AuditLogEntry,
)
from src.nqba_stack.security.compliance_manager import (
    ComplianceManager,
    ComplianceFramework,
    ControlCategory,
    DataSubjectType,
    DataProcessingPurpose,
)


class TestKMSManager:
    """Test KMS Manager functionality"""

    def setup_method(self):
        """Setup test environment"""
        self.kms_manager = KMSManager(provider=KMSProvider.LOCAL)

    def test_create_secret(self):
        """Test secret creation"""
        secret_id = asyncio.run(
            self.kms_manager.create_secret(
                name="test_secret", value="test_value", description="Test secret"
            )
        )

        assert secret_id is not None
        assert secret_id.startswith("test_secret_")

        # Verify secret was stored
        metadata = asyncio.run(self.kms_manager.get_secret_metadata(secret_id))
        assert metadata is not None
        assert metadata.name == "test_secret"
        assert metadata.description == "Test secret"

    def test_get_secret(self):
        """Test secret retrieval"""
        # Create a secret
        secret_id = asyncio.run(
            self.kms_manager.create_secret(
                name="retrieval_test",
                value="secret_value",
                description="Test retrieval",
            )
        )

        # Retrieve the secret
        value = asyncio.run(self.kms_manager.get_secret(secret_id))
        assert value == "secret_value"

    def test_update_secret(self):
        """Test secret update"""
        # Create a secret
        secret_id = asyncio.run(
            self.kms_manager.create_secret(
                name="update_test", value="old_value", description="Test update"
            )
        )

        # Update the secret
        success = asyncio.run(self.kms_manager.update_secret(secret_id, "new_value"))
        assert success is True

        # Verify update
        value = asyncio.run(self.kms_manager.get_secret(secret_id))
        assert value == "new_value"

    def test_delete_secret(self):
        """Test secret deletion"""
        # Create a secret
        secret_id = asyncio.run(
            self.kms_manager.create_secret(
                name="delete_test", value="delete_value", description="Test deletion"
            )
        )

        # Delete the secret
        success = asyncio.run(self.kms_manager.delete_secret(secret_id))
        assert success is True

        # Verify deletion
        with pytest.raises(ValueError):
            asyncio.run(self.kms_manager.get_secret(secret_id))

    def test_rotation_status(self):
        """Test rotation status reporting"""
        # Create multiple secrets
        secret_ids = []
        for i in range(3):
            secret_id = asyncio.run(
                self.kms_manager.create_secret(
                    name=f"rotation_test_{i}",
                    value=f"value_{i}",
                    description=f"Test rotation {i}",
                )
            )
            secret_ids.append(secret_id)

        # Get rotation status
        status = asyncio.run(self.kms_manager.get_rotation_status())
        assert status["total_secrets"] == 3
        assert status["secrets_needing_rotation"] == 0
        assert status["secrets_expired"] == 0


class TestEncryptionManager:
    """Test Encryption Manager functionality"""

    def setup_method(self):
        """Setup test environment"""
        self.encryption_manager = EncryptionManager()

    def test_create_tenant(self):
        """Test tenant creation"""
        tenant_id = "test_tenant"
        master_key_id = self.encryption_manager.create_tenant(
            tenant_id=tenant_id, encryption_level=EncryptionLevel.ENHANCED
        )

        assert master_key_id is not None
        assert master_key_id.startswith(f"tenant_{tenant_id}_master_")

        # Verify tenant was created
        status = self.encryption_manager.get_tenant_status(tenant_id)
        assert status["tenant_id"] == tenant_id
        assert status["encryption_level"] == EncryptionLevel.ENHANCED.value

    def test_encrypt_decrypt_data(self):
        """Test data encryption and decryption"""
        tenant_id = "encrypt_test_tenant"
        self.encryption_manager.create_tenant(tenant_id, EncryptionLevel.ENHANCED)

        # Test data
        test_data = {"name": "John Doe", "email": "john@example.com", "age": 30}

        # Encrypt data
        encrypted_package = self.encryption_manager.encrypt_data(test_data, tenant_id)
        assert "encrypted_data" in encrypted_package
        assert "encryption_metadata" in encrypted_package

        # Decrypt data
        decrypted_data = self.encryption_manager.decrypt_data(
            encrypted_package, tenant_id
        )
        assert decrypted_data == test_data

    def test_field_level_encryption(self):
        """Test field-level encryption for PII"""
        tenant_id = "pii_test_tenant"
        self.encryption_manager.create_tenant(tenant_id, EncryptionLevel.ENHANCED)

        # Add PII fields
        self.encryption_manager.add_pii_field(tenant_id, "ssn")
        self.encryption_manager.add_pii_field(tenant_id, "credit_card")

        # Encrypt PII fields
        ssn_encrypted = self.encryption_manager.encrypt_field(
            "123-45-6789", tenant_id, "ssn"
        )
        cc_encrypted = self.encryption_manager.encrypt_field(
            "4111-1111-1111-1111", tenant_id, "credit_card"
        )

        assert ssn_encrypted != "123-45-6789"
        assert cc_encrypted != "4111-1111-1111-1111"

        # Decrypt fields
        ssn_decrypted = self.encryption_manager.decrypt_field(ssn_encrypted, tenant_id)
        cc_decrypted = self.encryption_manager.decrypt_field(cc_encrypted, tenant_id)

        assert ssn_decrypted == "123-45-6789"
        assert cc_decrypted == "4111-1111-1111-1111"

    def test_key_rotation(self):
        """Test encryption key rotation"""
        tenant_id = "rotation_test_tenant"
        self.encryption_manager.create_tenant(tenant_id, EncryptionLevel.ENHANCED)

        # Encrypt data with old key
        test_data = {"message": "Hello World"}
        encrypted_package = self.encryption_manager.encrypt_data(test_data, tenant_id)

        # Rotate keys
        success = self.encryption_manager.rotate_keys(tenant_id)
        assert success is True

        # Verify data can still be decrypted
        decrypted_data = self.encryption_manager.decrypt_data(
            encrypted_package, tenant_id
        )
        assert decrypted_data == test_data


class TestIAMManager:
    """Test IAM Manager functionality"""

    def setup_method(self):
        """Setup test environment"""
        self.iam_manager = IAMManager()

    def test_create_organization(self):
        """Test organization creation"""
        result = self.iam_manager.create_organization(
            name="Test Corp",
            domain="testcorp.com",
            owner_email="owner@testcorp.com",
            owner_username="owner",
        )

        assert "org_id" in result
        assert "user_id" in result

        # Verify organization was created
        status = self.iam_manager.get_system_status()
        assert status["total_organizations"] == 1
        assert status["organizations"][0]["name"] == "Test Corp"

    def test_create_user(self):
        """Test user creation"""
        # Create organization first
        org_result = self.iam_manager.create_organization(
            name="User Test Corp",
            domain="usertestcorp.com",
            owner_email="owner@usertestcorp.com",
            owner_username="owner",
        )

        # Create additional user
        user_result = self.iam_manager.create_user(
            org_id=org_result["org_id"],
            email="user@usertestcorp.com",
            username="testuser",
            role=RoleLevel.ANALYST,
        )

        assert "user_id" in user_result
        assert user_result["org_id"] == org_result["org_id"]

        # Verify user was created
        org_users = self.iam_manager.get_organization_users(org_result["org_id"])
        assert len(org_users) == 2  # Owner + new user

    def test_api_key_management(self):
        """Test API key creation and management"""
        # Create organization and user
        org_result = self.iam_manager.create_organization(
            name="API Test Corp",
            domain="apitestcorp.com",
            owner_email="owner@apitestcorp.com",
            owner_username="owner",
        )

        user_result = self.iam_manager.create_user(
            org_id=org_result["org_id"],
            email="user@apitestcorp.com",
            username="apiuser",
            role=RoleLevel.ADMIN,
        )

        # Create API key
        key_result = self.iam_manager.create_api_key(
            user_id=user_result["user_id"],
            name="Test API Key",
            rate_limit_per_minute=50,
            rate_limit_per_hour=500,
        )

        assert "key_id" in key_result
        assert "api_key" in key_result
        assert "scopes" in key_result

        # Validate API key
        validation = self.iam_manager.validate_api_key(key_result["api_key"])
        assert validation is not None
        assert validation["user_id"] == user_result["user_id"]
        assert validation["org_id"] == org_result["org_id"]

    def test_permission_management(self):
        """Test permission checking and role updates"""
        # Create organization and user
        org_result = self.iam_manager.create_organization(
            name="Perm Test Corp",
            domain="permtestcorp.com",
            owner_email="owner@permtestcorp.com",
            owner_username="owner",
        )

        user_result = self.iam_manager.create_user(
            org_id=org_result["org_id"],
            email="user@permtestcorp.com",
            username="permuser",
            role=RoleLevel.VIEWER,
        )

        # Check permissions
        can_read = self.iam_manager.check_permission(
            user_result["user_id"], Permission.DATA_READ
        )
        can_write = self.iam_manager.check_permission(
            user_result["user_id"], Permission.DATA_WRITE
        )

        assert can_read is True
        assert can_write is False

        # Update role to analyst
        success = self.iam_manager.update_user_role(
            user_result["user_id"], RoleLevel.ANALYST
        )
        assert success is True

        # Check updated permissions
        can_write_after = self.iam_manager.check_permission(
            user_result["user_id"], Permission.DATA_WRITE
        )
        assert can_write_after is True


class TestAuditLogger:
    """Test Audit Logger functionality"""

    def setup_method(self):
        """Setup test environment"""
        self.audit_logger = AuditLogger()

    def test_log_event(self):
        """Test audit event logging"""
        event_id = self.audit_logger.log_event(
            event_type=AuditEventType.USER_LOGIN,
            severity=AuditSeverity.LOW,
            user_id="test_user",
            org_id="test_org",
            session_id="test_session",
            ip_address="192.168.1.1",
            user_agent="Test Browser",
            resource_type="authentication",
            resource_id="login_form",
            action="user_login",
            details={"method": "password", "success": True},
        )

        assert event_id is not None
        assert event_id.startswith("audit_")

        # Verify event was logged
        statistics = self.audit_logger.get_audit_statistics()
        assert statistics["total_events"] == 1
        assert statistics["event_type_counts"]["user_login"] == 1

    def test_chain_integrity(self):
        """Test audit log chain integrity"""
        # Log multiple events
        for i in range(3):
            self.audit_logger.log_event(
                event_type=AuditEventType.API_CALL,
                severity=AuditSeverity.MEDIUM,
                user_id=f"user_{i}",
                org_id="test_org",
                session_id=f"session_{i}",
                ip_address="192.168.1.1",
                user_agent="Test Browser",
                resource_type="api",
                resource_id=f"endpoint_{i}",
                action="api_call",
                details={"endpoint": f"/api/v1/test{i}"},
            )

        # Verify chain integrity
        integrity = self.audit_logger.verify_chain_integrity()
        assert integrity["valid"] is True
        assert integrity["total_entries"] == 3

    def test_audit_search(self):
        """Test audit log search functionality"""
        # Log events with different characteristics
        self.audit_logger.log_event(
            event_type=AuditEventType.DATA_READ,
            severity=AuditSeverity.LOW,
            user_id="search_user",
            org_id="search_org",
            session_id="search_session",
            ip_address="192.168.1.2",
            user_agent="Search Browser",
            resource_type="database",
            resource_id="user_table",
            action="data_read",
            details={"table": "users", "rows": 100},
        )

        # Search for events
        results = self.audit_logger.search_audit_log(
            user_id="search_user", event_type=AuditEventType.DATA_READ
        )

        assert len(results) == 1
        assert results[0]["user_id"] == "search_user"
        assert results[0]["event_type"] == "data_read"


class TestComplianceManager:
    """Test Compliance Manager functionality"""

    def setup_method(self):
        """Setup test environment"""
        self.compliance_manager = ComplianceManager()

    def test_soc2_control_assessment(self):
        """Test SOC 2 control assessment"""
        control_id = "CC1.1"

        # Assess control
        success = self.compliance_manager.assess_soc2_control(
            control_id=control_id,
            assessment_data={"is_implemented": True, "risk_level": "low"},
        )

        assert success is True

        # Check status
        status = self.compliance_manager.get_soc2_status()
        assert status["implemented_controls"] == 1
        assert status["compliance_percentage"] > 0

    def test_gdpr_consent_management(self):
        """Test GDPR consent management"""
        # Record consent
        consent_id = self.compliance_manager.record_consent(
            data_subject_id="test_subject",
            data_subject_type=DataSubjectType.INDIVIDUAL,
            purpose=DataProcessingPurpose.MARKETING,
            consent_given=True,
            consent_method="web_form",
            legal_basis="consent",
            data_categories=["contact_information", "preferences"],
            third_parties=["email_service"],
        )

        assert consent_id is not None

        # Check consent status
        status = self.compliance_manager.get_consent_status("test_subject")
        assert status["total_consents"] == 1
        assert status["active_consents"][0]["purpose"] == "marketing"

        # Withdraw consent
        success = self.compliance_manager.withdraw_consent(consent_id)
        assert success is True

        # Verify withdrawal
        status_after = self.compliance_manager.get_consent_status("test_subject")
        assert len(status_after["withdrawn_consents"]) == 1

    def test_data_flow_compliance(self):
        """Test data flow compliance assessment"""
        flow_id = "user_registration"

        # Assess compliance
        compliance = self.compliance_manager.assess_data_flow_compliance(flow_id)

        assert compliance is not None
        assert compliance["flow_id"] == flow_id
        assert "compliance_score" in compliance
        assert "compliance_checks" in compliance

    def test_sfg_compliance_assessment(self):
        """Test SFG insurance compliance assessment"""
        compliance_id = "sfg_001"

        # Assess compliance
        success = self.compliance_manager.assess_sfg_compliance(
            compliance_id=compliance_id,
            assessment_data={"status": "compliant", "risk_assessment": "low"},
        )

        assert success is True

        # Check status
        status = self.compliance_manager.get_sfg_compliance_status()
        assert status["compliant_requirements"] == 1
        assert status["compliance_percentage"] > 0

    def test_compliance_report_generation(self):
        """Test compliance report generation"""
        # Generate SOC 2 report
        soc2_report = self.compliance_manager.generate_compliance_report(
            ComplianceFramework.SOC2_TYPE2
        )

        assert soc2_report is not None
        assert soc2_report["framework"] == "SOC 2 Type 2"
        assert "status" in soc2_report
        assert "controls" in soc2_report

        # Generate GDPR report
        gdpr_report = self.compliance_manager.generate_compliance_report(
            ComplianceFramework.GDPR
        )

        assert gdpr_report is not None
        assert gdpr_report["framework"] == "GDPR"
        assert "status" in gdpr_report
        assert "data_flows" in gdpr_report


class TestSecurityIntegration:
    """Test integration between security components"""

    def setup_method(self):
        """Setup test environment"""
        self.kms_manager = KMSManager(provider=KMSProvider.LOCAL)
        self.encryption_manager = EncryptionManager()
        self.iam_manager = IAMManager()
        self.audit_logger = AuditLogger()
        self.compliance_manager = ComplianceManager()

    def test_end_to_end_security_workflow(self):
        """Test complete security workflow"""
        # 1. Create organization and user
        org_result = self.iam_manager.create_organization(
            name="Security Test Corp",
            domain="securitytestcorp.com",
            owner_email="owner@securitytestcorp.com",
            owner_username="owner",
        )

        user_result = self.iam_manager.create_user(
            org_id=org_result["org_id"],
            email="user@securitytestcorp.com",
            username="securityuser",
            role=RoleLevel.ADMIN,
        )

        # 2. Create API key
        key_result = self.iam_manager.create_api_key(
            user_id=user_result["user_id"], name="Security Test Key"
        )

        # 3. Create tenant for encryption
        tenant_id = "security_test_tenant"
        self.encryption_manager.create_tenant(tenant_id, EncryptionLevel.ENHANCED)

        # 4. Encrypt sensitive data
        sensitive_data = {
            "user_id": user_result["user_id"],
            "api_key": key_result["api_key"],
            "permissions": ["read", "write"],
        }

        encrypted_data = self.encryption_manager.encrypt_data(sensitive_data, tenant_id)

        # 5. Store encryption key in KMS
        secret_id = asyncio.run(
            self.kms_manager.create_secret(
                name="encryption_key",
                value="test_encryption_key",
                description="Key for tenant encryption",
            )
        )

        # 6. Log security events
        self.audit_logger.log_event(
            event_type=AuditEventType.USER_CREATE,
            severity=AuditSeverity.MEDIUM,
            user_id=user_result["user_id"],
            org_id=org_result["org_id"],
            session_id="security_test_session",
            ip_address="192.168.1.100",
            user_agent="Security Test Browser",
            resource_type="user_management",
            resource_id=user_result["user_id"],
            action="user_created",
            details={"role": "admin", "encryption_enabled": True},
        )

        # 7. Assess compliance
        self.compliance_manager.assess_soc2_control(
            control_id="CC4.1",
            assessment_data={"is_implemented": True, "risk_level": "low"},
        )

        # Verify all components are working together
        assert self.iam_manager.get_system_status()["total_organizations"] == 1
        assert (
            self.encryption_manager.get_tenant_status(tenant_id)["tenant_id"]
            == tenant_id
        )
        assert self.audit_logger.get_audit_statistics()["total_events"] > 0
        assert self.compliance_manager.get_soc2_status()["implemented_controls"] > 0


if __name__ == "__main__":
    pytest.main([__file__])
