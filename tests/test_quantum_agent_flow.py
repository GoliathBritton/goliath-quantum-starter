"""Integration Tests for Quantum Agent Flow

End-to-end testing of quantum-enhanced AI agent capabilities including:
- Agent initialization and configuration
- Quantum job submission and processing
- Parallel exploration workflows
- Reversal reasoning analysis
- Quantum ranking optimization
- Lead qualification processes
- MCP integration
- Error handling and recovery
"""

import asyncio
import json
import pytest
import time
from typing import Dict, List, Any
from unittest.mock import Mock, patch, AsyncMock

# Import core components
from core.agent_base import QuantumAgentBase
from core.quantum_job_manager import QuantumJobManager, JobType, JobStatus
from services.qdllm_worker.worker import QdLLMWorker
from services.qdllm_worker.models import (
    QdLLMRequest, QdLLMResponse, ExplorationResult, 
    ReasoningResult, RankingResult, LeadQualificationResult
)
from services.qdllm_worker.config import QdLLMConfig


class TestQuantumAgentFlow:
    """Integration tests for quantum agent workflows"""
    
    @pytest.fixture
    async def agent_config(self):
        """Create test agent configuration"""
        return {
            "agent_id": "test-agent-001",
            "name": "Test Quantum Agent",
            "role": "sales",
            "quantum_enabled": True,
            "risk_threshold": 0.7,
            "max_concurrent_jobs": 5,
            "dynex_enabled": False,  # Use mock for testing
            "openai_api_key": "test-key"
        }
    
    @pytest.fixture
    async def mock_dynex_client(self):
        """Mock Dynex client for testing"""
        mock_client = Mock()
        mock_client.submit_job = AsyncMock(return_value={
            "job_id": "dynex_job_123",
            "status": "submitted"
        })
        mock_client.get_job_status = AsyncMock(return_value={
            "job_id": "dynex_job_123",
            "status": "completed",
            "result": {"ranking": [0, 1, 2], "scores": [0.95, 0.87, 0.72]}
        })
        return mock_client
    
    @pytest.fixture
    async def quantum_agent(self, agent_config, mock_dynex_client):
        """Create quantum agent instance for testing"""
        with patch('core.quantum_job_manager.DynexClient', return_value=mock_dynex_client):
            agent = QuantumAgentBase(
                agent_id=agent_config["agent_id"],
                config=agent_config
            )
            await agent.initialize()
            return agent
    
    @pytest.fixture
    async def qdllm_worker(self):
        """Create qdLLM worker instance for testing"""
        config = QdLLMConfig(
            openai_api_key="test-key",
            quantum_job_manager_enabled=False,  # Use mock
            dynex_enabled=False
        )
        
        with patch('openai.ChatCompletion.acreate') as mock_openai:
            mock_openai.return_value = Mock(
                choices=[Mock(
                    message=Mock(
                        content=json.dumps({
                            "strategies": [
                                {
                                    "strategy_id": "S1",
                                    "strategy_name": "Consultative Discovery",
                                    "conversion_confidence": 0.85
                                }
                            ]
                        })
                    )
                )]
            )
            
            worker = QdLLMWorker(config)
            await worker.initialize()
            return worker
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, quantum_agent):
        """Test quantum agent initialization"""
        assert quantum_agent.agent_id == "test-agent-001"
        assert quantum_agent.quantum_enabled is True
        assert quantum_agent.job_manager is not None
        assert quantum_agent.is_initialized is True
    
    @pytest.mark.asyncio
    async def test_parallel_exploration_flow(self, quantum_agent, qdllm_worker):
        """Test end-to-end parallel exploration workflow"""
        # Prepare test data
        lead_profile = {
            "name": "John Smith",
            "company": "TechCorp",
            "title": "VP Engineering",
            "industry": "SaaS"
        }
        
        objective = "schedule_demo"
        
        # Submit parallel exploration request
        request = QdLLMRequest(
            request_type="parallel_exploration",
            context={
                "lead_profile": lead_profile,
                "objective": objective
            },
            parameters={
                "num_strategies": 6,
                "constraints": ["professional_tone", "under_160_chars"]
            }
        )
        
        # Process request through qdLLM worker
        response = await qdllm_worker.process_request(request)
        
        # Validate response
        assert response.request_id == request.request_id
        assert response.error is None
        assert isinstance(response.result, dict)
        assert "strategies" in response.result
        assert len(response.result["strategies"]) > 0
        
        # Test quantum ranking if enabled
        if quantum_agent.quantum_enabled:
            strategies = response.result["strategies"]
            ranking_job = await quantum_agent.submit_quantum_job(
                job_type=JobType.RANKING,
                payload={
                    "candidates": strategies,
                    "optimization_goal": "maximize_conversion"
                }
            )
            
            # Wait for job completion
            result = await quantum_agent.wait_for_job(ranking_job.id, timeout=30)
            assert result is not None
            assert "ranking" in result
    
    @pytest.mark.asyncio
    async def test_reversal_reasoning_flow(self, quantum_agent, qdllm_worker):
        """Test end-to-end reversal reasoning workflow"""
        # Prepare test data
        outcome = "Sales forecast dropped 15%"
        context = {
            "timeline": "Q4 2024",
            "stakeholders": ["Sales Team", "Marketing", "Product"],
            "metrics": {
                "conversion_rate": 0.12,
                "lead_quality": 0.68,
                "pipeline_velocity": 45
            },
            "previous_state": {
                "conversion_rate": 0.18,
                "lead_quality": 0.75
            }
        }
        
        # Submit reversal reasoning request
        request = QdLLMRequest(
            request_type="reversal_reasoning",
            context={
                "outcome": outcome,
                "context": context
            },
            parameters={
                "num_candidates": 6,
                "confidence_threshold": 0.7
            }
        )
        
        # Process request
        response = await qdllm_worker.process_request(request)
        
        # Validate response
        assert response.error is None
        assert isinstance(response.result, dict)
        assert "analysis" in response.result
        
        analysis = response.result["analysis"]
        assert "backtrace_candidates" in analysis
        assert len(analysis["backtrace_candidates"]) > 0
        
        # Validate candidate structure
        for candidate in analysis["backtrace_candidates"]:
            assert "cause_summary" in candidate
            assert "supporting_evidence" in candidate
            assert "likelihood_score" in candidate
            assert "corrective_action" in candidate
    
    @pytest.mark.asyncio
    async def test_quantum_ranking_flow(self, quantum_agent):
        """Test quantum ranking optimization"""
        # Prepare test candidates
        candidates = [
            {
                "id": "lead_001",
                "name": "TechCorp - John Smith",
                "attributes": {
                    "fit_score": 90,
                    "engagement_score": 85,
                    "urgency_score": 88
                }
            },
            {
                "id": "lead_002",
                "name": "StartupCo - Jane Doe",
                "attributes": {
                    "fit_score": 75,
                    "engagement_score": 92,
                    "urgency_score": 65
                }
            },
            {
                "id": "lead_003",
                "name": "Enterprise Inc - Bob Wilson",
                "attributes": {
                    "fit_score": 95,
                    "engagement_score": 70,
                    "urgency_score": 95
                }
            }
        ]
        
        # Submit quantum ranking job
        job = await quantum_agent.submit_quantum_job(
            job_type=JobType.RANKING,
            payload={
                "candidates": candidates,
                "optimization_goal": "maximize_conversion",
                "ranking_dimensions": ["fit_score", "engagement_score", "urgency_score"]
            }
        )
        
        # Wait for completion
        result = await quantum_agent.wait_for_job(job.id, timeout=30)
        
        # Validate result
        assert result is not None
        assert "ranking" in result
        assert len(result["ranking"]) == len(candidates)
        
        # Verify ranking order (should be optimized)
        ranking = result["ranking"]
        assert all("rank" in item for item in ranking)
        assert all("candidate_id" in item for item in ranking)
        assert all("overall_score" in item for item in ranking)
    
    @pytest.mark.asyncio
    async def test_lead_qualification_flow(self, qdllm_worker):
        """Test lead qualification process"""
        # Prepare test lead data
        lead_data = {
            "contact_info": {
                "name": "Alice Johnson",
                "email": "alice@techstartup.com",
                "title": "CTO"
            },
            "company_info": {
                "name": "TechStartup",
                "industry": "AI/ML",
                "size": "50-100",
                "revenue": "$5M-$10M"
            },
            "engagement_history": [
                {
                    "type": "website_visit",
                    "date": "2024-01-15",
                    "outcome": "pricing_page_viewed"
                },
                {
                    "type": "email_open",
                    "date": "2024-01-16",
                    "outcome": "clicked_demo_link"
                }
            ],
            "behavioral_data": {
                "website_visits": 5,
                "email_opens": 3,
                "content_downloads": 2,
                "demo_requests": 1
            }
        }
        
        # Submit qualification request
        request = QdLLMRequest(
            request_type="lead_qualification",
            context={"lead_data": lead_data},
            parameters={
                "scoring_model": "quantum_enhanced",
                "quantum_score": True
            }
        )
        
        # Process request
        response = await qdllm_worker.process_request(request)
        
        # Validate response
        assert response.error is None
        assert isinstance(response.result, dict)
        assert "qualification" in response.result
        
        qualification = response.result["qualification"]
        assert "overall_qualification" in qualification
        assert "dimension_scores" in qualification
        
        # Validate qualification structure
        overall = qualification["overall_qualification"]
        assert "composite_score" in overall
        assert "qualification_tier" in overall
        assert "recommended_action" in overall
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, quantum_agent):
        """Test error handling and recovery mechanisms"""
        # Test invalid job submission
        with pytest.raises(ValueError):
            await quantum_agent.submit_quantum_job(
                job_type="invalid_type",
                payload={}
            )
        
        # Test timeout handling
        job = await quantum_agent.submit_quantum_job(
            job_type=JobType.RANKING,
            payload={"candidates": [], "optimization_goal": "maximize_conversion"}
        )
        
        # Test short timeout
        result = await quantum_agent.wait_for_job(job.id, timeout=0.1)
        assert result is None  # Should timeout
    
    @pytest.mark.asyncio
    async def test_concurrent_job_processing(self, quantum_agent):
        """Test concurrent quantum job processing"""
        # Submit multiple jobs concurrently
        jobs = []
        for i in range(3):
            job = await quantum_agent.submit_quantum_job(
                job_type=JobType.RANKING,
                payload={
                    "candidates": [
                        {"id": f"candidate_{i}_{j}", "name": f"Test {j}", "attributes": {"score": j * 10}}
                        for j in range(3)
                    ],
                    "optimization_goal": "maximize_conversion"
                }
            )
            jobs.append(job)
        
        # Wait for all jobs to complete
        results = await asyncio.gather(*[
            quantum_agent.wait_for_job(job.id, timeout=30)
            for job in jobs
        ])
        
        # Validate all results
        assert len(results) == 3
        assert all(result is not None for result in results)
    
    @pytest.mark.asyncio
    async def test_audit_logging(self, quantum_agent):
        """Test audit logging functionality"""
        # Submit a job that should be audited
        job = await quantum_agent.submit_quantum_job(
            job_type=JobType.RANKING,
            payload={
                "candidates": [{"id": "test", "name": "Test", "attributes": {}}],
                "optimization_goal": "maximize_conversion"
            }
        )
        
        # Wait for completion
        await quantum_agent.wait_for_job(job.id, timeout=30)
        
        # Check audit logs
        audit_logs = quantum_agent.get_audit_logs()
        assert len(audit_logs) > 0
        
        # Validate audit log structure
        latest_log = audit_logs[-1]
        assert "timestamp" in latest_log
        assert "job_id" in latest_log
        assert "action" in latest_log
        assert "agent_id" in latest_log
    
    @pytest.mark.asyncio
    async def test_risk_threshold_enforcement(self, quantum_agent):
        """Test risk threshold enforcement"""
        # Set low risk threshold
        quantum_agent.risk_threshold = 0.1
        
        # Submit high-risk job (mock)
        with patch.object(quantum_agent, '_calculate_risk_score', return_value=0.8):
            with pytest.raises(Exception):  # Should be blocked by risk threshold
                await quantum_agent.submit_quantum_job(
                    job_type=JobType.RANKING,
                    payload={"high_risk_operation": True}
                )
    
    @pytest.mark.asyncio
    async def test_performance_metrics(self, quantum_agent, qdllm_worker):
        """Test performance metrics collection"""
        # Process several requests to generate metrics
        for i in range(5):
            request = QdLLMRequest(
                request_type="parallel_exploration",
                context={
                    "lead_profile": {"name": f"Test {i}", "company": "TestCorp"},
                    "objective": "schedule_demo"
                }
            )
            await qdllm_worker.process_request(request)
        
        # Get metrics
        metrics = qdllm_worker.get_metrics()
        
        # Validate metrics
        assert metrics.requests_processed >= 5
        assert metrics.parallel_explorations >= 5
        assert metrics.average_response_time > 0
        assert metrics.error_rate >= 0
    
    @pytest.mark.asyncio
    async def test_mcp_integration(self, quantum_agent):
        """Test MCP (Model Context Protocol) integration"""
        # Test MCP tool registration
        mcp_tools = quantum_agent.get_mcp_tools()
        assert len(mcp_tools) > 0
        
        # Validate tool structure
        for tool in mcp_tools:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
        
        # Test MCP resource access
        resources = quantum_agent.get_mcp_resources()
        assert len(resources) > 0
        
        # Test MCP prompt templates
        prompts = quantum_agent.get_mcp_prompts()
        assert len(prompts) > 0


