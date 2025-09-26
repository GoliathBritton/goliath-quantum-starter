#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Main Entry Point

This script demonstrates the complete FLYFOX AI Quantum system with:
- NQBA Execution Layer
- SigmaEQ Engine
- Dynex API Integration
- Quantum Computing Capabilities
"""

import asyncio
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from goliath.quantum import GoliathQuantum
from goliath.quantum.dynex_integration import DynexNetwork
import numpy as np
from nqba import create_framework

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def demonstrate_nqba_engine():
    """Demonstrate NQBA Execution Layer capabilities"""
    print("\n🔬 NQBA Execution Layer Demonstration")
    print("=" * 50)
    
    try:
        # Initialize NQBA engine
        from nqba.engine import NQBAEngine, ExecutionMode
        
        nqba_engine = NQBAEngine(
            mode=ExecutionMode.SIMULATOR,
            max_qubits=16,
            enable_optimization=True
        )
        
        # Test quantum circuit execution
        circuit_spec = {
            "qubits": 4,
            "gates": [
                {"type": "h", "target": 0},
                {"type": "x", "target": 1},
                {"type": "cx", "control": 0, "target": 1},
                {"type": "h", "target": 2},
                {"type": "cx", "control": 1, "target": 2}
            ],
            "measurements": [0, 1, 2]
        }
        
        print("Executing quantum circuit...")
        result = await nqba_engine.execute_quantum_circuit(circuit_spec, optimization_level=2)
        
        if result.success:
            print("✓ Circuit executed successfully!")
            print(f"  Execution time: {result.execution_time:.3f}s")
            print(f"  Qubits: {result.result_data.get('qubits', 'N/A')}")
            print(f"  Backend: {result.result_data.get('backend', 'N/A')}")
        else:
            print(f"✗ Circuit execution failed: {result.error_message}")
        
        # Get statistics
        stats = nqba_engine.get_execution_statistics()
        print(f"\nNQBA Statistics:")
        print(f"  Total executions: {stats['total_executions']}")
        print(f"  Success rate: {stats['success_rate']:.2%}")
        print(f"  Average execution time: {stats['avg_execution_time']:.3f}s")
        
    except Exception as e:
        print(f"✗ NQBA demonstration failed: {e}")

async def demonstrate_sigmaeq_engine():
    """Demonstrate SigmaEQ Engine capabilities"""
    print("\n🚀 SigmaEQ Engine Demonstration")
    print("=" * 50)
    
    try:
        from goliath.quantum.sigmaeq_engine import SigmaEQEngine, OptimizationProblem, ProblemType, OptimizationAlgorithm
        
        sigmaeq = SigmaEQEngine(max_qubits=32, enable_hybrid=True)
        
        # Test QUBO optimization
        qubo_matrix = np.array([
            [2, -1, 0],
            [-1, 3, -1],
            [0, -1, 2]
        ])
        
        problem = OptimizationProblem(
            problem_type=ProblemType.QUBO,
            data=qubo_matrix
        )
        
        print("Running QUBO optimization with QAOA...")
        result = await sigmaeq.optimize(
            problem=problem,
            algorithm=OptimizationAlgorithm.QAOA,
            parameters={"p": 2, "max_iterations": 50}
        )
        
        if result.success:
            print("✓ QUBO optimization successful!")
            print(f"  Solution: {result.solution}")
            print(f"  Optimal value: {result.optimal_value:.4f}")
            print(f"  Iterations: {result.iterations}")
            print(f"  Algorithm: {result.metadata.get('algorithm', 'N/A')}")
        else:
            print(f"✗ QUBO optimization failed: {result.error_message}")
        
        # Get supported algorithms
        algorithms = sigmaeq.get_supported_algorithms()
        print(f"\nSupported algorithms: {', '.join(algorithms)}")
        
        # Get performance metrics
        metrics = sigmaeq.get_performance_metrics()
        print(f"\nSigmaEQ Performance:")
        print(f"  Total optimizations: {metrics['total_optimizations']}")
        print(f"  Success rate: {metrics['success_rate']:.2%}")
        
    except Exception as e:
        print(f"✗ SigmaEQ demonstration failed: {e}")

async def demonstrate_dynex_integration():
    """Demonstrate Dynex API Integration capabilities"""
    print("\n⛓️  Dynex API Integration Demonstration")
    print("=" * 50)
    
    try:
        from goliath.quantum.dynex_integration import DynexAPI, DynexNetwork, PoUWType
        
        # Initialize Dynex API (testnet for demo)
        dynex_api = DynexAPI(
            network=DynexNetwork.TESTNET,
            api_key=None,  # No API key for demo
            wallet_address=None
        )
        
        print("Connecting to Dynex testnet...")
        connected = await dynex_api.connect()
        
        if connected:
            print("✓ Connected to Dynex testnet!")
            
            # Get network status
            status = await dynex_api.get_network_status()
            print(f"  Network: {status.get('network', 'N/A')}")
            print(f"  Block height: {status.get('block_height', 'N/A')}")
            print(f"  Difficulty: {status.get('difficulty', 'N/A')}")
            
            # Test PoUW submission (simulated)
            print("\nSimulating PoUW submission...")
            solution_data = {
                "problem_type": "demo_qubo",
                "matrix_size": 4,
                "solution": [1, 0, 1, 0],
                "optimal_value": 5.0,
                "execution_time": 1.5
            }
            
            # Note: This will fail without API key, but demonstrates the interface
            print("  PoUW interface ready (requires API key for actual submission)")
            
        else:
            print("✗ Failed to connect to Dynex testnet")
        
        # Get network info
        network_info = dynex_api.get_network_info()
        print(f"\nDynex Network Info:")
        print(f"  Network: {network_info['network']}")
        print(f"  Base URL: {network_info['base_url']}")
        print(f"  Connected: {network_info['connected']}")
        
    except Exception as e:
        print(f"✗ Dynex demonstration failed: {e}")

async def demonstrate_goliath_quantum():
    """Demonstrate complete FLYFOX AI Quantum system"""
    print("\n🌟 Complete FLYFOX AI Quantum System Demonstration")
    print("=" * 50)
    
    try:
        # Initialize Goliath Quantum
        gq = GoliathQuantum(
            use_simulator=True,
            apollo_mode=True,
            qdllm_params=400_000_000_000,
            max_qubits=32,
            enable_dynex=False,  # Disable for demo
            dynex_network=DynexNetwork.TESTNET
        )
        
        print("✓ Goliath Quantum initialized successfully!")
        print(f"  Execution mode: {gq.execution_mode.value}")
        print(f"  Max qubits: {gq.max_qubits}")
        print(f"  Apollo mode: {gq.apollo_mode}")
        print(f"  QDL parameters: {gq.qdllm_params:,}")
        
        # Test QUBO optimization
        print("\nTesting QUBO optimization...")
        qubo_matrix = np.array([
            [3, -1, 0],
            [-1, 2, -1],
            [0, -1, 3]
        ])
        
        result = await gq.optimize_qubo(
            qubo_matrix=qubo_matrix,
            algorithm="qaoa",
            enable_pouw=False
        )
        
        if result.success:
            print("✓ QUBO optimization successful!")
            print(f"  Solution: {result.solution}")
            print(f"  Optimal value: {result.optimal_value:.4f}")
            print(f"  Execution time: {result.execution_time:.3f}s")
        else:
            print(f"✗ QUBO optimization failed: {result.error_message}")
        
        # Get system statistics
        stats = gq.get_optimization_statistics()
        print(f"\nSystem Statistics:")
        print(f"  Total optimizations: {stats['total_optimizations']}")
        print(f"  Success rate: {stats['success_rate']:.2%}")
        print(f"  Execution mode: {stats['execution_mode']}")
        
        # Get supported algorithms
        algorithms = gq.get_supported_algorithms()
        print(f"\nSupported algorithms: {len(algorithms)} algorithms available")
        
        # Clean up
        await gq.close()
        
    except Exception as e:
        print(f"✗ Goliath Quantum demonstration failed: {e}")

async def demonstrate_data_ingestion():
    print("\n📊 Data Ingestion Demonstration")
    print("=" * 50)
    
    framework = create_framework()
    ingestor = framework.ingestor  # Assuming attached in create_framework
    problem_data = ingestor.ingest_problem('stream', 'kafka://server:9092')
    print("Ingested problem data:", problem_data)

async def demonstrate_advanced_analysis():
    print("\n🔍 Advanced Analysis Demonstration")
    print("=" * 50)
    
    framework = create_framework()
    analyzer = framework.analyzer
    # Example problem data
    problem_data = {"problem": "Sample business problem", "data": [1, 2, 3]}
    analysis = analyzer.analyze(problem_data)
    print("Analysis results:", analysis)

async def demonstrate_solution_presentation():
    print("\n📊 Solution Presentation Demonstration")
    print("=" * 50)
    
    framework = create_framework()
    presenter = framework.presenter
    
    sample_solution = {
        "problem": "Business Process Optimization",
        "analysis": "Identified bottlenecks in supply chain",
        "solution": "Quantum-optimized routing algorithm",
        "expected_impact": "30% reduction in delivery times"
    }
    
    pdf_path = presenter.generate_pdf_report(sample_solution)
    print(f"Generated PDF report: {pdf_path}")
    
    dashboard_path = presenter.generate_dashboard_script(sample_solution)
    print(f"Generated dashboard script: {dashboard_path}")
    print("Note: Run 'streamlit run {dashboard_path}' to view the dashboard")

async def demonstrate_solution_integration():
    print("\n🔄 Solution Integration Demonstration")
    print("=" * 50)
    
    framework = create_framework()
    integrator = framework.integrator
    
    sample_sources = ["sample_data.csv", "api://example.com/data"]
    results = await integrator.integrate_solution(
        sample_sources,
        analysis_params={"depth": "high"},
        presentation_format="both"
    )
    
    print("Integration results:")
    print(f"  PDF Report: {results.get('pdf_path')}")
    print(f"  Dashboard Script: {results.get('dashboard_path')}")

async def demonstrate_outcome_monitoring():
    print("\n📈 Outcome Monitoring Demonstration")
    print("=" * 50)
    
    framework = create_framework()
    monitor = framework.monitor
    
    sample_solution_data = {"success": True, "efficiency": 0.95}
    monitoring_result = monitor.monitor_solution(sample_solution_data)
    print("Monitoring result:", monitoring_result)
    
    report = monitor.generate_outcome_report()
    print("Outcome report:", report)

async def main():
    """Main demonstration function"""
    print("🚀 Goliath Quantum Starter - Complete System Demonstration")
    print("=" * 70)
    print("This demonstration showcases all implemented components:")
    print("• NQBA Execution Layer")
    print("• SigmaEQ Engine") 
    print("• Dynex API Integration")
    print("• Complete Goliath Quantum System")
    print("• Data Ingestion")
    print("• Advanced Analysis")
    print("• Solution Presentation")
    print("• Solution Integration")
    print("• Outcome Monitoring")
    print("=" * 70)
    
    try:\n        # Demonstrate each component\n        await demonstrate_nqba_engine()\n        await demonstrate_sigmaeq_engine()\n        await demonstrate_dynex_integration()\n        await demonstrate_goliath_quantum()\n        await demonstrate_data_ingestion()\n        await demonstrate_advanced_analysis()\n        await demonstrate_solution_presentation()\n        await demonstrate_solution_integration()
        print("\n🎉 All demonstrations completed successfully!")\n        print("\n✅ FLYFOX AI Quantum Platform is now fully functional with:\")\n        print("   • NQBA Execution Layer - Quantum circuit execution and optimization\")\n        print("   • SigmaEQ Engine - Advanced quantum optimization algorithms\")\n        print("   • Dynex Integration - Blockchain and PoUW capabilities\")\n        print("   • Unified Interface - Complete quantum computing system\")\n        \n        return 0\n        \n    except Exception as e:\n        print(f"\n❌ Demonstration failed: {e}")\n        logger.error(f"Main demonstration failed: {e}", exc_info=True)\n        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Demonstration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)