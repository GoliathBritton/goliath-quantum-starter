"""
NQBA Core - FLYFOX AI Quantum Hub Demo
Comprehensive demonstration of the integrated Neuromorphic Quantum Business Architecture
"""
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# Import NQBA components
from src.nqba_stack.core.business_assessment import (
    assess_business_comprehensive,
    AuditType,
    BEMFramework
)
from src.nqba_stack.core.scheduled_audits import (
    subscribe_company,
    get_subscription_stats,
    SubscriptionTier,
    AuditFrequency
)
from src.nqba_stack.core.automated_data_collection import (
    get_audit_readiness,
    get_data_summary,
    add_custom_data_point,
    DataSource,
    DataCategory
)

# Import FLYFOX AI Quantum Hub components
from src.nqba_stack.core.flyfox_quantum_hub import (
    flyfox_quantum_hub,
    QuantumOperation,
    QuantumProvider,
    submit_quantum_request,
    get_request_status,
    register_third_party_integration,
    get_available_providers,
    get_quantum_usage_stats
)

# Import Quantum Algorithms
from src.nqba_stack.algorithms.runner import (
    run_algorithm,
    AlgorithmType,
    AlgorithmConfig,
    BackendType
)

class NQBADemo:
    """Comprehensive NQBA demonstration"""
    
    def __init__(self):
        self.demo_results = {}
        self.client_id = None
    
    async def run_comprehensive_demo(self):
        """Run the complete NQBA demonstration"""
        print("🚀 FLYFOX AI - NQBA Core Demo")
        print("=" * 50)
        
        # Step 1: Register third-party integration
        await self.demo_third_party_registration()
        
        # Step 2: Business Assessment with Quantum Optimization
        await self.demo_business_assessment()
        
        # Step 3: Subscription Management
        await self.demo_subscription_management()
        
        # Step 4: Automated Data Collection
        await self.demo_data_collection()
        
        # Step 5: Quantum Computing Operations
        await self.demo_quantum_operations()
        
        # Step 6: Quantum Algorithms Demo
        await self.demo_quantum_algorithms()
        
        # Step 7: Usage Statistics
        await self.demo_usage_statistics()
        
        # Step 8: Summary
        self.print_demo_summary()
    
    async def demo_third_party_registration(self):
        """Demonstrate third-party integration registration"""
        print("\n📋 Step 1: Third-Party Integration Registration")
        print("-" * 40)
        
        try:
            # Register a demo client
            client_id = await register_third_party_integration(
                client_name="Demo Corporation",
                api_key="demo_api_key_12345",
                allowed_operations=[
                    QuantumOperation.OPTIMIZATION,
                    QuantumOperation.QUANTUM_LLM,
                    QuantumOperation.PORTFOLIO_OPTIMIZATION,
                    QuantumOperation.RISK_ASSESSMENT
                ],
                rate_limit_per_hour=1000,
                webhook_url="https://demo-corp.com/webhooks/quantum"
            )
            
            self.client_id = client_id
            self.demo_results["registration"] = {
                "status": "success",
                "client_id": client_id,
                "message": "Third-party integration registered successfully"
            }
            
            print(f"✅ Registered client: {client_id}")
            print(f"   Company: Demo Corporation")
            print(f"   Allowed operations: Optimization, Quantum LLM, Portfolio Optimization, Risk Assessment")
            print(f"   Rate limit: 1000 requests/hour")
            
        except Exception as e:
            print(f"❌ Registration failed: {e}")
            self.demo_results["registration"] = {"status": "failed", "error": str(e)}
    
    async def demo_business_assessment(self):
        """Demonstrate comprehensive business assessment with quantum optimization"""
        print("\n🏢 Step 2: Business Assessment with Quantum Optimization")
        print("-" * 50)
        
        try:
            # Perform comprehensive business assessment
            assessment_result = await assess_business_comprehensive(
                company_name="TechCorp Solutions",
                industry="Technology",
                company_size="Mid-market",
                audit_types=[
                    AuditType.FINANCIAL,
                    AuditType.OPERATIONAL,
                    AuditType.COMPLIANCE,
                    AuditType.IT_AUDIT
                ],
                framework=BEMFramework.BALDRIGE,
                include_quantum_optimization=True
            )
            
            self.demo_results["business_assessment"] = assessment_result
            
            print(f"✅ Business assessment completed for: TechCorp Solutions")
            print(f"   Overall Score: {assessment_result.overall_score:.2f}/100")
            print(f"   Framework: {assessment_result.framework.value}")
            print(f"   Quantum Optimization: {assessment_result.quantum_optimization_applied}")
            print(f"   Recommendations: {len(assessment_result.recommendations)} items")
            
            # Show top recommendations
            print("\n   Top Recommendations:")
            for i, rec in enumerate(assessment_result.recommendations[:3], 1):
                print(f"   {i}. {rec.title} (Priority: {rec.priority})")
            
        except Exception as e:
            print(f"❌ Business assessment failed: {e}")
            self.demo_results["business_assessment"] = {"status": "failed", "error": str(e)}
    
    async def demo_subscription_management(self):
        """Demonstrate NQBA subscription management"""
        print("\n💳 Step 3: Subscription Management")
        print("-" * 30)
        
        try:
            # Subscribe a company to NQBA services
            subscription_id = await subscribe_company(
                company_name="Innovation Labs Inc",
                tier=SubscriptionTier.ENTERPRISE,
                audit_types=[
                    AuditType.FINANCIAL,
                    AuditType.OPERATIONAL,
                    AuditType.COMPLIANCE,
                    AuditType.IT_AUDIT,
                    AuditType.SMETA
                ],
                contact_email="ceo@innovationlabs.com"
            )
            
            # Get subscription statistics
            stats = await get_subscription_stats()
            
            self.demo_results["subscription"] = {
                "subscription_id": subscription_id,
                "stats": stats
            }
            
            print(f"✅ Subscribed: Innovation Labs Inc")
            print(f"   Tier: Enterprise")
            print(f"   Subscription ID: {subscription_id}")
            print(f"   Total subscribers: {stats['total_subscribers']}")
            print(f"   Active subscriptions: {stats['active_subscriptions']}")
            
        except Exception as e:
            print(f"❌ Subscription management failed: {e}")
            self.demo_results["subscription"] = {"status": "failed", "error": str(e)}
    
    async def demo_data_collection(self):
        """Demonstrate automated data collection"""
        print("\n📊 Step 4: Automated Data Collection")
        print("-" * 35)
        
        try:
            company_id = "demo_company_001"
            
            # Add custom data points
            await add_custom_data_point({
                "company_id": company_id,
                "source": DataSource.FINANCIAL_SYSTEM,
                "category": DataCategory.FINANCIAL,
                "data": {
                    "revenue": 2500000,
                    "expenses": 1800000,
                    "profit_margin": 0.28,
                    "cash_flow": 450000
                },
                "timestamp": datetime.now().isoformat()
            })
            
            await add_custom_data_point({
                "company_id": company_id,
                "source": DataSource.CRM_SYSTEM,
                "category": DataCategory.CUSTOMER,
                "data": {
                    "total_customers": 1250,
                    "customer_satisfaction": 4.2,
                    "churn_rate": 0.08,
                    "lifetime_value": 8500
                },
                "timestamp": datetime.now().isoformat()
            })
            
            # Get audit readiness
            readiness = await get_audit_readiness(company_id)
            
            # Get data summary
            summary = await get_data_summary(company_id)
            
            self.demo_results["data_collection"] = {
                "readiness": readiness,
                "summary": summary
            }
            
            print(f"✅ Data collection completed for: {company_id}")
            print(f"   Audit Readiness: {readiness['readiness_score']:.1f}%")
            print(f"   Data Sources: {len(summary['data_sources'])}")
            print(f"   Total Data Points: {summary['total_data_points']}")
            print(f"   Last Updated: {summary['last_updated']}")
            
        except Exception as e:
            print(f"❌ Data collection failed: {e}")
            self.demo_results["data_collection"] = {"status": "failed", "error": str(e)}
    
    async def demo_quantum_operations(self):
        """Demonstrate quantum computing operations"""
        print("\n⚛️ Step 5: Quantum Computing Operations")
        print("-" * 35)
        
        if not self.client_id:
            print("❌ No client registered for quantum operations")
            return
        
        try:
            # Get available providers
            providers = await get_available_providers()
            print(f"✅ Available quantum providers: {len(providers)}")
            
            # Submit quantum optimization request
            optimization_request_id = await submit_quantum_request(
                client_id=self.client_id,
                operation_type=QuantumOperation.OPTIMIZATION,
                provider=QuantumProvider.DYNEX,
                parameters={
                    "variables": ["production_efficiency", "cost_reduction", "quality_score"],
                    "constraints": [
                        {"type": "budget", "max_value": 1000000},
                        {"type": "timeline", "max_days": 90}
                    ],
                    "objective_function": "maximize(production_efficiency * 0.4 + cost_reduction * 0.3 + quality_score * 0.3)"
                },
                priority=1
            )
            
            # Submit quantum LLM request
            llm_request_id = await submit_quantum_request(
                client_id=self.client_id,
                operation_type=QuantumOperation.QUANTUM_LLM,
                provider=QuantumProvider.DYNEX,
                parameters={
                    "prompt": "Analyze the business strategy for a mid-market technology company and provide quantum-enhanced insights for growth optimization.",
                    "max_tokens": 500,
                    "temperature": 0.7
                },
                priority=2
            )
            
            # Submit portfolio optimization request
            portfolio_request_id = await submit_quantum_request(
                client_id=self.client_id,
                operation_type=QuantumOperation.PORTFOLIO_OPTIMIZATION,
                provider=QuantumProvider.DYNEX,
                parameters={
                    "assets": ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"],
                    "returns": [0.15, 0.12, 0.18, 0.25, 0.20],
                    "risk_tolerance": 0.7,
                    "constraints": {
                        "max_allocation": 0.3,
                        "min_allocation": 0.05
                    }
                },
                priority=1
            )
            
            self.demo_results["quantum_operations"] = {
                "optimization_request_id": optimization_request_id,
                "llm_request_id": llm_request_id,
                "portfolio_request_id": portfolio_request_id,
                "providers": providers
            }
            
            print(f"✅ Submitted quantum requests:")
            print(f"   Optimization: {optimization_request_id}")
            print(f"   Quantum LLM: {llm_request_id}")
            print(f"   Portfolio Optimization: {portfolio_request_id}")
            
            # Wait for processing and check status
            print("\n   Checking request status...")
            await asyncio.sleep(3)
            
            for request_id, request_type in [
                (optimization_request_id, "Optimization"),
                (llm_request_id, "Quantum LLM"),
                (portfolio_request_id, "Portfolio")
            ]:
                try:
                    status = await get_request_status(request_id)
                    print(f"   {request_type}: {status['status']}")
                    if status['status'] == 'completed':
                        print(f"     Execution time: {status['execution_time']:.2f}s")
                        print(f"     Credits used: ${status['quantum_credits_used']:.4f}")
                except Exception as e:
                    print(f"   {request_type}: Error checking status - {e}")
            
        except Exception as e:
            print(f"❌ Quantum operations failed: {e}")
            self.demo_results["quantum_operations"] = {"status": "failed", "error": str(e)}
    
    async def demo_quantum_algorithms(self):
        """Demonstrate quantum algorithms (QAOA MaxCut, VQE Chemistry)"""
        print("\n🔬 Step 6: Quantum Algorithms Demo")
        print("-" * 35)
        
        try:
            # Demo 1: QAOA MaxCut for combinatorial optimization
            print("\n🎯 Running QAOA MaxCut Algorithm...")
            
            qaoa_config = AlgorithmConfig(
                algorithm_type=AlgorithmType.QAOA_MAXCUT,
                backend_type=BackendType.QISKIT,
                num_qubits=4,
                num_layers=2,
                max_iterations=50,
                shots=1024,
                optimization_level=1,
                noise_mitigation=True
            )
            
            # Create a sample graph for MaxCut
            graph_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
            qaoa_params = {
                "graph_edges": graph_edges,
                "warm_start": True,
                "layerwise_training": True
            }
            
            qaoa_result = await run_algorithm(
                config=qaoa_config,
                algorithm_params=qaoa_params
            )
            
            print(f"   ✅ QAOA MaxCut completed successfully")
            print(f"   Best Cut Value: {qaoa_result.best_value:.4f}")
            print(f"   Optimal Parameters: {qaoa_result.optimal_params[:4]}...")  # Show first 4
            print(f"   Execution Time: {qaoa_result.execution_time:.2f}s")
            print(f"   Iterations: {qaoa_result.iterations}")
            
            # Demo 2: VQE Chemistry for molecular simulation
            print("\n🧪 Running VQE Chemistry Algorithm...")
            
            vqe_config = AlgorithmConfig(
                algorithm_type=AlgorithmType.VQE_CHEMISTRY,
                backend_type=BackendType.QISKIT,
                num_qubits=4,
                num_layers=2,
                max_iterations=30,
                shots=1024,
                optimization_level=1,
                noise_mitigation=True
            )
            
            # H2 molecule parameters
            vqe_params = {
                "molecule": "H2",
                "bond_distance": 0.735,  # Angstroms
                "ansatz_type": "hardware_efficient",
                "gradient_method": "parameter_shift"
            }
            
            vqe_result = await run_algorithm(
                config=vqe_config,
                algorithm_params=vqe_params
            )
            
            print(f"   ✅ VQE Chemistry completed successfully")
            print(f"   Ground State Energy: {vqe_result.best_value:.6f} Hartree")
            print(f"   Optimal Parameters: {vqe_result.optimal_params[:4]}...")  # Show first 4
            print(f"   Execution Time: {vqe_result.execution_time:.2f}s")
            print(f"   Iterations: {vqe_result.iterations}")
            
            # Demo 3: Quantum Classifier for machine learning
            print("\n🤖 Running Quantum Classifier Algorithm...")
            
            classifier_result = await run_algorithm(
                algorithm_type="quantum_classifier",
                problem_data={
                    "dataset_name": "iris",
                    "num_samples": 100,
                    "test_size": 0.3,
                    "random_state": 42
                },
                backend_type="simulator",
                max_iterations=50,
                algorithm_params={
                    "feature_map": "ZZFeatureMap",
                    "ansatz": "RealAmplitudes",
                    "num_layers": 2
                }
            )
            
            print(f"   ✅ Quantum Classifier completed successfully")
            print(f"   Test Accuracy: {classifier_result.get('test_accuracy', 0):.3f}")
            print(f"   Train Accuracy: {classifier_result.get('train_accuracy', 0):.3f}")
            print(f"   Execution Time: {classifier_result.get('execution_time', 0):.2f}s")
            print(f"   Iterations: {classifier_result.get('iterations', 0)}")
            
            # Store results
            self.demo_results["quantum_algorithms"] = {
                "qaoa_maxcut": {
                    "status": "success",
                    "best_cut_value": qaoa_result.best_value,
                    "execution_time": qaoa_result.execution_time,
                    "iterations": qaoa_result.iterations
                },
                "vqe_chemistry": {
                    "status": "success",
                    "ground_state_energy": vqe_result.best_value,
                    "execution_time": vqe_result.execution_time,
                    "iterations": vqe_result.iterations
                },
                "quantum_classifier": {
                    "status": "success",
                    "test_accuracy": classifier_result.get('test_accuracy', 0),
                    "train_accuracy": classifier_result.get('train_accuracy', 0),
                    "execution_time": classifier_result.get('execution_time', 0),
                    "iterations": classifier_result.get('iterations', 0)
                }
            }
            
            total_time = (qaoa_result.execution_time + vqe_result.execution_time + 
                         classifier_result.get('execution_time', 0))
            print(f"\n   🎉 All three quantum algorithms completed successfully!")
            print(f"   Total Execution Time: {total_time:.2f}s")
            
        except Exception as e:
            print(f"❌ Quantum algorithms demo failed: {e}")
            self.demo_results["quantum_algorithms"] = {"status": "failed", "error": str(e)}
    
    async def demo_usage_statistics(self):
        """Demonstrate usage statistics"""
        print("\n📈 Step 7: Usage Statistics")
        print("-" * 20)
        
        if not self.client_id:
            print("❌ No client registered for usage statistics")
            return
        
        try:
            # Get quantum usage statistics
            usage_stats = await get_quantum_usage_stats(self.client_id)
            
            self.demo_results["usage_statistics"] = usage_stats
            
            print(f"✅ Usage statistics for client: {self.client_id}")
            print(f"   Total Requests: {usage_stats['total_requests']}")
            print(f"   Completed: {usage_stats['completed_requests']}")
            print(f"   Success Rate: {usage_stats['success_rate']:.1%}")
            print(f"   Total Credits Used: ${usage_stats['total_credits_used']:.4f}")
            print(f"   Average Execution Time: {usage_stats['average_execution_time']:.2f}s")
            
        except Exception as e:
            print(f"❌ Usage statistics failed: {e}")
            self.demo_results["usage_statistics"] = {"status": "failed", "error": str(e)}
    
    def print_demo_summary(self):
        """Print comprehensive demo summary"""
        print("\n🎯 Demo Summary")
        print("=" * 50)
        
        successful_steps = 0
        total_steps = len(self.demo_results)
        
        for step_name, result in self.demo_results.items():
            if isinstance(result, dict) and result.get("status") != "failed":
                successful_steps += 1
                print(f"✅ {step_name.replace('_', ' ').title()}: Success")
            else:
                print(f"❌ {step_name.replace('_', ' ').title()}: Failed")
        
        print(f"\n📊 Overall Results: {successful_steps}/{total_steps} steps successful")
        
        if successful_steps == total_steps:
            print("🎉 All NQBA components are working perfectly!")
        elif successful_steps >= total_steps * 0.8:
            print("👍 Most NQBA components are operational!")
        else:
            print("⚠️ Some components need attention.")
        
        print("\n🚀 FLYFOX AI - NQBA Core is ready for production!")
        print("   • Business Assessment with Quantum Optimization")
        print("   • Automated Audit Scheduling")
        print("   • Real-time Data Collection")
        print("   • MCP-style Quantum Computing Hub")
        print("   • Advanced Quantum Algorithms (QAOA, VQE, Quantum ML)")
        print("   • Third-party Integration Support")

async def main():
    """Main demo function"""
    demo = NQBADemo()
    await demo.run_comprehensive_demo()

if __name__ == "__main__":
    print("Starting NQBA Core - FLYFOX AI Quantum Hub Demo...")
    asyncio.run(main())
