"""Tests for the performance tracking and optimization engine."""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.nqba_stack.algorithms.performance_engine import (
    PerformanceTracker,
    AlgorithmBenchmarker,
    DynamicAlgorithmSelector,
    PerformanceMetrics,
    ResourceUsage,
    OptimizationCriteria,
    track_performance,
    performance_engine
)
from src.nqba_stack.algorithms.quantum_enhanced_algorithms import (
    AlgorithmType,
    AlgorithmResult,
    QuantumAlgorithmFactory
)


class TestPerformanceTracker:
    """Test cases for PerformanceTracker."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tracker = PerformanceTracker()
    
    def test_record_performance(self):
        """Test recording performance metrics."""
        metrics = PerformanceMetrics(
            execution_time=1.5,
            memory_usage=512.0,
            cpu_utilization=75.0,
            quantum_gate_count=100,
            circuit_depth=20,
            fidelity=0.95,
            success_rate=0.98
        )
        
        self.tracker.record_performance(
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            metrics=metrics,
            context={"problem_size": 10}
        )
        
        history = self.tracker.get_performance_history(AlgorithmType.PORTFOLIO_OPTIMIZATION)
        assert len(history) == 1
        assert history[0].metrics.execution_time == 1.5
        assert history[0].context["problem_size"] == 10
    
    def test_get_average_metrics(self):
        """Test calculating average performance metrics."""
        # Record multiple performance entries
        for i in range(3):
            metrics = PerformanceMetrics(
                execution_time=1.0 + i * 0.5,
                memory_usage=500.0 + i * 100,
                cpu_utilization=70.0 + i * 5,
                quantum_gate_count=100 + i * 10,
                circuit_depth=20 + i * 2,
                fidelity=0.95 - i * 0.01,
                success_rate=0.98 - i * 0.01
            )
            self.tracker.record_performance(
                algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
                metrics=metrics
            )
        
        avg_metrics = self.tracker.get_average_metrics(
            AlgorithmType.PORTFOLIO_OPTIMIZATION,
            time_window=timedelta(hours=1)
        )
        
        assert avg_metrics is not None
        assert abs(avg_metrics.execution_time - 2.0) < 0.01  # Average of 1.0, 1.5, 2.0
        assert abs(avg_metrics.memory_usage - 600.0) < 0.01  # Average of 500, 600, 700
    
    def test_get_performance_trends(self):
        """Test performance trend analysis."""
        # Record performance with improving trend
        for i in range(5):
            metrics = PerformanceMetrics(
                execution_time=2.0 - i * 0.2,  # Decreasing (improving)
                memory_usage=1000.0 - i * 50,  # Decreasing (improving)
                cpu_utilization=80.0 - i * 2,  # Decreasing (improving)
                quantum_gate_count=200 - i * 10,
                circuit_depth=40 - i * 2,
                fidelity=0.90 + i * 0.01,  # Increasing (improving)
                success_rate=0.95 + i * 0.005  # Increasing (improving)
            )
            self.tracker.record_performance(
                algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
                metrics=metrics
            )
        
        trends = self.tracker.get_performance_trends(
            AlgorithmType.PORTFOLIO_OPTIMIZATION,
            time_window=timedelta(hours=1)
        )
        
        assert trends is not None
        assert trends["execution_time"] < 0  # Negative trend (improving)
        assert trends["fidelity"] > 0  # Positive trend (improving)


class TestAlgorithmBenchmarker:
    """Test cases for AlgorithmBenchmarker."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.benchmarker = AlgorithmBenchmarker()
    
    @pytest.mark.asyncio
    async def test_benchmark_algorithm(self):
        """Test benchmarking a single algorithm."""
        # Mock algorithm function
        async def mock_algorithm(**kwargs):
            await asyncio.sleep(0.1)  # Simulate processing time
            return AlgorithmResult(
                algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
                result={"optimal_weights": [0.3, 0.4, 0.3]},
                metadata={"iterations": 100}
            )
        
        benchmark_result = await self.benchmarker.benchmark_algorithm(
            algorithm_func=mock_algorithm,
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            test_cases=[{"returns": [[0.1, 0.05, 0.08]]}],
            iterations=3
        )
        
        assert benchmark_result.algorithm_type == AlgorithmType.PORTFOLIO_OPTIMIZATION
        assert benchmark_result.iterations == 3
        assert benchmark_result.average_execution_time > 0
        assert len(benchmark_result.individual_results) == 3
    
    @pytest.mark.asyncio
    async def test_compare_algorithms(self):
        """Test comparing multiple algorithms."""
        # Mock algorithm functions
        async def fast_algorithm(**kwargs):
            await asyncio.sleep(0.05)
            return AlgorithmResult(
                algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
                result={"optimal_weights": [0.3, 0.4, 0.3]},
                metadata={"method": "fast"}
            )
        
        async def slow_algorithm(**kwargs):
            await asyncio.sleep(0.15)
            return AlgorithmResult(
                algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
                result={"optimal_weights": [0.35, 0.35, 0.3]},
                metadata={"method": "slow"}
            )
        
        algorithms = {
            "fast": fast_algorithm,
            "slow": slow_algorithm
        }
        
        comparison = await self.benchmarker.compare_algorithms(
            algorithms=algorithms,
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            test_cases=[{"returns": [[0.1, 0.05, 0.08]]}],
            iterations=2
        )
        
        assert len(comparison.results) == 2
        assert "fast" in comparison.results
        assert "slow" in comparison.results
        assert comparison.results["fast"].average_execution_time < comparison.results["slow"].average_execution_time


