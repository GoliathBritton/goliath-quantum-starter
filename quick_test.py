#!/usr/bin/env python3
"""
Quick test script to verify platform functionality
"""
import requests
import json
import time

def test_services():
    """Test if all services are running and responding"""
    print("Testing platform services...")
    # Force flush output
    import sys
    sys.stdout.flush()
    
    # Test orchestrator
    try:
        response = requests.get("http://localhost:8004/status", timeout=5)
        print(f"Orchestrator status: {'OK' if response.status_code == 200 else 'FAILED'}")
        print(f"Response: {response.text[:100]}...")
    except Exception as e:
        print(f"Orchestrator error: {str(e)}")
    
    # Test quantum worker
    try:
        response = requests.get("http://localhost:8003/status", timeout=5)
        print(f"Quantum Worker status: {'OK' if response.status_code == 200 else 'FAILED'}")
        print(f"Response: {response.text[:100]}...")
    except Exception as e:
        print(f"Quantum Worker error: {str(e)}")
    
    # Test job submission
    try:
        job_data = {
            "job_id": f"test-job-{int(time.time())}",
            "problem_type": "optimization",
            "data": {"test": "data"}
        }
        response = requests.post(
            "http://localhost:8003/api/jobs", 
            json=job_data,
            timeout=5
        )
        print(f"Job submission: {'OK' if response.status_code in [200, 201, 202] else 'FAILED'}")
        print(f"Response: {response.text[:100]}...")
    except Exception as e:
        print(f"Job submission error: {str(e)}")

if __name__ == "__main__":
    test_services()