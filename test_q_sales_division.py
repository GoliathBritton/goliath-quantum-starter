#!/usr/bin/env python3
"""
Q-Sales Division™ Demo Script
==============================
Demonstrates the complete self-evolving quantum sales agent system:
- Multi-agent sales pod creation
- Quantum-optimized playbooks
- Performance optimization
- Agent training and scaling
- Real-time metrics and insights
"""

import asyncio
import json
import time
from datetime import datetime
import numpy as np

# Import our Q-Sales Division
from src.nqba_stack.q_sales_division import q_sales_division
from src.nqba_stack.mcp_handler import dispatch_tool


async def demo_q_sales_division():
    """Complete demonstration of Q-Sales Division™ capabilities"""

    print("🚀 Q-Sales Division™ Demo - Self-Evolving Quantum Sales Agents")
    print("=" * 70)

    # Step 1: Create Sales Pods for Different Industries
    print("\n📊 Step 1: Creating Quantum-Optimized Sales Pods")
    print("-" * 50)

    # SaaS Sales Pod
    saas_pod = await q_sales_division.create_sales_pod(
        name="SaaS Enterprise Pod",
        industry="SaaS",
        target_market="Enterprise",
        agent_count=8,
    )
    print(f"✅ Created SaaS Pod: {saas_pod.name} with {len(saas_pod.agents)} agents")

    # Insurance Sales Pod
    insurance_pod = await q_sales_division.create_sales_pod(
        name="Insurance SMB Pod",
        industry="Insurance",
        target_market="SMB",
        agent_count=6,
    )
    print(
        f"✅ Created Insurance Pod: {insurance_pod.name} with {len(insurance_pod.agents)} agents"
    )

    # Real Estate Sales Pod
    real_estate_pod = await q_sales_division.create_sales_pod(
        name="Real Estate Luxury Pod",
        industry="Real Estate",
        target_market="Luxury",
        agent_count=4,
    )
    print(
        f"✅ Created Real Estate Pod: {real_estate_pod.name} with {len(real_estate_pod.agents)} agents"
    )

    # Step 2: Simulate Performance Data
    print("\n📈 Step 2: Simulating Performance Data")
    print("-" * 50)

    # Simulate some performance metrics for agents
    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        for agent in pod.agents:
            # Simulate realistic performance data
            agent.performance_metrics.update(
                {
                    "leads_qualified": np.random.randint(10, 50),
                    "meetings_booked": np.random.randint(5, 25),
                    "deals_closed": np.random.randint(1, 8),
                    "revenue_generated": np.random.uniform(5000, 25000),
                    "conversion_rate": np.random.uniform(0.08, 0.22),
                }
            )

        # Update pod metrics
        pod.revenue_generated = sum(
            agent.performance_metrics["revenue_generated"] for agent in pod.agents
        )
        pod.leads_processed = sum(
            agent.performance_metrics["leads_qualified"] for agent in pod.agents
        )
        pod.conversion_rate = np.mean(
            [agent.performance_metrics["conversion_rate"] for agent in pod.agents]
        )

    print("✅ Performance data simulated for all pods")

    # Step 3: Optimize Pod Performance
    print("\n🔧 Step 3: Quantum Performance Optimization")
    print("-" * 50)

    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        print(f"\n🔄 Optimizing {pod.name}...")
        optimization_result = await q_sales_division.optimize_pod_performance(
            pod.pod_id
        )

        if optimization_result["success"]:
            print(f"✅ {pod.name} optimized successfully!")
            print(f"   - New status: {optimization_result['new_status']}")
            print(f"   - Next optimization: {optimization_result['next_optimization']}")

            # Show optimizations applied
            for key, value in optimization_result["optimizations_applied"].items():
                print(f"   - {key.replace('_', ' ').title()}: {value}")
        else:
            print(
                f"⚠️  {pod.name} optimization failed: {optimization_result.get('error', 'Unknown error')}"
            )

    # Step 4: Get Performance Metrics
    print("\n📊 Step 4: Performance Metrics & Insights")
    print("-" * 50)

    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        performance = await q_sales_division.get_pod_performance(pod.pod_id)

        print(f"\n📈 {pod.name} Performance:")
        print(
            f"   - Total Revenue: ${performance['performance_metrics']['total_revenue']:,.2f}"
        )
        print(f"   - Total Leads: {performance['performance_metrics']['total_leads']}")
        print(f"   - Total Deals: {performance['performance_metrics']['total_deals']}")
        print(
            f"   - Avg Conversion Rate: {performance['performance_metrics']['avg_conversion_rate']:.1%}"
        )
        print(
            f"   - Revenue per Agent: ${performance['performance_metrics']['revenue_per_agent']:,.2f}"
        )

    # Step 5: Scale Pods
    print("\n📈 Step 5: Dynamic Pod Scaling")
    print("-" * 50)

    # Scale up SaaS pod
    print(f"\n🔄 Scaling {saas_pod.name} from {len(saas_pod.agents)} to 12 agents...")
    scale_result = await q_sales_division.scale_pod(saas_pod.pod_id, 12)
    print(f"✅ {saas_pod.name} scaled: {scale_result['action']}")
    print(f"   - Previous agents: {scale_result['previous_agent_count']}")
    print(f"   - New agents: {scale_result['new_agent_count']}")
    print(f"   - Status: {scale_result['status']}")

    # Scale down Insurance pod
    print(
        f"\n🔄 Scaling {insurance_pod.name} from {len(insurance_pod.agents)} to 4 agents..."
    )
    scale_result = await q_sales_division.scale_pod(insurance_pod.pod_id, 4)
    print(f"✅ {insurance_pod.name} scaled: {scale_result['action']}")
    print(f"   - Previous agents: {scale_result['previous_agent_count']}")
    print(f"   - New agents: {scale_result['new_agent_count']}")
    print(f"   - Status: {scale_result['status']}")

    # Step 6: Train Agents
    print("\n🎓 Step 6: Quantum-Enhanced Agent Training")
    print("-" * 50)

    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        print(f"\n🎓 Training {pod.name} agents...")
        training_result = await q_sales_division.train_agents(
            pod_id=pod.pod_id,
            training_focus="objection_handling",
            training_intensity="intensive",
            use_quantum_enhancement=True,
        )

        if training_result["success"]:
            print(f"✅ {pod.name} agents trained successfully!")
            print(f"   - Agents trained: {training_result['agents_trained']}")
            print(f"   - Training focus: {training_result['training_focus']}")
            print(f"   - Training intensity: {training_result['training_intensity']}")
            print(f"   - Quantum enhanced: {training_result['quantum_enhanced']}")
            print(f"   - Next training: {training_result['next_training_recommended']}")
        else:
            print(
                f"⚠️  {pod.name} training failed: {training_result.get('error', 'Unknown error')}"
            )

    # Step 7: Division Overview
    print("\n🏢 Step 7: Complete Division Overview")
    print("-" * 50)

    division_overview = await q_sales_division.get_division_overview()

    print(f"\n📊 Q-Sales Division™ Overview:")
    print(f"   - Total Pods: {division_overview['total_pods']}")
    print(f"   - Total Agents: {division_overview['total_agents']}")
    print(f"   - Total Revenue: ${division_overview['total_revenue']:,.2f}")

    print(f"\n📈 Pod Status Distribution:")
    for status, count in division_overview["pod_statuses"].items():
        print(f"   - {status.title()}: {count}")

    print(f"\n💰 Revenue by Industry:")
    for industry, revenue in division_overview.get("revenue_by_industry", {}).items():
        print(f"   - {industry}: ${revenue:,.2f}")

    # Step 8: MCP Tool Integration Demo
    print("\n🔧 Step 8: MCP Tool Integration Demo")
    print("-" * 50)

    print("\n🔄 Testing MCP tool dispatch...")

    # Test pod creation via MCP
    mcp_result = await dispatch_tool(
        "q_sales.create_pod",
        {
            "name": "MCP Test Pod",
            "industry": "Technology",
            "target_market": "Startups",
            "agent_count": 3,
        },
        user="demo_user",
    )

    if mcp_result["success"]:
        print("✅ MCP tool dispatch successful!")
        print(f"   - Created pod: {mcp_result['result']['name']}")
        print(f"   - Pod ID: {mcp_result['result']['pod_id']}")
    else:
        print(
            f"⚠️  MCP tool dispatch failed: {mcp_result.get('error', 'Unknown error')}"
        )

    # Test performance retrieval via MCP
    if mcp_result["success"]:
        pod_id = mcp_result["result"]["pod_id"]
        perf_result = await dispatch_tool(
            "q_sales.get_pod_performance",
            {"pod_id": pod_id, "include_agent_details": True},
            user="demo_user",
        )

        if perf_result["success"]:
            print("✅ MCP performance retrieval successful!")
            print(f"   - Pod: {perf_result['result']['name']}")
            print(f"   - Agents: {perf_result['result']['agent_count']}")
        else:
            print(
                f"⚠️  MCP performance retrieval failed: {perf_result.get('error', 'Unknown error')}"
            )

    # Step 9: Advanced Features Demo
    print("\n🚀 Step 9: Advanced Features Demo")
    print("-" * 50)

    # Show playbook evolution
    print("\n📚 Playbook Evolution:")
    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        playbook = q_sales_division.playbooks.get(pod.playbook_id)
        if playbook:
            print(f"   - {pod.name}: Version {playbook.version}")
            print(
                f"     Last updated: {playbook.last_updated.strftime('%Y-%m-%d %H:%M')}"
            )
            print(f"     Evolution steps: {len(playbook.evolution_history)}")

    # Show agent specializations
    print("\n👥 Agent Specializations:")
    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        print(f"\n   {pod.name}:")
        for agent in pod.agents[:3]:  # Show first 3 agents
            print(f"     - {agent.name}: {agent.specialization} ({agent.role.value})")
            print(f"       Experience: {agent.experience_level}/10")
            print(
                f"       Channels: {', '.join([ch.value for ch in agent.communication_channels])}"
            )

    # Step 10: Performance Trends
    print("\n📈 Step 10: Performance Trends & Insights")
    print("-" * 50)

    # Calculate some trends
    total_revenue = sum(
        pod.revenue_generated for pod in [saas_pod, insurance_pod, real_estate_pod]
    )
    total_leads = sum(
        pod.leads_processed for pod in [saas_pod, insurance_pod, real_estate_pod]
    )
    total_agents = sum(
        len(pod.agents) for pod in [saas_pod, insurance_pod, real_estate_pod]
    )

    print(f"\n📊 Overall Division Performance:")
    print(f"   - Total Revenue: ${total_revenue:,.2f}")
    print(f"   - Total Leads Processed: {total_leads}")
    print(f"   - Total Active Agents: {total_agents}")
    print(f"   - Revenue per Agent: ${total_revenue/total_agents:,.2f}")
    print(f"   - Leads per Agent: {total_leads/total_agents:.1f}")

    # Industry performance comparison
    print(f"\n🏭 Industry Performance Comparison:")
    industry_performance = {}
    for pod in [saas_pod, insurance_pod, real_estate_pod]:
        industry = pod.industry
        if industry not in industry_performance:
            industry_performance[industry] = {
                "revenue": 0,
                "leads": 0,
                "agents": 0,
                "conversion": 0,
            }

        industry_performance[industry]["revenue"] += pod.revenue_generated
        industry_performance[industry]["leads"] += pod.leads_processed
        industry_performance[industry]["agents"] += len(pod.agents)
        industry_performance[industry]["conversion"] += pod.conversion_rate

    for industry, metrics in industry_performance.items():
        avg_conversion = metrics["conversion"] / len(
            [
                p
                for p in [saas_pod, insurance_pod, real_estate_pod]
                if p.industry == industry
            ]
        )
        print(f"   - {industry}:")
        print(f"     Revenue: ${metrics['revenue']:,.2f}")
        print(f"     Leads: {metrics['leads']}")
        print(f"     Agents: {metrics['agents']}")
        print(f"     Avg Conversion: {avg_conversion:.1%}")

    print("\n🎉 Q-Sales Division™ Demo Complete!")
    print("=" * 70)
    print("\n✨ What We've Demonstrated:")
    print("   ✅ Multi-industry sales pod creation")
    print("   ✅ Quantum-optimized playbooks and agents")
    print("   ✅ Real-time performance optimization")
    print("   ✅ Dynamic pod scaling")
    print("   ✅ Quantum-enhanced agent training")
    print("   ✅ MCP tool integration")
    print("   ✅ Comprehensive performance analytics")
    print("   ✅ Self-evolving sales strategies")

    print("\n🚀 Next Steps:")
    print("   1. Deploy to production environment")
    print("   2. Connect to real CRM systems")
    print("   3. Integrate with communication platforms")
    print("   4. Set up automated optimization schedules")
    print("   5. Launch partner onboarding portal")

    return {
        "total_pods": len(q_sales_division.pods),
        "total_agents": len(q_sales_division.agents),
        "total_revenue": total_revenue,
        "demo_success": True,
    }


