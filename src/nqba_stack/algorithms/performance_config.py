"""Performance Optimization Configuration

This module provides configuration settings and utilities for optimizing
quantum algorithm performance across different deployment scenarios.
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

from .performance_engine import (
    PerformanceMetric, AlgorithmComplexity, SelectionCriteria
)


class DeploymentEnvironment(Enum):
    """Deployment environment types"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    EDGE = "edge"
    CLOUD = "cloud"


class ResourceTier(Enum):
    """Resource availability tiers"""
    MINIMAL = "minimal"      # Limited resources (edge devices)
    STANDARD = "standard"    # Standard cloud instances
    ENHANCED = "enhanced"    # High-performance instances
    PREMIUM = "premium"      # Maximum resources available


@dataclass
class PerformanceThresholds:
    """Performance threshold configuration"""
    max_execution_time: float = 30.0  # seconds
    min_quality_score: float = 0.8
    max_memory_usage: float = 1024.0  # MB
    max_cpu_usage: float = 80.0  # percentage
    min_confidence: float = 0.85
    max_cost_per_operation: float = 1.0  # arbitrary units
    
    # Quantum-specific thresholds
    min_quantum_advantage: float = 1.1
    max_quantum_operations: int = 10000
    

@dataclass
class OptimizationSettings:
    """Algorithm optimization settings"""
    enable_caching: bool = True
    cache_ttl: int = 3600  # seconds
    enable_parallel_execution: bool = True
    max_parallel_workers: int = 4
    enable_adaptive_selection: bool = True
    performance_history_limit: int = 1000
    
    # Auto-scaling settings
    enable_auto_scaling: bool = False
    scale_up_threshold: float = 0.8  # CPU usage
    scale_down_threshold: float = 0.3
    min_instances: int = 1
    max_instances: int = 10
    
    # Fallback settings
    enable_classical_fallback: bool = True
    fallback_threshold: float = 5.0  # seconds
    

@dataclass
class EnvironmentConfig:
    """Environment-specific configuration"""
    environment: DeploymentEnvironment
    resource_tier: ResourceTier
    thresholds: PerformanceThresholds
    optimization: OptimizationSettings
    
    # Algorithm selection preferences
    preferred_algorithms: List[str] = field(default_factory=list)
    disabled_algorithms: List[str] = field(default_factory=list)
    
    # Monitoring settings
    enable_detailed_metrics: bool = True
    metrics_retention_days: int = 30
    alert_on_threshold_breach: bool = True
    

