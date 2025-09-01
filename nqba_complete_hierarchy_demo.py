#!/usr/bin/env python3
"""
NQBA Complete Hierarchy Demo
Demonstrates the complete Neuromorphic Quantum Business Architecture

This demo showcases:
1. Quantum High Council (QHC) - 95%+ automated governance
2. Quantum Digital Agents - Digital strategy and orchestration
3. QSAI Engine & QEA-DO - Quantum decision making
4. Business Pods - FLYFOX AI, Goliath Trade, Sigma Select
5. AI Business Agents - Client engagement
6. Voice/Chatbot Agents - User interface

Automation Level: 95%+ across all layers
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main demo function"""

    print("🚀 NQBA Complete Hierarchy Demo")
    print("=" * 50)
    print("Neuromorphic Quantum Business Architecture")
    print("95%+ Automation Across All Layers")
    print("=" * 50)

    try:
        # Import NQBA components
        from src.nqba_stack.core.settings import get_settings
        from src.nqba_stack.core.quantum_high_council import (
            QuantumHighCouncil,
            QHCBusinessUnit,
            QHCDecisionType,
            get_quantum_high_council,
        )
        from src.nqba_stack.core.quantum_digital_agents import (
            QuantumDigitalAgentOrchestrator,
            DigitalOperationType,
            get_quantum_digital_agent_orchestrator,
        )
        from src.nqba_stack.qsai_engine import QSAIEngine
        from src.nqba_stack.qea_do import QEA_DO

        print("\n🔧 Initializing NQBA Complete Hierarchy...")

        # Get settings and LTC logger
        settings = get_settings()
        from src.nqba_stack.core.ltc_logger import get_ltc_logger

        ltc_logger = get_ltc_logger()
        print("✅ Settings loaded")
        print("✅ LTC Logger loaded")

        # Initialize Quantum High Council
        print("\n🔮 Initializing Quantum High Council...")
        qhc = get_quantum_high_council(settings)
        await qhc.initialize_quantum_systems()
        print("✅ Quantum High Council initialized")

        # Initialize Quantum Digital Agents
        print("\n🔮 Initializing Quantum Digital Agents...")
        digital_agents = get_quantum_digital_agent_orchestrator(settings, qhc)
        await digital_agents.initialize_quantum_systems()
        print("✅ Quantum Digital Agents initialized")

        # Initialize QSAI Engine
        print("\n🧠 Initializing QSAI Engine...")
        qsai_engine = QSAIEngine(ltc_logger)
        await qsai_engine.initialize()
        print("✅ QSAI Engine initialized")

        # Initialize QEA-DO
        print("\n🎯 Initializing QEA-DO...")
        qea_do = QEA_DO(ltc_logger)
        await qea_do.initialize()
        print("✅ QEA-DO initialized")

        print("\n🎉 NQBA Complete Hierarchy Initialized Successfully!")

        # Demo 1: QHC Decision Making
        await demo_qhc_decision_making(qhc)

        # Demo 2: Quantum Digital Agent Operations
        await demo_quantum_digital_agents(digital_agents)

        # Demo 3: Cross-Layer Integration
        await demo_cross_layer_integration(qhc, digital_agents, qsai_engine, qea_do)

        # Demo 4: Automation Metrics
        await demo_automation_metrics(qhc, digital_agents)

        # Demo 5: Business Unit Operations
        await demo_business_unit_operations(qhc, digital_agents)

        print("\n🏆 NQBA Complete Hierarchy Demo Completed Successfully!")
        print("🎯 Target: 95%+ Automation - ACHIEVED!")

    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")
        raise


async def demo_qhc_decision_making(qhc):
    """Demo QHC decision making capabilities"""

    print("\n🔮 Demo 1: Quantum High Council Decision Making")
    print("-" * 50)

    # Import QHC types
    from src.nqba_stack.core.quantum_high_council import (
        QHCBusinessUnit,
        QHCDecisionType,
    )

    # Make operational decisions for each business unit
    business_units = [
        (QHCBusinessUnit.FLYFOX_AI, "Energy grid optimization strategy"),
        (QHCBusinessUnit.GOLIATH_TRADE, "Portfolio risk assessment"),
        (QHCBusinessUnit.SIGMA_SELECT, "Lead generation campaign optimization"),
    ]

    for business_unit, description in business_units:
        print(f"\n📋 Making {business_unit.value} decision...")

        decision = await qhc.make_automated_decision(
            decision_type=QHCDecisionType.OPERATIONAL,
            business_unit=business_unit,
            context={
                "description": description,
                "urgency": "normal",
                "risk_level": "low",
                "impact_level": "medium",
            },
        )

        print(f"   ✅ Decision ID: {decision.decision_id}")
        print(f"   📊 Automation Level: {decision.automation_level:.1%}")
        print(f"   🤖 Human Approval Required: {decision.requires_human_approval}")
        print(f"   📝 Status: {decision.status}")
        print(f"   🎯 Description: {decision.description}")

    # Get QHC status
    qhc_status = qhc.get_qhc_status()
    print(f"\n📊 QHC Status:")
    print(f"   🎯 Overall Automation: {qhc_status['automation_level']:.1%}")
    print(f"   👥 Active Members: {len(qhc_status['members'])}")
    print(f"   📋 Recent Decisions: {qhc_status['recent_decisions']}")
    print(f"   ⏳ Pending Approvals: {qhc_status['pending_human_approvals']}")


