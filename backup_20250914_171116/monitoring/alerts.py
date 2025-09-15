"""Alerting System for Quantum Nexus Engine"""

import asyncio
import json
import logging
import smtplib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass, field
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import aiohttp
import redis.asyncio as redis

from .health_checks import HealthStatus, HealthCheckResult, SystemHealthStatus
from .metrics import JobStatus

# Configure logging
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class AlertStatus(Enum):
    """Alert status"""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"
    SUPPRESSED = "suppressed"

class NotificationChannel(Enum):
    """Notification channels"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    DISCORD = "discord"

@dataclass
class AlertRule:
    """Alert rule definition"""
    name: str
    description: str
    severity: AlertSeverity
    condition: str  # Prometheus-style query or condition
    threshold: float
    duration: int  # seconds
    channels: List[NotificationChannel]
    enabled: bool = True
    cooldown: int = 300  # seconds between alerts
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'severity': self.severity.value,
            'condition': self.condition,
            'threshold': self.threshold,
            'duration': self.duration,
            'channels': [ch.value for ch in self.channels],
            'enabled': self.enabled,
            'cooldown': self.cooldown,
            'tags': self.tags
        }

@dataclass
class Alert:
    """Alert instance"""
    rule_name: str
    severity: AlertSeverity
    title: str
    message: str
    status: AlertStatus = AlertStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    details: Dict[str, Any] = field(default_factory=dict)
    alert_id: str = field(default_factory=lambda: f"alert_{int(datetime.now().timestamp())}") 
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'rule_name': self.rule_name,
            'severity': self.severity.value,
            'title': self.title,
            'message': self.message,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'acknowledged_at': self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            'acknowledged_by': self.acknowledged_by,
            'tags': self.tags,
            'details': self.details
        }
    
    def acknowledge(self, acknowledged_by: str):
        """Acknowledge the alert"""
        self.status = AlertStatus.ACKNOWLEDGED
        self.acknowledged_at = datetime.now(timezone.utc)
        self.acknowledged_by = acknowledged_by
        self.updated_at = datetime.now(timezone.utc)
    
    def resolve(self):
        """Resolve the alert"""
        self.status = AlertStatus.RESOLVED
        self.resolved_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

class NotificationProvider:
    """Base notification provider"""
    
    def __init__(self, channel: NotificationChannel):
        self.channel = channel
    
    async def send_notification(self, alert: Alert, config: Dict[str, Any]) -> bool:
        """Send notification for alert"""
        raise NotImplementedError

class EmailNotificationProvider(NotificationProvider):
    """Email notification provider"""
    
    def __init__(self):
        super().__init__(NotificationChannel.EMAIL)
    
    async def send_notification(self, alert: Alert, config: Dict[str, Any]) -> bool:
        """Send email notification"""
        try:
            smtp_server = config.get('smtp_server', 'localhost')
            smtp_port = config.get('smtp_port', 587)
            username = config.get('username')
            password = config.get('password')
            from_email = config.get('from_email', 'alerts@quantum-nexus.com')
            to_emails = config.get('to_emails', [])
            
            if not to_emails:
                logger.warning("No email recipients configured")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            # Email body
            body = self._create_email_body(alert)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if username and password:
                    server.starttls()
                    server.login(username, password)
                
                server.send_message(msg)
            
            logger.info(f"Email alert sent for {alert.alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")
            return False
    
    def _create_email_body(self, alert: Alert) -> str:
        """Create HTML email body"""
        severity_colors = {
            AlertSeverity.CRITICAL: '#dc3545',
            AlertSeverity.HIGH: '#fd7e14',
            AlertSeverity.MEDIUM: '#ffc107',
            AlertSeverity.LOW: '#28a745',
            AlertSeverity.INFO: '#17a2b8'
        }
        
        color = severity_colors.get(alert.severity, '#6c757d')
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="background-color: {color}; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                    <h1 style="margin: 0; font-size: 24px;">{alert.title}</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Severity: {alert.severity.value.upper()}</p>
                </div>
                
                <div style="padding: 20px;">
                    <h2 style="color: #333; margin-top: 0;">Alert Details</h2>
                    <p style="color: #666; line-height: 1.6;">{alert.message}</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #333;">Alert ID:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; color: #666;">{alert.alert_id}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #333;">Rule:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; color: #666;">{alert.rule_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #333;">Created:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; color: #666;">{alert.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #333;">Status:</td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee; color: #666;">{alert.status.value.upper()}</td>
                        </tr>
                    </table>
                    
                    {self._format_alert_details(alert.details) if alert.details else ''}
                </div>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 0 0 8px 8px; text-align: center;">
                    <p style="margin: 0; color: #666; font-size: 12px;">Quantum Nexus Engine Monitoring System</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _format_alert_details(self, details: Dict[str, Any]) -> str:
        """Format alert details as HTML"""
        if not details:
            return ""
        
        html = "<h3 style='color: #333; margin-bottom: 10px;'>Additional Details</h3>"
        html += "<ul style='color: #666; line-height: 1.6;'>"
        
        for key, value in details.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        
        html += "</ul>"
        return html

class SlackNotificationProvider(NotificationProvider):
    """Slack notification provider"""
    
    def __init__(self):
        super().__init__(NotificationChannel.SLACK)
    
    async def send_notification(self, alert: Alert, config: Dict[str, Any]) -> bool:
        """Send Slack notification"""
        try:
            webhook_url = config.get('webhook_url')
            if not webhook_url:
                logger.warning("No Slack webhook URL configured")
                return False
            
            # Create Slack message
            message = self._create_slack_message(alert)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=message) as response:
                    if response.status == 200:
                        logger.info(f"Slack alert sent for {alert.alert_id}")
                        return True
                    else:
                        logger.error(f"Slack webhook returned status {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {str(e)}")
            return False
    
    def _create_slack_message(self, alert: Alert) -> Dict[str, Any]:
        """Create Slack message payload"""
        severity_colors = {
            AlertSeverity.CRITICAL: '#dc3545',
            AlertSeverity.HIGH: '#fd7e14',
            AlertSeverity.MEDIUM: '#ffc107',
            AlertSeverity.LOW: '#28a745',
            AlertSeverity.INFO: '#17a2b8'
        }
        
        color = severity_colors.get(alert.severity, '#6c757d')
        
        fields = [
            {
                "title": "Alert ID",
                "value": alert.alert_id,
                "short": True
            },
            {
                "title": "Rule",
                "value": alert.rule_name,
                "short": True
            },
            {
                "title": "Severity",
                "value": alert.severity.value.upper(),
                "short": True
            },
            {
                "title": "Status",
                "value": alert.status.value.upper(),
                "short": True
            }
        ]
        
        # Add details as fields
        for key, value in alert.details.items():
            fields.append({
                "title": key.replace('_', ' ').title(),
                "value": str(value),
                "short": True
            })
        
        return {
            "attachments": [
                {
                    "color": color,
                    "title": alert.title,
                    "text": alert.message,
                    "fields": fields,
                    "footer": "Quantum Nexus Engine",
                    "ts": int(alert.created_at.timestamp())
                }
            ]
        }

class WebhookNotificationProvider(NotificationProvider):
    """Generic webhook notification provider"""
    
    def __init__(self):
        super().__init__(NotificationChannel.WEBHOOK)
    
    async def send_notification(self, alert: Alert, config: Dict[str, Any]) -> bool:
        """Send webhook notification"""
        try:
            webhook_url = config.get('webhook_url')
            if not webhook_url:
                logger.warning("No webhook URL configured")
                return False
            
            headers = config.get('headers', {'Content-Type': 'application/json'})
            payload = alert.to_dict()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload, headers=headers) as response:
                    if 200 <= response.status < 300:
                        logger.info(f"Webhook alert sent for {alert.alert_id}")
                        return True
                    else:
                        logger.error(f"Webhook returned status {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {str(e)}")
            return False

class AlertManager:
    """Alert management system"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}
        self.providers: Dict[NotificationChannel, NotificationProvider] = {
            NotificationChannel.EMAIL: EmailNotificationProvider(),
            NotificationChannel.SLACK: SlackNotificationProvider(),
            NotificationChannel.WEBHOOK: WebhookNotificationProvider()
        }
        self.notification_configs: Dict[NotificationChannel, Dict[str, Any]] = {}
        self.last_alert_times: Dict[str, datetime] = {}
    
    def add_rule(self, rule: AlertRule):
        """Add alert rule"""
        self.rules[rule.name] = rule
        logger.info(f"Added alert rule: {rule.name}")
    
    def remove_rule(self, rule_name: str):
        """Remove alert rule"""
        if rule_name in self.rules:
            del self.rules[rule_name]
            logger.info(f"Removed alert rule: {rule_name}")
    
    def configure_notifications(self, channel: NotificationChannel, config: Dict[str, Any]):
        """Configure notification channel"""
        self.notification_configs[channel] = config
        logger.info(f"Configured {channel.value} notifications")
    
    async def trigger_alert(self, rule_name: str, title: str, message: str, 
                          details: Dict[str, Any] = None, tags: Dict[str, str] = None) -> Optional[Alert]:
        """Trigger an alert"""
        if rule_name not in self.rules:
            logger.warning(f"Alert rule {rule_name} not found")
            return None
        
        rule = self.rules[rule_name]
        
        if not rule.enabled:
            logger.debug(f"Alert rule {rule_name} is disabled")
            return None
        
        # Check cooldown
        if self._is_in_cooldown(rule_name, rule.cooldown):
            logger.debug(f"Alert rule {rule_name} is in cooldown")
            return None
        
        # Create alert
        alert = Alert(
            rule_name=rule_name,
            severity=rule.severity,
            title=title,
            message=message,
            tags=tags or {},
            details=details or {}
        )
        
        # Store alert
        self.active_alerts[alert.alert_id] = alert
        self.last_alert_times[rule_name] = datetime.now(timezone.utc)
        
        # Send notifications
        await self._send_notifications(alert, rule)
        
        # Store in Redis for persistence
        await self._store_alert(alert)
        
        logger.info(f"Triggered alert: {alert.alert_id} ({rule_name})")
        return alert
    
    def _is_in_cooldown(self, rule_name: str, cooldown_seconds: int) -> bool:
        """Check if rule is in cooldown period"""
        if rule_name not in self.last_alert_times:
            return False
        
        last_alert = self.last_alert_times[rule_name]
        cooldown_end = last_alert + timedelta(seconds=cooldown_seconds)
        return datetime.now(timezone.utc) < cooldown_end
    
    async def _send_notifications(self, alert: Alert, rule: AlertRule):
        """Send notifications for alert"""
        for channel in rule.channels:
            if channel in self.providers and channel in self.notification_configs:
                provider = self.providers[channel]
                config = self.notification_configs[channel]
                
                try:
                    success = await provider.send_notification(alert, config)
                    if success:
                        logger.info(f"Sent {channel.value} notification for {alert.alert_id}")
                    else:
                        logger.warning(f"Failed to send {channel.value} notification for {alert.alert_id}")
                except Exception as e:
                    logger.error(f"Error sending {channel.value} notification: {str(e)}")
    
    async def _store_alert(self, alert: Alert):
        """Store alert in Redis"""
        try:
            redis_client = redis.from_url(self.redis_url)
            
            # Store alert data
            await redis_client.hset(
                f"alert:{alert.alert_id}",
                mapping={
                    'data': json.dumps(alert.to_dict()),
                    'created_at': alert.created_at.isoformat()
                }
            )
            
            # Add to active alerts set
            await redis_client.sadd("active_alerts", alert.alert_id)
            
            # Set expiration (30 days)
            await redis_client.expire(f"alert:{alert.alert_id}", 30 * 24 * 3600)
            
            await redis_client.close()
            
        except Exception as e:
            logger.error(f"Failed to store alert in Redis: {str(e)}")
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.acknowledge(acknowledged_by)
            await self._store_alert(alert)
            logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
            return True
        return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolve()
            await self._store_alert(alert)
            
            # Remove from active alerts
            del self.active_alerts[alert_id]
            
            # Remove from Redis active set
            try:
                redis_client = redis.from_url(self.redis_url)
                await redis_client.srem("active_alerts", alert_id)
                await redis_client.close()
            except Exception as e:
                logger.error(f"Failed to update Redis: {str(e)}")
            
            logger.info(f"Alert {alert_id} resolved")
            return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts"""
        return list(self.active_alerts.values())
    
    def get_alert(self, alert_id: str) -> Optional[Alert]:
        """Get specific alert"""
        return self.active_alerts.get(alert_id)
    
    async def check_health_alerts(self, system_health: SystemHealthStatus):
        """Check for health-based alerts"""
        # System-wide health alert
        if system_health.status == HealthStatus.UNHEALTHY:
            await self.trigger_alert(
                'system_unhealthy',
                'System Health Critical',
                f'System status is {system_health.status.value}',
                details={
                    'unhealthy_components': [
                        comp.component for comp in system_health.components 
                        if comp.status == HealthStatus.UNHEALTHY
                    ],
                    'total_components': len(system_health.components)
                }
            )
        
        # Component-specific alerts
        for component in system_health.components:
            if component.status == HealthStatus.UNHEALTHY:
                await self.trigger_alert(
                    f'component_{component.component}_unhealthy',
                    f'Component {component.component} Unhealthy',
                    component.message,
                    details={
                        'component_type': component.component_type.value,
                        'response_time_ms': component.response_time_ms,
                        **component.details
                    }
                )
    
    async def check_quantum_job_alerts(self, job_id: str, status: JobStatus, 
                                     duration: float, error_message: str = None):
        """Check for quantum job alerts"""
        if status == JobStatus.FAILED:
            await self.trigger_alert(
                'quantum_job_failed',
                f'Quantum Job Failed: {job_id}',
                f'Job {job_id} failed after {duration:.2f} seconds',
                details={
                    'job_id': job_id,
                    'duration_seconds': duration,
                    'error_message': error_message
                }
            )
        elif duration > 300:  # 5 minutes
            await self.trigger_alert(
                'quantum_job_slow',
                f'Quantum Job Running Slowly: {job_id}',
                f'Job {job_id} has been running for {duration:.2f} seconds',
                details={
                    'job_id': job_id,
                    'duration_seconds': duration
                }
            )

def create_default_alert_rules() -> List[AlertRule]:
    """Create default alert rules"""
    return [
        AlertRule(
            name='system_unhealthy',
            description='System health is critical',
            severity=AlertSeverity.CRITICAL,
            condition='system_health == "unhealthy"',
            threshold=1,
            duration=60,
            channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK],
            cooldown=300
        ),
        AlertRule(
            name='high_error_rate',
            description='High error rate detected',
            severity=AlertSeverity.HIGH,
            condition='error_rate > 0.05',
            threshold=0.05,
            duration=300,
            channels=[NotificationChannel.EMAIL],
            cooldown=600
        ),
        AlertRule(
            name='quantum_job_failed',
            description='Quantum job failed',
            severity=AlertSeverity.MEDIUM,
            condition='job_status == "failed"',
            threshold=1,
            duration=0,
            channels=[NotificationChannel.SLACK],
            cooldown=60
        ),
        AlertRule(
            name='quantum_job_slow',
            description='Quantum job running slowly',
            severity=AlertSeverity.LOW,
            condition='job_duration > 300',
            threshold=300,
            duration=0,
            channels=[NotificationChannel.SLACK],
            cooldown=300
        ),
        AlertRule(
            name='component_unhealthy',
            description='Component health check failed',
            severity=AlertSeverity.MEDIUM,
            condition='component_health == "unhealthy"',
            threshold=1,
            duration=120,
            channels=[NotificationChannel.EMAIL],
            cooldown=600
        )
    ]

def setup_alerting(redis_url: str = "redis://localhost:6379") -> AlertManager:
    """Setup alerting system"""
    manager = AlertManager(redis_url)
    
    # Add default rules
    for rule in create_default_alert_rules():
        manager.add_rule(rule)
    
    logger.info(f"Alert manager initialized with {len(manager.rules)} rules")
    return manager

# Global alert manager
_alert_manager = None

def get_alert_manager() -> Optional[AlertManager]:
    """Get global alert manager"""
    return _alert_manager

def set_alert_manager(manager: AlertManager):
    """Set global alert manager"""
    global _alert_manager
    _alert_manager = manager