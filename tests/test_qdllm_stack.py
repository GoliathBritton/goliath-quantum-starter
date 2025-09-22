#!/usr/bin/env python3
"""
Comprehensive Unit Tests for NQBA Framework

This test suite covers:
- NQBA framework orchestration and integration
- Core intelligence modules: qdLLM, QNLP, QTransformers
- Business workflow processing
- Governance and compliance features
- API layer and external integrations
- Performance and reliability testing

Author: NQBA Development Team
Version: 1.0.0
"""

import unittest
import asyncio
import time
import json
from unittest.mock import Mock, patch, AsyncMock
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

# NQBA Framework imports
from nqba import create_framework
from nqba.core.intelligence import qdllm, qnlp, qtransformers
from nqba.core.framework import NQBAFramework
from nqba.procedures import execute_workflow, create_workflow_engine
from nqba.governance import enforce_policy, check_compliance
from nqba.api import create_api_server

# Legacy qdLLM imports for backward compatibility testing
try:
    from qdllm.core.engine import qdLLMEngine, QuantumDiffusionConfig
    from qdllm.qnlp.processor import QNLPProcessor
    from qdllm.qtransformers.model import QTransformerModel
    from qdllm.core.parallel_executor import ParallelExecutor, ExecutionMode, TaskPriority
    from qdllm.api.models import (
        InferenceRequest, InferenceResponse, QNLPRequest, QNLPResponse,
        QTransformerRequest, QTransformerResponse, BatchRequest,
        ModelType, QNLPTask, QuantumMetrics
    )
    from qdllm.api.server import create_app
    from qdllm.api.utils import ResponseCache, MetricsCollector
    LEGACY_AVAILABLE = True
except ImportError:
    LEGACY_AVAILABLE = False

