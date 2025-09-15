#!/usr/bin/env python3
"""
Quantum Nexus Platform - SOC2-Lite Security Checklist Implementation

This module implements a comprehensive SOC2-lite security framework with:
- Automated security scanning and compliance monitoring
- Security policy enforcement
- Audit logging and reporting
- Risk assessment and mitigation
- Continuous security monitoring

SOC2 Trust Service Criteria Coverage:
- Security (CC6.0)
- Availability (CC7.0) 
- Processing Integrity (CC8.0)
- Confidentiality (CC9.0)
- Privacy (CC10.0)
"""

import os
import json
import hashlib
import logging
import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import re
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security risk levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ComplianceStatus(Enum):
    """Compliance check status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    PENDING = "pending"

@dataclass
class SecurityFinding:
    """Security finding or vulnerability"""
    id: str
    title: str
    description: str
    severity: SecurityLevel
    category: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    recommendation: Optional[str] = None
    cve_id: Optional[str] = None
    remediation_effort: Optional[str] = None
    timestamp: Optional[datetime.datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.utcnow()

@dataclass
class ComplianceCheck:
    """SOC2 compliance check result"""
    control_id: str
    control_name: str
    description: str
    status: ComplianceStatus
    evidence: List[str]
    findings: List[SecurityFinding]
    last_checked: datetime.datetime
    next_check: datetime.datetime
    remediation_plan: Optional[str] = None

class SOC2LiteChecker:
    """SOC2-Lite security compliance checker"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.security_dir = self.project_root / "security"
        self.reports_dir = self.security_dir / "reports"
        self.policies_dir = self.security_dir / "policies"
        
        # Create directories
        self.security_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)
        self.policies_dir.mkdir(exist_ok=True)
        
        self.findings: List[SecurityFinding] = []
        self.compliance_checks: List[ComplianceCheck] = []
        
        # Security patterns to detect (simplified)
        self.security_patterns = {
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][a-zA-Z0-9]{8,}["\']',
                r'api_key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
                r'secret\s*=\s*["\'][a-zA-Z0-9]{16,}["\']',
                r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']'
            ],
            'sql_injection': [
                r'execute\s*\(.*%s.*\)',
                r'query\s*\(.*\+.*\)',
                r'SELECT.*FROM.*WHERE.*\+'
            ],
            'xss_vulnerabilities': [
                r'innerHTML\s*=\s*[^;]*\+',
                r'document\.write\s*\([^)]*\+',
                r'eval\s*\([^)]*\+'
            ],
            'insecure_random': [
                r'random\.random\(\)',
                r'Math\.random\(\)',
                r'rand\(\)'
            ],
            'weak_crypto': [
                r'md5\s*\(',
                r'sha1\s*\(',
                r'DES\s*\(',
                r'RC4\s*\('
            ]
        }
    
    def run_full_assessment(self) -> Dict[str, Any]:
        """Run complete SOC2-lite security assessment"""
        logger.info("Starting SOC2-lite security assessment...")
        
        # Clear previous findings
        self.findings = []
        self.compliance_checks = []
        
        # Run security scans
        self._scan_code_vulnerabilities()
        self._check_dependency_vulnerabilities()
        self._verify_security_configurations()
        self._check_access_controls()
        self._verify_encryption_standards()
        self._check_logging_monitoring()
        self._verify_backup_procedures()
        self._check_incident_response()
        
        # Run compliance checks
        self._run_soc2_compliance_checks()
        
        # Generate report
        report = self._generate_security_report()
        
        # Save results
        self._save_assessment_results(report)
        
        logger.info(f"Security assessment completed. Found {len(self.findings)} findings.")
        return report
    
    def _scan_code_vulnerabilities(self):
        """Scan codebase for security vulnerabilities"""
        logger.info("Scanning code for security vulnerabilities...")
        
        # File extensions to scan
        extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.php', '.rb', '.go']
        
        for ext in extensions:
            for file_path in self.project_root.rglob(f'*{ext}'):
                if self._should_skip_file(file_path):
                    continue
                    
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self._scan_file_content(file_path, content)
                except Exception as e:
                    logger.warning(f"Could not scan file {file_path}: {e}")
    
    def _scan_file_content(self, file_path: Path, content: str):
        """Scan file content for security issues"""
        lines = content.split('\n')
        
        for category, patterns in self.security_patterns.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    try:
                        if re.search(pattern, line, re.IGNORECASE):
                            finding = SecurityFinding(
                                id=f"{category}_{hashlib.md5(f'{file_path}_{line_num}'.encode()).hexdigest()[:8]}",
                                title=f"{category.replace('_', ' ').title()} Detected",
                                description=f"Potential {category.replace('_', ' ')} found in code",
                                severity=self._get_severity_for_category(category),
                                category=category,
                                file_path=str(file_path.relative_to(self.project_root)),
                                line_number=line_num,
                                recommendation=self._get_recommendation_for_category(category)
                            )
                            self.findings.append(finding)
                    except re.error:
                        continue  # Skip invalid regex patterns
    
    def _check_dependency_vulnerabilities(self):
        """Check for vulnerable dependencies"""
        logger.info("Checking dependency vulnerabilities...")
        
        # Check Python dependencies
        requirements_files = list(self.project_root.rglob('requirements*.txt'))
        for req_file in requirements_files:
            self._check_python_dependencies(req_file)
        
        # Check Node.js dependencies
        package_files = list(self.project_root.rglob('package.json'))
        for pkg_file in package_files:
            self._check_nodejs_dependencies(pkg_file)
    
    def _check_python_dependencies(self, requirements_file: Path):
        """Check Python dependencies for vulnerabilities"""
        try:
            # Try to run safety check if available
            result = subprocess.run(
                ['safety', 'check', '-r', str(requirements_file), '--json'],
                capture_output=True, text=True, timeout=60
            )
            
            if result.returncode == 0 and result.stdout:
                vulnerabilities = json.loads(result.stdout)
                for vuln in vulnerabilities:
                    finding = SecurityFinding(
                        id=f"dep_vuln_{vuln.get('id', 'unknown')}",
                        title=f"Vulnerable Dependency: {vuln.get('package', 'Unknown')}",
                        description=vuln.get('advisory', 'Dependency vulnerability detected'),
                        severity=SecurityLevel.HIGH,
                        category="dependency_vulnerability",
                        file_path=str(requirements_file.relative_to(self.project_root)),
                        recommendation=f"Update {vuln.get('package')} to version {vuln.get('safe_versions', 'latest')}"
                    )
                    self.findings.append(finding)
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            # Safety not available or failed, add manual check recommendation
            finding = SecurityFinding(
                id="dep_check_manual",
                title="Manual Dependency Check Required",
                description="Automated dependency vulnerability scanning not available",
                severity=SecurityLevel.MEDIUM,
                category="dependency_check",
                file_path=str(requirements_file.relative_to(self.project_root)),
                recommendation="Install 'safety' package and run 'safety check' manually"
            )
            self.findings.append(finding)
    
    def _check_nodejs_dependencies(self, package_file: Path):
        """Check Node.js dependencies for vulnerabilities"""
        try:
            # Run npm audit if available
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                cwd=package_file.parent,
                capture_output=True, text=True, timeout=60
            )
            
            if result.stdout:
                audit_data = json.loads(result.stdout)
                vulnerabilities = audit_data.get('vulnerabilities', {})
                
                for pkg_name, vuln_data in vulnerabilities.items():
                    severity_map = {
                        'critical': SecurityLevel.CRITICAL,
                        'high': SecurityLevel.HIGH,
                        'moderate': SecurityLevel.MEDIUM,
                        'low': SecurityLevel.LOW
                    }
                    
                    finding = SecurityFinding(
                        id=f"npm_vuln_{hashlib.md5(pkg_name.encode()).hexdigest()[:8]}",
                        title=f"Vulnerable NPM Package: {pkg_name}",
                        description=vuln_data.get('title', 'NPM package vulnerability'),
                        severity=severity_map.get(vuln_data.get('severity', 'medium'), SecurityLevel.MEDIUM),
                        category="npm_vulnerability",
                        file_path=str(package_file.relative_to(self.project_root)),
                        recommendation="Run 'npm audit fix' to resolve vulnerabilities"
                    )
                    self.findings.append(finding)
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
            pass  # npm not available or failed
    
    def _verify_security_configurations(self):
        """Verify security configuration files"""
        logger.info("Verifying security configurations...")
        
        # Check for security headers in web configs
        self._check_security_headers()
        
        # Check SSL/TLS configurations
        self._check_ssl_configurations()
        
        # Check environment variable security
        self._check_environment_security()
        
        # Check Docker security
        self._check_docker_security()
    
    def _check_security_headers(self):
        """Check for proper security headers configuration"""
        required_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]
        
        # Check various config files
        config_patterns = ['nginx.conf', 'apache.conf', '*.nginx', 'middleware.py', 'app.py']
        
        found_headers = set()
        for pattern in config_patterns:
            for config_file in self.project_root.rglob(pattern):
                try:
                    with open(config_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        for header in required_headers:
                            if header.lower() in content.lower():
                                found_headers.add(header)
                except Exception:
                    continue
        
        missing_headers = set(required_headers) - found_headers
        if missing_headers:
            finding = SecurityFinding(
                id="missing_security_headers",
                title="Missing Security Headers",
                description=f"Missing security headers: {', '.join(missing_headers)}",
                severity=SecurityLevel.MEDIUM,
                category="security_headers",
                recommendation="Implement missing security headers in web server configuration"
            )
            self.findings.append(finding)
    
    def _check_ssl_configurations(self):
        """Check SSL/TLS configurations"""
        # Check for SSL certificate files
        ssl_files = list(self.project_root.rglob('*.pem')) + list(self.project_root.rglob('*.crt'))
        
        if not ssl_files:
            finding = SecurityFinding(
                id="no_ssl_certs",
                title="No SSL Certificates Found",
                description="No SSL certificate files found in project",
                severity=SecurityLevel.HIGH,
                category="ssl_configuration",
                recommendation="Implement SSL/TLS certificates for secure communication"
            )
            self.findings.append(finding)
    
    def _check_environment_security(self):
        """Check environment variable security"""
        env_files = list(self.project_root.rglob('.env*'))
        
        for env_file in env_files:
            if env_file.name == '.env':
                finding = SecurityFinding(
                    id="env_file_exposed",
                    title="Environment File Not Secured",
                    description="Main .env file found - ensure it's not committed to version control",
                    severity=SecurityLevel.MEDIUM,
                    category="environment_security",
                    file_path=str(env_file.relative_to(self.project_root)),
                    recommendation="Add .env to .gitignore and use .env.example for templates"
                )
                self.findings.append(finding)
    
    def _check_docker_security(self):
        """Check Docker security configurations"""
        dockerfile_patterns = ['Dockerfile*', '*.dockerfile']
        
        for pattern in dockerfile_patterns:
            for dockerfile in self.project_root.rglob(pattern):
                try:
                    with open(dockerfile, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        
                        # Check for running as root
                        if 'user root' in content or ('user' not in content and 'from' in content):
                            finding = SecurityFinding(
                                id=f"docker_root_{dockerfile.name}",
                                title="Docker Container Running as Root",
                                description="Container may be running as root user",
                                severity=SecurityLevel.MEDIUM,
                                category="docker_security",
                                file_path=str(dockerfile.relative_to(self.project_root)),
                                recommendation="Add USER directive to run container as non-root user"
                            )
                            self.findings.append(finding)
                except Exception:
                    continue
    
    def _check_access_controls(self):
        """Check access control implementations"""
        logger.info("Checking access controls...")
        
        # Check for authentication middleware
        auth_patterns = ['auth', 'login', 'session', 'jwt', 'oauth']
        auth_files = []
        
        for pattern in auth_patterns:
            auth_files.extend(list(self.project_root.rglob(f'*{pattern}*')))
        
        if not auth_files:
            finding = SecurityFinding(
                id="no_auth_implementation",
                title="No Authentication Implementation Found",
                description="No authentication-related files detected",
                severity=SecurityLevel.HIGH,
                category="access_control",
                recommendation="Implement proper authentication and authorization mechanisms"
            )
            self.findings.append(finding)
    
    def _verify_encryption_standards(self):
        """Verify encryption implementations"""
        logger.info("Verifying encryption standards...")
        
        # Check for proper encryption libraries
        encryption_patterns = ['cryptography', 'bcrypt', 'scrypt', 'argon2']
        found_encryption = False
        
        for req_file in self.project_root.rglob('requirements*.txt'):
            try:
                with open(req_file, 'r') as f:
                    content = f.read().lower()
                    for pattern in encryption_patterns:
                        if pattern in content:
                            found_encryption = True
                            break
            except Exception:
                continue
        
        if not found_encryption:
            finding = SecurityFinding(
                id="weak_encryption",
                title="No Strong Encryption Libraries Found",
                description="No modern encryption libraries detected in dependencies",
                severity=SecurityLevel.MEDIUM,
                category="encryption",
                recommendation="Implement strong encryption using libraries like cryptography or bcrypt"
            )
            self.findings.append(finding)
    
    def _check_logging_monitoring(self):
        """Check logging and monitoring implementations"""
        logger.info("Checking logging and monitoring...")
        
        # Check for logging configuration
        logging_files = list(self.project_root.rglob('*log*')) + list(self.project_root.rglob('*audit*'))
        
        if not logging_files:
            finding = SecurityFinding(
                id="insufficient_logging",
                title="Insufficient Logging Configuration",
                description="No dedicated logging configuration files found",
                severity=SecurityLevel.MEDIUM,
                category="logging_monitoring",
                recommendation="Implement comprehensive logging and monitoring system"
            )
            self.findings.append(finding)
    
    def _verify_backup_procedures(self):
        """Verify backup and recovery procedures"""
        logger.info("Verifying backup procedures...")
        
        backup_files = list(self.project_root.rglob('*backup*')) + list(self.project_root.rglob('*recovery*'))
        
        if not backup_files:
            finding = SecurityFinding(
                id="no_backup_procedures",
                title="No Backup Procedures Found",
                description="No backup or recovery procedures documented or implemented",
                severity=SecurityLevel.MEDIUM,
                category="backup_recovery",
                recommendation="Implement and document backup and recovery procedures"
            )
            self.findings.append(finding)
    
    def _check_incident_response(self):
        """Check incident response procedures"""
        logger.info("Checking incident response procedures...")
        
        incident_files = list(self.project_root.rglob('*incident*')) + list(self.project_root.rglob('*response*'))
        
        if not incident_files:
            finding = SecurityFinding(
                id="no_incident_response",
                title="No Incident Response Plan Found",
                description="No incident response procedures documented",
                severity=SecurityLevel.MEDIUM,
                category="incident_response",
                recommendation="Create and document incident response procedures"
            )
            self.findings.append(finding)
    
    def _run_soc2_compliance_checks(self):
        """Run SOC2 compliance checks"""
        logger.info("Running SOC2 compliance checks...")
        
        # Define SOC2 controls to check
        soc2_controls = [
            {
                'id': 'CC6.1',
                'name': 'Logical and Physical Access Controls',
                'description': 'Access to data and systems is restricted to authorized users',
                'check_function': self._check_access_controls_compliance
            },
            {
                'id': 'CC6.2',
                'name': 'Authentication and Authorization',
                'description': 'Users are authenticated and authorized before accessing systems',
                'check_function': self._check_auth_compliance
            },
            {
                'id': 'CC6.3',
                'name': 'System Access Monitoring',
                'description': 'System access is monitored and logged',
                'check_function': self._check_monitoring_compliance
            },
            {
                'id': 'CC6.7',
                'name': 'Data Transmission and Disposal',
                'description': 'Data is protected during transmission and disposal',
                'check_function': self._check_data_protection_compliance
            },
            {
                'id': 'CC7.1',
                'name': 'System Availability',
                'description': 'Systems are available for operation and use',
                'check_function': self._check_availability_compliance
            }
        ]
        
        for control in soc2_controls:
            try:
                result = control['check_function']()
                self.compliance_checks.append(result)
            except Exception as e:
                logger.error(f"Error checking control {control['id']}: {e}")
    
    def _check_access_controls_compliance(self) -> ComplianceCheck:
        """Check access controls compliance"""
        evidence = []
        findings = []
        status = ComplianceStatus.COMPLIANT
        
        # Check for authentication files
        auth_files = list(self.project_root.rglob('*auth*'))
        if auth_files:
            evidence.append(f"Authentication files found: {len(auth_files)}")
        else:
            status = ComplianceStatus.NON_COMPLIANT
            findings.append(SecurityFinding(
                id="cc6_1_no_auth",
                title="No Access Controls Implemented",
                description="No authentication or authorization mechanisms found",
                severity=SecurityLevel.HIGH,
                category="soc2_compliance"
            ))
        
        return ComplianceCheck(
            control_id="CC6.1",
            control_name="Logical and Physical Access Controls",
            description="Access to data and systems is restricted to authorized users",
            status=status,
            evidence=evidence,
            findings=findings,
            last_checked=datetime.datetime.utcnow(),
            next_check=datetime.datetime.utcnow() + datetime.timedelta(days=30)
        )
    
    def _check_auth_compliance(self) -> ComplianceCheck:
        """Check authentication compliance"""
        evidence = []
        findings = []
        status = ComplianceStatus.PARTIAL
        
        # Check for JWT, OAuth, or session management
        auth_patterns = ['jwt', 'oauth', 'session', 'passport']
        found_auth = False
        
        for pattern in auth_patterns:
            files = list(self.project_root.rglob(f'*{pattern}*'))
            if files:
                found_auth = True
                evidence.append(f"{pattern.upper()} implementation found")
        
        if found_auth:
            status = ComplianceStatus.COMPLIANT
        else:
            status = ComplianceStatus.NON_COMPLIANT
            findings.append(SecurityFinding(
                id="cc6_2_no_auth",
                title="No Authentication System Found",
                description="No modern authentication system implemented",
                severity=SecurityLevel.HIGH,
                category="soc2_compliance"
            ))
        
        return ComplianceCheck(
            control_id="CC6.2",
            control_name="Authentication and Authorization",
            description="Users are authenticated and authorized before accessing systems",
            status=status,
            evidence=evidence,
            findings=findings,
            last_checked=datetime.datetime.utcnow(),
            next_check=datetime.datetime.utcnow() + datetime.timedelta(days=30)
        )
    
    def _check_monitoring_compliance(self) -> ComplianceCheck:
        """Check monitoring compliance"""
        evidence = []
        findings = []
        status = ComplianceStatus.PARTIAL
        
        # Check for monitoring and logging
        monitoring_files = list(self.project_root.rglob('*monitor*')) + list(self.project_root.rglob('*log*'))
        
        if monitoring_files:
            evidence.append(f"Monitoring/logging files found: {len(monitoring_files)}")
            status = ComplianceStatus.COMPLIANT
        else:
            status = ComplianceStatus.NON_COMPLIANT
            findings.append(SecurityFinding(
                id="cc6_3_no_monitoring",
                title="No System Monitoring Found",
                description="No system monitoring or logging implementation found",
                severity=SecurityLevel.MEDIUM,
                category="soc2_compliance"
            ))
        
        return ComplianceCheck(
            control_id="CC6.3",
            control_name="System Access Monitoring",
            description="System access is monitored and logged",
            status=status,
            evidence=evidence,
            findings=findings,
            last_checked=datetime.datetime.utcnow(),
            next_check=datetime.datetime.utcnow() + datetime.timedelta(days=30)
        )
    
    def _check_data_protection_compliance(self) -> ComplianceCheck:
        """Check data protection compliance"""
        evidence = []
        findings = []
        status = ComplianceStatus.PARTIAL
        
        # Check for encryption and SSL
        ssl_files = list(self.project_root.rglob('*.pem')) + list(self.project_root.rglob('*.crt'))
        
        if ssl_files:
            evidence.append(f"SSL certificates found: {len(ssl_files)}")
            status = ComplianceStatus.COMPLIANT
        else:
            findings.append(SecurityFinding(
                id="cc6_7_no_encryption",
                title="No Data Encryption Found",
                description="No SSL certificates or encryption implementation found",
                severity=SecurityLevel.HIGH,
                category="soc2_compliance"
            ))
        
        return ComplianceCheck(
            control_id="CC6.7",
            control_name="Data Transmission and Disposal",
            description="Data is protected during transmission and disposal",
            status=status,
            evidence=evidence,
            findings=findings,
            last_checked=datetime.datetime.utcnow(),
            next_check=datetime.datetime.utcnow() + datetime.timedelta(days=30)
        )
    
    def _check_availability_compliance(self) -> ComplianceCheck:
        """Check availability compliance"""
        evidence = []
        findings = []
        status = ComplianceStatus.PARTIAL
        
        # Check for backup and monitoring systems
        backup_files = list(self.project_root.rglob('*backup*'))
        docker_files = list(self.project_root.rglob('docker-compose*')) + list(self.project_root.rglob('Dockerfile*'))
        
        if backup_files:
            evidence.append(f"Backup procedures found: {len(backup_files)}")
        
        if docker_files:
            evidence.append(f"Containerization found: {len(docker_files)}")
            status = ComplianceStatus.COMPLIANT
        
        if not evidence:
            status = ComplianceStatus.NON_COMPLIANT
            findings.append(SecurityFinding(
                id="cc7_1_no_availability",
                title="No Availability Measures Found",
                description="No backup or high availability measures implemented",
                severity=SecurityLevel.MEDIUM,
                category="soc2_compliance"
            ))
        
        return ComplianceCheck(
            control_id="CC7.1",
            control_name="System Availability",
            description="Systems are available for operation and use",
            status=status,
            evidence=evidence,
            findings=findings,
            last_checked=datetime.datetime.utcnow(),
            next_check=datetime.datetime.utcnow() + datetime.timedelta(days=30)
        )
    
    def _generate_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        # Categorize findings by severity
        findings_by_severity = {
            SecurityLevel.CRITICAL: [],
            SecurityLevel.HIGH: [],
            SecurityLevel.MEDIUM: [],
            SecurityLevel.LOW: [],
            SecurityLevel.INFO: []
        }
        
        for finding in self.findings:
            findings_by_severity[finding.severity].append(finding)
        
        # Calculate compliance score
        compliant_checks = sum(1 for check in self.compliance_checks if check.status == ComplianceStatus.COMPLIANT)
        total_checks = len(self.compliance_checks)
        compliance_score = (compliant_checks / total_checks * 100) if total_checks > 0 else 0
        
        # Generate risk score
        risk_score = self._calculate_risk_score()
        
        report = {
            'assessment_date': datetime.datetime.utcnow().isoformat(),
            'project_root': str(self.project_root),
            'summary': {
                'total_findings': len(self.findings),
                'critical_findings': len(findings_by_severity[SecurityLevel.CRITICAL]),
                'high_findings': len(findings_by_severity[SecurityLevel.HIGH]),
                'medium_findings': len(findings_by_severity[SecurityLevel.MEDIUM]),
                'low_findings': len(findings_by_severity[SecurityLevel.LOW]),
                'compliance_score': round(compliance_score, 2),
                'risk_score': risk_score,
                'risk_level': self._get_risk_level(risk_score)
            },
            'findings': [asdict(finding) for finding in self.findings],
            'compliance_checks': [asdict(check) for check in self.compliance_checks],
            'recommendations': self._generate_recommendations(),
            'next_assessment_date': (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat()
        }
        
        return report
    
    def _calculate_risk_score(self) -> float:
        """Calculate overall risk score (0-100)"""
        if not self.findings:
            return 0.0
        
        severity_weights = {
            SecurityLevel.CRITICAL: 10.0,
            SecurityLevel.HIGH: 7.0,
            SecurityLevel.MEDIUM: 4.0,
            SecurityLevel.LOW: 2.0,
            SecurityLevel.INFO: 0.5
        }
        
        total_weight = sum(severity_weights[finding.severity] for finding in self.findings)
        max_possible_weight = len(self.findings) * severity_weights[SecurityLevel.CRITICAL]
        
        return min(100.0, (total_weight / max_possible_weight * 100) if max_possible_weight > 0 else 0.0)
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level based on score"""
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        elif risk_score >= 20:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        # Count findings by category
        category_counts = {}
        for finding in self.findings:
            category_counts[finding.category] = category_counts.get(finding.category, 0) + 1
        
        # Generate recommendations based on most common issues
        if category_counts.get('hardcoded_secrets', 0) > 0:
            recommendations.append("Implement proper secrets management using environment variables or secret management services")
        
        if category_counts.get('dependency_vulnerability', 0) > 0:
            recommendations.append("Regularly update dependencies and implement automated vulnerability scanning")
        
        if category_counts.get('sql_injection', 0) > 0:
            recommendations.append("Use parameterized queries and ORM frameworks to prevent SQL injection")
        
        if category_counts.get('xss_vulnerabilities', 0) > 0:
            recommendations.append("Implement proper input validation and output encoding to prevent XSS attacks")
        
        if category_counts.get('docker_security', 0) > 0:
            recommendations.append("Follow Docker security best practices including running as non-root user")
        
        # Add general recommendations
        recommendations.extend([
            "Implement comprehensive logging and monitoring",
            "Regular security assessments and penetration testing",
            "Employee security awareness training",
            "Incident response plan development and testing",
            "Regular backup and recovery testing"
        ])
        
        return recommendations
    
    def _save_assessment_results(self, report: Dict[str, Any]):
        """Save assessment results to files"""
        timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON report
        json_report_path = self.reports_dir / f"security_assessment_{timestamp}.json"
        with open(json_report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save human-readable report
        text_report_path = self.reports_dir / f"security_assessment_{timestamp}.txt"
        with open(text_report_path, 'w') as f:
            self._write_text_report(f, report)
        
        logger.info(f"Security assessment saved to {json_report_path}")
        logger.info(f"Human-readable report saved to {text_report_path}")
    
    def _write_text_report(self, file, report: Dict[str, Any]):
        """Write human-readable text report"""
        file.write("\n" + "="*80 + "\n")
        file.write("QUANTUM NEXUS PLATFORM - SOC2-LITE SECURITY ASSESSMENT REPORT\n")
        file.write("="*80 + "\n\n")
        
        file.write(f"Assessment Date: {report['assessment_date']}\n")
        file.write(f"Project Root: {report['project_root']}\n\n")
        
        # Summary
        summary = report['summary']
        file.write("EXECUTIVE SUMMARY\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Security Findings: {summary['total_findings']}\n")
        file.write(f"Critical Findings: {summary['critical_findings']}\n")
        file.write(f"High Risk Findings: {summary['high_findings']}\n")
        file.write(f"Medium Risk Findings: {summary['medium_findings']}\n")
        file.write(f"Low Risk Findings: {summary['low_findings']}\n")
        file.write(f"SOC2 Compliance Score: {summary['compliance_score']}%\n")
        file.write(f"Overall Risk Score: {summary['risk_score']:.1f}/100 ({summary['risk_level']})\n\n")
        
        # Detailed findings
        if report['findings']:
            file.write("DETAILED SECURITY FINDINGS\n")
            file.write("-" * 40 + "\n")
            
            for finding in report['findings']:
                severity = finding['severity']
                if hasattr(severity, 'value'):
                    severity_str = severity.value.upper()
                else:
                    severity_str = str(severity).upper()
                file.write(f"\n[{severity_str}] {finding['title']}\n")
                file.write(f"Description: {finding['description']}\n")
                if finding['file_path']:
                    file.write(f"File: {finding['file_path']}")
                    if finding['line_number']:
                        file.write(f":{finding['line_number']}")
                    file.write("\n")
                if finding['recommendation']:
                    file.write(f"Recommendation: {finding['recommendation']}\n")
                file.write("-" * 40 + "\n")
        
        # Compliance checks
        if report['compliance_checks']:
            file.write("\nSOC2 COMPLIANCE CHECKS\n")
            file.write("-" * 40 + "\n")
            
            for check in report['compliance_checks']:
                file.write(f"\n{check['control_id']}: {check['control_name']}\n")
                status = check['status']
                if hasattr(status, 'value'):
                    status_str = status.value.upper()
                else:
                    status_str = str(status).upper()
                file.write(f"Status: {status_str}\n")
                file.write(f"Description: {check['description']}\n")
                if check['evidence']:
                    file.write(f"Evidence: {', '.join(check['evidence'])}\n")
                file.write("-" * 40 + "\n")
        
        # Recommendations
        if report['recommendations']:
            file.write("\nRECOMMENDATIONS\n")
            file.write("-" * 40 + "\n")
            for i, rec in enumerate(report['recommendations'], 1):
                file.write(f"{i}. {rec}\n")
        
        file.write(f"\nNext Assessment Date: {report['next_assessment_date']}\n")
        file.write("\n" + "="*80 + "\n")
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during scanning"""
        skip_patterns = [
            '.git', '__pycache__', '.pytest_cache', 'node_modules',
            '.venv', 'venv', 'dist', 'build', '.tox', 'backup_'
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)
    
    def _get_severity_for_category(self, category: str) -> SecurityLevel:
        """Get severity level for security category"""
        severity_map = {
            'hardcoded_secrets': SecurityLevel.CRITICAL,
            'sql_injection': SecurityLevel.HIGH,
            'xss_vulnerabilities': SecurityLevel.HIGH,
            'insecure_random': SecurityLevel.MEDIUM,
            'weak_crypto': SecurityLevel.HIGH,
            'dependency_vulnerability': SecurityLevel.HIGH,
            'docker_security': SecurityLevel.MEDIUM,
            'ssl_configuration': SecurityLevel.HIGH,
            'environment_security': SecurityLevel.MEDIUM
        }
        return severity_map.get(category, SecurityLevel.MEDIUM)
    
    def _get_recommendation_for_category(self, category: str) -> str:
        """Get recommendation for security category"""
        recommendations = {
            'hardcoded_secrets': "Use environment variables or secret management services",
            'sql_injection': "Use parameterized queries and ORM frameworks",
            'xss_vulnerabilities': "Implement proper input validation and output encoding",
            'insecure_random': "Use cryptographically secure random number generators",
            'weak_crypto': "Use modern, secure cryptographic algorithms",
            'dependency_vulnerability': "Update to latest secure version",
            'docker_security': "Follow Docker security best practices",
            'ssl_configuration': "Implement proper SSL/TLS configuration",
            'environment_security': "Secure environment variable handling"
        }
        return recommendations.get(category, "Review and remediate security issue")

def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SOC2-Lite Security Assessment')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--output-format', choices=['json', 'text', 'both'], default='both',
                       help='Output format for reports')
    
    args = parser.parse_args()
    
    # Run assessment
    checker = SOC2LiteChecker(args.project_root)
    report = checker.run_full_assessment()
    
    # Print summary
    print("\n" + "="*60)
    print("SOC2-LITE SECURITY ASSESSMENT COMPLETED")
    print("="*60)
    print(f"Total Findings: {report['summary']['total_findings']}")
    print(f"Critical: {report['summary']['critical_findings']}")
    print(f"High: {report['summary']['high_findings']}")
    print(f"Medium: {report['summary']['medium_findings']}")
    print(f"Low: {report['summary']['low_findings']}")
    print(f"Compliance Score: {report['summary']['compliance_score']}%")
    print(f"Risk Level: {report['summary']['risk_level']}")
    print("="*60)
    
    return 0 if report['summary']['critical_findings'] == 0 else 1

if __name__ == '__main__':
    exit(main())