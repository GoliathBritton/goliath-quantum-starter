"""
NQBA Scheduled Audit System
Automated business assessment scheduling and execution
Provides continuous business intelligence and monitoring
"""
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import schedule
import time
from croniter import croniter

from .settings import get_settings
from .ltc_logger import get_ltc_logger
from .business_assessment import (
    assess_business_comprehensive,
    AuditType,
    BEMFramework,
    AssessmentResult
)

logger = logging.getLogger(__name__)

class AuditFrequency(Enum):
    """Audit frequency options"""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CONTINUOUS = "continuous"

class SubscriptionTier(Enum):
    """NQBA subscription tiers"""
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    QUANTUM_ELITE = "quantum_elite"

@dataclass
class AuditSchedule:
    """Audit schedule configuration"""
    company_id: str
    company_name: str
    subscription_tier: SubscriptionTier
    audit_frequency: AuditFrequency
    audit_types: List[AuditType]
    framework: BEMFramework
    use_quantum: bool
    next_audit_date: datetime
    last_audit_date: Optional[datetime] = None
    is_active: bool = True

@dataclass
class AuditExecution:
    """Audit execution record"""
    execution_id: str
    schedule_id: str
    company_id: str
    scheduled_date: datetime
    execution_date: datetime
    status: str  # "scheduled", "running", "completed", "failed"
    assessment_result: Optional[AssessmentResult] = None
    error_message: Optional[str] = None

