#!/usr/bin/env python3
"""
Observability Validation Script for NQBA Stack
Tests monitoring, metrics, and alerting capabilities
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8080"

class ObservabilityValidator:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.results = {}
    
    def test_health_endpoint(self):
        """Test the health endpoint and validate response structure"""
        print("🔍 Testing Health Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ Health endpoint responding (status: {health_data.get('status', 'unknown')})")
                
                # Validate health data structure
                required_fields = ['status', 'timestamp', 'ecosystem']
                missing_fields = [field for field in required_fields if field not in health_data]
                
                if missing_fields:
                    print(f"   ⚠️  Missing health fields: {missing_fields}")
                    return False
                
                ecosystem = health_data.get('ecosystem', {})
                if 'total_business_units' in ecosystem:
                    print(f"   📊 Business Units: {ecosystem['total_business_units']}")
                
                return True
            else:
                print(f"   ❌ Health endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Health endpoint error: {str(e)}")
            return False
    
    def test_metrics_endpoint(self):
        """Test the metrics endpoint and validate metrics structure"""
        print("\n📊 Testing Metrics Endpoint...")
        try:
            response = requests.get(f"{self.base_url}/observability/metrics", timeout=10)
            if response.status_code == 200:
                metrics_data = response.json()
                print(f"   ✅ Metrics endpoint responding (status: {metrics_data.get('status', 'unknown')})")
                
                # Validate metrics structure
                metrics = metrics_data.get('metrics', {})
                metric_categories = ['system_health', 'performance', 'business', 'quantum']
                
                available_categories = [cat for cat in metric_categories if cat in metrics]
                print(f"   📈 Available metric categories: {available_categories}")
                
                # Check for specific performance metrics
                performance = metrics.get('performance', {})
                if 'api_latency_p95' in performance:
                    print(f"   ⚡ API P95 Latency: {performance['api_latency_p95']}ms")
                
                if 'requests_per_second' in performance:
                    print(f"   🔥 Requests/sec: {performance['requests_per_second']}")
                
                return True
            else:
                print(f"   ❌ Metrics endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Metrics endpoint error: {str(e)}")
            return False
    
    def test_business_units_endpoint(self):
        """Test the business units endpoint for API functionality"""
        print("\n🏢 Testing Business Units API...")
        try:
            response = requests.get(f"{self.base_url}/api/v1/business-units", timeout=10)
            if response.status_code == 200:
                business_units = response.json()
                print(f"   ✅ Business Units API responding")
                print(f"   📋 Found {len(business_units)} business units")
                
                # Validate business unit structure
                if business_units and isinstance(business_units, list):
                    first_unit = business_units[0]
                    required_fields = ['id', 'name', 'type']
                    available_fields = [field for field in required_fields if field in first_unit]
                    print(f"   🔍 Business unit fields: {available_fields}")
                
                return True
            else:
                print(f"   ❌ Business Units API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Business Units API error: {str(e)}")
            return False
    
    def test_error_simulation(self):
        """Test error handling and potential alerting triggers"""
        print("\n🚨 Testing Error Handling...")
        try:
            # Test 404 endpoint
            response = requests.get(f"{self.base_url}/nonexistent-endpoint", timeout=5)
            if response.status_code == 404:
                print("   ✅ 404 handling working correctly")
            else:
                print(f"   ⚠️  Unexpected response for 404 test: {response.status_code}")
            
            # Test malformed request (if applicable)
            try:
                response = requests.post(f"{self.base_url}/api/v1/business-units", 
                                       json={"invalid": "data"}, timeout=5)
                print(f"   📝 POST error handling: {response.status_code}")
            except:
                print("   📝 POST endpoint not available or protected")
            
            return True
        except Exception as e:
            print(f"   ❌ Error simulation failed: {str(e)}")
            return False
    
    def validate_response_times(self):
        """Validate response times meet performance thresholds"""
        print("\n⏱️  Validating Response Times...")
        endpoints = [
            ("/health", "Health"),
            ("/observability/metrics", "Metrics"),
            ("/api/v1/business-units", "Business Units")
        ]
        
        performance_results = []
        
        for endpoint, name in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to ms
                performance_results.append((name, response_time, response.status_code))
                
                # Check against performance thresholds
                if response_time < 100:
                    status = "🚀 Excellent"
                elif response_time < 500:
                    status = "✅ Good"
                elif response_time < 1000:
                    status = "⚠️  Acceptable"
                else:
                    status = "❌ Slow"
                
                print(f"   {status} {name}: {response_time:.2f}ms")
                
            except Exception as e:
                print(f"   ❌ {name} failed: {str(e)}")
                performance_results.append((name, float('inf'), 0))
        
        return performance_results
    
    def generate_observability_report(self):
        """Generate a comprehensive observability report"""
        print("\n" + "="*60)
        print("📋 OBSERVABILITY VALIDATION REPORT")
        print("="*60)
        
        # Test all components
        health_ok = self.test_health_endpoint()
        metrics_ok = self.test_metrics_endpoint()
        api_ok = self.test_business_units_endpoint()
        error_handling_ok = self.test_error_simulation()
        performance_results = self.validate_response_times()
        
        # Summary
        print("\n📊 SUMMARY:")
        print(f"   Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"   Metrics Endpoint: {'✅ PASS' if metrics_ok else '❌ FAIL'}")
        print(f"   API Functionality: {'✅ PASS' if api_ok else '❌ FAIL'}")
        print(f"   Error Handling: {'✅ PASS' if error_handling_ok else '❌ FAIL'}")
        
        # Performance summary
        successful_requests = [r for r in performance_results if r[2] == 200]
        if successful_requests:
            avg_response_time = sum(r[1] for r in successful_requests) / len(successful_requests)
            print(f"   Average Response Time: {avg_response_time:.2f}ms")
        
        # Overall assessment
        total_tests = 4
        passed_tests = sum([health_ok, metrics_ok, api_ok, error_handling_ok])
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n🎯 OVERALL SCORE: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 100:
            print("🎉 OBSERVABILITY STATUS: EXCELLENT")
            print("   All monitoring endpoints are functional")
            print("   Ready for production monitoring")
        elif success_rate >= 75:
            print("✅ OBSERVABILITY STATUS: GOOD")
            print("   Most monitoring capabilities are working")
            print("   Minor issues may need attention")
        elif success_rate >= 50:
            print("⚠️  OBSERVABILITY STATUS: NEEDS IMPROVEMENT")
            print("   Some monitoring capabilities are failing")
            print("   Requires investigation before production")
        else:
            print("❌ OBSERVABILITY STATUS: CRITICAL")
            print("   Major monitoring failures detected")
            print("   Not ready for production deployment")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if not health_ok:
            print("   - Fix health endpoint implementation")
        if not metrics_ok:
            print("   - Verify metrics collection and endpoint")
        if not api_ok:
            print("   - Check API functionality and database connectivity")
        if not error_handling_ok:
            print("   - Review error handling and logging")
        
        print("   - Set up Prometheus/Grafana for production monitoring")
        print("   - Configure AlertManager for critical alerts")
        print("   - Implement log aggregation with structured logging")
        print("   - Set up distributed tracing for complex requests")
        
        return success_rate

def main():
    print("🔍 NQBA Observability Validation")
    print("=" * 40)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    validator = ObservabilityValidator()
    success_rate = validator.generate_observability_report()
    
    # Exit with appropriate code
    if success_rate >= 75:
        exit(0)  # Success
    else:
        exit(1)  # Failure

if __name__ == "__main__":
    main()