#!/usr/bin/env python3
"""
Load Testing Script for NQBA Stack
Tests key endpoints with concurrent requests and performance metrics
"""

import asyncio
import aiohttp
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import json

BASE_URL = "http://localhost:8080"

# Test endpoints
ENDPOINTS = {
    "health": "/health",
    "business_units": "/api/v1/business-units",
    "metrics": "/observability/metrics",
    "openapi": "/openapi.json"
}

class LoadTester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.results = {}
    
    async def make_request(self, session, endpoint_name, url):
        """Make a single HTTP request and measure response time"""
        start_time = time.time()
        try:
            async with session.get(url) as response:
                await response.text()  # Read response body
                end_time = time.time()
                return {
                    'endpoint': endpoint_name,
                    'status_code': response.status,
                    'response_time': (end_time - start_time) * 1000,  # ms
                    'success': response.status == 200
                }
        except Exception as e:
            end_time = time.time()
            return {
                'endpoint': endpoint_name,
                'status_code': 0,
                'response_time': (end_time - start_time) * 1000,
                'success': False,
                'error': str(e)
            }
    
    async def run_concurrent_test(self, endpoint_name, url, num_requests=20, concurrency=5):
        """Run concurrent requests against an endpoint"""
        print(f"\n🚀 Testing {endpoint_name} ({url})")
        print(f"   Requests: {num_requests}, Concurrency: {concurrency}")
        
        connector = aiohttp.TCPConnector(limit=concurrency)
        async with aiohttp.ClientSession(connector=connector) as session:
            # Create semaphore to limit concurrency
            semaphore = asyncio.Semaphore(concurrency)
            
            async def bounded_request():
                async with semaphore:
                    return await self.make_request(session, endpoint_name, url)
            
            # Execute all requests
            start_time = time.time()
            tasks = [bounded_request() for _ in range(num_requests)]
            results = await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            
            # Calculate metrics
            successful_requests = [r for r in results if r['success']]
            failed_requests = [r for r in results if not r['success']]
            
            if successful_requests:
                response_times = [r['response_time'] for r in successful_requests]
                metrics = {
                    'endpoint': endpoint_name,
                    'total_requests': num_requests,
                    'successful_requests': len(successful_requests),
                    'failed_requests': len(failed_requests),
                    'success_rate': len(successful_requests) / num_requests * 100,
                    'total_time': total_time,
                    'requests_per_second': num_requests / total_time,
                    'avg_response_time': statistics.mean(response_times),
                    'min_response_time': min(response_times),
                    'max_response_time': max(response_times),
                    'p95_response_time': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 1 else response_times[0],
                    'p99_response_time': statistics.quantiles(response_times, n=100)[98] if len(response_times) > 1 else response_times[0]
                }
            else:
                metrics = {
                    'endpoint': endpoint_name,
                    'total_requests': num_requests,
                    'successful_requests': 0,
                    'failed_requests': num_requests,
                    'success_rate': 0,
                    'error': 'All requests failed'
                }
            
            self.results[endpoint_name] = metrics
            self.print_metrics(metrics)
            return metrics
    
    def print_metrics(self, metrics):
        """Print formatted metrics"""
        print(f"   ✅ Success Rate: {metrics.get('success_rate', 0):.1f}%")
        if 'avg_response_time' in metrics:
            print(f"   ⚡ Avg Response Time: {metrics['avg_response_time']:.2f}ms")
            print(f"   📊 P95 Response Time: {metrics['p95_response_time']:.2f}ms")
            print(f"   🔥 Requests/sec: {metrics['requests_per_second']:.2f}")
        if metrics.get('failed_requests', 0) > 0:
            print(f"   ❌ Failed Requests: {metrics['failed_requests']}")
    
    async def run_all_tests(self):
        """Run load tests on all endpoints"""
        print("🧪 Starting NQBA Stack Load Tests")
        print("=" * 50)
        
        for endpoint_name, path in ENDPOINTS.items():
            url = f"{self.base_url}{path}"
            await self.run_concurrent_test(
                endpoint_name, 
                url, 
                num_requests=15,  # Moderate load
                concurrency=3     # Conservative concurrency
            )
            await asyncio.sleep(1)  # Brief pause between tests
        
        self.print_summary()
    
    def print_summary(self):
        """Print overall test summary"""
        print("\n" + "=" * 50)
        print("📋 LOAD TEST SUMMARY")
        print("=" * 50)
        
        total_requests = sum(r.get('total_requests', 0) for r in self.results.values())
        total_successful = sum(r.get('successful_requests', 0) for r in self.results.values())
        overall_success_rate = (total_successful / total_requests * 100) if total_requests > 0 else 0
        
        print(f"Total Requests: {total_requests}")
        print(f"Overall Success Rate: {overall_success_rate:.1f}%")
        
        # Find fastest and slowest endpoints
        endpoints_with_times = [(name, r.get('avg_response_time', float('inf'))) 
                               for name, r in self.results.items() 
                               if 'avg_response_time' in r]
        
        if endpoints_with_times:
            fastest = min(endpoints_with_times, key=lambda x: x[1])
            slowest = max(endpoints_with_times, key=lambda x: x[1])
            print(f"Fastest Endpoint: {fastest[0]} ({fastest[1]:.2f}ms)")
            print(f"Slowest Endpoint: {slowest[0]} ({slowest[1]:.2f}ms)")
        
        # Performance assessment
        if overall_success_rate >= 95:
            print("\n🎉 PERFORMANCE: EXCELLENT")
        elif overall_success_rate >= 90:
            print("\n✅ PERFORMANCE: GOOD")
        elif overall_success_rate >= 80:
            print("\n⚠️  PERFORMANCE: ACCEPTABLE")
        else:
            print("\n❌ PERFORMANCE: NEEDS IMPROVEMENT")

async def main():
    tester = LoadTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())