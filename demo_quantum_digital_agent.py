#!/usr/bin/env python3
"""
Quantum Digital Agent Demo
==========================
Demonstrates the Quantum Digital Agent's ability to make calls with:
- Quantum-enhanced AI optimization
- NVIDIA GPU acceleration
- Intelligent call scripting
- Call analytics and insights

Run this script to see your Quantum Digital Agent in action!
"""

import asyncio
import json
import time
from datetime import datetime
from src.nqba_stack.quantum_digital_agent import QuantumDigitalAgent, CallRequest
from src.nqba_stack.settings import NQBASettings


async def demo_quantum_digital_agent():
    """Demo the Quantum Digital Agent capabilities"""

    print("🚀 QUANTUM DIGITAL AGENT DEMO")
    print("=" * 50)
    print("🤖 Initializing Quantum Digital Agent...")

    # Initialize the agent
    settings = NQBASettings()
    agent = QuantumDigitalAgent(settings)

    print("✅ Quantum Digital Agent initialized!")
    print(f"🔧 Quantum Enhancement: Enabled")
    print(
        f"🚀 NVIDIA GPU Acceleration: {'Available' if agent.nvidia.is_gpu_available() else 'Not Available'}"
    )
    print()

    # Demo 1: Make a sales call
    print("📞 DEMO 1: Making a Quantum-Enhanced Sales Call")
    print("-" * 40)

    sales_call = CallRequest(
        to_number="+1-555-0123",
        from_number="+1-555-9999",
        agent_id="quantum_sales_001",
        call_purpose="Sales outreach for FLYFOX AI quantum computing services",
        script_template="Professional introduction to quantum computing benefits",
        quantum_optimization=True,
        gpu_acceleration=True,
    )

    print(f"📱 Calling: {sales_call.to_number}")
    print(f"🎯 Purpose: {sales_call.call_purpose}")
    print(f"⚡ Quantum Optimization: {sales_call.quantum_optimization}")
    print(f"🚀 GPU Acceleration: {sales_call.gpu_acceleration}")
    print()

    print("🔄 Making call...")
    start_time = time.time()

    result = await agent.make_call(sales_call)

    call_duration = time.time() - start_time
    print(f"✅ Call completed in {call_duration:.2f} seconds!")

    if result.success:
        print(f"📞 Call ID: {result.call_id}")
        print(f"⏱️  Call Duration: {result.session.duration} seconds")
        print(f"📊 Call Status: {result.session.status.value}")
        print()

        # Show quantum insights
        if result.quantum_insights:
            print("🧠 QUANTUM INSIGHTS:")
            print(
                f"   • Success Probability: {result.quantum_insights.get('success_probability', 0):.1%}"
            )
            print(
                f"   • Optimal Timing: {result.quantum_insights.get('optimal_timing', 'unknown')}"
            )
            print(
                f"   • Script Effectiveness: {result.quantum_insights.get('script_effectiveness', 0):.1%}"
            )
            print(
                f"   • Next Call Recommendation: {result.quantum_insights.get('next_call_recommendation', 'unknown')}"
            )
            print(
                f"   • Quantum Confidence: {result.quantum_insights.get('quantum_confidence', 0):.1%}"
            )
            print()
    else:
        print(f"❌ Call failed: {result.message}")
        print()

    # Demo 2: Make a customer service call
    print("📞 DEMO 2: Making a Quantum-Enhanced Customer Service Call")
    print("-" * 40)

    service_call = CallRequest(
        to_number="+1-555-0456",
        from_number="+1-555-9999",
        agent_id="quantum_service_001",
        call_purpose="Follow-up on GOLIATH financial services inquiry",
        script_template="Professional follow-up with personalized financial solutions",
        quantum_optimization=True,
        gpu_acceleration=True,
    )

    print(f"📱 Calling: {service_call.to_number}")
    print(f"🎯 Purpose: {service_call.call_purpose}")
    print()

    print("🔄 Making call...")
    start_time = time.time()

    result2 = await agent.make_call(service_call)

    call_duration = time.time() - start_time
    print(f"✅ Call completed in {call_duration:.2f} seconds!")

    if result2.success:
        print(f"📞 Call ID: {result2.call_id}")
        print(f"⏱️  Call Duration: {result2.session.duration} seconds")
        print(f"📊 Call Status: {result2.session.status.value}")
        print()
    else:
        print(f"❌ Call failed: {result2.message}")
        print()

    # Demo 3: Get call analytics
    print("📊 DEMO 3: Call Analytics with Quantum Insights")
    print("-" * 40)

    analytics = await agent.get_call_analytics()

    if "message" not in analytics:
        print("📈 CALL ANALYTICS:")
        print(f"   • Total Calls: {analytics.get('total_calls', 0)}")
        print(f"   • Successful Calls: {analytics.get('successful_calls', 0)}")
        print(f"   • Success Rate: {analytics.get('success_rate', 0):.1%}")
        print(
            f"   • Average Duration: {analytics.get('average_duration_seconds', 0):.1f} seconds"
        )
        print(
            f"   • GPU Acceleration: {'Available' if analytics.get('gpu_acceleration_status') else 'Not Available'}"
        )
        print(
            f"   • Quantum Enhancement: {'Active' if analytics.get('quantum_enhancement_status') else 'Inactive'}"
        )
        print()

        # Show quantum patterns if available
        if "quantum_patterns" in analytics and analytics["quantum_patterns"]:
            print("🧠 QUANTUM PATTERNS:")
            patterns = analytics["quantum_patterns"]
            for key, value in patterns.items():
                if key != "message":
                    print(f"   • {key.replace('_', ' ').title()}: {value}")
            print()
    else:
        print(f"ℹ️  {analytics['message']}")
        print()

    # Demo 4: Get call history
    print("📚 DEMO 4: Call History with Filtering")
    print("-" * 40)

    # Get recent calls
    recent_calls = await agent.get_call_history(limit=5)

    if recent_calls:
        print(f"📞 Recent Calls (Last {len(recent_calls)}):")
        for i, call in enumerate(recent_calls, 1):
            print(f"   {i}. Call ID: {call.call_id}")
            print(f"      📱 Type: {call.call_type.value}")
            print(f"      📊 Status: {call.status.value}")
            print(f"      ⏰ Start: {call.start_time.strftime('%H:%M:%S')}")
            print(f"      ⏱️  Duration: {call.duration} seconds")
            print(f"      🎯 Purpose: {call.metadata.get('purpose', 'Unknown')}")
            print()
    else:
        print("📚 No call history available yet.")
        print()

    # Demo 5: Performance summary
    print("🏆 DEMO SUMMARY")
    print("-" * 40)

    total_calls = len(agent.call_history)
    successful_calls = len(
        [c for c in agent.call_history if c.status.value == "completed"]
    )

    print(f"📊 Total Calls Made: {total_calls}")
    print(f"✅ Successful Calls: {successful_calls}")
    print(
        f"📈 Success Rate: {successful_calls/total_calls:.1%}"
        if total_calls > 0
        else "📈 Success Rate: N/A"
    )
    print(
        f"🚀 NVIDIA GPU: {'Accelerating' if agent.nvidia.is_gpu_available() else 'CPU Fallback'}"
    )
    print(f"🧠 Quantum Enhancement: Active")
    print(
        f"⚡ Average Call Time: {sum(c.duration or 0 for c in agent.call_history)/total_calls:.1f}s"
        if total_calls > 0
        else "⚡ Average Call Time: N/A"
    )
    print()

    print("🎉 QUANTUM DIGITAL AGENT DEMO COMPLETE!")
    print("=" * 50)
    print("🚀 Your agent is ready to dominate voice communications!")
    print("🔗 Access via API: POST /quantum-agent/make-call")
    print("📊 Analytics: GET /quantum-agent/analytics")
    print("📚 History: GET /quantum-agent/call-history")
    print()
    print("🌟 Next steps:")
    print("   1. Deploy to production with real phone numbers")
    print("   2. Integrate with your CRM system")
    print("   3. Scale to handle thousands of concurrent calls")
    print("   4. Leverage quantum insights for call optimization")


if __name__ == "__main__":
    print("🚀 Starting Quantum Digital Agent Demo...")
    print("⏳ This demo will showcase quantum-enhanced call capabilities")
    print()

    try:
        asyncio.run(demo_quantum_digital_agent())
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print(
            "💡 Make sure all dependencies are installed and NQBA Stack is configured"
        )
