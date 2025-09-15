#!/usr/bin/env python3
"""
Phase 2.2 Feature Testing Script
Advanced QUBO Engine & Real-Time Learning Engine
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8002"
TEST_TENANT_ID = "test_tenant_001"

# Test data
QUBO_PROBLEM_DATA = {
    "name": "Portfolio Optimization Test",
    "description": "Test portfolio optimization with quantum constraints",
    "objective_function": "minimize x1^2 + x2^2 + x3^2",
    "variables": ["x1", "x2", "x3"],
    "constraints": [
        {
            "name": "Budget Constraint",
            "type": "equality",
            "expression": "x1 + x2 + x3 = 1000000",
            "parameters": {"target": 1000000},
            "weight": 1.0,
            "evolution_strategy": "moderate",
        },
        {
            "name": "Risk Limit",
            "type": "inequality",
            "expression": "x1 + x2 <= 800000",
            "parameters": {"limit": 800000},
            "weight": 0.8,
            "evolution_strategy": "conservative",
        },
    ],
    "strategy": "adaptive",
}

LEARNING_MODEL_DATA = {
    "algorithm_type": "qubo_optimization",
    "learning_mode": "supervised",
    "initial_parameters": {
        "num_reads": 1000,
        "annealing_time": 100,
        "evolution_rate": 0.1,
        "adaptation_threshold": 0.2,
    },
}

LEARNING_EXAMPLE_DATA = {
    "input_data": {
        "portfolio_size": 1000000,
        "risk_tolerance": "medium",
        "time_horizon": 5,
    },
    "expected_output": {
        "optimal_allocation": {"x1": 400000, "x2": 300000, "x3": 300000},
        "expected_return": 0.08,
        "risk_level": 0.15,
    },
    "actual_output": {
        "optimal_allocation": {"x1": 380000, "x2": 320000, "x3": 300000},
        "expected_return": 0.075,
        "risk_level": 0.16,
    },
}


class Phase22Tester:
    """Test Phase 2.2 features"""

    def __init__(self):
        self.session = None
        self.test_results = []
        self.start_time = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, self_type, value, traceback):
        if self.session:
            await self.session.close()

    async def test_advanced_qubo_engine(self):
        """Test Advanced QUBO Engine features"""
        print("\n🧠 Testing Advanced QUBO Engine...")

        # Test 1: Create optimization problem
        print("  📝 Creating optimization problem...")
        try:
            # Send JSON data in request body
            request_data = {
                "name": QUBO_PROBLEM_DATA["name"],
                "description": QUBO_PROBLEM_DATA["description"],
                "objective_function": QUBO_PROBLEM_DATA["objective_function"],
                "variables": QUBO_PROBLEM_DATA["variables"],
                "constraints": QUBO_PROBLEM_DATA["constraints"],
                "strategy": QUBO_PROBLEM_DATA["strategy"],
                "tenant_id": TEST_TENANT_ID,
            }

            async with self.session.post(
                f"{API_BASE_URL}/phase2.2/qubo/create-problem", json=request_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    problem_id = result["data"]["problem_id"]
                    print(f"    ✅ Problem created: {problem_id}")

                    # Test 2: Get problem status
                    print("  📊 Getting problem status...")
                    async with self.session.get(
                        f"{API_BASE_URL}/phase2.2/qubo/problem/{problem_id}/status"
                    ) as status_response:
                        if status_response.status == 200:
                            status_result = await status_response.json()
                            print(
                                f"    ✅ Status retrieved: {status_result['data']['name']}"
                            )

                            # Test 3: Optimize problem
                            print("  ⚡ Optimizing problem...")
                            async with self.session.post(
                                f"{API_BASE_URL}/phase2.2/qubo/optimize/{problem_id}"
                            ) as optimize_response:
                                if optimize_response.status == 200:
                                    optimize_result = await optimize_response.json()
                                    print(
                                        f"    ✅ Optimization completed: {optimize_result['data']['quantum_advantage']:.2f}x advantage"
                                    )

                                    # Test 4: Get tenant problems
                                    print("  🏢 Getting tenant problems...")
                                    async with self.session.get(
                                        f"{API_BASE_URL}/phase2.2/qubo/tenant/{TEST_TENANT_ID}/problems"
                                    ) as problems_response:
                                        if problems_response.status == 200:
                                            problems_result = (
                                                await problems_response.json()
                                            )
                                            print(
                                                f"    ✅ Tenant problems retrieved: {len(problems_result['data'])} problems"
                                            )

                                            # Test 5: Get analytics
                                            print("  📈 Getting QUBO analytics...")
                                            async with self.session.get(
                                                f"{API_BASE_URL}/phase2.2/qubo/tenant/{TEST_TENANT_ID}/analytics"
                                            ) as analytics_response:
                                                if analytics_response.status == 200:
                                                    analytics_result = (
                                                        await analytics_response.json()
                                                    )
                                                    print(
                                                        f"    ✅ Analytics retrieved: {analytics_result['data']['total_problems']} total problems"
                                                    )
                                                    self.test_results.append(
                                                        ("Advanced QUBO Engine", "PASS")
                                                    )
                                                else:
                                                    print(
                                                        f"    ❌ Analytics failed: {analytics_response.status}"
                                                    )
                                                    self.test_results.append(
                                                        ("Advanced QUBO Engine", "FAIL")
                                                    )
                                            return
                                        else:
                                            print(
                                                f"    ❌ Tenant problems failed: {problems_response.status}"
                                            )
                                            self.test_results.append(
                                                ("Advanced QUBO Engine", "FAIL")
                                            )
                                            return
                                else:
                                    print(
                                        f"    ❌ Optimization failed: {optimize_response.status}"
                                    )
                                    self.test_results.append(
                                        ("Advanced QUBO Engine", "FAIL")
                                    )
                                    return
                        else:
                            print(
                                f"    ❌ Status retrieval failed: {status_response.status}"
                            )
                            self.test_results.append(("Advanced QUBO Engine", "FAIL"))
                            return
                else:
                    print(f"    ❌ Problem creation failed: {response.status}")
                    self.test_results.append(("Advanced QUBO Engine", "FAIL"))
                    return
        except Exception as e:
            print(f"    ❌ Advanced QUBO Engine test failed: {e}")
            self.test_results.append(("Advanced QUBO Engine", "FAIL"))

    async def test_real_time_learning_engine(self):
        """Test Real-Time Learning Engine features"""
        print("\n🧠 Testing Real-Time Learning Engine...")

        # Test 1: Create learning model
        print("  📝 Creating learning model...")
        try:
            # Send JSON data in request body
            request_data = {
                "algorithm_type": LEARNING_MODEL_DATA["algorithm_type"],
                "learning_mode": LEARNING_MODEL_DATA["learning_mode"],
                "initial_parameters": LEARNING_MODEL_DATA["initial_parameters"],
                "tenant_id": TEST_TENANT_ID,
            }

            async with self.session.post(
                f"{API_BASE_URL}/phase2.2/learning/create-model", json=request_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    model_id = result["data"]["model_id"]
                    print(f"    ✅ Learning model created: {model_id}")

                    # Test 2: Add learning example
                    print("  📚 Adding learning example...")
                    example_data = {
                        "model_id": model_id,
                        "input_data": LEARNING_EXAMPLE_DATA["input_data"],
                        "expected_output": LEARNING_EXAMPLE_DATA["expected_output"],
                        "actual_output": LEARNING_EXAMPLE_DATA["actual_output"],
                        "tenant_id": TEST_TENANT_ID,
                    }

                    async with self.session.post(
                        f"{API_BASE_URL}/phase2.2/learning/add-example",
                        json=example_data,
                    ) as example_response:
                        if example_response.status == 200:
                            example_result = await example_response.json()
                            print(
                                f"    ✅ Learning example added: {example_result['data']['performance_score']:.3f} score"
                            )

                            # Test 3: Get model performance
                            print("  📊 Getting model performance...")
                            async with self.session.get(
                                f"{API_BASE_URL}/phase2.2/learning/model/{model_id}/performance"
                            ) as performance_response:
                                if performance_response.status == 200:
                                    performance_result = (
                                        await performance_response.json()
                                    )
                                    print(
                                        f"    ✅ Performance retrieved: {performance_result['data']['current_accuracy']:.3f} accuracy"
                                    )

                                    # Test 4: Get learning summary
                                    print("  📋 Getting learning summary...")
                                    async with self.session.get(
                                        f"{API_BASE_URL}/phase2.2/learning/tenant/{TEST_TENANT_ID}/summary"
                                    ) as summary_response:
                                        if summary_response.status == 200:
                                            summary_result = (
                                                await summary_response.json()
                                            )
                                            print(
                                                f"    ✅ Learning summary retrieved: {summary_result['data']['total_models']} models"
                                            )

                                            # Test 5: Export learning data
                                            print("  📤 Exporting learning data...")
                                            async with self.session.post(
                                                f"{API_BASE_URL}/phase2.2/learning/export/{TEST_TENANT_ID}",
                                                params={"format": "json"},
                                            ) as export_response:
                                                if export_response.status == 200:
                                                    export_result = (
                                                        await export_response.json()
                                                    )
                                                    print(
                                                        f"    ✅ Learning data exported: {export_result['data']['summary']['total_models']} models"
                                                    )
                                                    self.test_results.append(
                                                        (
                                                            "Real-Time Learning Engine",
                                                            "PASS",
                                                        )
                                                    )
                                                else:
                                                    print(
                                                        f"    ❌ Learning data export failed: {export_response.status}"
                                                    )
                                                    self.test_results.append(
                                                        (
                                                            "Real-Time Learning Engine",
                                                            "FAIL",
                                                        )
                                                    )
                                            return
                                        else:
                                            print(
                                                f"    ❌ Learning summary failed: {summary_response.status}"
                                            )
                                            self.test_results.append(
                                                ("Real-Time Learning Engine", "FAIL")
                                            )
                                            return
                                else:
                                    print(
                                        f"    ❌ Model performance failed: {performance_response.status}"
                                    )
                                    self.test_results.append(
                                        ("Real-Time Learning Engine", "FAIL")
                                    )
                                    return
                        else:
                            print(
                                f"    ❌ Learning example addition failed: {example_response.status}"
                            )
                            self.test_results.append(
                                ("Real-Time Learning Engine", "FAIL")
                            )
                            return
                else:
                    print(f"    ❌ Learning model creation failed: {response.status}")
                    self.test_results.append(("Real-Time Learning Engine", "FAIL"))
                    return
        except Exception as e:
            print(f"    ❌ Real-Time Learning Engine test failed: {e}")
            self.test_results.append(("Real-Time Learning Engine", "FAIL"))

    async def test_integration_workflows(self):
        """Test integration workflows between Phase 2.2 components"""
        print("\n🔗 Testing Integration Workflows...")

        try:
            # Test 1: Create QUBO problem and learning model together
            print("  🔄 Testing QUBO + Learning integration...")

            # Create QUBO problem
            qubo_data = {
                "name": QUBO_PROBLEM_DATA["name"],
                "description": QUBO_PROBLEM_DATA["description"],
                "objective_function": QUBO_PROBLEM_DATA["objective_function"],
                "variables": QUBO_PROBLEM_DATA["variables"],
                "constraints": QUBO_PROBLEM_DATA["constraints"],
                "strategy": QUBO_PROBLEM_DATA["strategy"],
                "tenant_id": TEST_TENANT_ID,
            }

            async with self.session.post(
                f"{API_BASE_URL}/phase2.2/qubo/create-problem", json=qubo_data
            ) as qubo_response:
                if qubo_response.status == 200:
                    qubo_result = await qubo_response.json()
                    problem_id = qubo_result["data"]["problem_id"]

                    # Create learning model for QUBO optimization
                    learning_data = {
                        "algorithm_type": "qubo_optimization",
                        "learning_mode": LEARNING_MODEL_DATA["learning_mode"],
                        "initial_parameters": LEARNING_MODEL_DATA["initial_parameters"],
                        "tenant_id": TEST_TENANT_ID,
                    }

                    async with self.session.post(
                        f"{API_BASE_URL}/phase2.2/learning/create-model",
                        json=learning_data,
                    ) as learning_response:
                        if learning_response.status == 200:
                            learning_result = await learning_response.json()
                            model_id = learning_result["data"]["model_id"]

                            print(
                                f"    ✅ Integration test completed: QUBO problem {problem_id} + Learning model {model_id}"
                            )
                            self.test_results.append(("Integration Workflows", "PASS"))
                        else:
                            print(
                                f"    ❌ Learning model creation failed: {learning_response.status}"
                            )
                            self.test_results.append(("Integration Workflows", "FAIL"))
                else:
                    print(
                        f"    ❌ QUBO problem creation failed: {qubo_response.status}"
                    )
                    self.test_results.append(("Integration Workflows", "FAIL"))

        except Exception as e:
            print(f"    ❌ Integration workflow test failed: {e}")
            self.test_results.append(("Integration Workflows", "FAIL"))

    async def run_all_tests(self):
        """Run all Phase 2.2 tests"""
        print("🚀 Starting Phase 2.2 Feature Testing")
        print("=" * 50)

        self.start_time = time.time()

        # Run all test suites
        await self.test_advanced_qubo_engine()
        await self.test_real_time_learning_engine()
        await self.test_integration_workflows()

        # Generate test report
        await self.generate_test_report()

    async def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("📊 PHASE 2.2 TEST RESULTS")
        print("=" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, status in self.test_results if status == "PASS")
        failed_tests = total_tests - passed_tests

        # Individual test results
        for test_name, status in self.test_results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {status}")

        # Summary
        print("\n" + "-" * 50)
        print(f"📈 SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        # Performance metrics
        if self.start_time:
            total_time = time.time() - self.start_time
            print(f"   Total Test Time: {total_time:.2f} seconds")
            print(
                f"   Average Test Time: {total_time/total_tests:.2f} seconds per test"
            )

        # Recommendations
        print("\n" + "-" * 50)
        if failed_tests == 0:
            print(
                "🎉 All Phase 2.2 tests passed! The platform is ready for production."
            )
        else:
            print(
                f"⚠️  {failed_tests} test(s) failed. Please review and fix the issues."
            )

        print("\n🚀 Phase 2.2 testing completed!")


async def main():
    """Main test execution"""
    try:
        async with Phase22Tester() as tester:
            await tester.run_all_tests()
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        print("\n💡 Make sure the server is running on port 8002:")
        print(
            "   python -m uvicorn src.nqba_stack.api_server:app --host 0.0.0.0 --port 8002"
        )


if __name__ == "__main__":
    asyncio.run(main())