class TestQuantumJobManager:
    """Unit tests for Quantum Job Manager"""
    
    @pytest.fixture
    def mock_dynex_client(self):
        """Mock Dynex client"""
        mock = Mock()
        mock.submit_job = AsyncMock(return_value={"job_id": "test_job_123"})
        mock.get_job_status = AsyncMock(return_value={
            "status": "completed",
            "result": {"ranking": [0, 1, 2]}
        })
        return mock
    
    @pytest.fixture
    def job_manager(self, mock_dynex_client):
        """Create job manager instance"""
        return QuantumJobManager(
            dynex_client=mock_dynex_client,
            max_retries=3,
            enable_caching=True
        )
    
    @pytest.mark.asyncio
    async def test_job_submission(self, job_manager):
        """Test quantum job submission"""
        payload = {
            "type": "ranking",
            "candidates": [{"id": "1", "score": 0.8}],
            "optimization_goal": "maximize_conversion"
        }
        
        job = await job_manager.submit(payload)
        assert job.id is not None
        assert job.status == JobStatus.PENDING
        assert job.job_type == JobType.RANKING
    
    @pytest.mark.asyncio
    async def test_job_execution(self, job_manager):
        """Test quantum job execution"""
        payload = {"type": "ranking", "candidates": []}
        job = await job_manager.submit(payload)
        
        result = await job_manager.wait(job.id, timeout=30)
        assert result is not None
        assert "ranking" in result
    
    @pytest.mark.asyncio
    async def test_job_caching(self, job_manager):
        """Test job result caching"""
        payload = {"type": "ranking", "candidates": [{"id": "1"}]}
        
        # Submit same job twice
        job1 = await job_manager.submit(payload)
        result1 = await job_manager.wait(job1.id, timeout=30)
        
        job2 = await job_manager.submit(payload)
        result2 = await job_manager.wait(job2.id, timeout=30)
        
        # Second job should be faster (cached)
        assert result1 == result2


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([
        __file__,
        "-v",
        "--asyncio-mode=auto",
        "--tb=short"
    ])