#!/usr/bin/env python3
"""
Simple Demo: DIY/DFY Pricing Model for All Agents
==================================================

This simplified demo showcases the complete DIY/DFY pricing ecosystem for all agents 
within the NQBA system without requiring heavy dependencies.

- DIY: Clients build solutions with QHC guidance and NQBA integration
- DFY: Agents build solutions with QHC oversight and quality control
- QHC (Quantum High Council) consultation included in all tiers
- Quantum Architect support for technical implementation
- Consistent monthly pricing with varying setup fees based on complexity
"""

import json
from datetime import datetime
from typing import Dict, Any, List
from enum import Enum


class ServiceTier(Enum):
    """Service tier enumeration"""

    DIY = "diy"  # Do It Yourself with QHC guidance
    DFY = "dfy"  # Done For You by agents with oversight


class UseCaseComplexity(Enum):
    """Use case complexity enumeration"""

    BASIC = "basic"  # Simple use case
    STANDARD = "standard"  # Moderate complexity
    ENTERPRISE = "enterprise"  # Complex enterprise solution


class AgentType(Enum):
    """Agent type enumeration"""

    QUANTUM_DIGITAL_AGENT = "quantum_digital_agent"
    QHC_CONSULTANT = "qhc_consultant"  # Quantum High Council
    QUANTUM_ARCHITECT = "quantum_architect"
    SALES_AGENT = "sales_agent"
    SUPPORT_AGENT = "support_agent"
    CUSTOM_AGENT = "custom_agent"


class PricingTier:
    """Pricing tier structure"""

    def __init__(
        self,
        tier: ServiceTier,
        complexity: UseCaseComplexity,
        monthly_price: float,
        setup_fee: float,
        included_calls_per_month: int,
        additional_call_cost: float,
        features: List[str],
        qhc_consultation_hours: int,
        quantum_architect_support: bool,
        custom_agent_build: bool,
        nqba_integration_level: str,
        roi_estimate: Dict[str, Any],
    ):
        self.tier = tier
        self.complexity = complexity
        self.monthly_price = monthly_price
        self.setup_fee = setup_fee
        self.included_calls_per_month = included_calls_per_month
        self.additional_call_cost = additional_call_cost
        self.features = features
        self.qhc_consultation_hours = qhc_consultation_hours
        self.quantum_architect_support = quantum_architect_support
        self.custom_agent_build = custom_agent_build
        self.nqba_integration_level = nqba_integration_level
        self.roi_estimate = roi_estimate


class ClientSubscription:
    """Client subscription structure"""

    def __init__(
        self,
        client_id: str,
        company_name: str,
        tier: ServiceTier,
        complexity: UseCaseComplexity,
        start_date: datetime,
    ):
        self.client_id = client_id
        self.company_name = company_name
        self.tier = tier
        self.complexity = complexity
        self.start_date = start_date
        self.setup_fee_paid = False
        self.monthly_fee_paid = False
        self.calls_used_this_month = 0
        self.qhc_consultation_hours_used = 0
        self.quantum_architect_sessions = 0
        self.custom_agents_built = 0
        self.nqba_integration_status = "pending"
        self.status = "active"


