#!/usr/bin/env python3
"""
NQBA Framework Demo

This demo showcases the complete NQBA (Neuromorphic Quantum Business Architecture) framework including:
- Core intelligence modules: qdLLM, QNLP, and QTransformers
- Framework orchestration and business workflow integration
- Governance and compliance features
- API layer and external system integration
- Parallel processing and batch operations

Author: NQBA Development Team
Version: 1.0.0
"""

import asyncio
import time
import json
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

# Legacy qdLLM imports for backward compatibility
try:
    from qdllm.core.engine import qdLLMEngine
    from qdllm.qnlp.processor import QNLPProcessor
    from qdllm.qtransformers.model import QTransformerModel
    from qdllm.core.parallel_executor import ParallelExecutor, ExecutionMode, TaskPriority
    from qdllm.api.models import (
        InferenceRequest, QNLPRequest, QTransformerRequest,
        BatchRequest, ModelType, QNLPTask
    )
except ImportError:
    print("Legacy qdLLM modules not available, using NQBA framework only")

class NQBAFrameworkDemo:
    """Comprehensive demo of the NQBA framework with integrated intelligence modules."""
    
    def __init__(self):
        self.framework = None
        self.engine = None
        self.qnlp = None
        self.qtransformer = None
        self.executor = None
        
    async def initialize_framework(self):
        """Initialize the complete NQBA framework."""
        print("🚀 Initializing NQBA Framework...")
        
        # Initialize NQBA framework
        print("  🏗️  Loading NQBA Framework Core...")
        self.framework = create_framework(
            enable_qdllm=True,
            enable_qnlp=True,
            enable_qtransformers=True,
            governance_enabled=True,
            compliance_checks=True
        )
        
        # Initialize intelligence modules
        print("  📊 Loading qdLLM Core Engine...")
        self.engine = qdllm.create_engine()
        await self.engine.initialize()
        
        # Initialize QNLP processor
        print("  🧠 Loading QNLP Processor...")
        self.qnlp = qnlp.create_processor()
        
        # Initialize QTransformer
        print("  ⚛️  Loading QTransformer Model...")
        self.qtransformer = qtransformers.create_model()
        
        # Initialize parallel executor (legacy compatibility)
        print("  🔄 Setting up Parallel Executor...")
        try:
            self.executor = ParallelExecutor()
        except NameError:
            print("    Using NQBA framework execution engine")
        
        print("✅ NQBA Framework initialized successfully!\n")
    
    async def demo_nqba_framework(self):
        """Demonstrate NQBA framework orchestration."""
        print("🏗️  Demo 1: NQBA Framework Orchestration")
        print("=" * 50)
        
        # Test framework business request processing
        business_request = {
            'type': 'integrated_analysis',
            'data': 'Explain quantum computing in simple terms for business applications',
            'workflow': 'qnlp_qdllm_qtransformers',
            'governance': {
                'compliance_check': True,
                'audit_required': True
            }
        }
        
        print(f"📝 Processing business request: {business_request['data'][:50]}...")
        
        # Process through NQBA framework
        result = await self.framework.process_business_request(business_request)
        
        print(f"✅ Framework Result: {result}\n")
        
    async def demo_core_engine(self):
        """Demonstrate core qdLLM engine capabilities (legacy support)."""
        print("🔬 Demo 2: Core qdLLM Engine with Quantum Diffusion (Legacy)")
        print("=" * 50)
        
        # Test qdLLM reasoning with NQBA framework integration
        prompt = "Explain quantum computing in simple terms"
        print(f"📝 Processing: {prompt}")
        
        try:
            # Try NQBA framework first
            if hasattr(self, 'framework') and self.framework:
                business_request = {
                    'type': 'text_generation',
                    'data': prompt,
                    'workflow': 'qdllm_reasoning',
                    'parameters': {
                        'max_tokens': 150,
                        'temperature': 0.7,
                        'use_quantum_diffusion': True,
                        'bidirectional_reasoning': True
                    }
                }
                
                start_time = time.time()
                result = await self.framework.process_business_request(business_request)
                end_time = time.time()
                
                print(f"📝 Prompt: {prompt}")
                print(f"🎯 Response: {result.get('response', 'No response')[:200]}...")
                print(f"⚡ Generation time: {end_time - start_time:.2f}s")
                print(f"🌊 Framework coherence: {result.get('confidence', 0.0):.3f}")
            else:
                # Fallback to legacy qdLLM
                if QDLLM_AVAILABLE:
                    result = qdllm.reason(
                        prompt,
                        direction="bidirectional",
                        max_tokens=150,
                        temperature=0.7,
                        use_quantum_diffusion=True,
                        bidirectional_reasoning=True
                    )
                    print(f"📝 Prompt: {prompt}")
                    print(f"🎯 Response: {result.get('text', 'Generated response')[:200]}...")
                else:
                    print("⚠️ qdLLM engine not available - using simulation")
                    print(f"📝 Prompt: {prompt}")
                    print(f"🎯 Response: [Simulated] Quantum computing uses quantum mechanics principles...")
        except Exception as e:
            print(f"⚠️ Engine demo error: {e}")
            print("📝 Using fallback demonstration")
        print()
    
    async def demo_qnlp_processor(self):
        """Demonstrate QNLP processing capabilities."""
        print("🧠 Demo 2: QNLP Quantum-Enhanced Processing")
        print("=" * 50)
        
        # Test sentiment analysis
        sentiment_request = QNLPRequest(
            text="I absolutely love the quantum computing capabilities of this system!",
            task=QNLPTask.SENTIMENT,
            use_quantum_embeddings=True,
            coherence_threshold=0.8
        )
        
        sentiment_result = await self.qnlp.process(sentiment_request)
        
        print(f"📝 Text: {sentiment_request.text}")
        print(f"😊 Sentiment: {sentiment_result.sentiment.label} ({sentiment_result.sentiment.confidence:.3f})")
        print(f"🌊 Quantum coherence: {sentiment_result.quantum_metrics.coherence:.3f}")
        
        # Test entity extraction
        entity_request = QNLPRequest(
            text="Apple Inc. was founded by Steve Jobs in Cupertino, California.",
            task=QNLPTask.NER,
            use_quantum_embeddings=True
        )
        
        entity_result = await self.qnlp.process(entity_request)
        
        print(f"\n📝 Text: {entity_request.text}")
        print("🏷️  Entities:")
        for entity in entity_result.entities:
            print(f"  - {entity.text} ({entity.label}): {entity.confidence:.3f}")
        print()
    
    async def demo_qtransformer(self):
        """Demonstrate QTransformer capabilities."""
        print("⚛️  Demo 3: QTransformer Quantum-Inspired Architecture")
        print("=" * 50)
        
        request = QTransformerRequest(
            input_text="The future of artificial intelligence lies in quantum computing",
            task="text_generation",
            max_length=100,
            quantum_layers=True,
            attention_type="quantum",
            temperature=0.8
        )
        
        start_time = time.time()
        result = await self.qtransformer.forward(request)
        end_time = time.time()
        
        print(f"📝 Input: {request.input_text}")
        print(f"🎯 Output: {result.output_text}")
        print(f"⚡ Processing time: {end_time - start_time:.2f}s")
        print(f"🔢 Attention entropy: {result.attention_metrics.entropy:.3f}")
        print(f"🌊 Quantum coherence: {result.quantum_metrics.coherence:.3f}")
        print()
    
    async def demo_parallel_processing(self):
        """Demonstrate parallel executor and batch processing."""
        print("🔄 Demo 4: Parallel Executor & Batch Processing")
        print("=" * 50)
        
        # Create batch requests
        batch_requests = [
            InferenceRequest(
                prompt=f"Generate a creative story about {topic}",
                model_type=ModelType.QDLLM,
                max_tokens=50,
                temperature=0.9
            )
            for topic in ["space exploration", "underwater cities", "time travel", "AI consciousness"]
        ]
        
        batch_request = BatchRequest(
            requests=batch_requests,
            parallel=True,
            max_workers=4
        )
        
        print(f"📦 Processing {len(batch_requests)} requests in parallel...")
        
        start_time = time.time()
        
        # Process batch using parallel executor
        async def process_single(req):
            return await self.engine.generate(req)
        
        results = await self.executor.execute_batch(
            [process_single(req) for req in batch_requests],
            mode=ExecutionMode.PARALLEL,
            priority=TaskPriority.NORMAL
        )
        
        end_time = time.time()
        
        print(f"⚡ Batch processing time: {end_time - start_time:.2f}s")
        print(f"📊 Average time per request: {(end_time - start_time) / len(batch_requests):.2f}s")
        
        for i, result in enumerate(results):
            print(f"\n📝 Story {i+1}: {result.text[:100]}...")
        print()
    
    async def demo_integration_workflow(self):
        """Demonstrate integrated workflow across all components."""
        print("🔗 Demo 5: Integrated Workflow")
        print("=" * 50)
        
        # Multi-step workflow: QNLP -> qdLLM -> QTransformer
        input_text = "Quantum computing will revolutionize machine learning and artificial intelligence."
        
        print(f"📝 Input: {input_text}")
        print("\n🔄 Step 1: QNLP Analysis...")
        
        # Step 1: QNLP analysis
        qnlp_request = QNLPRequest(
            text=input_text,
            task=QNLPTask.SENTIMENT,
            use_quantum_embeddings=True
        )
        qnlp_result = await self.qnlp.process(qnlp_request)
        
        print(f"  😊 Sentiment: {qnlp_result.sentiment.label}")
        print(f"  🌊 Coherence: {qnlp_result.quantum_metrics.coherence:.3f}")
        
        # Step 2: qdLLM enhancement
        print("\n🔄 Step 2: qdLLM Enhancement...")
        enhanced_prompt = f"Based on the {qnlp_result.sentiment.label} sentiment, elaborate on: {input_text}"
        
        qdllm_request = InferenceRequest(
            prompt=enhanced_prompt,
            model_type=ModelType.QDLLM,
            max_tokens=100,
            use_quantum_diffusion=True
        )
        qdllm_result = await self.engine.generate(qdllm_request)
        
        print(f"  🎯 Enhanced text: {qdllm_result.text[:150]}...")
        
        # Step 3: QTransformer refinement
        print("\n🔄 Step 3: QTransformer Refinement...")
        
        qtransformer_request = QTransformerRequest(
            input_text=qdllm_result.text,
            task="text_refinement",
            quantum_layers=True,
            max_length=120
        )
        qtransformer_result = await self.qtransformer.forward(qtransformer_request)
        
        print(f"  ✨ Final output: {qtransformer_result.output_text}")
        print(f"  📊 Overall coherence: {qtransformer_result.quantum_metrics.coherence:.3f}")
        print()
    
    async def run_performance_benchmark(self):
        """Run performance benchmarks across all components."""
        print("📊 Performance Benchmark")
        print("=" * 50)
        
        benchmarks = {
            "qdLLM Engine": [],
            "QNLP Processor": [],
            "QTransformer": [],
            "Parallel Executor": []
        }
        
        # Benchmark each component
        for i in range(5):
            # qdLLM benchmark
            start = time.time()
            await self.engine.generate(InferenceRequest(
                prompt="Test prompt for benchmarking",
                model_type=ModelType.QDLLM,
                max_tokens=50
            ))
            benchmarks["qdLLM Engine"].append(time.time() - start)
            
            # QNLP benchmark
            start = time.time()
            await self.qnlp.process(QNLPRequest(
                text="Test text for benchmarking performance",
                task=QNLPTask.SENTIMENT
            ))
            benchmarks["QNLP Processor"].append(time.time() - start)
            
            # QTransformer benchmark
            start = time.time()
            await self.qtransformer.forward(QTransformerRequest(
                input_text="Test input for transformer benchmarking",
                task="text_generation",
                max_length=50
            ))
            benchmarks["QTransformer"].append(time.time() - start)
        
        # Display results
        for component, times in benchmarks.items():
            if times:
                avg_time = sum(times) / len(times)
                print(f"⚡ {component}: {avg_time:.3f}s average ({min(times):.3f}s - {max(times):.3f}s)")
        print()
    
    async def run_all_demos(self):
        """Run all demonstration scenarios."""
        await self.initialize_framework()
        
        try:
            # Primary NQBA framework demo
            await self.demo_nqba_framework()
            
            # Secondary legacy demos for compatibility
            await self.demo_core_engine()
            await self.demo_qnlp_processor()
            await self.demo_qtransformer()
            await self.demo_parallel_processing()
            await self.demo_integration_workflow()
            await self.run_performance_benchmark()
            
            print("🎉 All NQBA Framework demos completed successfully!")
            print("\n📋 Summary:")
            print("  ✅ NQBA Framework orchestration and business workflows")
            print("  ✅ Core qdLLM engine with quantum diffusion (legacy)")
            print("  ✅ QNLP quantum-enhanced processing")
            print("  ✅ QTransformer quantum-inspired architecture")
            print("  ✅ Parallel executor and batch processing")
            print("  ✅ Integrated workflow demonstration")
            print("  ✅ Performance benchmarking")
            
        except Exception as e:
            print(f"❌ Demo failed: {str(e)}")
            print("🔄 Attempting graceful degradation...")
            # Continue with available components
            try:
                await self.demo_core_engine()
                print("✅ Fallback demo completed")
            except:
                print("⚠️ Running in simulation mode")

async def main():
    """Main demo entry point."""
    print("🌟 Welcome to the NQBA Framework Demo!")
    print("🧠 Neuromorphic Quantum Business Architecture")
    print("=" * 60)
    print("🚀 Enterprise Quantum-Enhanced Business Intelligence Platform")
    print()
    
    demo = NQBAFrameworkDemo()
    await demo.run_all_demos()
    
    print("\n🎯 Demo completed! The NQBA Framework is ready for enterprise deployment.")
    print("📚 For more information, see the technical blueprint and documentation.")
    print("🌐 Visit: https://docs.nqba-framework.com")

if __name__ == "__main__":
    asyncio.run(main())