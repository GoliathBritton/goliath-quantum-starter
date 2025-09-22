#!/usr/bin/env python3
"""
Comprehensive Phase 2.1 Test Suite
Tests all Phase 2.1 components with real API connectivity
"""

import json
import time
import subprocess
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

class Phase21TestSuite:
    def __init__(self, api_base_url="http://localhost:8002"):
        self.api_base_url = api_base_url
        self.test_results = []
        self.start_time = time.time()
    
    def make_api_request(self, endpoint, method="GET", data=None):
        """Make API request using urllib"""
        url = f"{self.api_base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = urlopen(url, timeout=10)
            elif method == "POST":
                req = Request(url, data=json.dumps(data).encode() if data else None)
                req.add_header('Content-Type', 'application/json')
                response = urlopen(req, timeout=10)
            
            content = response.read().decode()
            return json.loads(content), response.getcode()
        
        except (URLError, HTTPError) as e:
            return None, getattr(e, 'code', 500)
        except Exception as e:
            return None, 500
    
    def run_test(self, test_name, test_func):
        """Run a single test and record results"""
        print(f"🧪 Running {test_name}...")
        start_time = time.time()
        
        try:
            result = test_func()
            execution_time = time.time() - start_time
            
            test_result = {
                "name": test_name,
                "status": "PASSED" if result["success"] else "FAILED",
                "execution_time": f"{execution_time:.2f}s",
                "details": result["details"],
                "error": result.get("error")
            }
            
            status_emoji = "✅" if result["success"] else "❌"
            print(f"{status_emoji} {test_name}: {test_result['status']} ({test_result['execution_time']})")
            
            if not result["success"] and result.get("error"):
                print(f"   Error: {result['error']}")
            
        except Exception as e:
            execution_time = time.time() - start_time
            test_result = {
                "name": test_name,
                "status": "FAILED",
                "execution_time": f"{execution_time:.2f}s",
                "details": "Test execution failed",
                "error": str(e)
            }
            print(f"❌ {test_name}: FAILED ({test_result['execution_time']})")
            print(f"   Error: {str(e)}")
        
        self.test_results.append(test_result)
        return test_result
    
    def test_api_health_check(self):
        """Test API server health endpoint"""
        data, status_code = self.make_api_request("/health")
        
        if status_code == 200 and data:
            return {
                "success": True,
                "details": f"API server healthy - {data.get('service', 'Unknown service')}"
            }
        else:
            return {
                "success": False,
                "details": "API health check failed",
                "error": f"HTTP {status_code}"
            }
    
    def test_phase21_status(self):
        """Test Phase 2.1 overall status endpoint"""
        data, status_code = self.make_api_request("/api/phase2.1/status")
        
        if status_code == 200 and data and data.get("status") == "operational":
            components = data.get("components", {})
            active_components = sum(1 for status in components.values() if status == "active")
            return {
                "success": True,
                "details": f"Phase 2.1 operational with {active_components} active components"
            }
        else:
            return {
                "success": False,
                "details": "Phase 2.1 status check failed",
                "error": f"HTTP {status_code}"
            }
    
    def test_constraint_evolution_engine(self):
        """Test Constraint Evolution Engine endpoint"""
        data, status_code = self.make_api_request("/api/constraints/evolution")
        
        if status_code == 200 and data and data.get("status") == "operational":
            return {
                "success": True,
                "details": f"Constraint Evolution Engine active - {data.get('active_constraints', 0)} constraints, {data.get('optimization_rate', 'N/A')} optimization rate"
            }
        else:
            return {
                "success": False,
                "details": "Constraint Evolution Engine test failed",
                "error": f"HTTP {status_code}"
            }
    
    def test_predictive_scaler(self):
        """Test Predictive Scaling System endpoint"""
        data, status_code = self.make_api_request("/api/scaling/predictive")
        
        if status_code == 200 and data and data.get("status") == "operational":
            return {
                "success": True,
                "details": f"Predictive Scaler active - {data.get('prediction_accuracy', 'N/A')} accuracy, {data.get('active_policies', 0)} policies"
            }
        else:
            return {
                "success": False,
                "details": "Predictive Scaler test failed",
                "error": f"HTTP {status_code}"
            }
    
    def test_enterprise_security_manager(self):
        """Test Enterprise Security Manager endpoint"""
        data, status_code = self.make_api_request("/api/enterprise/security")
        
        if status_code == 200 and data and data.get("status") == "operational":
            frameworks = len(data.get("compliance_frameworks", []))
            return {
                "success": True,
                "details": f"Enterprise Security Manager active - {frameworks} compliance frameworks, {data.get('security_level', 'unknown')} security level"
            }
        else:
            return {
                "success": False,
                "details": "Enterprise Security Manager test failed",
                "error": f"HTTP {status_code}"
            }
    
    def test_community_platform(self):
        """Test Community Platform endpoint"""
        data, status_code = self.make_api_request("/api/community/platform")
        
        if status_code == 200 and data and data.get("status") == "operational":
            return {
                "success": True,
                "details": f"Community Platform active - {data.get('active_developers', 0)} developers, {data.get('published_algorithms', 0)} algorithms"
            }
        else:
            return {
                "success": False,
                "details": "Community Platform test failed",
                "error": f"HTTP {status_code}"
            }
    
    def test_end_to_end_workflow(self):
        """Test end-to-end workflow"""
        data, status_code = self.make_api_request("/api/test/workflow", method="POST")
        
        if status_code == 200 and data and data.get("status") == "success":
            steps = len(data.get("steps_completed", []))
            return {
                "success": True,
                "details": f"End-to-end workflow completed - {steps} steps in {data.get('execution_time', 'N/A')}"
            }
        else:
            return {
                "success": False,
                "details": "End-to-end workflow test failed",
                "error": f"HTTP {status_code}"
            }
    
    def run_all_tests(self):
        """Run all Phase 2.1 tests"""
        print("=== Comprehensive Phase 2.1 Test Suite Starting ===")
        print(f"🎯 Target API: {self.api_base_url}")
        print()
        
        # Core API tests
        self.run_test("test_api_health_check", self.test_api_health_check)
        self.run_test("test_phase21_status", self.test_phase21_status)
        
        # Phase 2.1 component tests
        self.run_test("test_constraint_evolution_engine", self.test_constraint_evolution_engine)
        self.run_test("test_predictive_scaler", self.test_predictive_scaler)
        self.run_test("test_enterprise_security_manager", self.test_enterprise_security_manager)
        self.run_test("test_community_platform", self.test_community_platform)
        
        # Integration tests
        self.run_test("test_end_to_end_workflow", self.test_end_to_end_workflow)
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary and save results"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for test in self.test_results if test["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        total_time = time.time() - self.start_time
        
        summary = {
            "test_suite": "Comprehensive Phase 2.1 Features",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "skipped": 0,
            "execution_time": f"{total_time:.2f} seconds",
            "success_rate": f"{(passed_tests/total_tests)*100:.1f}%",
            "tests": self.test_results,
            "environment": {
                "api_server": self.api_base_url,
                "python_version": "3.14.0a5",
                "test_framework": "Comprehensive Phase 2.1 Test Suite"
            }
        }
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_phase2.1_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Print summary
        print()
        print("=== Test Summary ===")
        print(f"📊 Tests: {passed_tests}/{total_tests} passed ({summary['success_rate']})")
        print(f"⏱️  Total execution time: {summary['execution_time']}")
        print(f"💾 Results saved to: {filename}")
        
        if failed_tests > 0:
            print()
            print("❌ Failed Tests:")
            for test in self.test_results:
                if test["status"] == "FAILED":
                    print(f"   • {test['name']}: {test.get('error', 'Unknown error')}")
        
        print()
        print("=== Comprehensive Phase 2.1 Test Complete ===")
        return filename

def main():
    """Main test execution"""
    try:
        test_suite = Phase21TestSuite()
        result_file = test_suite.run_all_tests()
        print(f"✅ Test execution completed successfully")
        print(f"📄 Full results available in: {result_file}")
        
    except Exception as e:
        print(f"❌ Test suite execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()