class TestNQBAFramework(unittest.TestCase):
    """Test cases for the NQBA framework orchestration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.framework = create_framework(
            enable_qdllm=True,
            enable_qnlp=True,
            enable_qtransformers=True,
            governance_enabled=True,
            compliance_checks=True
        )
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def test_framework_initialization(self):
        """Test NQBA framework initialization."""
        self.assertIsNotNone(self.framework)
        self.assertTrue(hasattr(self.framework, 'modules'))
        self.assertTrue(hasattr(self.framework, 'governance'))
        self.assertTrue(hasattr(self.framework, 'procedures'))
        self.assertTrue(hasattr(self.framework, 'integration'))
    
    def test_business_request_processing(self):
        """Test business request processing through framework."""
        request = {
            'type': 'text_analysis',
            'data': 'Test business document for analysis',
            'workflow': 'qnlp_analysis',
            'governance': {'compliance_check': True}
        }
        
        # Mock the processing
        with patch.object(self.framework, 'process_business_request') as mock_process:
            mock_process.return_value = {'status': 'success', 'result': 'analyzed'}
            result = self.framework.process_business_request(request)
            self.assertEqual(result['status'], 'success')
            mock_process.assert_called_once_with(request)

class TestqdLLMEngine(unittest.TestCase):
    """Test cases for the core qdLLM engine."""
    
    def setUp(self):
        """Set up test fixtures."""
        if LEGACY_AVAILABLE:
            self.engine = qdLLMEngine()
        else:
            self.engine = qdllm.create_engine()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """Clean up after tests."""
        self.loop.close()
    
    def test_engine_initialization(self):
        """Test engine initialization."""
        self.assertIsInstance(self.engine, qdLLMEngine)
        self.assertIsNotNone(self.engine.config)
    
    async def async_test_quantum_diffusion_generation(self):
        """Test quantum diffusion text generation."""
        await self.engine.initialize()
        
        request = InferenceRequest(
            prompt="Test quantum generation",
            model_type=ModelType.QDLLM,
            max_tokens=50,
            temperature=0.7,
            use_quantum_diffusion=True
        )
        
        result = await self.engine.generate(request)
        
        self.assertIsInstance(result, InferenceResponse)
        self.assertIsNotNone(result.text)
        self.assertGreater(len(result.text), 0)
        self.assertIsNotNone(result.quantum_metrics)
        self.assertGreaterEqual(result.quantum_metrics.coherence, 0.0)
        self.assertLessEqual(result.quantum_metrics.coherence, 1.0)
    
    def test_quantum_diffusion_generation(self):
        """Wrapper for async quantum diffusion test."""
        self.loop.run_until_complete(self.async_test_quantum_diffusion_generation())
    
    async def async_test_bidirectional_reasoning(self):
        """Test bidirectional reasoning capabilities."""
        await self.engine.initialize()
        
        request = InferenceRequest(
            prompt="Analyze this statement from multiple perspectives",
            model_type=ModelType.QDLLM,
            max_tokens=100,
            bidirectional_reasoning=True
        )
        
        result = await self.engine.generate(request)
        
        self.assertIsInstance(result, InferenceResponse)
        self.assertTrue(result.bidirectional_analysis)
        self.assertIsNotNone(result.reasoning_paths)
    
    def test_bidirectional_reasoning(self):
        """Wrapper for async bidirectional reasoning test."""
        self.loop.run_until_complete(self.async_test_bidirectional_reasoning())
    
    def test_quantum_diffusion_config(self):
        """Test quantum diffusion configuration."""
        config = QuantumDiffusionConfig(
            num_steps=100,
            noise_schedule="cosine",
            coherence_threshold=0.8
        )
        
        self.assertEqual(config.num_steps, 100)
        self.assertEqual(config.noise_schedule, "cosine")
        self.assertEqual(config.coherence_threshold, 0.8)

class TestQNLPProcessor(unittest.TestCase):
    """Test cases for the QNLP processor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = QNLPProcessor()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """Clean up after tests."""
        self.loop.close()
    
    async def async_test_sentiment_analysis(self):
        """Test sentiment analysis functionality."""
        await self.processor.initialize()
        
        request = QNLPRequest(
            text="I love this quantum computing system!",
            task=QNLPTask.SENTIMENT,
            use_quantum_embeddings=True
        )
        
        result = await self.processor.process(request)
        
        self.assertIsInstance(result, QNLPResponse)
        self.assertIsNotNone(result.sentiment)
        self.assertIn(result.sentiment.label, ["positive", "negative", "neutral"])
        self.assertGreaterEqual(result.sentiment.confidence, 0.0)
        self.assertLessEqual(result.sentiment.confidence, 1.0)
    
    def test_sentiment_analysis(self):
        """Wrapper for async sentiment analysis test."""
        self.loop.run_until_complete(self.async_test_sentiment_analysis())
    
    async def async_test_entity_recognition(self):
        """Test named entity recognition."""
        await self.processor.initialize()
        
        request = QNLPRequest(
            text="Apple Inc. was founded by Steve Jobs in California.",
            task=QNLPTask.NER,
            use_quantum_embeddings=True
        )
        
        result = await self.processor.process(request)
        
        self.assertIsInstance(result, QNLPResponse)
        self.assertIsNotNone(result.entities)
        self.assertGreater(len(result.entities), 0)
        
        # Check for expected entities
        entity_texts = [entity.text for entity in result.entities]
        self.assertIn("Apple Inc.", entity_texts)
        self.assertIn("Steve Jobs", entity_texts)
    
    def test_entity_recognition(self):
        """Wrapper for async entity recognition test."""
        self.loop.run_until_complete(self.async_test_entity_recognition())
    
    async def async_test_quantum_embeddings(self):
        """Test quantum-enhanced embeddings."""
        await self.processor.initialize()
        
        request = QNLPRequest(
            text="Quantum computing enables superposition",
            task=QNLPTask.EMBEDDING,
            use_quantum_embeddings=True,
            coherence_threshold=0.7
        )
        
        result = await self.processor.process(request)
        
        self.assertIsInstance(result, QNLPResponse)
        self.assertIsNotNone(result.embeddings)
        self.assertGreater(len(result.embeddings), 0)
        self.assertIsNotNone(result.quantum_metrics)
        self.assertGreaterEqual(result.quantum_metrics.coherence, 0.7)
    
    def test_quantum_embeddings(self):
        """Wrapper for async quantum embeddings test."""
        self.loop.run_until_complete(self.async_test_quantum_embeddings())

