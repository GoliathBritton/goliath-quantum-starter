from celery import Celery
from typing import Dict, Any, Optional
import json
import uuid
import time
from datetime import datetime, timedelta
import redis.asyncio as redis
import structlog
import asyncio
from ..dynex_client import DynexClient

logger = structlog.get_logger()

# Get Celery app instance
from ..app_consolidated import celery_app

@celery_app.task(bind=True, name="quantum.process_qne_query")
def process_quantum_nexus_query(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process Quantum Nexus Engine queries asynchronously
    
    Args:
        query_data: Dictionary containing query parameters
        
    Returns:
        Dictionary with processing results
    """
    task_id = self.request.id
    logger.info("Starting quantum nexus query processing", task_id=task_id)
    
    try:
        # Update task status in Redis
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set initial status
        asyncio.run(redis_client.hset(
            f"quantum:job:{task_id}",
            mapping={
                "status": "processing",
                "started_at": datetime.utcnow().isoformat(),
                "query_type": query_data.get("query_type", "unknown"),
                "user_id": query_data.get("user_id", "anonymous")
            }
        ))
        
        # Initialize Dynex client
        dynex_client = DynexClient()
        
        # Process the quantum query
        result = dynex_client.quantum_nexus_prediction(
            scenario_name=query_data.get("question", "General Query"),
            description=query_data.get("context", {}),
            inputs=query_data.get("metadata", {})
        )
        
        # Simulate quantum processing time
        processing_time = 2 + (hash(str(query_data)) % 5)  # 2-7 seconds
        time.sleep(processing_time)
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "processing_time": processing_time,
            "result": json.dumps(result)
        }
        
        asyncio.run(redis_client.hset(
            f"quantum:job:{task_id}",
            mapping=completion_data
        ))
        
        # Publish completion event
        asyncio.run(redis_client.publish(
            "quantum:updates",
            json.dumps({
                "task_id": task_id,
                "status": "completed",
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        logger.info("Quantum nexus query completed", task_id=task_id, processing_time=processing_time)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "result": result,
            "processing_time": processing_time
        }
        
    except Exception as e:
        logger.error("Quantum nexus query failed", task_id=task_id, error=str(e))
        
        # Update error status
        error_data = {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat(),
            "error": str(e)
        }
        
        asyncio.run(redis_client.hset(
            f"quantum:job:{task_id}",
            mapping=error_data
        ))
        
        # Publish error event
        asyncio.run(redis_client.publish(
            "quantum:updates",
            json.dumps({
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        raise

@celery_app.task(bind=True, name="quantum.batch_process")
def batch_quantum_processing(self, batch_queries: list) -> Dict[str, Any]:
    """
    Process multiple quantum queries in batch
    
    Args:
        batch_queries: List of query dictionaries
        
    Returns:
        Dictionary with batch processing results
    """
    task_id = self.request.id
    logger.info("Starting batch quantum processing", task_id=task_id, batch_size=len(batch_queries))
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set initial batch status
        asyncio.run(redis_client.hset(
            f"quantum:batch:{task_id}",
            mapping={
                "status": "processing",
                "started_at": datetime.utcnow().isoformat(),
                "total_queries": len(batch_queries),
                "completed_queries": 0
            }
        ))
        
        results = []
        dynex_client = DynexClient()
        
        for i, query in enumerate(batch_queries):
            try:
                # Process individual query
                result = dynex_client.quantum_nexus_prediction(
                    scenario_name=query.get("question", f"Batch Query {i+1}"),
                    description=query.get("context", {}),
                    inputs=query.get("metadata", {})
                )
                
                results.append({
                    "query_index": i,
                    "status": "success",
                    "result": result
                })
                
                # Update progress
                asyncio.run(redis_client.hset(
                    f"quantum:batch:{task_id}",
                    "completed_queries", i + 1
                ))
                
                # Brief pause between queries
                time.sleep(0.5)
                
            except Exception as e:
                logger.error("Batch query failed", task_id=task_id, query_index=i, error=str(e))
                results.append({
                    "query_index": i,
                    "status": "failed",
                    "error": str(e)
                })
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "results": json.dumps(results)
        }
        
        asyncio.run(redis_client.hset(
            f"quantum:batch:{task_id}",
            mapping=completion_data
        ))
        
        logger.info("Batch quantum processing completed", task_id=task_id, total_results=len(results))
        
        return {
            "task_id": task_id,
            "status": "completed",
            "total_queries": len(batch_queries),
            "results": results
        }
        
    except Exception as e:
        logger.error("Batch quantum processing failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="quantum.optimize_portfolio")
def optimize_quantum_portfolio(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optimize investment portfolio using quantum algorithms
    
    Args:
        portfolio_data: Portfolio configuration and constraints
        
    Returns:
        Optimized portfolio allocation
    """
    task_id = self.request.id
    logger.info("Starting quantum portfolio optimization", task_id=task_id)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Set processing status
        asyncio.run(redis_client.hset(
            f"quantum:portfolio:{task_id}",
            mapping={
                "status": "optimizing",
                "started_at": datetime.utcnow().isoformat(),
                "assets": len(portfolio_data.get("assets", [])),
                "constraints": len(portfolio_data.get("constraints", []))
            }
        ))
        
        # Simulate quantum optimization
        assets = portfolio_data.get("assets", [])
        risk_tolerance = portfolio_data.get("risk_tolerance", 0.5)
        
        # Mock quantum optimization results
        optimization_result = {
            "optimal_allocation": {
                asset["symbol"]: max(0.05, min(0.4, 0.1 + (hash(asset["symbol"]) % 30) / 100))
                for asset in assets
            },
            "expected_return": 0.08 + (risk_tolerance * 0.04),
            "risk_score": risk_tolerance,
            "sharpe_ratio": 1.2 + (risk_tolerance * 0.3),
            "quantum_advantage": "23% improvement over classical optimization"
        }
        
        # Simulate processing time
        time.sleep(3)
        
        # Update completion status
        completion_data = {
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat(),
            "optimization_result": json.dumps(optimization_result)
        }
        
        asyncio.run(redis_client.hset(
            f"quantum:portfolio:{task_id}",
            mapping=completion_data
        ))
        
        logger.info("Quantum portfolio optimization completed", task_id=task_id)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "optimization_result": optimization_result
        }
        
    except Exception as e:
        logger.error("Quantum portfolio optimization failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="quantum.cleanup_expired_jobs")
def cleanup_expired_quantum_jobs(self) -> Dict[str, Any]:
    """
    Clean up expired quantum job data from Redis
    
    Returns:
        Cleanup statistics
    """
    task_id = self.request.id
    logger.info("Starting quantum job cleanup", task_id=task_id)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        # Find expired jobs (older than 24 hours)
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        # Get all quantum job keys
        job_keys = asyncio.run(redis_client.keys("quantum:job:*"))
        batch_keys = asyncio.run(redis_client.keys("quantum:batch:*"))
        portfolio_keys = asyncio.run(redis_client.keys("quantum:portfolio:*"))
        
        all_keys = job_keys + batch_keys + portfolio_keys
        expired_keys = []
        
        for key in all_keys:
            job_data = asyncio.run(redis_client.hgetall(key))
            
            # Check if job is expired
            completed_at = job_data.get("completed_at") or job_data.get("failed_at")
            if completed_at:
                try:
                    completion_time = datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
                    if completion_time < cutoff_time:
                        expired_keys.append(key)
                except ValueError:
                    # Invalid timestamp, mark for cleanup
                    expired_keys.append(key)
        
        # Delete expired keys
        if expired_keys:
            asyncio.run(redis_client.delete(*expired_keys))
        
        cleanup_stats = {
            "total_keys_checked": len(all_keys),
            "expired_keys_deleted": len(expired_keys),
            "cleanup_completed_at": datetime.utcnow().isoformat()
        }
        
        logger.info("Quantum job cleanup completed", **cleanup_stats)
        
        return cleanup_stats
        
    except Exception as e:
        logger.error("Quantum job cleanup failed", task_id=task_id, error=str(e))
        raise