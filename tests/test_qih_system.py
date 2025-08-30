"""
Test suite for the Quantum Integration Hub (QIH) system

Tests the complete QIH functionality including:
- Job submission and management
- Entitlements and feature gating
- API endpoints and validation
- Circuit breaker and fallback mechanisms
"""

import pytest
import asyncio
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from src.nqba_stack.quantum.qih import (
    QuantumIntegrationHub,
    QuantumJob,
    OptimizationRequest,
    OptimizationResult,
    JobStatus,
    JobPriority,
    SolverType,
    CircuitBreaker,
    RetryPolicy,
    UsageTracker,
)
from src.nqba_stack.core.entitlements import (
    EntitlementsEngine,
    Tier,
    Feature,
    UserEntitlements,
    TierLimits,
)
from src.nqba_stack.api.qih import (
    submit_job,
    get_job_status_endpoint,
    list_user_jobs,
    get_user_usage,
    get_solver_info,
    get_qih_health,
    cancel_job,
    retry_job,
)


class TestQuantumIntegrationHub:
    """Test the core QIH functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.qih = QuantumIntegrationHub()
        self.test_user_id = "test_user_123"
        self.test_request = OptimizationRequest(
            operation="qubo",
            inputs={"qubo_matrix": {(0, 0): 1.0, (1, 1): 2.0}},
            timeout_seconds=60,
            priority=JobPriority.NORMAL,
        )

    def test_qih_initialization(self):
        """Test QIH initialization and solver setup"""
        assert self.qih is not None
        assert hasattr(self.qih, "jobs")
        assert hasattr(self.qih, "job_queue")
        assert hasattr(self.qih, "circuit_breaker")
        assert hasattr(self.qih, "retry_policy")
        assert hasattr(self.qih, "usage_tracker")

    def test_job_submission(self):
        """Test job submission and queue management"""
        # Submit job
        job_id = self.qih.submit_job(self.test_user_id, self.test_request)

        # Verify job was created
        assert job_id in self.qih.jobs
        job = self.qih.jobs[job_id]
        assert job.user_id == self.test_user_id
        assert job.status == JobStatus.QUEUED
        assert job.request.operation == "qubo"

        # Verify job was added to queue
        assert job_id in self.qih.job_queue

    def test_job_priority_queue(self):
        """Test priority-based job queuing"""
        # Submit jobs with different priorities
        high_priority_request = OptimizationRequest(
            operation="qubo", inputs={"test": "data"}, priority=JobPriority.HIGH
        )
        low_priority_request = OptimizationRequest(
            operation="qubo", inputs={"test": "data"}, priority=JobPriority.LOW
        )

        # Submit low priority first, then high priority
        low_job_id = self.qih.submit_job(self.test_user_id, low_priority_request)
        high_job_id = self.qih.submit_job(self.test_user_id, high_priority_request)

        # High priority should be first in queue
        assert self.qih.job_queue[0] == high_job_id
        assert self.qih.job_queue[1] == low_job_id

    def test_idempotency(self):
        """Test job idempotency with duplicate requests"""
        # Submit same job twice with same idempotency key
        idempotency_key = "test_key_123"

        job_id_1 = self.qih.submit_job(
            self.test_user_id, self.test_request, idempotency_key
        )
        job_id_2 = self.qih.submit_job(
            self.test_user_id, self.test_request, idempotency_key
        )

        # Should return same job ID
        assert job_id_1 == job_id_2

        # Should only have one job
        assert len(self.qih.jobs) == 1

    def test_circuit_breaker(self):
        """Test circuit breaker functionality"""
        cb = self.qih.circuit_breaker

        # Initially closed
        assert cb.state == "CLOSED"
        assert cb.can_execute() is True

        # Record failures until threshold
        for _ in range(5):
            cb.record_failure()

        # Should be open now
        assert cb.state == "OPEN"
        assert cb.can_execute() is False

        # Wait for recovery timeout
        cb.last_failure_time = datetime.utcnow() - timedelta(seconds=70)
        assert cb.can_execute() is True
        assert cb.state == "HALF_OPEN"

        # Record success to close circuit
        cb.record_success()
        assert cb.state == "CLOSED"

    def test_retry_policy(self):
        """Test retry policy with exponential backoff"""
        policy = self.qih.retry_policy

        # Test delay calculation
        delay_1 = policy.get_delay(1)
        delay_2 = policy.get_delay(2)
        delay_3 = policy.get_delay(3)

        assert delay_1 == 1.0
        assert delay_2 == 2.0
        assert delay_3 == 4.0

        # Test max delay cap
        delay_10 = policy.get_delay(10)
        assert delay_10 <= policy.max_delay


class TestEntitlementsEngine:
    """Test the entitlements system"""

    def setup_method(self):
        """Set up test fixtures"""
        self.engine = EntitlementsEngine()
        self.test_user_id = "test_user_456"

    def test_tier_initialization(self):
        """Test tier configuration initialization"""
        # Check all tiers are available
        tiers = self.engine.get_available_tiers()
        assert Tier.FREE in tiers
        assert Tier.BUSINESS in tiers
        assert Tier.PREMIUM in tiers
        assert Tier.LUXURY in tiers

    def test_feature_mapping(self):
        """Test feature availability across tiers"""
        # Free tier should have basic features
        free_features = self.engine.get_feature_tiers(Feature.BASIC_OPTIMIZATION)
        assert Tier.FREE in free_features

        # Quantum optimization should require higher tier
        quantum_features = self.engine.get_feature_tiers(Feature.QUANTUM_OPTIMIZATION)
        assert Tier.FREE not in quantum_features
        assert Tier.PREMIUM in quantum_features
        assert Tier.LUXURY in quantum_features

    def test_user_tier_management(self):
        """Test user tier assignment and updates"""
        # Set user to business tier
        self.engine.set_user_tier(self.test_user_id, Tier.BUSINESS)

        # Verify entitlements
        user_ent = self.engine.get_user_entitlements(self.test_user_id)
        assert user_ent.tier == Tier.BUSINESS
        assert Feature.FLYFOX_AI_ACCESS in user_ent.features
        assert Feature.QUANTUM_OPTIMIZATION not in user_ent.features

    def test_feature_access_control(self):
        """Test feature access based on user tier"""
        # Set user to free tier
        self.engine.set_user_tier(self.test_user_id, Tier.FREE)

        # Should have access to basic features
        assert self.engine.has_feature_access(
            self.test_user_id, Feature.BASIC_OPTIMIZATION
        )

        # Should not have access to premium features
        assert not self.engine.has_feature_access(
            self.test_user_id, Feature.QUANTUM_OPTIMIZATION
        )

    def test_usage_limits(self):
        """Test usage limit enforcement"""
        # Set user to business tier
        self.engine.set_user_tier(self.test_user_id, Tier.BUSINESS)

        # Check various limits
        assert self.engine.check_usage_limit(
            self.test_user_id, "optimizations_per_month", 500
        )
        assert not self.engine.check_usage_limit(
            self.test_user_id, "optimizations_per_month", 1500
        )

        assert self.engine.check_usage_limit(
            self.test_user_id, "api_calls_per_day", 5000
        )
        assert not self.engine.check_usage_limit(
            self.test_user_id, "api_calls_per_day", 15000
        )

    def test_tier_upgrade(self):
        """Test user tier upgrade functionality"""
        # Start with free tier
        self.engine.set_user_tier(self.test_user_id, Tier.FREE)

        # Upgrade to premium
        self.engine.upgrade_user_tier(self.test_user_id, Tier.PREMIUM)

        # Verify upgrade
        user_ent = self.engine.get_user_entitlements(self.test_user_id)
        assert user_ent.tier == Tier.PREMIUM
        assert Feature.QUANTUM_OPTIMIZATION in user_ent.features

        # Should not allow downgrade
        with pytest.raises(ValueError):
            self.engine.upgrade_user_tier(self.test_user_id, Tier.BUSINESS)


class TestUsageTracker:
    """Test usage tracking functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.tracker = UsageTracker()
        self.test_user_id = "test_user_789"

    def test_job_completion_tracking(self):
        """Test tracking job completion metrics"""
        # Create mock job
        mock_job = Mock()
        mock_job.user_id = self.test_user_id
        mock_job.metrics.qpu_time_ms = 1000
        mock_job.metrics.reads = 100
        mock_job.metrics.problems_solved = 1
        mock_job.metrics.bytes_in = 1024
        mock_job.metrics.bytes_out = 2048
        mock_job.result = Mock()
        mock_job.result.solver_used = SolverType.QUANTUM_DYNEX

        # Record completion
        self.tracker.record_job_completion(mock_job)

        # Verify user metrics
        user_usage = self.tracker.get_user_usage(self.test_user_id)
        assert user_usage["jobs_completed"] == 1
        assert user_usage["qpu_time_ms"] == 1000
        assert user_usage["reads"] == 100
        assert user_usage["problems_solved"] == 1
        assert user_usage["bytes_processed"] == 3072  # 1024 + 2048

        # Verify global metrics
        global_metrics = self.tracker.get_global_metrics()
        assert global_metrics["total_jobs"] == 1
        assert global_metrics["quantum_jobs"] == 1
        assert global_metrics["total_qpu_time_ms"] == 1000


