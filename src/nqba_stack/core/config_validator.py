"""Configuration Validator and Setup Helper

Validates environment configuration and provides setup guidance
for IPFS, Dynex, and other external services.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ServiceStatus(Enum):
    """Service configuration status"""
    CONFIGURED = "configured"
    MISSING_CONFIG = "missing_config"
    INVALID_CONFIG = "invalid_config"
    CONNECTION_ERROR = "connection_error"
    DISABLED = "disabled"


@dataclass
class ServiceValidation:
    """Service validation result"""
    service: str
    status: ServiceStatus
    message: str
    required_vars: List[str]
    missing_vars: List[str]
    suggestions: List[str]


class ConfigValidator:
    """Validates and helps setup configuration for external services"""
    
    def __init__(self):
        self.validations: Dict[str, ServiceValidation] = {}
        self.project_root = Path(__file__).parent.parent.parent.parent
        
    def validate_all_services(self) -> Dict[str, ServiceValidation]:
        """Validate all external service configurations"""
        self.validations = {
            "dynex": self._validate_dynex(),
            "ipfs": self._validate_ipfs(),
            "llm": self._validate_llm(),
            "database": self._validate_database(),
            "email": self._validate_email(),
            "monitoring": self._validate_monitoring()
        }
        return self.validations
    
    def _validate_dynex(self) -> ServiceValidation:
        """Validate Dynex quantum computing configuration"""
        required_vars = ["DYNEX_API_KEY"]
        optional_vars = ["DYNEX_ENDPOINT", "DYNEX_FTP_HOST", "DYNEX_FTP_USER", "DYNEX_FTP_PASS"]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return ServiceValidation(
                service="dynex",
                status=ServiceStatus.MISSING_CONFIG,
                message="Dynex quantum computing is not configured",
                required_vars=required_vars + optional_vars,
                missing_vars=missing_vars,
                suggestions=[
                    "Sign up for Dynex account at https://dynex.network",
                    "Get API key from Dynex dashboard",
                    "Set DYNEX_API_KEY environment variable",
                    "Optionally configure FTP access for large files"
                ]
            )
        
        api_key = os.getenv("DYNEX_API_KEY")
        if len(api_key) < 20:
            return ServiceValidation(
                service="dynex",
                status=ServiceStatus.INVALID_CONFIG,
                message="Dynex API key appears to be invalid (too short)",
                required_vars=required_vars,
                missing_vars=[],
                suggestions=["Verify API key from Dynex dashboard"]
            )
        
        return ServiceValidation(
            service="dynex",
            status=ServiceStatus.CONFIGURED,
            message="Dynex quantum computing is properly configured",
            required_vars=required_vars,
            missing_vars=[],
            suggestions=[]
        )
    
    def _validate_ipfs(self) -> ServiceValidation:
        """Validate IPFS distributed storage configuration"""
        required_vars = ["IPFS_PROJECT_ID", "IPFS_PROJECT_SECRET"]
        optional_vars = ["IPFS_GATEWAY_URL", "IPFS_API_URL"]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return ServiceValidation(
                service="ipfs",
                status=ServiceStatus.MISSING_CONFIG,
                message="IPFS distributed storage is not configured",
                required_vars=required_vars + optional_vars,
                missing_vars=missing_vars,
                suggestions=[
                    "Sign up for Pinata account at https://pinata.cloud",
                    "Create API key in Pinata dashboard",
                    "Set IPFS_PROJECT_ID and IPFS_PROJECT_SECRET",
                    "Alternatively, run local IPFS node and set IPFS_API_URL"
                ]
            )
        
        return ServiceValidation(
            service="ipfs",
            status=ServiceStatus.CONFIGURED,
            message="IPFS distributed storage is properly configured",
            required_vars=required_vars,
            missing_vars=[],
            suggestions=[]
        )
    
    def _validate_llm(self) -> ServiceValidation:
        """Validate LLM service configuration"""
        required_vars = ["LLM_API_KEY", "OPENAI_API_KEY"]
        
        has_llm = bool(os.getenv("LLM_API_KEY"))
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        
        if not has_llm and not has_openai:
            return ServiceValidation(
                service="llm",
                status=ServiceStatus.MISSING_CONFIG,
                message="No LLM service configured",
                required_vars=required_vars,
                missing_vars=required_vars,
                suggestions=[
                    "Set OPENAI_API_KEY for OpenAI GPT models",
                    "Or set LLM_API_KEY for other LLM providers",
                    "Get OpenAI API key from https://platform.openai.com"
                ]
            )
        
        return ServiceValidation(
            service="llm",
            status=ServiceStatus.CONFIGURED,
            message="LLM service is properly configured",
            required_vars=[],
            missing_vars=[],
            suggestions=[]
        )
    
    def _validate_database(self) -> ServiceValidation:
        """Validate database configuration"""
        db_url = os.getenv("DATABASE_URL", "sqlite:///./nqba_stack.db")
        
        return ServiceValidation(
            service="database",
            status=ServiceStatus.CONFIGURED,
            message=f"Database configured: {db_url}",
            required_vars=["DATABASE_URL"],
            missing_vars=[],
            suggestions=[]
        )
    
    def _validate_email(self) -> ServiceValidation:
        """Validate email service configuration"""
        required_vars = ["SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            return ServiceValidation(
                service="email",
                status=ServiceStatus.MISSING_CONFIG,
                message="Email service is not configured",
                required_vars=required_vars,
                missing_vars=missing_vars,
                suggestions=[
                    "Configure SMTP settings for email notifications",
                    "Use Gmail, SendGrid, or other SMTP provider",
                    "Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD"
                ]
            )
        
        return ServiceValidation(
            service="email",
            status=ServiceStatus.CONFIGURED,
            message="Email service is properly configured",
            required_vars=required_vars,
            missing_vars=[],
            suggestions=[]
        )
    
    def _validate_monitoring(self) -> ServiceValidation:
        """Validate monitoring configuration"""
        sentry_dsn = os.getenv("SENTRY_DSN")
        
        if not sentry_dsn:
            return ServiceValidation(
                service="monitoring",
                status=ServiceStatus.MISSING_CONFIG,
                message="Monitoring is not configured",
                required_vars=["SENTRY_DSN"],
                missing_vars=["SENTRY_DSN"],
                suggestions=[
                    "Sign up for Sentry account at https://sentry.io",
                    "Create project and get DSN",
                    "Set SENTRY_DSN environment variable"
                ]
            )
        
        return ServiceValidation(
            service="monitoring",
            status=ServiceStatus.CONFIGURED,
            message="Monitoring is properly configured",
            required_vars=["SENTRY_DSN"],
            missing_vars=[],
            suggestions=[]
        )
    
    def generate_setup_report(self) -> str:
        """Generate a comprehensive setup report"""
        if not self.validations:
            self.validate_all_services()
        
        report = ["\n" + "=" * 60]
        report.append("FLYFOX AI Quantum Platform - Configuration Report")
        report.append("=" * 60)
        
        configured_count = sum(1 for v in self.validations.values() 
                             if v.status == ServiceStatus.CONFIGURED)
        total_count = len(self.validations)
        
        report.append(f"\nOverall Status: {configured_count}/{total_count} services configured")
        report.append("\nService Details:")
        report.append("-" * 40)
        
        for service, validation in self.validations.items():
            status_icon = "✅" if validation.status == ServiceStatus.CONFIGURED else "❌"
            report.append(f"\n{status_icon} {service.upper()}: {validation.message}")
            
            if validation.missing_vars:
                report.append(f"   Missing: {', '.join(validation.missing_vars)}")
            
            if validation.suggestions:
                report.append("   Suggestions:")
                for suggestion in validation.suggestions:
                    report.append(f"   - {suggestion}")
        
        report.append("\n" + "=" * 60)
        report.append("Next Steps:")
        report.append("1. Copy .env.example to .env")
        report.append("2. Update .env with your actual configuration values")
        report.append("3. Restart the application")
        report.append("4. Run this validator again to verify setup")
        report.append("=" * 60 + "\n")
        
        return "\n".join(report)
    
    def create_env_file(self) -> bool:
        """Create .env file from .env.example if it doesn't exist"""
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        if env_file.exists():
            logger.info(".env file already exists")
            return True
        
        if not env_example.exists():
            logger.error(".env.example file not found")
            return False
        
        try:
            env_file.write_text(env_example.read_text())
            logger.info("Created .env file from .env.example")
            return True
        except Exception as e:
            logger.error(f"Failed to create .env file: {e}")
            return False


def validate_configuration() -> Dict[str, ServiceValidation]:
    """Convenience function to validate all services"""
    validator = ConfigValidator()
    return validator.validate_all_services()


def print_setup_report():
    """Print configuration setup report"""
    validator = ConfigValidator()
    validator.validate_all_services()
    print(validator.generate_setup_report())


def setup_environment():
    """Interactive environment setup"""
    validator = ConfigValidator()
    
    print("\n🚀 FLYFOX AI Quantum Platform Setup")
    print("=" * 40)
    
    # Create .env file if needed
    if not validator.create_env_file():
        print("❌ Failed to create .env file")
        return
    
    # Validate current configuration
    validator.validate_all_services()
    print(validator.generate_setup_report())
    
    # Offer to open .env file for editing
    env_file = validator.project_root / ".env"
    print(f"\n📝 Edit your configuration file: {env_file}")
    print("\n💡 Tip: Use the suggestions above to configure each service")


if __name__ == "__main__":
    setup_environment()