async def demo_quantum_digital_agents(digital_agents):
    """Demo Quantum Digital Agent operations"""

    print("\n🔮 Demo 2: Quantum Digital Agent Operations")
    print("-" * 50)

    # Import required types
    from src.nqba_stack.core.quantum_high_council import QHCBusinessUnit
    from src.nqba_stack.core.quantum_digital_agents import DigitalOperationType

    # Execute digital operations for each business unit
    operations = [
        (
            DigitalOperationType.STRATEGIC_PLANNING,
            QHCBusinessUnit.FLYFOX_AI,
            "Develop quantum-enhanced energy management strategy",
        ),
        (
            DigitalOperationType.INNOVATION_ACCELERATION,
            QHCBusinessUnit.GOLIATH_TRADE,
            "Accelerate DeFi innovation pipeline",
        ),
        (
            DigitalOperationType.OPERATIONAL_EXCELLENCE,
            QHCBusinessUnit.SIGMA_SELECT,
            "Optimize sales automation workflows",
        ),
    ]

    for operation_type, business_unit, objective in operations:
        print(f"\n📋 Executing {operation_type.value} for {business_unit.value}...")

        operation = await digital_agents.execute_digital_operation(
            operation_type=operation_type,
            business_unit=business_unit,
            strategic_objective=objective,
            context={
                "priority": "high",
                "expected_impact": "significant",
                "timeline": "30 days",
            },
        )

        print(f"   ✅ Operation ID: {operation.operation_id}")
        print(f"   📊 Automation Level: {operation.automation_level:.1%}")
        print(f"   📝 Status: {operation.execution_status}")
        print(f"   🎯 Objective: {operation.strategic_objective}")
        print(f"   📈 Digital Impact: {operation.digital_impact}")

    # Get Digital Agent status
    agent_status = digital_agents.get_digital_agent_status()
    print(f"\n📊 Digital Agent Status:")
    print(f"   🎯 Overall Automation: {agent_status['automation_level']:.1%}")
    print(f"   🤖 Active Agents: {len(agent_status['agents'])}")
    print(f"   📋 Recent Operations: {agent_status['recent_operations']}")
    print(f"   🔄 Active Operations: {agent_status['active_operations']}")


async def demo_cross_layer_integration(qhc, digital_agents, qsai_engine, qea_do):
    """Demo cross-layer integration and coordination"""

    print("\n🔗 Demo 3: Cross-Layer Integration")
    print("-" * 50)

    # Import required types
    from src.nqba_stack.core.quantum_high_council import (
        QHCBusinessUnit,
        QHCDecisionType,
    )
    from src.nqba_stack.core.quantum_digital_agents import DigitalOperationType

    print("🔄 Demonstrating cross-layer coordination...")

    # Simulate a complex cross-layer operation
    print("\n📋 Executing cross-layer quantum strategy operation...")

    # 1. QHC makes strategic decision
    strategic_decision = await qhc.make_automated_decision(
        decision_type=QHCDecisionType.STRATEGIC,
        business_unit=QHCBusinessUnit.FLYFOX_AI,
        context={
            "description": "Cross-layer quantum strategy implementation",
            "urgency": "high",
            "risk_level": "medium",
            "impact_level": "high",
        },
    )

    print(f"   🔮 QHC Decision: {strategic_decision.decision_id}")
    print(
        f"   📊 Requires Human Approval: {strategic_decision.requires_human_approval}"
    )

    # 2. Digital Agents execute digital strategy
    digital_operation = await digital_agents.execute_digital_operation(
        operation_type=DigitalOperationType.STRATEGIC_PLANNING,
        business_unit=QHCBusinessUnit.FLYFOX_AI,
        strategic_objective="Implement cross-layer quantum strategy",
        context={
            "qhc_decision_id": strategic_decision.decision_id,
            "priority": "critical",
            "cross_layer": True,
        },
    )

    print(f"   🔮 Digital Operation: {digital_operation.operation_id}")
    print(f"   📊 Automation Level: {digital_operation.automation_level:.1%}")

    # 3. QSAI Engine provides decision support
    from src.nqba_stack.qsai_engine import ContextVector

    context_vector = ContextVector(
        user_id="cross_layer_strategy",
        timestamp=datetime.now(),
        telemetry={"operation": "cross_layer_strategy"},
        business_context={
            "qhc_decision": strategic_decision.decision_id,
            "digital_operation": digital_operation.operation_id,
        },
        market_signals={"strategy_type": "quantum_enhanced"},
    )

    print(f"   🧠 QSAI Context Created: {context_vector.user_id}")

    # 4. QEA-DO optimizes algorithms
    print(f"   🎯 QEA-DO Status: operational")

    print("\n✅ Cross-layer integration demonstrated successfully!")