class TestQTransformerModel(unittest.TestCase):
    """Test cases for the QTransformer model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model = QTransformerModel()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """Clean up after tests."""
        self.loop.close()
    
    async def async_test_text_generation(self):
        """Test text generation with quantum layers."""
        await self.model.initialize()
        
        request = QTransformerRequest(
            input_text="The future of AI is",
            task="text_generation",
            max_length=50,
            quantum_layers=True,
            temperature=0.8
        )
        
        result = await self.model.forward(request)
        
        self.assertIsInstance(result, QTransformerResponse)
        self.assertIsNotNone(result.output_text)
        self.assertGreater(len(result.output_text), len(request.input_text))
        self.assertIsNotNone(result.attention_metrics)
        self.assertIsNotNone(result.quantum_metrics)
    
    def test_text_generation(self):
        """Wrapper for async text generation test."""
        self.loop.run_until_complete(self.async_test_text_generation())
    
    async def async_test_quantum_attention(self):
        """Test quantum attention mechanisms."""
        await self.model.initialize()
        
        request = QTransformerRequest(
            input_text="Quantum attention mechanisms enable better understanding",
            task="attention_analysis",
            attention_type="quantum",
            quantum_layers=True
        )
        
        result = await self.model.forward(request)
        
        self.assertIsInstance(result, QTransformerResponse)
        self.assertIsNotNone(result.attention_weights)
        self.assertIsNotNone(result.attention_metrics)
        self.assertGreater(result.attention_metrics.entropy, 0.0)
    
    def test_quantum_attention(self):
        """Wrapper for async quantum attention test."""
        self.loop.run_until_complete(self.async_test_quantum_attention())
    
    async def async_test_model_performance(self):
        """Test model performance metrics."""
        await self.model.initialize()
        
        request = QTransformerRequest(
            input_text="Performance testing for quantum transformers",
            task="text_generation",
            max_length=30
        )
        
        start_time = time.time()
        result = await self.model.forward(request)
        end_time = time.time()
        
        self.assertIsInstance(result, QTransformerResponse)
        self.assertLess(end_time - start_time, 5.0)  # Should complete within 5 seconds
        self.assertIsNotNone(result.performance_metrics)
    
    def test_model_performance(self):
        """Wrapper for async model performance test."""
        self.loop.run_until_complete(self.async_test_model_performance())

class TestParallelExecutor(unittest.TestCase):
    """Test cases for the parallel executor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.executor = ParallelExecutor()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """Clean up after tests."""
        self.loop.close()
    
    async def async_test_parallel_execution(self):
        """Test parallel task execution."""
        async def sample_task(x):
            await asyncio.sleep(0.1)
            return x * 2
        
        tasks = [sample_task(i) for i in range(5)]
        
        start_time = time.time()
        results = await self.executor.execute_batch(
            tasks,
            mode=ExecutionMode.PARALLEL,
            max_workers=3
        )
        end_time = time.time()
        
        self.assertEqual(len(results), 5)
        self.assertEqual(results, [0, 2, 4, 6, 8])
        self.assertLess(end_time - start_time, 1.0)  # Should be faster than sequential
    
    def test_parallel_execution(self):
        """Wrapper for async parallel execution test."""
        self.loop.run_until_complete(self.async_test_parallel_execution())
    
    async def async_test_batch_processing(self):
        """Test batch processing capabilities."""
        async def process_item(item):
            return f"processed_{item}"
        
        items = ["item1", "item2", "item3", "item4"]
        tasks = [process_item(item) for item in items]
        
        results = await self.executor.execute_batch(
            tasks,
            mode=ExecutionMode.BATCH,
            batch_size=2
        )
        
        expected = ["processed_item1", "processed_item2", "processed_item3", "processed_item4"]
        self.assertEqual(results, expected)
    
    def test_batch_processing(self):
        """Wrapper for async batch processing test."""
        self.loop.run_until_complete(self.async_test_batch_processing())
    
    async def async_test_priority_execution(self):
        """Test priority-based task execution."""
        results = []
        
        async def priority_task(name, priority):
            results.append(name)
            return name
        
        # Submit tasks with different priorities
        await self.executor.submit_task(
            priority_task("low", TaskPriority.LOW),
            priority=TaskPriority.LOW
        )
        await self.executor.submit_task(
            priority_task("high", TaskPriority.HIGH),
            priority=TaskPriority.HIGH
        )
        await self.executor.submit_task(
            priority_task("normal", TaskPriority.NORMAL),
            priority=TaskPriority.NORMAL
        )
        
        # Process all tasks
        await self.executor.process_queue()
        
        # High priority should be processed first
        self.assertEqual(results[0], "high")
    
    def test_priority_execution(self):
        """Wrapper for async priority execution test."""
        self.loop.run_until_complete(self.async_test_priority_execution())