class TestQIHAPIEndpoints:
    """Test QIH API endpoints"""

    def setup_method(self):
        """Set up test fixtures"""
        self.test_user_id = "test_user_api"
        self.test_job_id = "test_job_123"

        # Mock authentication
        self.mock_auth_patcher = patch("src.nqba_stack.api.qih.get_current_user")
        self.mock_auth = self.mock_auth_patcher.start()
        self.mock_auth.return_value = self.test_user_id

    def teardown_method(self):
        """Clean up test fixtures"""
        self.mock_auth_patcher.stop()

    @pytest.mark.asyncio
    async def test_submit_job_endpoint(self):
        """Test job submission endpoint"""
        from fastapi import HTTPException
        from src.nqba_stack.api.qih import OptimizationRequestModel

        # Create test request
        request_data = OptimizationRequestModel(
            operation="qubo",
            inputs={"qubo_matrix": {(0, 0): 1.0}},
            timeout_seconds=60,
            priority="normal",
        )

        # Mock QIH
        with patch("src.nqba_stack.api.qih.submit_optimization_job") as mock_submit:
            mock_submit.return_value = self.test_job_id

            # Call endpoint
            result = await submit_job(request_data, Mock(), self.test_user_id)

            # Verify result
            assert result["job_id"] == self.test_job_id
            assert result["status"] == "submitted"
            mock_submit.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_job_status_endpoint(self):
        """Test job status retrieval endpoint"""
        # Mock job data
        mock_job_data = {
            "user_id": self.test_user_id,
            "status": "completed",
            "started_at": "2024-01-01T00:00:00",
            "result": {"solution": [1, 0, 1]},
            "error": None,
        }

        with patch("src.nqba_stack.api.qih.get_job_status") as mock_get_status:
            mock_get_status.return_value = mock_job_data

            # Call endpoint
            result = await get_job_status_endpoint(self.test_job_id, self.test_user_id)

            # Verify result
            assert result.job_id == self.test_job_id
            assert result.status == "completed"
            assert result.result == {"solution": [1, 0, 1]}

    @pytest.mark.asyncio
    async def test_list_user_jobs_endpoint(self):
        """Test user job listing endpoint"""
        # Mock job list
        mock_jobs = [
            {
                "job_id": "job1",
                "user_id": self.test_user_id,
                "status": "completed",
                "priority": "normal",
                "created_at": "2024-01-01T00:00:00",
                "started_at": None,
                "completed_at": None,
                "result": None,
                "error": None,
                "metrics": {},
                "retry_count": 0,
                "max_retries": 3,
            }
        ]

        with patch("src.nqba_stack.api.qih.get_user_jobs") as mock_get_jobs:
            mock_get_jobs.return_value = mock_jobs

            # Call endpoint
            result = await list_user_jobs(
                status=None, limit=50, offset=0, current_user=self.test_user_id
            )

            # Verify result
            assert len(result) == 1
            assert result[0].job_id == "job1"
            assert result[0].status == "completed"

    @pytest.mark.asyncio
    async def test_get_qih_health_endpoint(self):
        """Test QIH health endpoint"""
        # Mock QIH instance
        mock_qih = Mock()
        mock_qih.circuit_breaker.state = "CLOSED"
        mock_qih.solvers = {}
        mock_qih.jobs = {}
        mock_qih.job_queue = []
        mock_qih.usage_tracker.global_metrics = {"total_jobs": 0}

        with patch("src.nqba_stack.api.qih.get_qih") as mock_get_qih:
            mock_get_qih.return_value = mock_qih

            # Call endpoint
            result = await get_qih_health()

            # Verify result
            assert result.status == "healthy"
            assert result.circuit_breaker_status == "CLOSED"
            assert result.active_jobs == 0
            assert result.queued_jobs == 0


