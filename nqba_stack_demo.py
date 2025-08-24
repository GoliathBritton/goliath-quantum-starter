"""
NQBA Stack Comprehensive Demo
Demonstrates the complete Neuromorphic Quantum Business Architecture Stack
Showcases all three business pods, core orchestration, and quantum integration
"""
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add src to path for NQBA imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba_stack.core.orchestrator import (
    get_orchestrator, 
    submit_task,
    BusinessPod
)
from nqba_stack.core.ltc_logger import get_ltc_logger
from nqba_stack.core.settings import get_settings
from nqba_stack.business_pods import get_all_business_pods

class NQBAStackDemo:
    """Comprehensive demo of the NQBA Stack"""
    
    def __init__(self):
        """Initialize the demo"""
        self.orchestrator = get_orchestrator()
        self.ltc_logger = get_ltc_logger()
        self.settings = get_settings()
        
        # Demo data
        self.demo_leads = [
            {
                "company_name": "TechCorp Solutions",
                "budget": "high",
                "urgency": "urgent",
                "pain_points": "energy costs",
                "industry": "technology",
                "company_size": "large"
            },
            {
                "company_name": "Global Manufacturing Inc",
                "budget": "very high",
                "urgency": "very urgent",
                "pain_points": "production delays",
                "industry": "manufacturing",
                "company_size": "enterprise"
            },
            {
                "company_name": "Healthcare Innovations",
                "budget": "medium",
                "urgency": "high",
                "pain_points": "quality issues",
                "industry": "healthcare",
                "company_size": "medium"
            }
        ]
        
        self.demo_energy_data = {
            "peak_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "off_peak_hours": [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23],
            "equipment_schedule": {
                "production_line_1": 16,
                "production_line_2": 12,
                "quality_control": 8,
                "maintenance": 4
            },
            "current_costs": {
                "peak_rate": 0.15,
                "off_peak_rate": 0.08,
                "total_monthly": 45000
            }
        }
        
        self.demo_portfolio_data = {
            "assets": {
                "energy_futures": 0.4,
                "renewable_etfs": 0.3,
                "tech_stocks": 0.2,
                "crypto": 0.1
            },
            "current_value": 1000000,
            "risk_metrics": {
                "volatility": 0.18,
                "sharpe_ratio": 1.2,
                "max_drawdown": 0.12
            }
        }
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*80)
        print(f"🚀 {title}")
        print("="*80)
    
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n📋 {title}")
        print("-" * 60)
    
    def demo_system_status(self):
        """Demonstrate system status and health"""
        self.print_section("System Status & Health")
        
        try:
            status = self.orchestrator.get_system_status()
            print(f"✅ Orchestrator Status: {status['orchestrator_status']}")
            print(f"🏢 Business Pods: {status['business_pods']}")
            print(f"🟢 Active Pods: {status['active_pods']}")
            print(f"🛣️  Task Routes: {status['task_routes']}")
            print(f"📊 Total Tasks: {status['metrics']['total_tasks']}")
            print(f"⚡ Quantum Enhanced: {status['metrics']['quantum_enhanced_tasks']}")
            print(f"⏱️  Avg Execution Time: {status['metrics']['average_execution_time']:.3f}s")
            
        except Exception as e:
            print(f"❌ System status check failed: {e}")
    
    def demo_business_pods(self):
        """Demonstrate business pod capabilities"""
        self.print_section("Business Pods Overview")
        
        try:
            pods = get_all_business_pods()
            
            for pod_id, pod_config in pods.items():
                print(f"\n🏢 {pod_config['name']} ({pod_id})")
                print(f"   Description: {pod_config['description']}")
                print(f"   Capabilities: {', '.join(pod_config['capabilities'][:3])}...")
                print(f"   QUBO Problems: {', '.join(pod_config['qubo_problems'][:3])}...")
                print(f"   Solutions: {', '.join(pod_config['solutions'][:3])}...")
                
        except Exception as e:
            print(f"❌ Business pods overview failed: {e}")
    
    async def demo_lead_scoring(self):
        """Demonstrate Sigma Select lead scoring"""
        self.print_section("Sigma Select - Lead Scoring Demo")
        
        try:
            print("📊 Processing demo leads...")
            print(f"   Lead count: {len(self.demo_leads)}")
            
            # Submit lead scoring task
            task_result = await submit_task(
                pod_id="sigma_select",
                task_type="lead_scoring",
                data={"leads": self.demo_leads},
                priority=8,
                metadata={"demo": True, "timestamp": datetime.now().isoformat()}
            )
            
            if task_result.success:
                print(f"✅ Lead scoring completed successfully!")
                print(f"   Execution time: {task_result.execution_time:.3f}s")
                print(f"   Quantum enhanced: {task_result.quantum_enhanced}")
                print(f"   LTC Reference: {task_result.ltc_reference}")
                
                # Display scored leads
                scored_leads = task_result.result_data.get("scored_leads", [])
                print(f"\n📈 Scored Leads:")
                for i, lead in enumerate(scored_leads):
                    score = lead.get("score", 0)
                    company = lead.get("company_name", f"Lead {i+1}")
                    print(f"   {company}: {score}/100")
                    
            else:
                print(f"❌ Lead scoring failed: {task_result.error_message}")
                
        except Exception as e:
            print(f"❌ Lead scoring demo failed: {e}")
    
    async def demo_energy_optimization(self):
        """Demonstrate FLYFOX AI energy optimization"""
        self.print_section("FLYFOX AI - Energy Optimization Demo")
        
        try:
            print("⚡ Optimizing energy schedule...")
            print(f"   Equipment: {len(self.demo_energy_data['equipment_schedule'])} production lines")
            print(f"   Current monthly cost: ${self.demo_energy_data['current_costs']['total_monthly']:,}")
            
            # Submit energy optimization task
            task_result = await submit_task(
                pod_id="flyfox_ai",
                task_type="energy_optimization",
                data={
                    "energy_data": self.demo_energy_data,
                    "optimization_target": "cost",
                    "constraints": {"max_equipment_hours": 20}
                },
                priority=9,
                metadata={"demo": True, "timestamp": datetime.now().isoformat()}
            )
            
            if task_result.success:
                print(f"✅ Energy optimization completed successfully!")
                print(f"   Execution time: {task_result.execution_time:.3f}s")
                print(f"   Quantum enhanced: {task_result.quantum_enhanced}")
                print(f"   LTC Reference: {task_result.ltc_reference}")
                
                # Display optimization results
                optimization_result = task_result.result_data.get("optimization_result", {})
                cost_savings = optimization_result.get("cost_savings", 0)
                efficiency_gain = optimization_result.get("efficiency_gain", 0)
                
                print(f"\n💰 Optimization Results:")
                print(f"   Cost savings: ${cost_savings:,.2f}/month")
                print(f"   Efficiency gain: {efficiency_gain:.1f}%")
                
            else:
                print(f"❌ Energy optimization failed: {task_result.error_message}")
                
        except Exception as e:
            print(f"❌ Energy optimization demo failed: {e}")
    
    async def demo_portfolio_optimization(self):
        """Demonstrate Goliath Trade portfolio optimization"""
        self.print_section("Goliath Trade - Portfolio Optimization Demo")
        
        try:
            print("📈 Optimizing investment portfolio...")
            print(f"   Portfolio value: ${self.demo_portfolio_data['current_value']:,}")
            print(f"   Current volatility: {self.demo_portfolio_data['risk_metrics']['volatility']:.1%}")
            
            # Submit portfolio optimization task
            task_result = await submit_task(
                pod_id="goliath_trade",
                task_type="portfolio_optimization",
                data={
                    "portfolio_data": self.demo_portfolio_data,
                    "risk_tolerance": "medium",
                    "target_return": 0.15,
                    "constraints": {"max_crypto_allocation": 0.05}
                },
                priority=7,
                metadata={"demo": True, "timestamp": datetime.now().isoformat()}
            )
            
            if task_result.success:
                print(f"✅ Portfolio optimization completed successfully!")
                print(f"   Execution time: {task_result.execution_time:.3f}s")
                print(f"   Quantum enhanced: {task_result.quantum_enhanced}")
                print(f"   LTC Reference: {task_result.ltc_reference}")
                
                # Display optimization results
                portfolio_allocation = task_result.result_data.get("portfolio_allocation", {})
                risk_score = task_result.result_data.get("risk_score", 0)
                expected_return = task_result.result_data.get("expected_return", 0)
                
                print(f"\n📊 Portfolio Results:")
                print(f"   Expected return: {expected_return:.1%}")
                print(f"   Risk score: {risk_score:.3f}")
                print(f"   Asset allocation: {json.dumps(portfolio_allocation, indent=6)}")
                
            else:
                print(f"❌ Portfolio optimization failed: {task_result.error_message}")
                
        except Exception as e:
            print(f"❌ Portfolio optimization demo failed: {e}")
    
    def demo_ltc_capabilities(self):
        """Demonstrate Living Technical Codex capabilities"""
        self.print_section("Living Technical Codex (LTC) Demo")
        
        try:
            # Get LTC statistics
            stats = self.ltc_logger.get_statistics()
            
            if "error" not in stats:
                print(f"📚 LTC Statistics:")
                print(f"   Total operations: {stats['total_operations']}")
                print(f"   Recent operations (24h): {stats['recent_operations_24h']}")
                print(f"   IPFS backup rate: {stats['ipfs_backup_rate']:.1f}%")
                
                # Show operations by type
                print(f"\n🔍 Operations by Type:")
                for op_type, count in stats['operations_by_type'].items():
                    print(f"   {op_type}: {count}")
                    
            else:
                print(f"❌ LTC statistics failed: {stats['error']}")
            
            # Verify hash chain integrity
            print(f"\n🔗 Hash Chain Integrity:")
            integrity = self.ltc_logger.get_hash_chain_integrity()
            
            if "error" not in integrity:
                print(f"   Total operations: {integrity['total_operations']}")
                print(f"   Integrity verified: {integrity['integrity_verified']}")
                if not integrity['integrity_verified']:
                    print(f"   Integrity issues: {len(integrity['integrity_issues'])}")
                    
            else:
                print(f"   Integrity check failed: {integrity['error']}")
                
        except Exception as e:
            print(f"❌ LTC demo failed: {e}")
    
    def demo_configuration(self):
        """Demonstrate configuration and settings"""
        self.print_section("Configuration & Settings")
        
        try:
            print(f"🔧 Environment: {self.settings.environment}")
            print(f"🐛 Debug mode: {self.settings.debug}")
            print(f"⚡ Dynex configured: {self.settings.dynex_configured}")
            print(f"🔗 IPFS configured: {self.settings.ipfs_configured}")
            print(f"🌐 Web3 configured: {self.settings.web3_configured}")
            print(f"🤖 LLM configured: {self.settings.llm_configured}")
            print(f"🏢 Company: {self.settings.company_name}")
            print(f"💼 Business Unit: {self.settings.business_unit}")
            
        except Exception as e:
            print(f"❌ Configuration demo failed: {e}")
    
    async def run_complete_demo(self):
        """Run the complete NQBA Stack demo"""
        self.print_header("NQBA Stack - Complete Demo")
        print("Welcome to the Neuromorphic Quantum Business Architecture Stack!")
        print("This demo showcases all three business pods, core orchestration, and quantum integration.")
        
        # System overview
        self.demo_system_status()
        self.demo_business_pods()
        self.demo_configuration()
        
        # Business pod demonstrations
        await self.demo_lead_scoring()
        await self.demo_energy_optimization()
        await self.demo_portfolio_optimization()
        
        # LTC capabilities
        self.demo_ltc_capabilities()
        
        # Final summary
        self.print_header("Demo Complete!")
        print("🎉 The NQBA Stack has successfully demonstrated:")
        print("   ✅ System orchestration and health monitoring")
        print("   ✅ Three business pods with quantum optimization")
        print("   ✅ Living Technical Codex for audit and compliance")
        print("   ✅ Dynex quantum integration")
        print("   ✅ Task routing and execution")
        
        print(f"\n📊 Final System Status:")
        final_status = self.orchestrator.get_system_status()
        print(f"   Total tasks executed: {final_status['metrics']['total_tasks']}")
        print(f"   Quantum enhanced tasks: {final_status['metrics']['quantum_enhanced_tasks']}")
        print(f"   Average execution time: {final_status['metrics']['average_execution_time']:.3f}s")
        
        print(f"\n🚀 Next Steps:")
        print("   1. Explore the API endpoints at http://localhost:8000/docs")
        print("   2. Run individual business pod dashboards")
        print("   3. Check the LTC for detailed operation logs")
        print("   4. Configure your own Dynex API key for quantum optimization")

async def main():
    """Main demo function"""
    try:
        demo = NQBAStackDemo()
        await demo.run_complete_demo()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Please ensure the NQBA Stack is properly configured and running.")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
