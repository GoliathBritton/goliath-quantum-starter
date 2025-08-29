#!/usr/bin/env python3
"""
FLYFOX AI GoHighLevel Integration Platform Demo
===============================================

Demonstrates the GoHighLevel-inspired platform with:
- GoHighLevel SaaS integration
- Voice calling agents for sales & appointments
- Calendar integration with your booking widget
- Admin access for platform owner
- Quantum AI enhancement layer

This platform integrates with your existing GoHighLevel while adding quantum AI capabilities.
"""

import asyncio
import json
from datetime import datetime
from src.nqba_stack.platform.flyfox_gohighlevel_platform import (
    FLYFOXGoHighLevelPlatform,
    PlatformConfig,
    PlatformTier,
    VoiceAgentConfig,
    VoiceAgentType
)

def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"🚀 {title}")
    print("=" * 70)

def print_section(title: str):
    """Print formatted section"""
    print(f"\n📋 {title}")
    print("-" * 50)

def demo_gohighlevel_platform():
    """Demonstrate the GoHighLevel-inspired FLYFOX AI platform"""
    
    print_header("FLYFOX AI GoHighLevel Integration Platform Demo")
    print("Integrating with your existing GoHighLevel SaaS + Quantum AI capabilities! 🚀")
    
    # Initialize platform
    platform = FLYFOXGoHighLevelPlatform()
    
    # 1. Show admin access for John Britton
    print_section("John Britton - Platform Owner Admin Access")
    
    admin_access = platform.get_admin_access("john_britton")
    if "error" not in admin_access:
        user_info = admin_access["user_info"]
        print(f"👤 {user_info['name']} - {user_info['role']}")
        print(f"📧 Email: {user_info['email']}")
        print(f"📱 Phone: {user_info['phone']}")
        print(f"🔑 Access Level: {user_info['access_level']}")
        print(f"📅 Created: {user_info['created_at']}")
        print(f"✅ Status: {user_info['status']}")
        
        print("\n🔐 Full Permissions:")
        for permission in user_info['permissions']:
            print(f"   • {permission.replace('_', ' ').title()}")
        
        print("\n📊 Platform Access:")
        platform_access = admin_access["platform_access"]
        print(f"   • Customers: {platform_access['customers']}")
        print(f"   • Voice Agents: {platform_access['voice_agents']}")
        print(f"   • Integrations: {platform_access['integrations']}")
        print(f"   • Calendars: {platform_access['calendars']}")
        
        print("\n🏥 System Health:")
        system_health = admin_access["system_health"]
        print(f"   • Status: {system_health['status']}")
        print(f"   • Uptime: {system_health['uptime']}")
        print(f"   • Quantum AI: {system_health['quantum_ai_status']}")
        print(f"   • Last Backup: {system_health['last_backup']}")
    else:
        print(f"❌ Admin access error: {admin_access['error']}")
    
    # 2. Show available integrations
    print_section("Available Platform Integrations")
    
    integrations = platform.integrations
    for integration_id, integration in integrations.items():
        print(f"\n🔗 {integration['name']}")
        print(f"   • Type: {integration['type'].value}")
        print(f"   • URL: {integration.get('url', 'N/A')}")
        print(f"   • Sync: {'✅ Enabled' if integration['sync_enabled'] else '❌ Disabled'}")
        print(f"   • Features:")
        for feature in integration['features']:
            print(f"      - {feature}")
    
    # 3. Show calendar integrations
    print_section("Calendar Integrations")
    
    calendars = platform.calendar_integrations
    for calendar_id, calendar in calendars.items():
        print(f"\n📅 {calendar.platform}")
        print(f"   • URL: {calendar.url}")
        print(f"   • Sync Frequency: {calendar.sync_frequency}")
        if calendar.api_key:
            print(f"   • API Key: {'✅ Configured' if calendar.api_key else '❌ Not configured'}")
        if calendar.webhook_url:
            print(f"   • Webhook: {'✅ Configured' if calendar.webhook_url else '❌ Not configured'}")
    
    # 4. Demo customer platform setup
    print_section("Customer Platform Setup Demo")
    
    # Create sample customers
    customer_configs = [
        PlatformConfig(
            tier=PlatformTier.STARTER,
            company_size="Small Business",
            industry="Technology",
            primary_use_case="Basic AI features",
            expected_usage="Low to moderate"
        ),
        PlatformConfig(
            tier=PlatformTier.PROFESSIONAL,
            company_size="Medium Business",
            industry="Manufacturing",
            primary_use_case="Advanced AI + automation",
            expected_usage="Moderate to high"
        ),
        PlatformConfig(
            tier=PlatformTier.ENTERPRISE,
            company_size="Large Enterprise",
            industry="Financial Services",
            primary_use_case="Full quantum AI suite",
            expected_usage="High volume"
        ),
        PlatformConfig(
            tier=PlatformTier.AGENCY,
            company_size="Agency",
            industry="Marketing",
            primary_use_case="White label + partner program",
            expected_usage="Multi-client"
        )
    ]
    
    print("Setting up customer platforms...")
    for i, config in enumerate(customer_configs, 1):
        print(f"\n🏢 Customer {i}: {config.tier.value.title()} Tier")
        print(f"   • Company Size: {config.company_size}")
        print(f"   • Industry: {config.industry}")
        print(f"   • Use Case: {config.primary_use_case}")
        
        result = platform.setup_customer_platform(config)
        
        if result["success"]:
            print(f"   ✅ Success! Customer ID: {result['customer_id']}")
            print(f"   🌐 Platform URL: {result['platform_url']}")
            print(f"   🔗 GoHighLevel Sync: {result['gohighlevel_sync']}")
            print(f"   🤖 Voice Agents: {result['voice_agents']}")
            print(f"   📅 Calendar Access: {result['calendar_access']}")
            print("   📋 Next Steps:")
            for step in result["next_steps"]:
                print(f"      • {step}")
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    # 5. Demo voice agent creation
    print_section("Voice Calling Agent Creation Demo")
    
    # Create sample voice agents
    voice_agent_configs = [
        VoiceAgentConfig(
            agent_type=VoiceAgentType.SALES_AGENT,
            name="Quantum Sales Agent",
            personality="Consultative and solution-focused",
            script_template="Hi {name}, I'm calling about your interest in quantum AI solutions...",
            target_audience="Prospects and leads",
            call_objectives=["Generate sales", "Qualify opportunities", "Set appointments"],
            success_metrics=["Sales generated", "Conversion rate", "Appointments set"]
        ),
        VoiceAgentConfig(
            agent_type=VoiceAgentType.APPOINTMENT_SETTER,
            name="Appointment Setter Pro",
            personality="Professional and friendly",
            script_template="Hi {name}, this is {agent_name} from FLYFOX AI...",
            target_audience="Qualified leads",
            call_objectives=["Set appointments", "Qualify leads", "Follow up"],
            success_metrics=["Appointments booked", "Lead qualification rate", "Follow-up success"]
        ),
        VoiceAgentConfig(
            agent_type=VoiceAgentType.FOLLOW_UP_AGENT,
            name="Follow-up Specialist",
            personality="Helpful and persistent",
            script_template="Hi {name}, I'm following up on our recent conversation...",
            target_audience="Existing prospects",
            call_objectives=["Follow up", "Re-engage", "Nurture relationships"],
            success_metrics=["Re-engagement rate", "Follow-up success", "Relationship building"]
        )
    ]
    
    print("Creating voice calling agents...")
    for i, agent_config in enumerate(voice_agent_configs, 1):
        print(f"\n🤖 Voice Agent {i}: {agent_config.name}")
        print(f"   • Type: {agent_config.agent_type.value}")
        print(f"   • Personality: {agent_config.personality}")
        print(f"   • Target Audience: {agent_config.target_audience}")
        print(f"   • Call Objectives:")
        for objective in agent_config.call_objectives:
            print(f"      - {objective}")
        
        # Create agent for first customer (Professional tier)
        customer_ids = list(platform.customers.keys())
        if customer_ids:
            result = platform.create_voice_agent(customer_ids[0], agent_config)
            
            if result["success"]:
                print(f"   ✅ Success! Agent ID: {result['agent_id']}")
                print(f"   🎯 Status: {result['status']}")
                print(f"   🔗 Integration: {result['integration']}")
                print(f"   🚀 Capabilities:")
                for capability in result["capabilities"]:
                    print(f"      - {capability}")
            else:
                print(f"   ❌ Failed: {result['error']}")
    
    # 6. Demo GoHighLevel sync
    print_section("GoHighLevel Integration Sync Demo")
    
    customer_ids = list(platform.customers.keys())
    if customer_ids:
        print("Syncing with GoHighLevel SaaS...")
        
        sync_types = ["leads", "appointments", "automations", "funnels"]
        for sync_type in sync_types:
            print(f"\n🔄 Syncing {sync_type}...")
            result = platform.sync_with_gohighlevel(customer_ids[0], sync_type)
            
            if result["success"]:
                sync_result = result["sync_result"]
                print(f"   ✅ Successfully synced {sync_type}")
                print(f"   📊 Items Synced:")
                for item, count in sync_result["items_synced"].items():
                    print(f"      - {item.title()}: {count}")
                print(f"   ⏰ Timestamp: {sync_result['timestamp']}")
            else:
                print(f"   ❌ Failed: {result['error']}")
    
    # 7. Demo appointment booking
    print_section("Calendar Integration & Appointment Booking Demo")
    
    if customer_ids:
        print("Booking appointments through integrated calendar system...")
        
        appointment_details = {
            "client_name": "Sarah Johnson",
            "client_email": "sarah@techstartup.com",
            "service": "Quantum AI Consultation",
            "date": "2024-01-25",
            "time": "2:00 PM EST",
            "duration": "60 minutes",
            "notes": "Interested in qdLLM integration for SaaS platform"
        }
        
        result = platform.book_appointment(customer_ids[0], appointment_details)
        
        if result["success"]:
            print(f"   ✅ Appointment booked successfully!")
            print(f"   🆔 Appointment ID: {result['appointment_id']}")
            print(f"   📅 Status: {result['status']}")
            print(f"   🌐 Calendar URL: {result['calendar_url']}")
            print(f"   📧 Message: {result['message']}")
        else:
            print(f"   ❌ Failed: {result['error']}")
    
    # 8. Show platform analytics
    print_section("Platform Analytics & Performance")
    
    analytics = platform.get_platform_analytics()
    
    print("📊 Overview:")
    overview = analytics["overview"]
    print(f"   • Total Customers: {overview['total_customers']}")
    print(f"   • Total Revenue: ${overview['total_revenue']:,.2f}")
    print(f"   • Voice Agent Calls: {overview['voice_agent_calls']}")
    print(f"   • Appointments Booked: {overview['appointments_booked']}")
    print(f"   • GoHighLevel Syncs: {overview['gohighlevel_syncs']}")
    print(f"   • Quantum AI Usage: {overview['quantum_ai_usage']}")
    
    print("\n👥 Customer Breakdown:")
    customer_breakdown = analytics["customer_breakdown"]
    for tier, count in customer_breakdown["by_tier"].items():
        print(f"   • {tier.title()}: {count}")
    
    print("\n🤖 Voice Agent Performance:")
    voice_performance = analytics["voice_agent_performance"]
    print(f"   • Total Agents: {voice_performance['total_agents']}")
    print(f"   • Total Calls: {voice_performance['total_calls']}")
    print(f"   • Appointments Booked: {voice_performance['appointments_booked']}")
    
    print("\n🔗 Integration Status:")
    integration_status = analytics["integration_status"]
    for integration, status in integration_status.items():
        print(f"   • {integration.replace('_', ' ').title()}: {status}")
    
    # 9. Summary and next steps
    print_section("Platform Summary & Next Steps")
    
    print("🎯 What We've Built:")
    print("   1. 🔗 GoHighLevel Integration - Seamless CRM and automation")
    print("   2. 🤖 Voice Calling Agents - Sales and appointment setting")
    print("   3. 📅 Calendar Integration - Your booking widget connected")
    print("   4. 🔐 Admin Access - Full platform control for John")
    print("   5. ⚡ Quantum AI Layer - Enhanced capabilities")
    
    print("\n🚀 Ready to Use:")
    print("   • Access your platform: https://platform.flyfoxai.com")
    print("   • GoHighLevel: https://app.gohighlevel.com/agency_dashboard/")
    print("   • Calendar: https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8")
    print("   • Contact: john.britton@goliathomniedge.com | (517) 213-8392")
    
    print("\n💡 Next Steps:")
    print("   1. Start marketing your integrated platform")
    print("   2. Configure voice agents for your specific needs")
    print("   3. Set up automated workflows in GoHighLevel")
    print("   4. Begin using quantum AI features")
    print("   5. Scale with white label options")
    
    print_header("Demo Complete - Your GoHighLevel + FLYFOX AI Platform is Ready! 🚀✨")

if __name__ == "__main__":
    try:
        demo_gohighlevel_platform()
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please ensure all dependencies are properly installed.")
        import traceback
        traceback.print_exc()