class TestDynamicAlgorithmSelector:
    """Test cases for DynamicAlgorithmSelector."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.selector = DynamicAlgorithmSelector()
        
        # Mock performance tracker with some data
        self.mock_tracker = Mock()
        self.selector.performance_tracker = self.mock_tracker
    
    def test_select_optimal_algorithm_performance_based(self):
        """Test selecting algorithm based on performance criteria."""
        # Mock performance data
        self.mock_tracker.get_average_metrics.return_value = PerformanceMetrics(
            execution_time=1.5,
            memory_usage=512.0,
            cpu_utilization=75.0,
            quantum_gate_count=100,
            circuit_depth=20,
            fidelity=0.95,
            success_rate=0.98
        )
        
        criteria = OptimizationCriteria.SPEED
        context = {"problem_size": 10, "time_limit": 5.0}
        
        selected = self.selector.select_optimal_algorithm(
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            criteria=criteria,
            context=context
        )
        
        assert selected is not None
        assert "algorithm_variant" in selected
        assert "confidence_score" in selected
        assert "reasoning" in selected
    
    def test_select_optimal_algorithm_no_history(self):
        """Test selecting algorithm when no performance history exists."""
        # Mock no performance data
        self.mock_tracker.get_average_metrics.return_value = None
        
        criteria = OptimizationCriteria.ACCURACY
        context = {"problem_size": 5}
        
        selected = self.selector.select_optimal_algorithm(
            algorithm_type=AlgorithmType.ENERGY_MANAGEMENT,
            criteria=criteria,
            context=context
        )
        
        assert selected is not None
        assert selected["algorithm_variant"] == "standard"  # Default fallback
        assert selected["confidence_score"] < 0.5  # Low confidence without data


class TestPerformanceDecorator:
    """Test cases for the performance tracking decorator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Clear any existing performance data
        performance_engine.performance_tracker._performance_history.clear()
    
    @pytest.mark.asyncio
    async def test_track_performance_decorator(self):
        """Test the performance tracking decorator."""
        @track_performance
        async def sample_algorithm(problem_size: int = 10):
            """Sample algorithm for testing."""
            await asyncio.sleep(0.1)  # Simulate processing
            return AlgorithmResult(
                algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
                result={"optimal_weights": [0.3, 0.4, 0.3]},
                metadata={"problem_size": problem_size}
            )
        
        result = await sample_algorithm(problem_size=15)
        
        # Check that result includes performance metadata
        assert hasattr(result, 'performance_metrics')
        assert result.performance_metrics is not None
        assert result.performance_metrics.execution_time > 0
        
        # Check that performance was recorded
        history = performance_engine.performance_tracker.get_performance_history(
            AlgorithmType.PORTFOLIO_OPTIMIZATION
        )
        assert len(history) == 1
        assert history[0].context["problem_size"] == 15
    
    def test_track_performance_decorator_sync(self):
        """Test the performance tracking decorator with synchronous function."""
        @track_performance
        def sync_algorithm(iterations: int = 100):
            """Synchronous algorithm for testing."""
            import time
            time.sleep(0.05)  # Simulate processing
            return AlgorithmResult(
                algorithm_type=AlgorithmType.RISK_ASSESSMENT,
                result={"risk_score": 0.75},
                metadata={"iterations": iterations}
            )
        
        result = sync_algorithm(iterations=200)
        
        # Check that result includes performance metadata
        assert hasattr(result, 'performance_metrics')
        assert result.performance_metrics is not None
        assert result.performance_metrics.execution_time > 0
        
        # Check that performance was recorded
        history = performance_engine.performance_tracker.get_performance_history(
            AlgorithmType.RISK_ASSESSMENT
        )
        assert len(history) == 1
        assert history[0].context["iterations"] == 200