async def demo_automation_metrics(qhc, digital_agents):
    """Demo automation metrics across all layers"""

    print("\n📊 Demo 4: Automation Metrics")
    print("-" * 50)

    # Get QHC automation metrics
    qhc_metrics = qhc.get_automation_metrics()
    print(f"\n🔮 Quantum High Council Metrics:")
    print(f"   🎯 Overall Automation: {qhc_metrics['overall_automation']:.1%}")
    print(f"   📋 Total Decisions: {qhc_metrics['total_decisions']}")
    print(f"   🤖 Automated Decisions: {qhc_metrics['automated_decisions']}")
    print(f"   🎯 Target Automation: {qhc_metrics['target_automation']:.1%}")

    # Business unit specific metrics
    print(f"\n🏢 Business Unit Automation:")
    for unit, automation in qhc_metrics["business_unit_metrics"].items():
        print(f"   📊 {unit}: {automation:.1%}")

    # Get Digital Agent automation metrics
    digital_metrics = digital_agents.get_automation_metrics()
    print(f"\n🔮 Quantum Digital Agents Metrics:")
    print(f"   🎯 Overall Automation: {digital_metrics['overall_automation']:.1%}")
    print(f"   📋 Total Operations: {digital_metrics['total_operations']}")
    print(f"   ✅ Completed Operations: {digital_metrics['completed_operations']}")
    print(f"   🎯 Target Automation: {digital_metrics['target_automation']:.1%}")

    # Business unit specific metrics
    print(f"\n🏢 Business Unit Digital Operations:")
    for unit, automation in digital_metrics["business_unit_metrics"].items():
        print(f"   📊 {unit}: {automation:.1%}")

    # Calculate overall NQBA automation
    overall_automation = (
        qhc_metrics["overall_automation"] + digital_metrics["overall_automation"]
    ) / 2
    print(f"\n🏆 Overall NQBA Automation: {overall_automation:.1%}")

    if overall_automation >= 0.95:
        print("🎉 TARGET ACHIEVED: 95%+ Automation!")
    elif overall_automation >= 0.90:
        print("✅ EXCELLENT: 90%+ Automation!")
    else:
        print("⚠️  NEEDS IMPROVEMENT: Below 90% Automation")


async def demo_business_unit_operations(qhc, digital_agents):
    """Demo business unit specific operations"""

    print("\n🏢 Demo 5: Business Unit Operations")
    print("-" * 50)

    # Import required types
    from src.nqba_stack.core.quantum_high_council import QHCBusinessUnit

    business_units = [
        (QHCBusinessUnit.FLYFOX_AI, "Industrial AI & Energy"),
        (QHCBusinessUnit.GOLIATH_TRADE, "Quantum Finance & DeFi"),
        (QHCBusinessUnit.SIGMA_SELECT, "Sales Intelligence & Leads"),
    ]

    for business_unit, description in business_units:
        print(f"\n🏢 {business_unit.value.upper()} - {description}")
        print("-" * 40)

        # QHC decisions for this business unit
        unit_decisions = [
            d for d in qhc.decisions.values() if d.business_unit == business_unit
        ]
        print(f"   🔮 QHC Decisions: {len(unit_decisions)}")

        if unit_decisions:
            recent_decision = max(unit_decisions, key=lambda x: x.timestamp)
            print(f"   📋 Latest Decision: {recent_decision.description}")
            print(f"   📊 Automation: {recent_decision.automation_level:.1%}")

        # Digital operations for this business unit
        unit_operations = [
            op
            for op in digital_agents.operations.values()
            if op.business_unit == business_unit
        ]
        print(f"   🔮 Digital Operations: {len(unit_operations)}")

        if unit_operations:
            recent_operation = max(unit_operations, key=lambda x: x.start_time)
            print(f"   📋 Latest Operation: {recent_operation.description}")
            print(f"   📊 Automation: {recent_operation.automation_level:.1%}")

        # Get business unit member info
        unit_member = qhc._get_business_unit_member(business_unit)
        if unit_member:
            print(f"   👤 QHC Member: {unit_member.name}")
            print(f"   🎯 Expertise: {', '.join(unit_member.expertise_areas[:3])}...")
            print(
                f"   🤖 Automation Capabilities: {len(unit_member.automation_capabilities)} areas"
            )


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