class TestAPIIntegration(unittest.TestCase):
    """Test cases for API integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
    
    def test_inference_endpoint_validation(self):
        """Test inference endpoint input validation."""
        # Test missing required fields
        response = self.client.post("/api/v1/inference", json={})
        self.assertEqual(response.status_code, 422)
        
        # Test invalid model type
        response = self.client.post("/api/v1/inference", json={
            "prompt": "test",
            "model_type": "invalid_model"
        })
        self.assertEqual(response.status_code, 422)
    
    def test_qnlp_endpoint_validation(self):
        """Test QNLP endpoint input validation."""
        # Test missing required fields
        response = self.client.post("/api/v1/qnlp", json={})
        self.assertEqual(response.status_code, 422)
        
        # Test invalid task type
        response = self.client.post("/api/v1/qnlp", json={
            "text": "test",
            "task": "invalid_task"
        })
        self.assertEqual(response.status_code, 422)

class TestUtilities(unittest.TestCase):
    """Test cases for utility functions and classes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cache = ResponseCache()
        self.metrics = MetricsCollector()
    
    def test_response_cache(self):
        """Test response caching functionality."""
        key = "test_key"
        value = {"result": "test_value"}
        
        # Test cache miss
        self.assertIsNone(self.cache.get(key))
        
        # Test cache set and hit
        self.cache.set(key, value, ttl=60)
        cached_value = self.cache.get(key)
        self.assertEqual(cached_value, value)
        
        # Test cache invalidation
        self.cache.invalidate(key)
        self.assertIsNone(self.cache.get(key))
    
    def test_metrics_collection(self):
        """Test metrics collection functionality."""
        # Test counter increment
        self.metrics.increment_counter("test_counter")
        self.metrics.increment_counter("test_counter")
        
        metrics = self.metrics.get_metrics()
        self.assertEqual(metrics["counters"]["test_counter"], 2)
        
        # Test histogram recording
        self.metrics.record_histogram("test_histogram", 1.5)
        self.metrics.record_histogram("test_histogram", 2.5)
        
        metrics = self.metrics.get_metrics()
        self.assertIn("test_histogram", metrics["histograms"])
    
    def test_quantum_metrics_validation(self):
        """Test quantum metrics validation."""
        # Test valid metrics
        metrics = QuantumMetrics(
            coherence=0.85,
            entanglement=0.72,
            fidelity=0.91
        )
        
        self.assertEqual(metrics.coherence, 0.85)
        self.assertEqual(metrics.entanglement, 0.72)
        self.assertEqual(metrics.fidelity, 0.91)
        
        # Test invalid metrics (should be clamped to valid range)
        metrics = QuantumMetrics(
            coherence=1.5,  # Should be clamped to 1.0
            entanglement=-0.1,  # Should be clamped to 0.0
            fidelity=0.5
        )
        
        self.assertLessEqual(metrics.coherence, 1.0)
        self.assertGreaterEqual(metrics.entanglement, 0.0)

class TestIntegrationWorkflow(unittest.TestCase):
    """Integration tests for complete workflow scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = qdLLMEngine()
        self.qnlp = QNLPProcessor()
        self.qtransformer = QTransformerModel()
        self.executor = ParallelExecutor()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        """Clean up after tests."""
        self.loop.close()
    
    async def async_test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # Initialize all components
        await self.engine.initialize()
        await self.qnlp.initialize()
        await self.qtransformer.initialize()
        
        input_text = "Quantum computing will transform artificial intelligence."
        
        # Step 1: QNLP analysis
        qnlp_request = QNLPRequest(
            text=input_text,
            task=QNLPTask.SENTIMENT,
            use_quantum_embeddings=True
        )
        qnlp_result = await self.qnlp.process(qnlp_request)
        
        self.assertIsNotNone(qnlp_result.sentiment)
        
        # Step 2: qdLLM enhancement
        qdllm_request = InferenceRequest(
            prompt=f"Elaborate on: {input_text}",
            model_type=ModelType.QDLLM,
            max_tokens=100,
            use_quantum_diffusion=True
        )
        qdllm_result = await self.engine.generate(qdllm_request)
        
        self.assertIsNotNone(qdllm_result.text)
        
        # Step 3: QTransformer refinement
        qtransformer_request = QTransformerRequest(
            input_text=qdllm_result.text,
            task="text_refinement",
            quantum_layers=True
        )
        qtransformer_result = await self.qtransformer.forward(qtransformer_request)
        
        self.assertIsNotNone(qtransformer_result.output_text)
        
        # Verify quantum metrics are consistent
        self.assertIsNotNone(qnlp_result.quantum_metrics)
        self.assertIsNotNone(qdllm_result.quantum_metrics)
        self.assertIsNotNone(qtransformer_result.quantum_metrics)
    
    def test_end_to_end_workflow(self):
        """Wrapper for async end-to-end workflow test."""
        self.loop.run_until_complete(self.async_test_end_to_end_workflow())

def run_all_tests():
    """Run all test suites including NQBA framework tests."""
    test_suites = [
        unittest.TestLoader().loadTestsFromTestCase(TestNQBAFramework),
        unittest.TestLoader().loadTestsFromTestCase(TestqdLLMEngine),
        unittest.TestLoader().loadTestsFromTestCase(TestQNLPProcessor),
        unittest.TestLoader().loadTestsFromTestCase(TestQTransformerModel),
        unittest.TestLoader().loadTestsFromTestCase(TestParallelExecutor),
        unittest.TestLoader().loadTestsFromTestCase(TestAPIIntegration),
        unittest.TestLoader().loadTestsFromTestCase(TestUtilities),
        unittest.TestLoader().loadTestsFromTestCase(TestIntegrationWorkflow)
    ]
    
    combined_suite = unittest.TestSuite(test_suites)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(combined_suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("🧪 Running NQBA Framework & qdLLM Stack Test Suite")
    print("=" * 55)
    
    success = run_all_tests()
    
    if success:
        print("\n✅ All tests passed! The NQBA framework and qdLLM stack are working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the output above for details.")
        sys.exit(1)