class TestQIHIntegration:
    """Test QIH integration with other systems"""

    def setup_method(self):
        """Set up test fixtures"""
        self.qih = QuantumIntegrationHub()
        self.entitlements = EntitlementsEngine()
        self.test_user_id = "integration_test_user"

    def test_entitlements_integration(self):
        """Test QIH integration with entitlements system"""
        # Set user tier
        self.entitlements.set_user_tier(self.test_user_id, Tier.PREMIUM)

        # Verify user has quantum optimization access
        assert self.entitlements.has_feature_access(
            self.test_user_id, Feature.QUANTUM_OPTIMIZATION
        )

        # Submit quantum optimization job
        request = OptimizationRequest(
            operation="qubo",
            inputs={"test": "data"},
            solver_preference=SolverType.QUANTUM_DYNEX,
        )

        job_id = self.qih.submit_job(self.test_user_id, request)

        # Verify job was created
        assert job_id in self.qih.jobs
        job = self.qih.jobs[job_id]
        assert job.user_id == self.test_user_id
        assert job.request.solver_preference == SolverType.QUANTUM_DYNEX

    def test_usage_tracking_integration(self):
        """Test QIH integration with usage tracking"""
        # Submit job
        request = OptimizationRequest(operation="qubo", inputs={"test": "data"})

        job_id = self.qih.submit_job(self.test_user_id, request)

        # Simulate job completion
        job = self.qih.jobs[job_id]
        job.status = JobStatus.COMPLETED
        job.metrics.qpu_time_ms = 500
        job.metrics.reads = 50
        job.metrics.problems_solved = 1
        job.metrics.bytes_in = 512
        job.metrics.bytes_out = 1024

        # Record completion
        self.qih.usage_tracker.record_job_completion(job)

        # Verify usage was tracked
        user_usage = self.qih.usage_tracker.get_user_usage(self.test_user_id)
        assert user_usage["jobs_completed"] == 1
        assert user_usage["qpu_time_ms"] == 500


# Test data and utilities
@pytest.fixture
def sample_qubo_data():
    """Sample QUBO data for testing"""
    return {"qubo_matrix": {(0, 0): 1.0, (1, 1): 2.0, (0, 1): -0.5}, "offset": 0.0}


@pytest.fixture
def sample_optimization_request():
    """Sample optimization request for testing"""
    return OptimizationRequest(
        operation="qubo",
        inputs={"qubo_matrix": {(0, 0): 1.0, (1, 1): 2.0}},
        timeout_seconds=60,
        priority=JobPriority.NORMAL,
        metadata={"test": True},
    )


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
