#!/usr/bin/env python3
"""
FLYFOX AI - Live Integration Demo Script
Demonstrates the complete lead capture → quantum scoring → dashboard update flow
"""

import requests
import json
import time
from datetime import datetime
import random

# Configuration
API_BASE = "http://localhost:8000"
DASHBOARD_URL = "http://localhost:3000"


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)


def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)


def test_api_health():
    """Test API health endpoint"""
    print_step(1, "Testing API Health")

    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['ok']}")
            print(f"🔬 Quantum Backend: {data['quantum_backend']}")
            print(f"⚡ Performance Multiplier: {data['multiplier']}x")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health Check Error: {e}")
        return False


def test_quantum_lead_scoring():
    """Test quantum lead scoring endpoint"""
    print_step(2, "Testing Quantum Lead Scoring")

    # Sample lead data
    lead_data = {
        "company": "FutureTech Solutions",
        "industry": "technology",
        "name": "John Smith",
        "email": "john@futuretech.com",
        "budget": 25000.0,
        "signals": {"intent": 4.2, "hiring": 2.8, "techfit": 3.5},
    }

    try:
        response = requests.post(
            f"{API_BASE}/v2/sigma/quantum-scoring",
            json=lead_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Lead Scored Successfully!")
            print(f"🆔 Lead ID: {data['id']}")
            print(f"📊 Quantum Score: {data['score']}")
            print(f"🔬 Backend: {data['quantum_backend']}")
            print(f"⚡ Multiplier: {data['multiplier']}x")
            print(f"📈 Dashboard Updated: {data['dashboard_updated']}")
            print(f"📝 Rationale: {', '.join(data['rationale'][:2])}...")
            return data
        else:
            print(f"❌ Lead Scoring Failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Lead Scoring Error: {e}")
        return None


def test_dashboard_update():
    """Test dashboard data update"""
    print_step(3, "Testing Dashboard Update")

    try:
        response = requests.get(f"{API_BASE}/v2/dashboard/overview")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard Data Retrieved!")
            print(f"📊 KPIs Available: {len(data.get('kpis', {}))}")
            print(f"🔬 Quantum Jobs: {data.get('quantum_jobs_running', 0)}")
            print(f"⏰ Last Updated: {data.get('last_updated', 'N/A')}")
            return data
        else:
            print(f"❌ Dashboard Update Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Dashboard Update Error: {e}")
        return None


def simulate_n8n_webhook():
    """Simulate n8n webhook call"""
    print_step(4, "Simulating n8n Webhook Call")

    # Simulate the webhook payload that n8n would send
    webhook_payload = {
        "name": "Sarah Johnson",
        "email": "sarah@innovatecorp.com",
        "company": "InnovateCorp",
        "industry": "consulting",
        "budget": "45000",
    }

    print(f"📤 Sending webhook payload: {json.dumps(webhook_payload, indent=2)}")

    try:
        # This would be the actual n8n webhook URL in production
        # For demo, we're calling our API directly
        response = requests.post(
            f"{API_BASE}/v2/sigma/quantum-scoring",
            json={
                "company": webhook_payload["company"],
                "industry": webhook_payload["industry"],
                "name": webhook_payload["name"],
                "email": webhook_payload["email"],
                "budget": float(webhook_payload["budget"]),
                "signals": {
                    "intent": random.uniform(3.0, 5.0),
                    "hiring": random.uniform(1.0, 4.0),
                    "techfit": random.uniform(2.0, 4.5),
                },
            },
            headers={
                "Content-Type": "application/json",
                "X-FLYFOX-Source": "n8n-integration",
            },
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Webhook Processing Successful!")
            print(f"🆔 New Lead ID: {data['id']}")
            print(f"📊 Quantum Score: {data['score']}")
            print(f"📈 Dashboard Updated: {data['dashboard_updated']}")
            return data
        else:
            print(f"❌ Webhook Processing Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Webhook Processing Error: {e}")
        return None


def test_performance_metrics():
    """Test performance metrics endpoint"""
    print_step(5, "Testing Performance Metrics")

    try:
        response = requests.get(f"{API_BASE}/v2/sigma/performance-summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Performance Metrics Retrieved!")
            print(f"📊 Leads Processed: {data['leads_processed']}")
            print(f"📈 Average Score: {data['average_lead_score']:.3f}")
            print(f"⭐ High Value Leads: {data['high_value_leads']}")
            print(f"🔬 Quantum Jobs: {data['quantum_jobs_completed']}")
            print(f"⚡ System Uptime: {data['system_uptime']}%")
            return data
        else:
            print(f"❌ Performance Metrics Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Performance Metrics Error: {e}")
        return None


def test_qei_calculation():
    """Test QEI calculation"""
    print_step(6, "Testing QEI Calculation")

    qei_data = {
        "inputs": {
            "cycle_time": 42.0,
            "win_rate": 31.0,
            "acv": 85.0,
            "cac": 23.0,
            "ltv": 420.0,
        },
        "window": "7d",
    }

    try:
        response = requests.post(
            f"{API_BASE}/v2/sigma/qei-calculation",
            json=qei_data,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ QEI Calculation Successful!")
            print(f"📊 QEI Score: {data['qei_score']}")
            print(f"🔬 Quantum Backend: {data['quantum_backend']}")
            print(f"⚡ Multiplier: {data['multiplier']}x")
            print(
                f"📈 Drivers: {', '.join([f'{k}={v:.3f}' for k, v in data['drivers'].items()])}"
            )
            return data
        else:
            print(f"❌ QEI Calculation Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ QEI Calculation Error: {e}")
        return None


def run_live_demo():
    """Run the complete live demo"""
    print_header("FLYFOX AI - Live Integration Demo")
    print(f"🕐 Demo Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Base: {API_BASE}")
    print(f"📊 Dashboard: {DASHBOARD_URL}")

    # Run all tests
    results = {}

    # Test 1: API Health
    results["health"] = test_api_health()
    if not results["health"]:
        print("\n❌ API Health check failed. Please ensure the backend is running.")
        return

    # Test 2: Quantum Lead Scoring
    results["scoring"] = test_quantum_lead_scoring()

    # Test 3: Dashboard Update
    results["dashboard"] = test_dashboard_update()

    # Test 4: n8n Webhook Simulation
    results["webhook"] = simulate_n8n_webhook()

    # Test 5: Performance Metrics
    results["performance"] = test_performance_metrics()

    # Test 6: QEI Calculation
    results["qei"] = test_qei_calculation()

    # Summary
    print_header("Demo Summary")
    successful_tests = sum(1 for result in results.values() if result is not None)
    total_tests = len(results)

    print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
    print(f"📊 Success Rate: {(successful_tests/total_tests)*100:.1f}%")

    if successful_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Live integration is working perfectly!")
        print("\n🚀 Next Steps:")
        print("1. Open your browser to http://localhost:3000")
        print("2. Navigate to the Dashboard to see real-time updates")
        print("3. Import the n8n workflow from integrations/n8n-demo-workflow.json")
        print("4. Test the complete flow with real webhook calls")
    else:
        print("\n⚠️ Some tests failed. Check the logs above for details.")

    print(f"\n🕐 Demo Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    run_live_demo()