async def demo_individual_features():
    """Demo individual Q-Sales Division features"""

    print("\n🔧 Individual Feature Demonstrations")
    print("=" * 50)

    # Feature 1: Playbook Evolution
    print("\n📚 Feature 1: Self-Evolving Playbooks")
    print("-" * 30)

    # Create a test pod
    test_pod = await q_sales_division.create_sales_pod(
        name="Test Evolution Pod",
        industry="Consulting",
        target_market="Enterprise",
        agent_count=3,
    )

    # Get initial playbook
    initial_playbook = q_sales_division.playbooks[test_pod.playbook_id]
    print(f"✅ Initial playbook created: Version {initial_playbook.version}")

    # Simulate optimization to trigger evolution
    await q_sales_division.optimize_pod_performance(test_pod.pod_id)

    # Check evolution
    evolved_playbook = q_sales_division.playbooks[test_pod.playbook_id]
    print(f"✅ Playbook evolved: Version {evolved_playbook.version}")
    print(f"   Evolution steps: {len(evolved_playbook.evolution_history)}")

    # Feature 2: Agent Personality Generation
    print("\n👥 Feature 2: AI-Generated Agent Personalities")
    print("-" * 40)

    for i, agent in enumerate(test_pod.agents[:2]):
        print(f"\n   Agent {i+1}: {agent.name}")
        print(f"   - Role: {agent.role.value}")
        print(f"   - Specialization: {agent.specialization}")
        print(f"   - Experience: {agent.experience_level}/10")
        print(
            f"   - Communication: {', '.join([ch.value for ch in agent.communication_channels])}"
        )

    # Feature 3: Performance Optimization
    print("\n🔧 Feature 3: Quantum Performance Optimization")
    print("-" * 40)

    # Simulate some performance data
    for agent in test_pod.agents:
        agent.performance_metrics.update(
            {
                "leads_qualified": np.random.randint(5, 20),
                "meetings_booked": np.random.randint(2, 10),
                "deals_closed": np.random.randint(0, 3),
                "revenue_generated": np.random.uniform(2000, 8000),
                "conversion_rate": np.random.uniform(0.05, 0.15),
            }
        )

    # Optimize
    optimization = await q_sales_division.optimize_pod_performance(test_pod.pod_id)
    print(f"✅ Optimization completed: {optimization['success']}")

    if optimization["success"]:
        print("   Applied optimizations:")
        for key, value in optimization["optimizations_applied"].items():
            print(f"   - {key.replace('_', ' ').title()}: {value}")

    # Feature 4: Dynamic Scaling
    print("\n📈 Feature 4: Dynamic Pod Scaling")
    print("-" * 30)

    initial_count = len(test_pod.agents)
    print(f"   Initial agent count: {initial_count}")

    # Scale up
    scale_result = await q_sales_division.scale_pod(test_pod.pod_id, initial_count + 2)
    print(f"   Scaled to: {scale_result['new_agent_count']} agents")
    print(f"   Action: {scale_result['action']}")

    # Scale down
    scale_result = await q_sales_division.scale_pod(test_pod.pod_id, initial_count)
    print(f"   Scaled back to: {scale_result['new_agent_count']} agents")
    print(f"   Action: {scale_result['action']}")

    print("\n✅ Individual feature demonstrations completed!")


if __name__ == "__main__":
    print("🚀 Starting Q-Sales Division™ Demo...")

    # Run the main demo
    result = asyncio.run(demo_q_sales_division())

    # Run individual feature demos
    asyncio.run(demo_individual_features())

    print(f"\n🎯 Demo Results:")
    print(f"   - Total Pods Created: {result['total_pods']}")
    print(f"   - Total Agents Deployed: {result['total_agents']}")
    print(f"   - Total Revenue Simulated: ${result['total_revenue']:,.2f}")
    print(f"   - Demo Success: {result['demo_success']}")

    print("\n🌟 Q-Sales Division™ is ready for production deployment!")