class NQBAScheduledAudits:
    """NQBA Scheduled Audit System"""
    
    def __init__(self):
        """Initialize the scheduled audit system"""
        self.settings = get_settings()
        self.ltc_logger = get_ltc_logger()
        
        # In-memory storage (would be database in production)
        self.audit_schedules: Dict[str, AuditSchedule] = {}
        self.audit_executions: Dict[str, AuditExecution] = {}
        
        # Subscription tier configurations
        self.tier_configs = self._initialize_tier_configurations()
        
        # Start the scheduler
        self.scheduler_running = False
        asyncio.create_task(self._start_scheduler())
    
    def _initialize_tier_configurations(self) -> Dict[SubscriptionTier, Dict[str, Any]]:
        """Initialize subscription tier configurations"""
        return {
            SubscriptionTier.BASIC: {
                "audit_frequency": AuditFrequency.MONTHLY,
                "audit_types": [AuditType.FINANCIAL, AuditType.OPERATIONAL],
                "framework": BEMFramework.BALDRIGE,
                "use_quantum": False,
                "monthly_price": 5000,
                "audit_included": False
            },
            SubscriptionTier.PROFESSIONAL: {
                "audit_frequency": AuditFrequency.QUARTERLY,
                "audit_types": [AuditType.FINANCIAL, AuditType.OPERATIONAL, AuditType.COMPLIANCE],
                "framework": BEMFramework.BALDRIGE,
                "use_quantum": True,
                "monthly_price": 15000,
                "audit_included": True
            },
            SubscriptionTier.ENTERPRISE: {
                "audit_frequency": AuditFrequency.MONTHLY,
                "audit_types": [
                    AuditType.FINANCIAL, AuditType.OPERATIONAL, AuditType.COMPLIANCE,
                    AuditType.IT_SECURITY, AuditType.STRATEGIC
                ],
                "framework": BEMFramework.EFQM,
                "use_quantum": True,
                "monthly_price": 50000,
                "audit_included": True
            },
            SubscriptionTier.QUANTUM_ELITE: {
                "audit_frequency": AuditFrequency.CONTINUOUS,
                "audit_types": [
                    AuditType.FINANCIAL, AuditType.OPERATIONAL, AuditType.COMPLIANCE,
                    AuditType.IT_SECURITY, AuditType.STRATEGIC, AuditType.RISK,
                    AuditType.SMETA, AuditType.SUSTAINABILITY
                ],
                "framework": BEMFramework.EFQM,
                "use_quantum": True,
                "monthly_price": 100000,
                "audit_included": True
            }
        }
    
    async def _start_scheduler(self):
        """Start the audit scheduler"""
        if self.scheduler_running:
            return
        
        self.scheduler_running = True
        logger.info("NQBA Scheduled Audit System started")
        
        while self.scheduler_running:
            try:
                # Check for scheduled audits
                await self._check_scheduled_audits()
                
                # Sleep for 1 minute before next check
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def _check_scheduled_audits(self):
        """Check for audits that need to be executed"""
        current_time = datetime.now()
        
        for schedule_id, audit_schedule in self.audit_schedules.items():
            if not audit_schedule.is_active:
                continue
            
            # Check if it's time for the next audit
            if current_time >= audit_schedule.next_audit_date:
                await self._execute_scheduled_audit(audit_schedule)
    
    async def _execute_scheduled_audit(self, audit_schedule: AuditSchedule):
        """Execute a scheduled audit"""
        execution_id = f"EXEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{audit_schedule.company_id}"
        
        # Create execution record
        execution = AuditExecution(
            execution_id=execution_id,
            schedule_id=audit_schedule.company_id,
            company_id=audit_schedule.company_id,
            scheduled_date=audit_schedule.next_audit_date,
            execution_date=datetime.now(),
            status="running"
        )
        
        self.audit_executions[execution_id] = execution
        
        try:
            # Log audit execution start
            self.ltc_logger.log_operation(
                operation_type="scheduled_audit_started",
                operation_data={
                    "execution_id": execution_id,
                    "company_id": audit_schedule.company_id,
                    "company_name": audit_schedule.company_name,
                    "audit_frequency": audit_schedule.audit_frequency.value,
                    "audit_types": [at.value for at in audit_schedule.audit_types],
                    "framework": audit_schedule.framework.value,
                    "use_quantum": audit_schedule.use_quantum
                },
                thread_ref="SCHEDULED_AUDITS"
            )
            
            # Get company data (would be from database in production)
            company_data = await self._get_company_data(audit_schedule.company_id)
            
            # Perform comprehensive assessment
            assessment_result = await assess_business_comprehensive(
                company_data=company_data,
                audit_types=audit_schedule.audit_types,
                framework=audit_schedule.framework,
                use_quantum=audit_schedule.use_quantum
            )
            
            # Update execution record
            execution.status = "completed"
            execution.assessment_result = assessment_result
            
            # Update schedule
            audit_schedule.last_audit_date = datetime.now()
            audit_schedule.next_audit_date = self._calculate_next_audit_date(
                audit_schedule.audit_frequency, datetime.now()
            )
            
            # Log audit completion
            self.ltc_logger.log_operation(
                operation_type="scheduled_audit_completed",
                operation_data={
                    "execution_id": execution_id,
                    "company_id": audit_schedule.company_id,
                    "overall_score": assessment_result.overall_score,
                    "recommendations_count": len(assessment_result.recommendations),
                    "next_audit_date": audit_schedule.next_audit_date.isoformat()
                },
                thread_ref="SCHEDULED_AUDITS"
            )
            
            # Send notifications (would integrate with notification system)
            await self._send_audit_notifications(audit_schedule, assessment_result)
            
        except Exception as e:
            logger.error(f"Audit execution failed for {audit_schedule.company_id}: {e}")
            
            # Update execution record
            execution.status = "failed"
            execution.error_message = str(e)
            
            # Log audit failure
            self.ltc_logger.log_operation(
                operation_type="scheduled_audit_failed",
                operation_data={
                    "execution_id": execution_id,
                    "company_id": audit_schedule.company_id,
                    "error_message": str(e)
                },
                thread_ref="SCHEDULED_AUDITS"
            )
    
    def _calculate_next_audit_date(self, frequency: AuditFrequency, current_date: datetime) -> datetime:
        """Calculate the next audit date based on frequency"""
        if frequency == AuditFrequency.WEEKLY:
            return current_date + timedelta(weeks=1)
        elif frequency == AuditFrequency.MONTHLY:
            return current_date + timedelta(days=30)
        elif frequency == AuditFrequency.QUARTERLY:
            return current_date + timedelta(days=90)
        elif frequency == AuditFrequency.YEARLY:
            return current_date + timedelta(days=365)
        elif frequency == AuditFrequency.CONTINUOUS:
            return current_date + timedelta(days=7)  # Weekly for continuous
        else:
            return current_date + timedelta(days=30)  # Default to monthly
    
    async def _get_company_data(self, company_id: str) -> Dict[str, Any]:
        """Get company data for assessment (placeholder implementation)"""
        # In production, this would fetch from database
        return {
            "company_id": company_id,
            "revenue": 10000000,  # $10M
            "expenses": 8000000,  # $8M
            "assets": 15000000,   # $15M
            "liabilities": 5000000,  # $5M
            "current_assets": 3000000,  # $3M
            "current_liabilities": 1000000,  # $1M
            "operational_efficiency": 0.85,
            "productivity_score": 0.82,
            "quality_score": 0.88,
            "regulatory_compliance": 0.92,
            "internal_policies": 0.87,
            "ethical_standards": 0.95
        }
    
    async def _send_audit_notifications(self, audit_schedule: AuditSchedule, assessment_result: AssessmentResult):
        """Send audit notifications to stakeholders"""
        # Placeholder implementation - would integrate with notification system
        logger.info(f"Audit notification sent for {audit_schedule.company_name}")
    
    # Public API methods
    
    async def subscribe_company(
        self,
        company_id: str,
        company_name: str,
        subscription_tier: SubscriptionTier,
        custom_audit_types: List[AuditType] = None,
        custom_framework: BEMFramework = None
    ) -> str:
        """Subscribe a company to NQBA scheduled audits"""
        
        # Get tier configuration
        tier_config = self.tier_configs[subscription_tier]
        
        # Use custom settings if provided, otherwise use tier defaults
        audit_types = custom_audit_types or tier_config["audit_types"]
        framework = custom_framework or tier_config["framework"]
        audit_frequency = tier_config["audit_frequency"]
        use_quantum = tier_config["use_quantum"]
        
        # Create audit schedule
        audit_schedule = AuditSchedule(
            company_id=company_id,
            company_name=company_name,
            subscription_tier=subscription_tier,
            audit_frequency=audit_frequency,
            audit_types=audit_types,
            framework=framework,
            use_quantum=use_quantum,
            next_audit_date=self._calculate_next_audit_date(audit_frequency, datetime.now())
        )
        
        # Store schedule
        self.audit_schedules[company_id] = audit_schedule
        
        # Log subscription
        self.ltc_logger.log_operation(
            operation_type="company_subscribed",
            operation_data={
                "company_id": company_id,
                "company_name": company_name,
                "subscription_tier": subscription_tier.value,
                "audit_frequency": audit_frequency.value,
                "audit_types": [at.value for at in audit_types],
                "framework": framework.value,
                "use_quantum": use_quantum,
                "monthly_price": tier_config["monthly_price"]
            },
            thread_ref="SCHEDULED_AUDITS"
        )
        
        return company_id
    
    async def unsubscribe_company(self, company_id: str) -> bool:
        """Unsubscribe a company from NQBA scheduled audits"""
        if company_id in self.audit_schedules:
            self.audit_schedules[company_id].is_active = False
            
            # Log unsubscription
            self.ltc_logger.log_operation(
                operation_type="company_unsubscribed",
                operation_data={"company_id": company_id},
                thread_ref="SCHEDULED_AUDITS"
            )
            
            return True
        return False
    
    async def upgrade_subscription(
        self,
        company_id: str,
        new_tier: SubscriptionTier
    ) -> bool:
        """Upgrade a company's subscription tier"""
        if company_id not in self.audit_schedules:
            return False
        
        old_tier = self.audit_schedules[company_id].subscription_tier
        new_tier_config = self.tier_configs[new_tier]
        
        # Update schedule with new tier configuration
        self.audit_schedules[company_id].subscription_tier = new_tier
        self.audit_schedules[company_id].audit_frequency = new_tier_config["audit_frequency"]
        self.audit_schedules[company_id].audit_types = new_tier_config["audit_types"]
        self.audit_schedules[company_id].framework = new_tier_config["framework"]
        self.audit_schedules[company_id].use_quantum = new_tier_config["use_quantum"]
        
        # Log upgrade
        self.ltc_logger.log_operation(
            operation_type="subscription_upgraded",
            operation_data={
                "company_id": company_id,
                "old_tier": old_tier.value,
                "new_tier": new_tier.value,
                "new_monthly_price": new_tier_config["monthly_price"]
            },
            thread_ref="SCHEDULED_AUDITS"
        )
        
        return True
    
    async def get_company_audit_history(self, company_id: str) -> List[AuditExecution]:
        """Get audit history for a company"""
        return [
            execution for execution in self.audit_executions.values()
            if execution.company_id == company_id
        ]
    
    async def get_upcoming_audits(self, days: int = 30) -> List[AuditSchedule]:
        """Get upcoming audits in the next N days"""
        cutoff_date = datetime.now() + timedelta(days=days)
        return [
            schedule for schedule in self.audit_schedules.values()
            if schedule.is_active and schedule.next_audit_date <= cutoff_date
        ]
    
    async def get_subscription_stats(self) -> Dict[str, Any]:
        """Get subscription statistics"""
        total_subscribers = len([s for s in self.audit_schedules.values() if s.is_active])
        tier_counts = {}
        revenue_by_tier = {}
        
        for tier in SubscriptionTier:
            tier_subscribers = len([
                s for s in self.audit_schedules.values()
                if s.is_active and s.subscription_tier == tier
            ])
            tier_counts[tier.value] = tier_subscribers
            revenue_by_tier[tier.value] = tier_subscribers * self.tier_configs[tier]["monthly_price"]
        
        total_monthly_revenue = sum(revenue_by_tier.values())
        
        return {
            "total_subscribers": total_subscribers,
            "tier_distribution": tier_counts,
            "revenue_by_tier": revenue_by_tier,
            "total_monthly_revenue": total_monthly_revenue,
            "annual_revenue_projection": total_monthly_revenue * 12
        }

# Global instance
scheduled_audits = NQBAScheduledAudits()

# Convenience functions
async def subscribe_company(
    company_id: str,
    company_name: str,
    subscription_tier: SubscriptionTier,
    custom_audit_types: List[AuditType] = None,
    custom_framework: BEMFramework = None
) -> str:
    """Subscribe a company to NQBA scheduled audits"""
    return await scheduled_audits.subscribe_company(
        company_id, company_name, subscription_tier, custom_audit_types, custom_framework
    )

async def get_subscription_stats() -> Dict[str, Any]:
    """Get subscription statistics"""
    return await scheduled_audits.get_subscription_stats()
