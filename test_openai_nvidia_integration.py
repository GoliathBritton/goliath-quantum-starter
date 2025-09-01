#!/usr/bin/env python3
"""
Test Script for OpenAI and NVIDIA Integration
============================================
Demonstrates the enhanced integration capabilities:
- OpenAI with quantum enhancement
- NVIDIA cuQuantum simulation
- NVIDIA TensorRT acceleration
- GPU monitoring and optimization
"""

import asyncio
import json
import time
from datetime import datetime
import numpy as np

# Import our integrations
from src.nqba_stack.openai_integration import openai_integration, OpenAIRequest
from src.nqba_stack.nvidia_integration import (
    nvidia_integration,
    QuantumSimulationRequest,
    TensorRTRequest,
)
from src.nqba_stack.mcp_handler import dispatch_tool


async def test_openai_integration():
    """Test OpenAI integration with quantum enhancement"""
    print("🚀 Testing OpenAI Integration...")
    print("=" * 50)

    # Test 1: Basic text generation
    print("\n1. Basic Text Generation:")
    request = OpenAIRequest(
        prompt="Explain quantum computing in simple terms",
        model="gpt-4o",
        temperature=0.7,
        max_tokens=200,
        use_quantum_enhancement=True,
    )

    try:
        response = await openai_integration.generate(request)
        print(f"✅ Response: {response.content[:100]}...")
        print(f"   Model: {response.model}")
        print(f"   Quantum Enhanced: {response.quantum_enhanced}")
        print(f"   Processing Time: {response.processing_time:.2f}s")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Streaming generation
    print("\n2. Streaming Generation:")
    request.stream = True
    try:
        chunks = []
        async for chunk in openai_integration.generate(request):
            chunks.append(chunk.content)
            print(f"   Chunk: {chunk.content}")

        full_response = "".join(chunks)
        print(f"✅ Full Response: {full_response[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Embeddings
    print("\n3. Embeddings Generation:")
    try:
        embeddings = await openai_integration.get_embeddings(
            text="Quantum computing is the future", model="text-embedding-3-small"
        )
        print(f"✅ Embeddings: {len(embeddings)} dimensions")
        print(f"   Sample: {embeddings[:5]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 50)


async def test_nvidia_integration():
    """Test NVIDIA integration capabilities"""
    print("🚀 Testing NVIDIA Integration...")
    print("=" * 50)

    # Test 1: GPU Information
    print("\n1. GPU Information:")
    try:
        gpu_info = nvidia_integration.gpu_info
        print(f"✅ GPUs Available: {len(gpu_info)}")

        for gpu in gpu_info:
            print(f"   GPU {gpu.device_id}: {gpu.name}")
            print(f"     Memory: {gpu.memory_total}MB")
            print(f"     CUDA Cores: {gpu.cuda_cores}")
            print(f"     Tensor Cores: {gpu.tensor_cores}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Quantum Simulation
    print("\n2. Quantum Simulation (QAOA):")
    request = QuantumSimulationRequest(
        qubits=4, algorithm="qaoa", use_gpu=True, max_iterations=100
    )

    try:
        result = await nvidia_integration.simulate_quantum(request)
        print(f"✅ Simulation Success: {result.success}")
        print(f"   Energy: {result.energy:.6f}")
        print(f"   Iterations: {result.iterations}")
        print(f"   Processing Time: {result.processing_time:.3f}s")
        print(f"   GPU Used: {result.gpu_used}")

        if result.result is not None:
            print(f"   State Vector Shape: {result.result.shape}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: TensorRT Inference
    print("\n3. TensorRT Inference Acceleration:")
    # Create sample input data
    input_data = np.random.random((1, 10)).astype(np.float32)

    request = TensorRTRequest(
        model_path="sample_model.trt",
        input_data=input_data,
        batch_size=1,
        precision="fp16",
        optimization_level=3,
        use_gpu=True,
    )

    try:
        result = await nvidia_integration.accelerate_inference(request)
        print(f"✅ Inference Success: {result.success}")
        print(
            f"   Output Shape: {result.output.shape if result.output is not None else 'None'}"
        )
        print(f"   Inference Time: {result.inference_time:.3f}s")
        print(f"   Throughput: {result.throughput:.1f} samples/s")
        print(f"   GPU Used: {result.gpu_used}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 4: Energy Optimization
    print("\n4. Energy Optimization:")
    try:
        optimization = nvidia_integration.optimize_energy_usage("quantum")
        print(f"✅ Workload Type: {optimization['workload_type']}")
        print(f"   Recommendations:")
        for rec in optimization["recommendations"]:
            print(f"     - {rec}")

        if "gpu_power_modes" in optimization:
            print(f"   GPU Power Modes: {optimization['gpu_power_modes']}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 50)


async def test_mcp_integration():
    """Test MCP tool integration"""
    print("🚀 Testing MCP Tool Integration...")
    print("=" * 50)

    # Test 1: OpenAI MCP Tool
    print("\n1. OpenAI Generate MCP Tool:")
    payload = {
        "prompt": "What is the future of quantum AI?",
        "model": "gpt-4o",
        "temperature": 0.8,
        "max_tokens": 150,
        "use_quantum_enhancement": True,
    }

    try:
        result = await dispatch_tool("openai.generate", payload, user="test_user")
        print(f"✅ Success: {result['success']}")
        if result["success"]:
            print(f"   Result: {result['result'][:100]}...")
            print(f"   Model: {result.get('model', 'Unknown')}")
            print(f"   Quantum Enhanced: {result.get('quantum_enhanced', False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: NVIDIA Quantum Simulation MCP Tool
    print("\n2. NVIDIA Quantum Simulation MCP Tool:")
    payload = {"qubits": 3, "algorithm": "qaoa", "use_gpu": True, "max_iterations": 50}

    try:
        result = await dispatch_tool(
            "nvidia.simulate.quantum", payload, user="test_user"
        )
        print(f"✅ Success: {result['success']}")
        if result["success"]:
            print(f"   Energy: {result.get('energy', 'N/A')}")
            print(f"   Processing Time: {result.get('processing_time', 'N/A')}s")
            print(f"   GPU Used: {result.get('gpu_used', False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: NVIDIA GPU Info MCP Tool
    print("\n3. NVIDIA GPU Info MCP Tool:")
    payload = {"include_memory": True, "include_performance": False}

    try:
        result = await dispatch_tool("nvidia.gpu.info", payload, user="test_user")
        print(f"✅ Success: {result['success']}")
        if result["success"]:
            print(f"   Total GPUs: {result.get('total_gpus', 0)}")
            print(f"   CUDA Available: {result.get('cuda_available', False)}")
            print(f"   cuQuantum Available: {result.get('cuquantum_available', False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 50)


async def test_performance_benchmarks():
    """Test performance benchmarks"""
    print("🚀 Testing Performance Benchmarks...")
    print("=" * 50)

    # Benchmark 1: OpenAI vs Quantum Generation
    print("\n1. OpenAI vs Quantum Generation Benchmark:")

    prompts = [
        "Explain machine learning",
        "What is quantum computing?",
        "Describe artificial intelligence",
    ]

    # Test OpenAI
    start_time = time.time()
    for prompt in prompts:
        request = OpenAIRequest(
            prompt=prompt, max_tokens=100, use_quantum_enhancement=False
        )
        try:
            response = await openai_integration.generate(request)
            print(f"   OpenAI: {response.processing_time:.3f}s")
        except:
            print(f"   OpenAI: Failed")

    openai_time = time.time() - start_time

    # Test Quantum
    start_time = time.time()
    for prompt in prompts:
        request = OpenAIRequest(
            prompt=prompt, max_tokens=100, use_quantum_enhancement=True
        )
        try:
            response = await openai_integration.generate(request)
            print(f"   Quantum: {response.processing_time:.3f}s")
        except:
            print(f"   Quantum: Failed")

    quantum_time = time.time() - start_time

    print(f"✅ OpenAI Total: {openai_time:.3f}s")
    print(f"✅ Quantum Total: {quantum_time:.3f}s")

    # Benchmark 2: GPU vs CPU Quantum Simulation
    print("\n2. GPU vs CPU Quantum Simulation Benchmark:")

    qubit_counts = [3, 4, 5]

    for qubits in qubit_counts:
        print(f"   {qubits} qubits:")

        # GPU simulation
        request = QuantumSimulationRequest(
            qubits=qubits, use_gpu=True, max_iterations=100
        )
        try:
            result = await nvidia_integration.simulate_quantum(request)
            print(f"     GPU: {result.processing_time:.3f}s")
        except:
            print(f"     GPU: Failed")

        # CPU simulation
        request.use_gpu = False
        try:
            result = await nvidia_integration.simulate_quantum(request)
            print(f"     CPU: {result.processing_time:.3f}s")
        except:
            print(f"     CPU: Failed")

    print("\n" + "=" * 50)


async def main():
    """Main test function"""
    print("🚀 FLYFOX AI - OpenAI & NVIDIA Integration Test Suite")
    print("=" * 60)
    print(f"Timestamp: {datetime.now()}")
    print("=" * 60)

    try:
        # Run all tests
        await test_openai_integration()
        await test_nvidia_integration()
        await test_mcp_integration()
        await test_performance_benchmarks()

        print("\n🎉 All tests completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
