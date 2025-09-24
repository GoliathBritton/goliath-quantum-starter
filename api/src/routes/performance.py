"""Performance Monitoring API Routes

Provides endpoints for monitoring and analyzing quantum algorithm performance,
including real-time metrics, historical analysis, and optimization recommendations.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

# Import performance tracking components
from src.nqba_stack.algorithms.performance_engine import (
    performance_tracker, benchmarker, algorithm_selector,
    PerformanceMetric, AlgorithmComplexity, SelectionCriteria,
    PerformanceRecord, BenchmarkResult
)
from src.nqba_stack.algorithms.performance_config import (
    config_manager, DeploymentEnvironment, ResourceTier,
    get_current_config, validate_performance
)

router = APIRouter(prefix="/performance", tags=["performance"])


# Request/Response Models
class PerformanceMetricsResponse(BaseModel):
    """Performance metrics response model"""
    algorithm_name: str
    total_executions: int
    average_execution_time: float
    average_quality_score: float
    success_rate: float
    last_execution: Optional[datetime]
    performance_trend: str  # "improving", "stable", "degrading"
    
class AlgorithmSelectionRequest(BaseModel):
    """Algorithm selection request model"""
    problem_size: int = Field(..., ge=1, description="Size of the problem")
    complexity: str = Field(..., description="Problem complexity: low, medium, high")
    time_constraint: float = Field(..., gt=0, description="Time constraint in seconds")
    accuracy_requirement: float = Field(..., ge=0, le=1, description="Required accuracy (0-1)")
    cost_budget: float = Field(..., gt=0, description="Cost budget")
    selection_criteria: str = Field("balanced", description="Selection criteria: speed, quality, cost, reliability, balanced, performance")

class AlgorithmSelectionResponse(BaseModel):
    """Algorithm selection response model"""
    recommended_algorithm: str
    confidence_score: float
    expected_performance: Dict[str, float]
    alternative_algorithms: List[Dict[str, Any]]
    reasoning: str

class BenchmarkRequest(BaseModel):
    """Benchmark request model"""
    algorithm_names: List[str]
    test_iterations: int = Field(5, ge=1, le=20, description="Number of test iterations")
    problem_size: int = Field(10, ge=1, description="Test problem size")
    
class PerformanceConfigResponse(BaseModel):
    """Performance configuration response model"""
    environment: str
    resource_tier: str
    thresholds: Dict[str, float]
    optimization_settings: Dict[str, Any]
    
class PerformanceAlert(BaseModel):
    """Performance alert model"""
    alert_id: str
    algorithm_name: str
    metric: str
    threshold_value: float
    actual_value: float
    severity: str  # "warning", "critical"
    timestamp: datetime
    message: str


# Dependency for admin authentication (placeholder)
async def get_admin_user():
    """Admin authentication dependency"""
    # TODO: Implement proper admin authentication
    return {"user_id": "admin", "role": "admin"}


@router.get("/metrics", response_model=List[PerformanceMetricsResponse])
async def get_performance_metrics(
    algorithm_name: Optional[str] = Query(None, description="Filter by algorithm name"),
    days: int = Query(7, ge=1, le=90, description="Number of days to analyze")
):
    """Get performance metrics for algorithms"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get all tracked algorithms or filter by name
        if algorithm_name:
            algorithm_names = [algorithm_name]
        else:
            algorithm_names = performance_tracker.get_tracked_algorithms()
        
        metrics_list = []
        
        for algo_name in algorithm_names:
            history = performance_tracker.get_performance_history(
                algo_name, start_date, end_date
            )
            
            if not history:
                continue
                
            # Calculate aggregate metrics
            total_executions = len(history)
            avg_execution_time = sum(r.execution_time for r in history) / total_executions
            avg_quality_score = sum(r.quality_score for r in history) / total_executions
            success_rate = sum(1 for r in history if r.success) / total_executions
            last_execution = max(r.timestamp for r in history)
            
            # Determine performance trend
            if len(history) >= 10:
                recent_quality = sum(r.quality_score for r in history[-5:]) / 5
                older_quality = sum(r.quality_score for r in history[-10:-5]) / 5
                
                if recent_quality > older_quality * 1.05:
                    trend = "improving"
                elif recent_quality < older_quality * 0.95:
                    trend = "degrading"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            metrics_list.append(PerformanceMetricsResponse(
                algorithm_name=algo_name,
                total_executions=total_executions,
                average_execution_time=avg_execution_time,
                average_quality_score=avg_quality_score,
                success_rate=success_rate,
                last_execution=last_execution,
                performance_trend=trend
            ))
        
        return metrics_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")