class TestIntegration:
    """Integration tests for the complete performance system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Clear any existing performance data
        performance_engine.performance_tracker._performance_history.clear()
    
    @pytest.mark.asyncio
    async def test_end_to_end_performance_tracking(self):
        """Test complete end-to-end performance tracking workflow."""
        # Create a factory instance
        factory = QuantumAlgorithmFactory()
        
        # Test data
        returns_data = [[0.1, 0.05, 0.08], [0.02, 0.15, 0.03], [0.08, 0.01, 0.12]]
        risk_tolerance = 0.5
        
        # Run algorithm with performance tracking
        algorithm = factory.create_algorithm(AlgorithmType.PORTFOLIO_OPTIMIZATION)
        result = await algorithm.optimize_portfolio(
            returns_data=returns_data,
            risk_tolerance=risk_tolerance
        )
        
        # Verify performance tracking
        assert hasattr(result, 'performance_metrics')
        assert result.performance_metrics.execution_time > 0
        
        # Verify performance history
        history = performance_engine.performance_tracker.get_performance_history(
            AlgorithmType.PORTFOLIO_OPTIMIZATION
        )
        assert len(history) >= 1
        
        # Test dynamic selection
        selector = DynamicAlgorithmSelector()
        optimal_config = selector.select_optimal_algorithm(
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            criteria=OptimizationCriteria.SPEED,
            context={"problem_size": len(returns_data)}
        )
        
        assert optimal_config is not None
        assert "algorithm_variant" in optimal_config
        assert "confidence_score" in optimal_config
    
    @pytest.mark.asyncio
    async def test_benchmarking_integration(self):
        """Test integration with benchmarking system."""
        factory = QuantumAlgorithmFactory()
        
        # Benchmark portfolio optimization
        benchmark_results = await factory.benchmark_algorithms(
            algorithm_type=AlgorithmType.PORTFOLIO_OPTIMIZATION,
            test_cases=[
                {"returns_data": [[0.1, 0.05]], "risk_tolerance": 0.3},
                {"returns_data": [[0.08, 0.12]], "risk_tolerance": 0.7}
            ],
            iterations=2
        )
        
        assert benchmark_results is not None
        assert len(benchmark_results.results) > 0
        
        # Verify that benchmarking recorded performance data
        history = performance_engine.performance_tracker.get_performance_history(
            AlgorithmType.PORTFOLIO_OPTIMIZATION
        )
        assert len(history) >= 2  # At least 2 iterations


if __name__ == "__main__":
    pytest.main([__file__, "-v"])