class SimplePricingDemo:
    """Simple demo class for showcasing the DIY/DFY pricing ecosystem"""

    def __init__(self):
        self.pricing_tiers = self._initialize_pricing_tiers()
        self.demo_clients = {}

    def _initialize_pricing_tiers(self) -> Dict[str, PricingTier]:
        """Initialize all pricing tiers for DIY and DFY options"""
        tiers = {}

        # DIY Tiers - Clients build with QHC guidance and NQBA integration
        tiers["diy_basic"] = PricingTier(
            tier=ServiceTier.DIY,
            complexity=UseCaseComplexity.BASIC,
            monthly_price=2500.0,
            setup_fee=20000.0,
            included_calls_per_month=1000,
            additional_call_cost=0.50,
            features=[
                "QHC consultation (10 hours/month)",
                "Quantum Architect guidance",
                "NQBA integration framework",
                "Basic agent templates",
                "Self-service dashboard",
                "Email support",
            ],
            qhc_consultation_hours=10,
            quantum_architect_support=True,
            custom_agent_build=False,
            nqba_integration_level="basic",
            roi_estimate={"time_to_value": "2-4 weeks", "expected_roi": "300-500%"},
        )

        tiers["diy_standard"] = PricingTier(
            tier=ServiceTier.DIY,
            complexity=UseCaseComplexity.STANDARD,
            monthly_price=2500.0,
            setup_fee=35000.0,
            included_calls_per_month=2500,
            additional_call_cost=0.40,
            features=[
                "QHC consultation (20 hours/month)",
                "Quantum Architect dedicated support",
                "Advanced NQBA integration",
                "Custom agent development",
                "Advanced analytics",
                "Priority support",
                "Training sessions",
            ],
            qhc_consultation_hours=20,
            quantum_architect_support=True,
            custom_agent_build=True,
            nqba_integration_level="standard",
            roi_estimate={"time_to_value": "4-6 weeks", "expected_roi": "400-700%"},
        )

        tiers["diy_enterprise"] = PricingTier(
            tier=ServiceTier.DIY,
            complexity=UseCaseComplexity.ENTERPRISE,
            monthly_price=2500.0,
            setup_fee=50000.0,
            included_calls_per_month=5000,
            additional_call_cost=0.30,
            features=[
                "QHC consultation (40 hours/month)",
                "Quantum Architect dedicated team",
                "Full NQBA integration",
                "Custom enterprise agents",
                "White-label solutions",
                "API access",
                "Dedicated support team",
                "Custom training programs",
            ],
            qhc_consultation_hours=40,
            quantum_architect_support=True,
            custom_agent_build=True,
            nqba_integration_level="enterprise",
            roi_estimate={"time_to_value": "6-8 weeks", "expected_roi": "500-1000%"},
        )

        # DFY Tiers - Agents build solutions with oversight
        tiers["dfy_basic"] = PricingTier(
            tier=ServiceTier.DFY,
            complexity=UseCaseComplexity.BASIC,
            monthly_price=2500.0,
            setup_fee=20000.0,
            included_calls_per_month=1000,
            additional_call_cost=0.50,
            features=[
                "Full solution built by agents",
                "QHC oversight and quality control",
                "NQBA integration completed",
                "Ready-to-use agents",
                "Ongoing maintenance",
                "24/7 support",
            ],
            qhc_consultation_hours=5,
            quantum_architect_support=True,
            custom_agent_build=True,
            nqba_integration_level="basic",
            roi_estimate={"time_to_value": "1-2 weeks", "expected_roi": "400-600%"},
        )

        tiers["dfy_standard"] = PricingTier(
            tier=ServiceTier.DFY,
            complexity=UseCaseComplexity.STANDARD,
            monthly_price=2500.0,
            setup_fee=35000.0,
            included_calls_per_month=2500,
            additional_call_cost=0.40,
            features=[
                "Advanced solution built by agents",
                "QHC strategic oversight",
                "Advanced NQBA integration",
                "Custom enterprise agents",
                "Advanced analytics dashboard",
                "Custom workflows",
                "Priority support",
                "Regular optimization",
            ],
            qhc_consultation_hours=10,
            quantum_architect_support=True,
            custom_agent_build=True,
            nqba_integration_level="standard",
            roi_estimate={"time_to_value": "2-3 weeks", "expected_roi": "500-800%"},
        )

        tiers["dfy_enterprise"] = PricingTier(
            tier=ServiceTier.DFY,
            complexity=UseCaseComplexity.ENTERPRISE,
            monthly_price=2500.0,
            setup_fee=50000.0,
            included_calls_per_month=5000,
            additional_call_cost=0.30,
            features=[
                "Enterprise solution built by agents",
                "QHC executive oversight",
                "Full NQBA integration",
                "Custom enterprise agents",
                "White-label platform",
                "Full API access",
                "Dedicated support team",
                "Custom training programs",
                "Strategic consulting",
            ],
            qhc_consultation_hours=20,
            quantum_architect_support=True,
            custom_agent_build=True,
            nqba_integration_level="enterprise",
            roi_estimate={"time_to_value": "3-4 weeks", "expected_roi": "600-1200%"},
        )

        return tiers

    def create_client_subscription(
        self,
        client_id: str,
        company_name: str,
        tier: ServiceTier,
        complexity: UseCaseComplexity,
        setup_fee_paid: bool = False,
    ) -> ClientSubscription:
        """Create a new client subscription"""
        subscription = ClientSubscription(
            client_id=client_id,
            company_name=company_name,
            tier=tier,
            complexity=complexity,
            start_date=datetime.now(),
        )
        subscription.setup_fee_paid = setup_fee_paid

        self.demo_clients[client_id] = subscription
        print(
            f"✅ Created subscription for {company_name}: {tier.value} {complexity.value}"
        )

        return subscription

    def get_pricing_quote(
        self,
        tier: ServiceTier,
        complexity: UseCaseComplexity,
        estimated_calls_per_month: int = None,
    ) -> Dict[str, Any]:
        """Get pricing quote for specific tier and complexity"""
        tier_key = f"{tier.value}_{complexity.value}"
        if tier_key not in self.pricing_tiers:
            raise ValueError(
                f"Invalid tier combination: {tier.value}_{complexity.value}"
            )

        pricing = self.pricing_tiers[tier_key]

        quote = {
            "tier": tier.value,
            "complexity": complexity.value,
            "monthly_price": pricing.monthly_price,
            "setup_fee": pricing.setup_fee,
            "included_calls": pricing.included_calls_per_month,
            "additional_call_cost": pricing.additional_call_cost,
            "features": pricing.features,
            "qhc_consultation_hours": pricing.qhc_consultation_hours,
            "quantum_architect_support": pricing.quantum_architect_support,
            "custom_agent_build": pricing.custom_agent_build,
            "nqba_integration_level": pricing.nqba_integration_level,
            "roi_estimate": pricing.roi_estimate,
        }

        if estimated_calls_per_month:
            if estimated_calls_per_month > pricing.included_calls_per_month:
                additional_calls = (
                    estimated_calls_per_month - pricing.included_calls_per_month
                )
                additional_cost = additional_calls * pricing.additional_call_cost
                quote["estimated_monthly_cost"] = (
                    pricing.monthly_price + additional_cost
                )
                quote["additional_calls_cost"] = additional_cost
            else:
                quote["estimated_monthly_cost"] = pricing.monthly_price
                quote["additional_calls_cost"] = 0

        return quote

    def get_all_pricing_tiers(self) -> Dict[str, Any]:
        """Get all available DIY and DFY pricing tiers"""
        return {
            "diy_tiers": {
                "basic": self.pricing_tiers["diy_basic"],
                "standard": self.pricing_tiers["diy_standard"],
                "enterprise": self.pricing_tiers["diy_enterprise"],
            },
            "dfy_tiers": {
                "basic": self.pricing_tiers["dfy_basic"],
                "standard": self.pricing_tiers["dfy_standard"],
                "enterprise": self.pricing_tiers["dfy_enterprise"],
            },
            "summary": {
                "diy_description": "Build your own solution with QHC guidance and NQBA integration",
                "dfy_description": "Have agents build your solution with QHC oversight and quality control",
                "common_features": [
                    "Same monthly price ($2,500) across all tiers",
                    "Setup fees vary by complexity ($20K-$50K)",
                    "QHC consultation included",
                    "Quantum Architect support",
                    "NQBA integration",
                    "Custom agent development",
                ],
            },
        }

    def run_comprehensive_demo(self):
        """Run the complete pricing demo"""
        print("🚀 COMPREHENSIVE DIY/DFY PRICING DEMO")
        print("=" * 60)
        print("Showcasing the complete pricing ecosystem for all agents")
        print("in the Neuromorphic Quantum Business Architecture (NQBA)")
        print()

        # Demo 1: Show all pricing tiers
        self.demo_pricing_tiers()

        # Demo 2: Create client subscriptions
        self.demo_client_subscriptions()

        # Demo 3: Show pricing quotes
        self.demo_pricing_quotes()

        # Demo 4: Demonstrate subscription management
        self.demo_subscription_management()

        # Demo 5: Demonstrate QHC consultation system
        self.demo_qhc_consultation()

        # Demo 6: Show Quantum Architect support
        self.demo_quantum_architect_support()

        # Demo 7: Demonstrate NQBA integration levels
        self.demo_nqba_integration()

        # Demo 8: Show ROI estimates and business value
        self.demo_roi_and_business_value()

        print("🎉 COMPREHENSIVE PRICING DEMO COMPLETE!")
        print("=" * 60)
        print("The system now supports:")
        print("✅ DIY: Build with QHC guidance and NQBA integration")
        print("✅ DFY: Have agents build with QHC oversight")
        print("✅ QHC consultation included in all tiers")
        print("✅ Quantum Architect technical support")
        print("✅ Consistent monthly pricing ($2,500)")
        print("✅ Setup fees based on complexity ($20K-$50K)")
        print("✅ All agent types supported")
        print("✅ Comprehensive subscription management")
        print()
        print("Next steps:")
        print("1. Deploy the updated system")
        print("2. Onboard clients with the new pricing model")
        print("3. Begin QHC consultation services")
        print("4. Scale Quantum Architect support")
        print("5. Monitor ROI and business impact")

    def demo_pricing_tiers(self):
        """Demo 1: Show all available pricing tiers"""
        print("📊 DEMO 1: COMPREHENSIVE PRICING TIERS")
        print("-" * 40)

        print("DIY TIERS (Do It Yourself with QHC guidance):")
        print("  Basic: $20K setup + $2.5K/month")
        print("    - QHC consultation: 10 hours/month")
        print("    - Quantum Architect guidance")
        print("    - Basic NQBA integration")
        print("    - Self-service dashboard")
        print()

        print("  Standard: $35K setup + $2.5K/month")
        print("    - QHC consultation: 20 hours/month")
        print("    - Quantum Architect dedicated support")
        print("    - Advanced NQBA integration")
        print("    - Custom agent development")
        print()

        print("  Enterprise: $50K setup + $2.5K/month")
        print("    - QHC consultation: 40 hours/month")
        print("    - Quantum Architect dedicated team")
        print("    - Full NQBA integration")
        print("    - White-label solutions")
        print()

        print("DFY TIERS (Done For You by agents with oversight):")
        print("  Basic: $20K setup + $2.5K/month")
        print("    - Full solution built by agents")
        print("    - QHC oversight and quality control")
        print("    - NQBA integration completed")
        print("    - Ready-to-use agents")
        print()

        print("  Standard: $35K setup + $2.5K/month")
        print("    - Advanced solution built by agents")
        print("    - QHC strategic oversight")
        print("    - Advanced NQBA integration")
        print("    - Custom enterprise agents")
        print()

        print("  Enterprise: $50K setup + $2.5K/month")
        print("    - Enterprise solution built by agents")
        print("    - QHC executive oversight")
        print("    - Full NQBA integration")
        print("    - White-label platform")
        print()

        print("Key Benefits:")
        print("✅ Same monthly price across all tiers")
        print("✅ Setup fees reflect complexity, not features")
        print("✅ QHC consultation included in all tiers")
        print("✅ Quantum Architect support available")
        print("✅ NQBA integration at all levels")
        print()

    def demo_client_subscriptions(self):
        """Demo 2: Create client subscriptions"""
        print("👥 DEMO 2: CLIENT SUBSCRIPTION CREATION")
        print("-" * 40)

        # Create demo clients
        clients = [
            {
                "client_id": "demo_tech_startup",
                "company_name": "TechStartup Inc.",
                "tier": ServiceTier.DIY,
                "complexity": UseCaseComplexity.BASIC,
                "description": "Small tech startup wanting to build their own solution",
            },
            {
                "client_id": "demo_enterprise_corp",
                "company_name": "Enterprise Corp",
                "tier": ServiceTier.DFY,
                "complexity": UseCaseComplexity.ENTERPRISE,
                "description": "Large enterprise wanting full-service solution",
            },
            {
                "client_id": "demo_mid_market",
                "company_name": "MidMarket Solutions",
                "tier": ServiceTier.DIY,
                "complexity": UseCaseComplexity.STANDARD,
                "description": "Mid-market company with moderate complexity needs",
            },
        ]

        for client in clients:
            print(f"Creating subscription for {client['company_name']}:")
            print(f"  Tier: {client['tier'].value.upper()}")
            print(f"  Complexity: {client['complexity'].value.title()}")
            print(f"  Description: {client['description']}")

            subscription = self.create_client_subscription(
                client_id=client["client_id"],
                company_name=client["company_name"],
                tier=client["tier"],
                complexity=client["complexity"],
                setup_fee_paid=True,  # Demo: assume setup fee paid
            )

            print(f"  Status: {subscription.status}")
            print(f"  Start Date: {subscription.start_date.strftime('%Y-%m-%d')}")
            print()

    def demo_pricing_quotes(self):
        """Demo 3: Show pricing quotes for different scenarios"""
        print("💰 DEMO 3: PRICING QUOTES")
        print("-" * 40)

        # Get quotes for different scenarios
        scenarios = [
            {
                "tier": ServiceTier.DIY,
                "complexity": UseCaseComplexity.BASIC,
                "calls": 1500,
                "description": "Small business DIY with moderate call volume",
            },
            {
                "tier": ServiceTier.DFY,
                "complexity": UseCaseComplexity.STANDARD,
                "calls": 3000,
                "description": "Mid-market DFY with high call volume",
            },
            {
                "tier": ServiceTier.DIY,
                "complexity": UseCaseComplexity.ENTERPRISE,
                "calls": 8000,
                "description": "Enterprise DIY with very high call volume",
            },
        ]

        for scenario in scenarios:
            print(f"Quote for: {scenario['description']}")
            print(f"  Tier: {scenario['tier'].value.upper()}")
            print(f"  Complexity: {scenario['complexity'].value.title()}")
            print(f"  Estimated calls/month: {scenario['calls']}")

            quote = self.get_pricing_quote(
                tier=scenario["tier"],
                complexity=scenario["complexity"],
                estimated_calls_per_month=scenario["calls"],
            )

            print(f"  Monthly price: ${quote['monthly_price']:,.2f}")
            print(f"  Setup fee: ${quote['setup_fee']:,.2f}")
            print(f"  Included calls: {quote['included_calls']:,}")
            print(f"  Additional call cost: ${quote['additional_call_cost']:.2f}")

            if "estimated_monthly_cost" in quote:
                print(
                    f"  Estimated monthly cost: ${quote['estimated_monthly_cost']:,.2f}"
                )
                if quote["additional_calls_cost"] > 0:
                    print(
                        f"  Additional calls cost: ${quote['additional_calls_cost']:,.2f}"
                    )

            print(f"  ROI estimate: {quote['roi_estimate']['expected_roi']}")
            print(f"  Time to value: {quote['roi_estimate']['time_to_value']}")
            print()

    def demo_subscription_management(self):
        """Demo 4: Demonstrate subscription management"""
        print("🔧 DEMO 4: SUBSCRIPTION MANAGEMENT")
        print("-" * 40)

        for client_id, subscription in self.demo_clients.items():
            print(f"Subscription Status for {subscription.company_name}:")
            print(f"  Client ID: {subscription.client_id}")
            print(f"  Company: {subscription.company_name}")
            print(f"  Tier: {subscription.tier.value.title()}")
            print(f"  Complexity: {subscription.complexity.value.title()}")
            print(f"  Status: {subscription.status}")
            print(f"  Setup fee paid: {'Yes' if subscription.setup_fee_paid else 'No'}")
            print(
                f"  Monthly fee paid: {'Yes' if subscription.monthly_fee_paid else 'No'}"
            )
            print(f"  Calls used this month: {subscription.calls_used_this_month}")
            print(f"  QHC hours used: {subscription.qhc_consultation_hours_used}")
            print(
                f"  Quantum Architect sessions: {subscription.quantum_architect_sessions}"
            )
            print(f"  Custom agents built: {subscription.custom_agents_built}")
            print(f"  NQBA integration status: {subscription.nqba_integration_status}")
            print()

    def demo_qhc_consultation(self):
        """Demo 5: Demonstrate QHC consultation system"""
        print("👑 DEMO 5: QUANTUM HIGH COUNCIL (QHC) CONSULTATION")
        print("-" * 40)

        print("QHC Consultation Services:")
        print("  🎯 Strategic Guidance")
        print("    - Business process optimization")
        print("    - Quantum strategy development")
        print("    - Technology roadmap planning")
        print()

        print("  🏗️ Architecture Design")
        print("    - NQBA integration planning")
        print("    - System architecture design")
        print("    - Scalability planning")
        print()

        print("  📊 Performance Optimization")
        print("    - Call script optimization")
        print("    - Agent performance tuning")
        print("    - ROI maximization strategies")
        print()

        print("  🚀 Innovation Advisory")
        print("    - Emerging technology assessment")
        print("    - Competitive advantage development")
        print("    - Future-proofing strategies")
        print()

        print("Consultation Hours by Tier:")
        for tier_key, tier_info in self.pricing_tiers.items():
            print(
                f"  {tier_key.replace('_', ' ').title()}: {tier_info.qhc_consultation_hours} hours/month"
            )
        print()

    def demo_quantum_architect_support(self):
        """Demo 6: Show Quantum Architect support"""
        print("🏗️ DEMO 6: QUANTUM ARCHITECT SUPPORT")
        print("-" * 40)

        print("Quantum Architect Services:")
        print("  🔧 Technical Implementation")
        print("    - NQBA integration setup")
        print("    - Custom agent development")
        print("    - API integration and customization")
        print()

        print("  ⚡ Performance Optimization")
        print("    - GPU acceleration setup")
        print("    - Quantum algorithm optimization")
        print("    - System performance tuning")
        print()

        print("  🛡️ Security & Compliance")
        print("    - Security architecture design")
        print("    - Compliance framework implementation")
        print("    - Data protection strategies")
        print()

        print("  📚 Training & Knowledge Transfer")
        print("    - Technical team training")
        print("    - Best practices documentation")
        print("    - Ongoing technical support")
        print()

        print("Support Levels by Tier:")
        for tier_key, tier_info in self.pricing_tiers.items():
            support_level = (
                "Dedicated Team"
                if tier_info.complexity == UseCaseComplexity.ENTERPRISE
                else (
                    "Dedicated Support"
                    if tier_info.complexity == UseCaseComplexity.STANDARD
                    else "Guidance"
                )
            )
            print(f"  {tier_key.replace('_', ' ').title()}: {support_level}")
        print()

    def demo_nqba_integration(self):
        """Demo 7: Demonstrate NQBA integration levels"""
        print("🔗 DEMO 7: NQBA INTEGRATION LEVELS")
        print("-" * 40)

        print("NQBA Integration Framework:")
        print("  🚀 Basic Integration")
        print("    - Core NQBA services access")
        print("    - Standard templates and workflows")
        print("    - Basic quantum enhancement")
        print("    - Standard analytics dashboard")
        print()

        print("  ⚡ Standard Integration")
        print("    - Advanced NQBA services")
        print("    - Custom workflows and templates")
        print("    - Advanced quantum algorithms")
        print("    - Custom analytics and reporting")
        print("    - API access for custom integrations")
        print()

        print("  🏢 Enterprise Integration")
        print("    - Full NQBA platform access")
        print("    - White-label solutions")
        print("    - Custom quantum algorithms")
        print("    - Enterprise analytics and BI")
        print("    - Full API ecosystem access")
        print("    - Multi-tenant architecture")
        print()

        print("Integration by Tier:")
        for tier_key, tier_info in self.pricing_tiers.items():
            print(
                f"  {tier_key.replace('_', ' ').title()}: {tier_info.nqba_integration_level.title()}"
            )
        print()

    def demo_roi_and_business_value(self):
        """Demo 8: Show ROI estimates and business value"""
        print("📊 DEMO 8: ROI ESTIMATES & BUSINESS VALUE")
        print("-" * 40)

        print("Expected ROI by Tier:")
        for tier_key, tier_info in self.pricing_tiers.items():
            print(f"  {tier_key.replace('_', ' ').title()}:")
            print(f"    ROI: {tier_info.roi_estimate['expected_roi']}")
            print(f"    Time to Value: {tier_info.roi_estimate['time_to_value']}")
            print()

        print("Business Value Drivers:")
        print("  💰 Cost Reduction")
        print("    - Automated call handling")
        print("    - Reduced manual labor costs")
        print("    - Optimized resource allocation")
        print()

        print("  📈 Revenue Growth")
        print("    - Improved conversion rates")
        print("    - Better lead qualification")
        print("    - Enhanced customer experience")
        print()

        print("  🚀 Operational Efficiency")
        print("    - Streamlined workflows")
        print("    - Faster response times")
        print("    - Better resource utilization")
        print()

        print("  🎯 Competitive Advantage")
        print("    - Quantum-enhanced intelligence")
        print("    - Advanced AI capabilities")
        print("    - Cutting-edge technology")
        print()


def main():
    """Main demo function"""
    demo = SimplePricingDemo()
    demo.run_comprehensive_demo()


if __name__ == "__main__":
    main()
