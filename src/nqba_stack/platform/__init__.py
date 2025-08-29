"""
FLYFOX AI Platform - Complete AI Service Ecosystem
==================================================

Platform components for FLYFOX AI:
- Dynamic Landing Pages
- QAaaS Platform
- Client Portal
- Service Dashboard
- Agent Suite
- FLYFOX Platform (Built Like GoHighLevel from Scratch)
- Client Communication System
"""

from .landing_pages import LandingPageGenerator, LandingPageConfig, LandingPageType
from .qaas_platform import QAaaSPlatform
from .client_portal import ClientPortal, ClientConfig, ClientTier, PortalFeature
from .service_dashboard import ServiceDashboard, ServiceMetrics, DashboardMetric
from .agent_suite import AgentSuite, AgentSuiteConfig, WhiteLabelType
from .flyfox_platform import FLYFOXPlatform, PlatformConfig, PlatformTier, ServiceCategory
from .flyfox_platform_like_gohighlevel import (
    FLYFOXPlatform as FLYFOXPlatformGoHighLevel,
    PlatformConfig as GoHighLevelPlatformConfig,
    PlatformTier as GoHighLevelPlatformTier,
    VoiceAgentConfig,
    VoiceAgentType,
    ModuleType,
    CalendarConfig,
    CRMModule,
    MarketingModule,
    FunnelModule
)
from .client_communication import (
    ClientCommunicationSystem, 
    ContactForm, 
    SupportTicket, 
    CommunicationRecord,
    CommunicationType,
    PriorityLevel,
    Status,
    TeamMember
)

__all__ = [
    # Landing Pages
    "LandingPageGenerator",
    "LandingPageConfig", 
    "LandingPageType",
    
    # QAaaS Platform
    "QAaaSPlatform",
    
    # Client Portal
    "ClientPortal",
    "ClientConfig",
    "ClientTier",
    "PortalFeature",
    
    # Service Dashboard
    "ServiceDashboard",
    "ServiceMetrics",
    "DashboardMetric",
    
    # Agent Suite
    "AgentSuite",
    "AgentSuiteConfig",
    "WhiteLabelType",
    
    # FLYFOX Platform (Original)
    "FLYFOXPlatform",
    "PlatformConfig",
    "PlatformTier",
    "ServiceCategory",
    
    # FLYFOX Platform (Built Like GoHighLevel from Scratch)
    "FLYFOXPlatformGoHighLevel",
    "GoHighLevelPlatformConfig",
    "GoHighLevelPlatformTier",
    "VoiceAgentConfig",
    "VoiceAgentType",
    "ModuleType",
    "CalendarConfig",
    "CRMModule",
    "MarketingModule",
    "FunnelModule",
    
    # Client Communication System
    "ClientCommunicationSystem",
    "ContactForm",
    "SupportTicket", 
    "CommunicationRecord",
    "CommunicationType",
    "PriorityLevel",
    "Status",
    "TeamMember"
]