class PerformanceConfigManager:
    """Manages performance configuration across environments"""
    
    def __init__(self):
        self._configs: Dict[DeploymentEnvironment, EnvironmentConfig] = {}
        self._current_environment = DeploymentEnvironment.DEVELOPMENT
        self._initialize_default_configs()
    
    def _initialize_default_configs(self):
        """Initialize default configurations for all environments"""
        
        # Development environment - relaxed thresholds for testing
        dev_thresholds = PerformanceThresholds(
            max_execution_time=60.0,
            min_quality_score=0.7,
            max_memory_usage=2048.0,
            max_cpu_usage=90.0,
            min_confidence=0.8,
            max_cost_per_operation=5.0
        )
        
        dev_optimization = OptimizationSettings(
            enable_caching=True,
            enable_parallel_execution=False,  # Easier debugging
            enable_adaptive_selection=True,
            enable_auto_scaling=False,
            enable_classical_fallback=True,
            fallback_threshold=10.0
        )
        
        self._configs[DeploymentEnvironment.DEVELOPMENT] = EnvironmentConfig(
            environment=DeploymentEnvironment.DEVELOPMENT,
            resource_tier=ResourceTier.STANDARD,
            thresholds=dev_thresholds,
            optimization=dev_optimization,
            enable_detailed_metrics=True,
            metrics_retention_days=7
        )
        
        # Production environment - strict thresholds for reliability
        prod_thresholds = PerformanceThresholds(
            max_execution_time=15.0,
            min_quality_score=0.9,
            max_memory_usage=512.0,
            max_cpu_usage=70.0,
            min_confidence=0.9,
            max_cost_per_operation=0.5
        )
        
        prod_optimization = OptimizationSettings(
            enable_caching=True,
            cache_ttl=7200,
            enable_parallel_execution=True,
            max_parallel_workers=8,
            enable_adaptive_selection=True,
            enable_auto_scaling=True,
            scale_up_threshold=0.7,
            scale_down_threshold=0.2,
            max_instances=20,
            enable_classical_fallback=True,
            fallback_threshold=3.0
        )
        
        self._configs[DeploymentEnvironment.PRODUCTION] = EnvironmentConfig(
            environment=DeploymentEnvironment.PRODUCTION,
            resource_tier=ResourceTier.ENHANCED,
            thresholds=prod_thresholds,
            optimization=prod_optimization,
            enable_detailed_metrics=False,  # Reduce overhead
            metrics_retention_days=90,
            alert_on_threshold_breach=True
        )
        
        # Edge environment - minimal resource usage
        edge_thresholds = PerformanceThresholds(
            max_execution_time=5.0,
            min_quality_score=0.75,
            max_memory_usage=128.0,
            max_cpu_usage=60.0,
            min_confidence=0.8,
            max_cost_per_operation=0.1,
            max_quantum_operations=1000
        )
        
        edge_optimization = OptimizationSettings(
            enable_caching=True,
            cache_ttl=1800,
            enable_parallel_execution=False,
            enable_adaptive_selection=True,
            enable_auto_scaling=False,
            enable_classical_fallback=True,
            fallback_threshold=2.0
        )
        
        self._configs[DeploymentEnvironment.EDGE] = EnvironmentConfig(
            environment=DeploymentEnvironment.EDGE,
            resource_tier=ResourceTier.MINIMAL,
            thresholds=edge_thresholds,
            optimization=edge_optimization,
            disabled_algorithms=["quantum_portfolio_optimizer"],  # Too resource intensive
            enable_detailed_metrics=False,
            metrics_retention_days=3
        )
    
    def get_config(self, environment: DeploymentEnvironment = None) -> EnvironmentConfig:
        """Get configuration for specified environment"""
        env = environment or self._current_environment
        return self._configs.get(env, self._configs[DeploymentEnvironment.DEVELOPMENT])
    
    def set_environment(self, environment: DeploymentEnvironment):
        """Set current deployment environment"""
        self._current_environment = environment
    
    def update_config(self, environment: DeploymentEnvironment, **kwargs):
        """Update configuration for specific environment"""
        if environment in self._configs:
            config = self._configs[environment]
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
    
    def get_selection_criteria_for_environment(self, environment: DeploymentEnvironment = None) -> SelectionCriteria:
        """Get optimal selection criteria for environment"""
        env = environment or self._current_environment
        
        if env == DeploymentEnvironment.PRODUCTION:
            return SelectionCriteria.RELIABILITY
        elif env == DeploymentEnvironment.EDGE:
            return SelectionCriteria.SPEED
        elif env in [DeploymentEnvironment.DEVELOPMENT, DeploymentEnvironment.TESTING]:
            return SelectionCriteria.BALANCED
        else:
            return SelectionCriteria.PERFORMANCE
    
    def validate_performance_against_thresholds(
        self, 
        metrics: Dict[PerformanceMetric, float],
        resource_usage: Dict[str, float],
        environment: DeploymentEnvironment = None
    ) -> Dict[str, bool]:
        """Validate performance metrics against environment thresholds"""
        config = self.get_config(environment)
        thresholds = config.thresholds
        
        validation_results = {
            "execution_time_ok": metrics.get(PerformanceMetric.EXECUTION_TIME, 0) <= thresholds.max_execution_time,
            "quality_ok": metrics.get(PerformanceMetric.SOLUTION_QUALITY, 0) >= thresholds.min_quality_score,
            "confidence_ok": metrics.get(PerformanceMetric.CONFIDENCE, 0) >= thresholds.min_confidence,
            "memory_ok": resource_usage.get("memory_mb", 0) <= thresholds.max_memory_usage,
            "cpu_ok": resource_usage.get("cpu_percent", 0) <= thresholds.max_cpu_usage,
            "quantum_advantage_ok": metrics.get(PerformanceMetric.QUANTUM_ADVANTAGE, 1.0) >= thresholds.min_quantum_advantage
        }
        
        validation_results["overall_ok"] = all(validation_results.values())
        return validation_results
    
    def get_recommended_algorithm_config(
        self, 
        problem_size: int,
        complexity: AlgorithmComplexity,
        environment: DeploymentEnvironment = None
    ) -> Dict[str, Any]:
        """Get recommended algorithm configuration for problem and environment"""
        config = self.get_config(environment)
        
        # Base configuration
        algo_config = {
            "enable_caching": config.optimization.enable_caching,
            "parallel_execution": config.optimization.enable_parallel_execution,
            "max_workers": min(config.optimization.max_parallel_workers, problem_size // 10 + 1),
            "timeout": config.thresholds.max_execution_time,
            "quality_threshold": config.thresholds.min_quality_score
        }
        
        # Adjust based on complexity and environment
        if complexity == AlgorithmComplexity.HIGH and config.resource_tier == ResourceTier.MINIMAL:
            algo_config["enable_approximation"] = True
            algo_config["approximation_factor"] = 0.9
        
        if config.environment == DeploymentEnvironment.EDGE:
            algo_config["quantum_operations_limit"] = config.thresholds.max_quantum_operations
            algo_config["memory_limit"] = config.thresholds.max_memory_usage
        
        return algo_config


# Global configuration manager instance
config_manager = PerformanceConfigManager()

# Environment detection from environment variables
if os.getenv("DEPLOYMENT_ENV"):
    env_name = os.getenv("DEPLOYMENT_ENV").upper()
    try:
        detected_env = DeploymentEnvironment(env_name.lower())
        config_manager.set_environment(detected_env)
    except ValueError:
        pass  # Use default development environment


def get_current_config() -> EnvironmentConfig:
    """Get current environment configuration"""
    return config_manager.get_config()


def set_deployment_environment(environment: DeploymentEnvironment):
    """Set deployment environment"""
    config_manager.set_environment(environment)


def validate_performance(metrics: Dict[PerformanceMetric, float], resource_usage: Dict[str, float]) -> bool:
    """Validate performance against current environment thresholds"""
    results = config_manager.validate_performance_against_thresholds(metrics, resource_usage)
    return results["overall_ok"]