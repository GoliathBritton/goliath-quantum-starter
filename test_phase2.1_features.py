#!/usr/bin/env python3
"""
Phase 2.1 Features Test Script

Comprehensive testing of all Phase 2.1 components:
- Advanced Constraint Evolution Engine
- Predictive Scaling System
- Enterprise Integration Framework
- Community Launch Platform
"""

import asyncio
import json
import requests
import time
from datetime import datetime
from typing import Dict, Any, List

# Configuration
API_BASE_URL = "http://localhost:8002"
TEST_TENANT_NAME = "Phase2.1TestCorp"
TEST_ALGORITHM_NAME = "TestAdvancedAlgorithm_v2.1"


class Phase21TestSuite:
    """Test suite for Phase 2.1 features"""

    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.test_results = []
        self.start_time = datetime.now()

    def log_test(
        self, test_name: str, success: bool, details: str = "", error: str = ""
    ):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
        print()

    def run_all_tests(self):
        """Run all Phase 2.1 test suites"""
        print("🚀 **Phase 2.1 Features Test Suite**")
        print("=" * 50)
        print()

        # Test Constraint Evolution Engine
        self.test_constraint_evolution()

        # Test Predictive Scaling System
        self.test_predictive_scaling()

        # Test Enterprise Integration Framework
        self.test_enterprise_integration()

        # Test Community Launch Platform
        self.test_community_platform()

        # Test Integration Workflows
        self.test_integration_workflows()

        # Generate test report
        self.generate_test_report()

    def test_constraint_evolution(self):
        """Test Constraint Evolution Engine features"""
        print("🧠 **Testing Constraint Evolution Engine**")
        print("-" * 40)

        # Test 1: Evolve constraints
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/constraints/evolve",
                json={
                    "tenant_id": TEST_TENANT_NAME,
                    "constraint_ids": ["constraint_1", "constraint_2"],
                    "performance_threshold": 0.85,
                    "evolution_strategy": "moderate",
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("updates_count", 0) > 0:
                    self.log_test(
                        "Constraint Evolution - Evolve Constraints",
                        True,
                        f"Generated {data['updates_count']} constraint updates",
                    )
                else:
                    self.log_test(
                        "Constraint Evolution - Evolve Constraints",
                        False,
                        "No constraint updates generated",
                    )
            else:
                self.log_test(
                    "Constraint Evolution - Evolve Constraints",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Constraint Evolution - Evolve Constraints", False, error=str(e)
            )

        # Test 2: Predict constraint performance
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/constraints/predict-performance",
                json={
                    "constraint_id": "constraint_1",
                    "scenario_data": {
                        "scenario_name": "high_volatility",
                        "market_volatility": 0.2,
                        "trend_change": 0.1,
                    },
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("predicted_performance"):
                    self.log_test(
                        "Constraint Evolution - Performance Prediction",
                        True,
                        f"Predicted performance: {data['predicted_performance']:.3f}",
                    )
                else:
                    self.log_test(
                        "Constraint Evolution - Performance Prediction",
                        False,
                        "No performance prediction generated",
                    )
            else:
                self.log_test(
                    "Constraint Evolution - Performance Prediction",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Constraint Evolution - Performance Prediction", False, error=str(e)
            )

        # Test 3: Get evolution history
        try:
            response = requests.get(
                f"{self.api_base_url}/phase2.1/constraints/evolution-history/{TEST_TENANT_NAME}",
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(
                        "Constraint Evolution - Evolution History",
                        True,
                        f"Retrieved {data.get('history_count', 0)} evolution records",
                    )
                else:
                    self.log_test(
                        "Constraint Evolution - Evolution History",
                        False,
                        "Failed to retrieve evolution history",
                    )
            else:
                self.log_test(
                    "Constraint Evolution - Evolution History",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Constraint Evolution - Evolution History", False, error=str(e)
            )

    def test_predictive_scaling(self):
        """Test Predictive Scaling System features"""
        print("📈 **Testing Predictive Scaling System**")
        print("-" * 40)

        # Test 1: Predict resource demand
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/scaling/predict-demand",
                json={
                    "tenant_id": TEST_TENANT_NAME,
                    "time_horizon": 24,
                    "resource_types": ["compute", "memory", "storage"],
                    "include_business_cycles": True,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("predictions_count", 0) > 0:
                    self.log_test(
                        "Predictive Scaling - Resource Demand Prediction",
                        True,
                        f"Generated {data['predictions_count']} resource predictions",
                    )
                else:
                    self.log_test(
                        "Predictive Scaling - Resource Demand Prediction",
                        False,
                        "No resource predictions generated",
                    )
            else:
                self.log_test(
                    "Predictive Scaling - Resource Demand Prediction",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Predictive Scaling - Resource Demand Prediction", False, error=str(e)
            )

        # Test 2: Optimize scaling schedule
        try:
            # Mock predictions data
            mock_predictions = [
                {
                    "resource_type": "compute",
                    "predicted_demand": 0.8,
                    "confidence_interval": [0.7, 0.9],
                    "trend_direction": "increasing",
                },
                {
                    "resource_type": "memory",
                    "predicted_demand": 0.6,
                    "confidence_interval": [0.5, 0.7],
                    "trend_direction": "stable",
                },
            ]

            response = requests.post(
                f"{self.api_base_url}/phase2.1/scaling/optimize-schedule",
                json={
                    "predictions": mock_predictions,
                    "tenant_id": TEST_TENANT_NAME,
                    "optimization_algorithm": "genetic",
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("schedule_id"):
                    self.log_test(
                        "Predictive Scaling - Schedule Optimization",
                        True,
                        f"Created schedule {data['schedule_id']} with {data.get('actions_count', 0)} actions",
                    )
                else:
                    self.log_test(
                        "Predictive Scaling - Schedule Optimization",
                        False,
                        "Failed to create scaling schedule",
                    )
            else:
                self.log_test(
                    "Predictive Scaling - Schedule Optimization",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Predictive Scaling - Schedule Optimization", False, error=str(e)
            )

        # Test 3: Apply scaling schedule
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/scaling/apply-schedule",
                params={"schedule_id": "test_schedule_001", "auto_approve": True},
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(
                        "Predictive Scaling - Apply Schedule",
                        True,
                        f"Applied {data.get('actions_applied', 0)} scaling actions",
                    )
                else:
                    self.log_test(
                        "Predictive Scaling - Apply Schedule",
                        False,
                        "Failed to apply scaling schedule",
                    )
            else:
                self.log_test(
                    "Predictive Scaling - Apply Schedule",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test("Predictive Scaling - Apply Schedule", False, error=str(e))

    def test_enterprise_integration(self):
        """Test Enterprise Integration Framework features"""
        print("🏢 **Testing Enterprise Integration Framework**")
        print("-" * 40)

        # Test 1: Enterprise authentication (SAML)
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/enterprise/authenticate",
                json={
                    "auth_type": "saml",
                    "assertion": "mock_saml_assertion_data_here_for_testing_purposes_only_this_is_a_very_long_assertion_string_to_meet_the_minimum_length_requirement_of_100_characters_for_saml_validation_in_the_test_environment",
                    "issuer": "https://test-enterprise-idp.com",
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("user_id"):
                    self.log_test(
                        "Enterprise Integration - SAML Authentication",
                        True,
                        f"Authenticated user: {data.get('username', 'Unknown')}",
                    )
                else:
                    self.log_test(
                        "Enterprise Integration - SAML Authentication",
                        False,
                        "Authentication failed",
                    )
            else:
                self.log_test(
                    "Enterprise Integration - SAML Authentication",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Enterprise Integration - SAML Authentication", False, error=str(e)
            )

        # Test 2: Compliance check
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/enterprise/compliance-check",
                json={
                    "operation": "financial_optimization",
                    "data": {
                        "data_type": "financial",
                        "contains_pii": False,
                        "risk_level": "medium",
                    },
                    "frameworks": ["soc2", "iso27001"],
                    "timeout": 30,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    compliance_status = (
                        "Compliant" if data.get("is_compliant") else "Non-compliant"
                    )
                    self.log_test(
                        "Enterprise Integration - Compliance Check",
                        True,
                        f"Compliance status: {compliance_status}, {data.get('compliant_requirements', 0)}/{data.get('requirements_checked', 0)} requirements met",
                    )
                else:
                    self.log_test(
                        "Enterprise Integration - Compliance Check",
                        False,
                        "Compliance check failed",
                    )
            else:
                self.log_test(
                    "Enterprise Integration - Compliance Check",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Enterprise Integration - Compliance Check", False, error=str(e)
            )

        # Test 3: Audit logging
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/enterprise/audit-log",
                json={
                    "user_id": "test_user_001",
                    "action": "test_operation",
                    "details": {
                        "test": "data",
                        "timestamp": datetime.now().isoformat(),
                    },
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("entry_id"):
                    self.log_test(
                        "Enterprise Integration - Audit Logging",
                        True,
                        f"Created audit entry: {data.get('entry_id', 'Unknown')}",
                    )
                else:
                    self.log_test(
                        "Enterprise Integration - Audit Logging",
                        False,
                        "Failed to create audit log entry",
                    )
            else:
                self.log_test(
                    "Enterprise Integration - Audit Logging",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test("Enterprise Integration - Audit Logging", False, error=str(e))

    def test_community_platform(self):
        """Test Community Launch Platform features"""
        print("🌐 **Testing Community Launch Platform**")
        print("-" * 40)

        # Test 1: Submit algorithm
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/community/submit-algorithm",
                json={
                    "name": TEST_ALGORITHM_NAME,
                    "description": "Advanced quantum optimization algorithm for testing Phase 2.1 features",
                    "category": "Optimization",
                    "complexity": "Advanced",
                    "price": 49.99,
                    "source_code": "def test_algorithm():\n    return 'Hello from Phase 2.1!'",
                    "documentation": "# Test Algorithm\n\nThis is a test algorithm for Phase 2.1 testing.",
                    "tags": ["test", "phase2.1", "quantum", "optimization"],
                    "requirements": ["numpy", "qiskit"],
                    "example_usage": "result = test_algorithm()",
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("algorithm_id"):
                    self.log_test(
                        "Community Platform - Algorithm Submission",
                        True,
                        f"Submitted algorithm: {data.get('algorithm_id', 'Unknown')}",
                    )
                else:
                    self.log_test(
                        "Community Platform - Algorithm Submission",
                        False,
                        f"Submission failed: {data.get('message', 'Unknown error')}",
                    )
            else:
                self.log_test(
                    "Community Platform - Algorithm Submission",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Community Platform - Algorithm Submission", False, error=str(e)
            )

        # Test 2: Discover algorithms
        try:
            response = requests.get(
                f"{self.api_base_url}/phase2.1/community/discover-algorithms",
                params={
                    "category": "Optimization",
                    "complexity": "Advanced",
                    "max_price": 100.0,
                    "limit": 10,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(
                        "Community Platform - Algorithm Discovery",
                        True,
                        f"Found {data.get('algorithms_count', 0)} algorithms",
                    )
                else:
                    self.log_test(
                        "Community Platform - Algorithm Discovery",
                        False,
                        "Algorithm discovery failed",
                    )
            else:
                self.log_test(
                    "Community Platform - Algorithm Discovery",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test(
                "Community Platform - Algorithm Discovery", False, error=str(e)
            )

        # Test 3: Create tutorial
        try:
            response = requests.post(
                f"{self.api_base_url}/phase2.1/community/create-tutorial",
                json={
                    "title": "Phase 2.1 Testing Tutorial",
                    "content": "This comprehensive tutorial explains how to test Phase 2.1 features of the Goliath Quantum Starter platform. It covers all aspects including constraint evolution, predictive scaling, enterprise integration, and community features. This guide will help developers understand and implement the advanced capabilities of the platform.",
                    "category": "Testing",
                    "difficulty": "Intermediate",
                    "tags": ["testing", "phase2.1", "tutorial"],
                    "estimated_time": 30,
                    "prerequisites": ["Python basics", "API testing"],
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("tutorial_id"):
                    self.log_test(
                        "Community Platform - Tutorial Creation",
                        True,
                        f"Created tutorial: {data.get('tutorial_id', 'Unknown')}",
                    )
                else:
                    self.log_test(
                        "Community Platform - Tutorial Creation",
                        False,
                        f"Tutorial creation failed: {data.get('message', 'Unknown error')}",
                    )
            else:
                self.log_test(
                    "Community Platform - Tutorial Creation",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test("Community Platform - Tutorial Creation", False, error=str(e))

        # Test 4: Get active forums
        try:
            response = requests.get(
                f"{self.api_base_url}/phase2.1/community/forums", timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(
                        "Community Platform - Forum Listing",
                        True,
                        f"Found {data.get('forums_count', 0)} active forums",
                    )
                else:
                    self.log_test(
                        "Community Platform - Forum Listing",
                        False,
                        "Failed to retrieve forums",
                    )
            else:
                self.log_test(
                    "Community Platform - Forum Listing",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test("Community Platform - Forum Listing", False, error=str(e))

        # Test 5: Get upcoming events
        try:
            response = requests.get(
                f"{self.api_base_url}/phase2.1/community/events", timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test(
                        "Community Platform - Event Listing",
                        True,
                        f"Found {data.get('events_count', 0)} upcoming events",
                    )
                else:
                    self.log_test(
                        "Community Platform - Event Listing",
                        False,
                        "Failed to retrieve events",
                    )
            else:
                self.log_test(
                    "Community Platform - Event Listing",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                )
        except Exception as e:
            self.log_test("Community Platform - Event Listing", False, error=str(e))

    def test_integration_workflows(self):
        """Test integration workflows between Phase 2.1 components"""
        print("🔗 **Testing Integration Workflows**")
        print("-" * 40)

        # Test 1: End-to-end enterprise workflow
        try:
            # Step 1: Enterprise authentication
            auth_response = requests.post(
                f"{self.api_base_url}/phase2.1/enterprise/authenticate",
                json={"auth_type": "ldap", "assertion": "admin", "issuer": "admin123"},
                timeout=30,
            )

            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                if auth_data.get("success"):
                    user_id = auth_data.get("user_id")

                    # Step 2: Compliance check
                    compliance_response = requests.post(
                        f"{self.api_base_url}/phase2.1/enterprise/compliance-check",
                        json={
                            "operation": "constraint_evolution",
                            "data": {
                                "user_id": user_id,
                                "operation_type": "ai_optimization",
                            },
                            "frameworks": ["soc2"],
                            "timeout": 30,
                        },
                        timeout=30,
                    )

                    if compliance_response.status_code == 200:
                        compliance_data = compliance_response.json()
                        if compliance_data.get("success") and compliance_data.get(
                            "is_compliant"
                        ):

                            # Step 3: Constraint evolution
                            evolution_response = requests.post(
                                f"{self.api_base_url}/phase2.1/constraints/evolve",
                                json={
                                    "tenant_id": TEST_TENANT_NAME,
                                    "constraint_ids": ["constraint_1"],
                                    "performance_threshold": 0.9,
                                    "evolution_strategy": "conservative",
                                },
                                timeout=30,
                            )

                            if evolution_response.status_code == 200:
                                evolution_data = evolution_response.json()
                                if evolution_data.get("success"):

                                    # Step 4: Audit logging
                                    audit_response = requests.post(
                                        f"{self.api_base_url}/phase2.1/enterprise/audit-log",
                                        params={
                                            "user_id": user_id,
                                            "action": "constraint_evolution_completed",
                                            "details": json.dumps(
                                                {
                                                    "tenant_id": TEST_TENANT_NAME,
                                                    "updates_count": evolution_data.get(
                                                        "updates_count", 0
                                                    ),
                                                    "strategy": "conservative",
                                                }
                                            ),
                                        },
                                        timeout=30,
                                    )

                                    if audit_response.status_code == 200:
                                        self.log_test(
                                            "Integration Workflows - Enterprise Workflow",
                                            True,
                                            "Completed full enterprise workflow: auth → compliance → evolution → audit",
                                        )
                                    else:
                                        self.log_test(
                                            "Integration Workflows - Enterprise Workflow",
                                            False,
                                            "Workflow failed at audit logging step",
                                        )
                                else:
                                    self.log_test(
                                        "Integration Workflows - Enterprise Workflow",
                                        False,
                                        "Workflow failed at constraint evolution step",
                                    )
                            else:
                                self.log_test(
                                    "Integration Workflows - Enterprise Workflow",
                                    False,
                                    "Workflow failed at constraint evolution step",
                                )
                        else:
                            self.log_test(
                                "Integration Workflows - Enterprise Workflow",
                                False,
                                "Workflow failed at compliance check step",
                            )
                    else:
                        self.log_test(
                            "Integration Workflows - Enterprise Workflow",
                            False,
                            "Workflow failed at compliance check step",
                        )
                else:
                    self.log_test(
                        "Integration Workflows - Enterprise Workflow",
                        False,
                        "Workflow failed at authentication step",
                    )
            else:
                self.log_test(
                    "Integration Workflows - Enterprise Workflow",
                    False,
                    "Workflow failed at authentication step",
                )
        except Exception as e:
            self.log_test(
                "Integration Workflows - Enterprise Workflow", False, error=str(e)
            )

        # Test 2: Predictive scaling with constraint evolution
        try:
            # Step 1: Predict resource demand
            demand_response = requests.post(
                f"{self.api_base_url}/phase2.1/scaling/predict-demand",
                json={
                    "tenant_id": TEST_TENANT_NAME,
                    "time_horizon": 12,
                    "resource_types": ["compute", "memory"],
                    "include_business_cycles": True,
                },
                timeout=30,
            )

            if demand_response.status_code == 200:
                demand_data = demand_response.json()
                if demand_data.get("success") and demand_data.get("predictions"):

                    # Step 2: Optimize scaling schedule
                    scaling_response = requests.post(
                        f"{self.api_base_url}/phase2.1/scaling/optimize-schedule",
                        json={
                            "predictions": demand_data.get("predictions", []),
                            "tenant_id": TEST_TENANT_NAME,
                            "optimization_algorithm": "genetic",
                        },
                        timeout=30,
                    )

                    if scaling_response.status_code == 200:
                        scaling_data = scaling_response.json()
                        if scaling_data.get("success"):

                            # Step 3: Evolve constraints based on scaling needs
                            evolution_response = requests.post(
                                f"{self.api_base_url}/phase2.1/constraints/evolve",
                                json={
                                    "tenant_id": TEST_TENANT_NAME,
                                    "constraint_ids": ["scaling_constraint_1"],
                                    "performance_threshold": 0.8,
                                    "evolution_strategy": "adaptive",
                                },
                                timeout=30,
                            )

                            if evolution_response.status_code == 200:
                                self.log_test(
                                    "Integration Workflows - Scaling + Evolution",
                                    True,
                                    "Completed scaling + evolution workflow: demand prediction → schedule optimization → constraint evolution",
                                )
                            else:
                                self.log_test(
                                    "Integration Workflows - Scaling + Evolution",
                                    False,
                                    "Workflow failed at constraint evolution step",
                                )
                        else:
                            self.log_test(
                                "Integration Workflows - Scaling + Evolution",
                                False,
                                "Workflow failed at schedule optimization step",
                            )
                    else:
                        self.log_test(
                            "Integration Workflows - Scaling + Evolution",
                            False,
                            "Workflow failed at schedule optimization step",
                        )
                else:
                    self.log_test(
                        "Integration Workflows - Scaling + Evolution",
                        False,
                        "Workflow failed at demand prediction step",
                    )
            else:
                self.log_test(
                    "Integration Workflows - Scaling + Evolution",
                    False,
                    "Workflow failed at demand prediction step",
                )
        except Exception as e:
            self.log_test(
                "Integration Workflows - Scaling + Evolution", False, error=str(e)
            )

    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("📊 **Test Report Summary**")
        print("=" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()

        if failed_tests > 0:
            print("❌ **Failed Tests:**")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test_name']}")
                    if result["error"]:
                        print(f"    Error: {result['error']}")
            print()

        # Save detailed results to file
        report_filename = (
            f"phase2.1_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_filename, "w") as f:
            json.dump(
                {
                    "test_suite": "Phase 2.1 Features",
                    "start_time": self.start_time.isoformat(),
                    "end_time": datetime.now().isoformat(),
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": (passed_tests / total_tests) * 100,
                    "test_results": self.test_results,
                },
                f,
                indent=2,
            )

        print(f"📄 Detailed results saved to: {report_filename}")

        # Overall assessment
        if failed_tests == 0:
            print(
                "🎉 **All Phase 2.1 tests passed! The platform is ready for production.**"
            )
        elif failed_tests <= total_tests * 0.1:  # Less than 10% failure
            print(
                "⚠️  **Most tests passed. Minor issues detected that should be addressed.**"
            )
        else:
            print(
                "🚨 **Significant test failures detected. Platform needs attention before production.**"
            )


def main():
    """Main test execution"""
    print("Starting Phase 2.1 Features Test Suite...")
    print(f"API Base URL: {API_BASE_URL}")
    print()

    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(5)

    # Run tests
    test_suite = Phase21TestSuite(API_BASE_URL)
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()
