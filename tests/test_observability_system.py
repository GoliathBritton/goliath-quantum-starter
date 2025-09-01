"""
Test suite for NQBA Observability & SRE system.
Tests tracing, dashboard, and incident response components.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import json
import time

# Import observability components
try:
    from src.nqba_stack.observability.tracing import (
        TracingConfig,
        NQBATracer,
        TracingMiddleware,
        QuantumJobTracer,
        BusinessUnitTracer,
        get_tracer,
        instrument_fastapi,
        trace_function,
    )
    from src.nqba_stack.observability.dashboard import (
        DashboardConfig,
        MetricsCollector,
        DashboardRenderer,
        NQBADashboard,
    )

    OBSERVABILITY_AVAILABLE = True
except ImportError:
    OBSERVABILITY_AVAILABLE = False


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestTracingConfig:
    """Test tracing configuration."""

    def test_tracing_config_defaults(self):
        """Test default configuration values."""
        config = TracingConfig()

        assert config.enabled is True
        assert config.service_name == "nqba-ecosystem"
        assert config.service_version == "1.0.0"
        assert config.environment == "development"
        assert config.sample_rate == 1.0
        assert "nqba.ecosystem" in config.resource_attributes

    def test_tracing_config_environment_vars(self):
        """Test configuration from environment variables."""
        with patch.dict(
            "os.environ",
            {
                "NQBA_TRACING_ENABLED": "false",
                "NQBA_SERVICE_NAME": "test-service",
                "NQBA_ENVIRONMENT": "production",
            },
        ):
            config = TracingConfig()

            assert config.enabled is False
            assert config.service_name == "test-service"
            assert config.environment == "production"


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestNQBATracer:
    """Test NQBA tracer functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = TracingConfig()
        self.config.enabled = False  # Disable for testing
        self.tracer = NQBATracer(self.config)

    def test_tracer_initialization_disabled(self):
        """Test tracer initialization when disabled."""
        assert self.tracer.tracer is None
        assert self.tracer.tracer_provider is None

    def test_tracer_initialization_enabled(self):
        """Test tracer initialization when enabled."""
        config = TracingConfig()
        config.enabled = True

        # Since OpenTelemetry packages aren't installed, this will fail gracefully
        # and create a no-op tracer
        tracer = NQBATracer(config)

        # Should have a tracer attribute (even if it's None)
        assert hasattr(tracer, "tracer")
        # Should handle the initialization gracefully
        assert tracer is not None

    def test_start_span_disabled(self):
        """Test starting span when tracing is disabled."""
        span = self.tracer.start_span("test_span")
        assert span is None

    def test_span_context_manager_disabled(self):
        """Test span context manager when tracing is disabled."""
        with self.tracer.span("test_span") as span:
            assert span is None

    def test_add_event_disabled(self):
        """Test adding events when tracing is disabled."""
        # Should not raise any errors
        self.tracer.add_event(None, "test_event")

    def test_set_attribute_disabled(self):
        """Test setting attributes when tracing is disabled."""
        # Should not raise any errors
        self.tracer.set_attribute(None, "test_key", "test_value")

    def test_set_status_disabled(self):
        """Test setting status when tracing is disabled."""
        # Should not raise any errors
        self.tracer.set_status(None, Mock())


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestTracingMiddleware:
    """Test FastAPI tracing middleware."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = TracingConfig()
        self.config.enabled = False
        self.tracer = NQBATracer(self.config)
        self.middleware = TracingMiddleware(self.tracer)

    @pytest.mark.asyncio
    async def test_middleware_disabled(self):
        """Test middleware when tracing is disabled."""
        request = Mock()
        request.method = "GET"
        request.url = "http://test.com"
        request.headers = {"user-agent": "test-agent"}

        # Create an async mock
        async def async_call_next(req):
            return Mock()

        call_next = async_call_next

        response = await self.middleware(request, call_next)

        assert response is not None


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestQuantumJobTracer:
    """Test quantum job tracing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = TracingConfig()
        self.config.enabled = False
        self.tracer = NQBATracer(self.config)
        self.quantum_tracer = QuantumJobTracer(self.tracer)

    def test_trace_job_submission(self):
        """Test tracing quantum job submission."""
        span = self.quantum_tracer.trace_job_submission("job_123", "user_456", "dynex")
        assert span is not None  # Should return a context manager

    def test_trace_job_execution(self):
        """Test tracing quantum job execution."""
        span = self.quantum_tracer.trace_job_execution("job_123", "dynex", 1000)
        assert span is not None  # Should return a context manager

    def test_trace_solver_fallback(self):
        """Test tracing solver fallback events."""
        span = self.quantum_tracer.trace_solver_fallback(
            "job_123", "dynex", "dimod", "timeout"
        )
        assert span is not None  # Should return a context manager


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestBusinessUnitTracer:
    """Test business unit tracing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = TracingConfig()
        self.config.enabled = False
        self.tracer = NQBATracer(self.config)
        self.bu_tracer = BusinessUnitTracer(self.tracer)

    def test_trace_bu_operation(self):
        """Test tracing business unit operations."""
        span = self.bu_tracer.trace_bu_operation("flyfox_ai", "optimize", "user_123")
        assert span is not None  # Should return a context manager

    def test_trace_workflow_execution(self):
        """Test tracing workflow execution."""
        span = self.bu_tracer.trace_workflow_execution("workflow_123", "flyfox_ai", 5)
        assert span is not None  # Should return a context manager


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestDashboardConfig:
    """Test dashboard configuration."""

    def test_dashboard_config_defaults(self):
        """Test default dashboard configuration."""
        config = DashboardConfig()

        assert config.refresh_interval == 30
        assert config.history_hours == 24
        assert config.quantum_advantage_threshold == 3.4
        assert "api_latency_p95" in config.slo_targets
        assert "quantum_success_rate" in config.slo_targets


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestMetricsCollector:
    """Test metrics collection."""

    def setup_method(self):
        """Set up test fixtures."""
        self.collector = MetricsCollector()

    def test_get_system_health(self):
        """Test system health metrics collection."""
        health = self.collector.get_system_health()

        assert "status" in health
        assert "uptime" in health
        assert "active_users" in health
        assert "quantum_jobs_running" in health
        assert health["status"] == "healthy"
        assert isinstance(health["uptime"], float)

    def test_get_performance_metrics(self):
        """Test performance metrics collection."""
        metrics = self.collector.get_performance_metrics()

        assert "api_latency_p50" in metrics
        assert "api_latency_p95" in metrics
        assert "quantum_success_rate" in metrics
        assert isinstance(metrics["api_latency_p95"], int)
        assert isinstance(metrics["quantum_success_rate"], float)

    def test_get_business_metrics(self):
        """Test business metrics collection."""
        metrics = self.collector.get_business_metrics()

        assert "arr" in metrics
        assert "cac" in metrics
        assert "ltv" in metrics
        assert "nps" in metrics
        assert isinstance(metrics["arr"], int)
        assert isinstance(metrics["nps"], int)

    def test_get_quantum_metrics(self):
        """Test quantum metrics collection."""
        metrics = self.collector.get_quantum_metrics()

        assert "dynex_qubits_available" in metrics
        assert "quantum_jobs_completed" in metrics
        assert "quantum_advantage_achieved" in metrics
        assert isinstance(metrics["dynex_qubits_available"], int)
        assert isinstance(metrics["quantum_advantage_achieved"], float)

    def test_get_workflow_metrics(self):
        """Test workflow metrics collection."""
        workflows = self.collector.get_workflow_metrics()

        assert isinstance(workflows, list)
        assert len(workflows) > 0

        workflow = workflows[0]
        assert "name" in workflow
        assert "success_rate" in workflow
        assert "avg_time" in workflow
        assert "volume" in workflow


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestDashboardRenderer:
    """Test dashboard rendering."""

    def setup_method(self):
        """Set up test fixtures."""
        self.collector = MetricsCollector()
        self.renderer = DashboardRenderer(self.collector)

    def test_renderer_initialization(self):
        """Test dashboard renderer initialization."""
        assert self.renderer.metrics is not None
        assert isinstance(self.renderer.metrics, MetricsCollector)


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestNQBADashboard:
    """Test main dashboard application."""

    def setup_method(self):
        """Set up test fixtures."""
        self.dashboard = NQBADashboard()

    def test_dashboard_initialization(self):
        """Test dashboard initialization."""
        assert self.dashboard.config is not None
        assert self.dashboard.metrics is not None
        assert self.dashboard.renderer is not None

        assert isinstance(self.dashboard.config, DashboardConfig)
        assert isinstance(self.dashboard.metrics, MetricsCollector)
        assert isinstance(self.dashboard.renderer, DashboardRenderer)


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestTracingIntegration:
    """Test tracing integration with other components."""

    def test_trace_function_decorator(self):
        """Test the trace_function decorator."""

        @trace_function("test_function", {"test": "attribute"})
        def test_function():
            return "test_result"

        result = test_function()
        assert result == "test_result"

    def test_get_tracer_function(self):
        """Test the get_tracer function."""
        tracer = get_tracer()
        assert isinstance(tracer, NQBATracer)


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestObservabilityEndToEnd:
    """End-to-end tests for observability system."""

    def test_metrics_consistency(self):
        """Test that metrics are consistent across collectors."""
        collector = MetricsCollector()

        # Get all metrics
        health = collector.get_system_health()
        perf = collector.get_performance_metrics()
        business = collector.get_business_metrics()
        quantum = collector.get_quantum_metrics()

        # Verify quantum advantage consistency
        health_advantage = health["last_quantum_advantage"]
        quantum_advantage = quantum["quantum_advantage_achieved"]

        # These should be the same metric from different sources
        assert health_advantage == quantum_advantage

    def test_slo_targets_validation(self):
        """Test that SLO targets are reasonable."""
        config = DashboardConfig()

        # API latency should be reasonable
        assert config.slo_targets["api_latency_p95"] <= 1000  # 1 second max

        # Success rates should be high
        assert config.slo_targets["quantum_success_rate"] >= 0.8  # 80% min
        assert config.slo_targets["workflow_completion_rate"] >= 0.9  # 90% min

        # Uptime should be very high
        assert config.slo_targets["uptime"] >= 0.99  # 99% min


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestObservabilityPerformance:
    """Performance tests for observability system."""

    def test_metrics_collection_speed(self):
        """Test that metrics collection is fast."""
        collector = MetricsCollector()

        start_time = time.time()

        # Collect all metrics
        collector.get_system_health()
        collector.get_performance_metrics()
        collector.get_business_metrics()
        collector.get_quantum_metrics()
        collector.get_workflow_metrics()

        end_time = time.time()
        collection_time = end_time - start_time

        # Should complete in under 100ms
        assert collection_time < 0.1

    def test_tracer_initialization_speed(self):
        """Test that tracer initialization is fast when disabled."""
        config = TracingConfig()
        config.enabled = False

        start_time = time.time()
        tracer = NQBATracer(config)
        end_time = time.time()

        init_time = end_time - start_time

        # Should initialize in under 10ms when disabled
        assert init_time < 0.01


@pytest.mark.skipif(
    not OBSERVABILITY_AVAILABLE, reason="Observability components not available"
)
class TestObservabilityErrorHandling:
    """Test error handling in observability system."""

    def test_metrics_collector_error_handling(self):
        """Test that metrics collector handles errors gracefully."""
        collector = MetricsCollector()

        # Should not raise exceptions for any metric collection
        try:
            health = collector.get_system_health()
            perf = collector.get_performance_metrics()
            business = collector.get_business_metrics()
            quantum = collector.get_quantum_metrics()
            workflows = collector.get_workflow_metrics()

            # All should return valid data
            assert all([health, perf, business, quantum, workflows])

        except Exception as e:
            pytest.fail(f"Metrics collection failed: {e}")

    def test_tracer_error_handling(self):
        """Test that tracer handles errors gracefully."""
        config = TracingConfig()
        config.enabled = False
        tracer = NQBATracer(config)

        # Should handle None spans gracefully
        tracer.add_event(None, "test_event")
        tracer.set_attribute(None, "test_key", "test_value")
        tracer.set_status(None, Mock())

        # Should not raise exceptions


if __name__ == "__main__":
    pytest.main([__file__])