@router.post("/select-algorithm", response_model=AlgorithmSelectionResponse)
async def select_optimal_algorithm(request: AlgorithmSelectionRequest):
    """Select optimal algorithm based on problem characteristics"""
    try:
        # Convert string complexity to enum
        complexity_map = {
            "low": AlgorithmComplexity.LOW,
            "medium": AlgorithmComplexity.MEDIUM,
            "high": AlgorithmComplexity.HIGH
        }
        complexity = complexity_map.get(request.complexity.lower(), AlgorithmComplexity.MEDIUM)
        
        # Convert string criteria to enum
        criteria_map = {
            "speed": SelectionCriteria.SPEED,
            "quality": SelectionCriteria.QUALITY,
            "cost": SelectionCriteria.COST,
            "reliability": SelectionCriteria.RELIABILITY,
            "balanced": SelectionCriteria.BALANCED,
            "performance": SelectionCriteria.PERFORMANCE
        }
        criteria = criteria_map.get(request.selection_criteria.lower(), SelectionCriteria.BALANCED)
        
        # Select optimal algorithm
        selected_algorithm = algorithm_selector.select_algorithm(
            problem_size=request.problem_size,
            complexity=complexity,
            time_constraint=request.time_constraint,
            accuracy_requirement=request.accuracy_requirement,
            cost_budget=request.cost_budget,
            criteria=criteria
        )
        
        # Get expected performance metrics
        expected_performance = algorithm_selector.get_expected_performance(
            selected_algorithm,
            request.problem_size,
            complexity
        )
        
        # Get alternative algorithms
        alternatives = algorithm_selector.get_alternative_algorithms(
            selected_algorithm,
            request.problem_size,
            complexity,
            top_k=3
        )
        
        # Generate reasoning
        reasoning = f"Selected {selected_algorithm.value} based on {criteria.value} criteria for problem size {request.problem_size} with {complexity.value} complexity."
        
        return AlgorithmSelectionResponse(
            recommended_algorithm=selected_algorithm.value,
            confidence_score=expected_performance.get("confidence", 0.8),
            expected_performance=expected_performance,
            alternative_algorithms=[
                {
                    "algorithm": alt.value,
                    "score": score,
                    "reason": f"Alternative with different trade-offs"
                }
                for alt, score in alternatives
            ],
            reasoning=reasoning
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Algorithm selection failed: {str(e)}")


@router.post("/benchmark")
async def run_algorithm_benchmark(
    request: BenchmarkRequest,
    admin_user = Depends(get_admin_user)
):
    """Run performance benchmark for specified algorithms"""
    try:
        # Validate algorithm names
        available_algorithms = ["quantum_portfolio_optimizer", "quantum_energy_manager", 
                              "quantum_risk_assessor", "quantum_personalization_engine"]
        
        invalid_algorithms = [name for name in request.algorithm_names if name not in available_algorithms]
        if invalid_algorithms:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid algorithm names: {invalid_algorithms}"
            )
        
        benchmark_results = {}
        
        for algo_name in request.algorithm_names:
            # Create test cases based on problem size
            test_cases = []
            for i in range(request.test_iterations):
                test_case = {
                    "size": request.problem_size,
                    "iteration": i,
                    "timestamp": datetime.now()
                }
                test_cases.append(test_case)
            
            # Run benchmark (simplified for demo)
            try:
                # This would normally run actual algorithm benchmarks
                import random
                import time
                
                execution_times = []
                quality_scores = []
                
                for _ in range(request.test_iterations):
                    start_time = time.time()
                    # Simulate algorithm execution
                    time.sleep(random.uniform(0.1, 0.5))
                    execution_time = time.time() - start_time
                    
                    execution_times.append(execution_time)
                    quality_scores.append(random.uniform(0.7, 0.95))
                
                benchmark_results[algo_name] = {
                    "average_execution_time": sum(execution_times) / len(execution_times),
                    "min_execution_time": min(execution_times),
                    "max_execution_time": max(execution_times),
                    "average_quality_score": sum(quality_scores) / len(quality_scores),
                    "min_quality_score": min(quality_scores),
                    "max_quality_score": max(quality_scores),
                    "success_rate": 1.0,
                    "iterations": request.test_iterations
                }
                
            except Exception as algo_error:
                benchmark_results[algo_name] = {
                    "error": str(algo_error),
                    "success_rate": 0.0
                }
        
        return {
            "benchmark_id": f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now(),
            "test_configuration": {
                "iterations": request.test_iterations,
                "problem_size": request.problem_size
            },
            "results": benchmark_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")


@router.get("/config", response_model=PerformanceConfigResponse)
async def get_performance_config():
    """Get current performance configuration"""
    try:
        config = get_current_config()
        
        return PerformanceConfigResponse(
            environment=config.environment.value,
            resource_tier=config.resource_tier.value,
            thresholds={
                "max_execution_time": config.thresholds.max_execution_time,
                "min_quality_score": config.thresholds.min_quality_score,
                "max_memory_usage": config.thresholds.max_memory_usage,
                "max_cpu_usage": config.thresholds.max_cpu_usage,
                "min_confidence": config.thresholds.min_confidence,
                "max_cost_per_operation": config.thresholds.max_cost_per_operation
            },
            optimization_settings={
                "enable_caching": config.optimization.enable_caching,
                "cache_ttl": config.optimization.cache_ttl,
                "enable_parallel_execution": config.optimization.enable_parallel_execution,
                "max_parallel_workers": config.optimization.max_parallel_workers,
                "enable_adaptive_selection": config.optimization.enable_adaptive_selection,
                "enable_auto_scaling": config.optimization.enable_auto_scaling
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get configuration: {str(e)}")


@router.put("/config/environment")
async def update_deployment_environment(
    environment: str,
    admin_user = Depends(get_admin_user)
):
    """Update deployment environment"""
    try:
        env_map = {
            "development": DeploymentEnvironment.DEVELOPMENT,
            "testing": DeploymentEnvironment.TESTING,
            "staging": DeploymentEnvironment.STAGING,
            "production": DeploymentEnvironment.PRODUCTION,
            "edge": DeploymentEnvironment.EDGE,
            "cloud": DeploymentEnvironment.CLOUD
        }
        
        if environment.lower() not in env_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid environment. Must be one of: {list(env_map.keys())}"
            )
        
        new_env = env_map[environment.lower()]
        config_manager.set_environment(new_env)
        
        return {
            "message": f"Environment updated to {environment}",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update environment: {str(e)}")


@router.get("/alerts")
async def get_performance_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity: warning, critical"),
    hours: int = Query(24, ge=1, le=168, description="Hours to look back")
):
    """Get performance alerts"""
    try:
        # This would normally query a real alerting system
        # For demo purposes, we'll generate some sample alerts
        
        alerts = []
        
        # Check recent performance data for threshold breaches
        algorithm_names = performance_tracker.get_tracked_algorithms()
        config = get_current_config()
        
        for algo_name in algorithm_names:
            recent_history = performance_tracker.get_performance_history(
                algo_name,
                datetime.now() - timedelta(hours=hours),
                datetime.now()
            )
            
            for record in recent_history[-10:]:  # Check last 10 executions
                # Check execution time threshold
                if record.execution_time > config.thresholds.max_execution_time:
                    alerts.append(PerformanceAlert(
                        alert_id=f"exec_time_{algo_name}_{record.timestamp.strftime('%Y%m%d_%H%M%S')}",
                        algorithm_name=algo_name,
                        metric="execution_time",
                        threshold_value=config.thresholds.max_execution_time,
                        actual_value=record.execution_time,
                        severity="warning" if record.execution_time < config.thresholds.max_execution_time * 1.5 else "critical",
                        timestamp=record.timestamp,
                        message=f"Execution time exceeded threshold: {record.execution_time:.2f}s > {config.thresholds.max_execution_time}s"
                    ))
                
                # Check quality score threshold
                if record.quality_score < config.thresholds.min_quality_score:
                    alerts.append(PerformanceAlert(
                        alert_id=f"quality_{algo_name}_{record.timestamp.strftime('%Y%m%d_%H%M%S')}",
                        algorithm_name=algo_name,
                        metric="quality_score",
                        threshold_value=config.thresholds.min_quality_score,
                        actual_value=record.quality_score,
                        severity="warning" if record.quality_score > config.thresholds.min_quality_score * 0.9 else "critical",
                        timestamp=record.timestamp,
                        message=f"Quality score below threshold: {record.quality_score:.2f} < {config.thresholds.min_quality_score}"
                    ))
        
        # Filter by severity if specified
        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity.lower()]
        
        # Sort by timestamp (most recent first)
        alerts.sort(key=lambda x: x.timestamp, reverse=True)
        
        return alerts[:50]  # Limit to 50 most recent alerts
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve alerts: {str(e)}")


@router.get("/health")
async def get_performance_health():
    """Get overall performance health status"""
    try:
        config = get_current_config()
        algorithm_names = performance_tracker.get_tracked_algorithms()
        
        health_status = {
            "overall_status": "healthy",
            "timestamp": datetime.now(),
            "environment": config.environment.value,
            "algorithms": {},
            "summary": {
                "total_algorithms": len(algorithm_names),
                "healthy_algorithms": 0,
                "warning_algorithms": 0,
                "critical_algorithms": 0
            }
        }
        
        for algo_name in algorithm_names:
            recent_history = performance_tracker.get_performance_history(
                algo_name,
                datetime.now() - timedelta(hours=1),
                datetime.now()
            )
            
            if not recent_history:
                status = "no_data"
            else:
                latest_record = recent_history[-1]
                
                # Check against thresholds
                issues = []
                if latest_record.execution_time > config.thresholds.max_execution_time:
                    issues.append("execution_time")
                if latest_record.quality_score < config.thresholds.min_quality_score:
                    issues.append("quality_score")
                
                if not issues:
                    status = "healthy"
                    health_status["summary"]["healthy_algorithms"] += 1
                elif len(issues) == 1:
                    status = "warning"
                    health_status["summary"]["warning_algorithms"] += 1
                else:
                    status = "critical"
                    health_status["summary"]["critical_algorithms"] += 1
            
            health_status["algorithms"][algo_name] = {
                "status": status,
                "last_execution": recent_history[-1].timestamp if recent_history else None,
                "recent_executions": len(recent_history)
            }
        
        # Determine overall status
        if health_status["summary"]["critical_algorithms"] > 0:
            health_status["overall_status"] = "critical"
        elif health_status["summary"]["warning_algorithms"] > 0:
            health_status["overall_status"] = "warning"
        
        return health_status
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get health status: {str(e)}")