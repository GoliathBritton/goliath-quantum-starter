#!/usr/bin/env python3
"""
Integration test script to verify all optimizations are working properly.
Tests the NQBA Orchestrator, Quantum Worker, and leads import functionality.
"""

import requests
import time
import json
import logging
import statistics
import os
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Service endpoints
ORCHESTRATOR_URL = "http://localhost:8004"
QUANTUM_WORKER_URL = "http://localhost:8003"
SIMPLE_API_URL = "http://localhost:8002"
NUCO_CLOUD_TIMEOUT = 10  # seconds

def test_orchestrator_performance():
    """Test the performance of the NQBA Orchestrator"""
    logger.info("Testing NQBA Orchestrator performance...")
    
    # Test response times for status endpoint
    response_times = []
    for _ in range(10):
        start_time = time.time()
        response = requests.get(f"{ORCHESTRATOR_URL}/status")
        end_time = time.time()
        
        if response.status_code == 200:
            response_times.append(end_time - start_time)
        else:
            logger.error(f"Failed to get status: {response.status_code}")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    # Calculate statistics
    avg_response_time = statistics.mean(response_times)
    max_response_time = max(response_times)
    min_response_time = min(response_times)
    
    logger.info(f"Orchestrator Status Response Times:")
    logger.info(f"  Average: {avg_response_time:.4f}s")
    logger.info(f"  Maximum: {max_response_time:.4f}s")
    logger.info(f"  Minimum: {min_response_time:.4f}s")
    
    # Check if leads count endpoint is working
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/api/leads/count")
        if response.status_code == 200:
            lead_count = response.json().get('count', 0)
            logger.info(f"Current lead count: {lead_count}")
        else:
            logger.error(f"Failed to get lead count: {response.status_code}")
    except Exception as e:
        logger.error(f"Error checking lead count: {str(e)}")
    
    return avg_response_time < 0.1  # Consider test passed if average response time is under 100ms

def test_quantum_worker():
    """Test the Quantum Worker service"""
    logger.info("Testing Quantum Worker service...")
    
    # Test job submission
    test_job = {
        "job_id": "test-job-1",
        "problem_type": "optimization",
        "parameters": {
            "objective_function": "x^2 + y^2",
            "constraints": ["x + y <= 10", "x >= 0", "y >= 0"]
        }
    }
    
    try:
        response = requests.post(
            f"{QUANTUM_WORKER_URL}/api/jobs",
            json=test_job
        )
        
        if response.status_code == 200:
            job_id = response.json().get("job_id")
            logger.info(f"Successfully submitted job: {job_id}")
            
            # Wait for job to complete
            max_attempts = 10
            for attempt in range(max_attempts):
                time.sleep(0.5)
                status_response = requests.get(f"{QUANTUM_WORKER_URL}/api/jobs/{job_id}")
                
                if status_response.status_code == 200:
                    job_status = status_response.json()
                    if job_status.get("status") in ["completed", "failed"]:
                        logger.info(f"Job completed with status: {job_status.get('status')}")
                        return job_status.get("status") == "completed"
                else:
                    logger.error(f"Failed to get job status: {status_response.status_code}")
            
            logger.error("Job did not complete in the expected time")
            return False
        else:
            logger.error(f"Failed to submit job: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error testing quantum worker: {str(e)}")
        return False

def test_concurrent_requests():
    """Test the system's ability to handle concurrent requests"""
    logger.info("Testing concurrent request handling...")
    
    def make_request(endpoint):
        try:
            start_time = time.time()
            response = requests.get(endpoint)
            end_time = time.time()
            return {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "response_time": end_time - start_time
            }
        except Exception as e:
            return {
                "endpoint": endpoint,
                "error": str(e)
            }
    
    # List of endpoints to test
    endpoints = [
        f"{ORCHESTRATOR_URL}/status",
        f"{ORCHESTRATOR_URL}/health",
        f"{ORCHESTRATOR_URL}/metrics",
        f"{QUANTUM_WORKER_URL}/api/status",
        f"{SIMPLE_API_URL}/api/status"
    ]
    
    # Make concurrent requests
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, endpoint) for endpoint in endpoints * 2]  # Test each endpoint twice
        for future in futures:
            results.append(future.result())
    
    # Analyze results
    success_count = sum(1 for r in results if r.get("status_code") == 200)
    avg_response_time = statistics.mean([r.get("response_time", 0) for r in results if "response_time" in r])
    
    logger.info(f"Concurrent requests results:")
    logger.info(f"  Total requests: {len(results)}")
    logger.info(f"  Successful requests: {success_count}")
    logger.info(f"  Average response time: {avg_response_time:.4f}s")
    
    return success_count == len(results)  # All requests should succeed

def test_nuco_cloud_integration():
    """Test nuco.cloud integration"""
    logger.info("Testing nuco.cloud integration...")
    
    # Check if nuco.cloud API key is set
    api_key = os.environ.get("NUCO_CLOUD_API_KEY")
    if not api_key:
        logger.warning("NUCO_CLOUD_API_KEY environment variable not set, using development key")
    
    # Test nuco.cloud connection via Quantum Worker
    try:
        response = requests.get(f"{QUANTUM_WORKER_URL}/api/nuco/status", timeout=NUCO_CLOUD_TIMEOUT)
        
        if response.status_code == 200:
            status_data = response.json()
            logger.info(f"nuco.cloud status: {status_data.get('status', 'unknown')}")
            
            # Check if nuco.cloud is properly integrated
            if status_data.get('status') in ['active', 'connected']:
                logger.info("nuco.cloud integration is active")
                return True
            else:
                logger.error(f"nuco.cloud integration is not active: {status_data.get('message', 'unknown error')}")
                return False
        else:
            logger.error(f"Failed to get nuco.cloud status: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error testing nuco.cloud integration: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    logger.info("Starting integration tests...")
    
    test_results = {
        "orchestrator_performance": test_orchestrator_performance(),
        "quantum_worker": test_quantum_worker(),
        "nuco_cloud_integration": test_nuco_cloud_integration(),
        "concurrent_requests": test_concurrent_requests()
    }
    
    # Print summary
    logger.info("\n=== TEST RESULTS SUMMARY ===")
    all_passed = True
    for test_name, result in test_results.items():
        status = "PASSED" if result else "FAILED"
        logger.info(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        logger.info("\n🎉 All tests passed! The optimizations are working properly.")
    else:
        logger.warning("\n⚠️ Some tests failed. Please check the logs for details.")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()