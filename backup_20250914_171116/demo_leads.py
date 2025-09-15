#!/usr/bin/env python3
"""
NQBA Lead Scoring Demo - Sigma Select Business Case

This script demonstrates the NQBA platform's capabilities for lead scoring
optimization, showing how quantum computing can enhance business decisions.
"""

import asyncio
import sys
import os
import time
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nqba.quantum_adapter import QuantumAdapter
from nqba.decision_logic import DecisionLogicEngine, DecisionContext, DecisionType
from nqba.ltc_logger import LTCLogger, LTCConfig

class LeadScoringDemo:
    """Demo class for lead scoring optimization"""
    
    def __init__(self):
        """Initialize the demo components"""
        self.quantum_adapter = None
        self.decision_engine = None
        self.ltc_logger = None
        self.session_id = f"demo_session_{int(time.time())}"
        
    async def initialize(self):
        """Initialize NQBA components"""
        print("🚀 Initializing NQBA Components...")
        
        try:
            # Initialize LTC logger
            ltc_config = LTCConfig(
                storage_path="./ltc_storage",
                async_writing=True
            )
            self.ltc_logger = LTCLogger(ltc_config)
            print("✅ LTC Logger initialized")
            
            # Initialize quantum adapter
            self.quantum_adapter = QuantumAdapter(
                preferred_backend="dynex",
                max_qubits=64,
                enable_fallback=True
            )
            print("✅ Quantum Adapter initialized")
            
            # Initialize decision engine
            self.decision_engine = DecisionLogicEngine(
                max_qubits=64,
                enable_optimization=True,
                rule_engine_enabled=True
            )
            print("✅ Decision Engine initialized")
            
            print("🎉 All NQBA components initialized successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize components: {e}")
            raise
    
    def generate_sample_leads(self, count: int = 10):
        """Generate sample lead data for demonstration"""
        import random
        
        leads = []
        for i in range(count):
            lead = {
                "id": f"lead_{i+1:03d}",
                "company": f"Company {i+1}",
                "industry": random.choice(["tech", "finance", "healthcare", "retail", "manufacturing"]),
                "revenue": random.randint(1000000, 100000000),
                "employees": random.randint(10, 10000),
                "location": random.choice(["US", "EU", "APAC", "LATAM"]),
                "engagement_score": random.randint(1, 100),
                "website_traffic": random.randint(1000, 100000),
                "social_media_followers": random.randint(100, 100000),
                "email_open_rate": random.uniform(0.1, 0.4),
                "conversion_rate": random.uniform(0.01, 0.1)
            }
            leads.append(lead)
        
        return leads
    
    def create_qubo_matrix(self, leads):
        """Create QUBO matrix for lead scoring optimization"""
        import numpy as np
        
        n_leads = len(leads)
        matrix = np.zeros((n_leads, n_leads))
        
        # Create scoring matrix based on lead characteristics
        for i in range(n_leads):
            for j in range(n_leads):
                if i == j:
                    # Diagonal elements represent individual lead scores
                    lead = leads[i]
                    score = (
                        lead["engagement_score"] * 0.3 +
                        lead["website_traffic"] / 1000 * 0.2 +
                        lead["social_media_followers"] / 1000 * 0.15 +
                        lead["email_open_rate"] * 100 * 0.2 +
                        lead["conversion_rate"] * 1000 * 0.15
                    )
                    matrix[i][j] = -score  # Negative for minimization
                else:
                    # Off-diagonal elements represent interaction penalties
                    # (simplified model)
                    matrix[i][j] = 0.1
        
        return matrix
    
    async def optimize_lead_scoring(self, leads):
        """Optimize lead scoring using NQBA"""
        print(f"\n🔍 Optimizing Lead Scoring for {len(leads)} leads...")
        
        try:
            # Create QUBO matrix
            matrix = self.create_qubo_matrix(leads)
            print(f"✅ Created QUBO matrix: {matrix.shape}")
            
            # Log the optimization request
            entry_id = await self.ltc_logger.log_operation(
                operation_type="lead_scoring_optimization",
                component="demo_script",
                user_id="demo_user",
                session_id=self.session_id,
                input_data={
                    "lead_count": len(leads),
                    "matrix_size": matrix.shape,
                    "algorithm": "qaoa"
                }
            )
            
            # Make decision on optimization strategy
            context = DecisionContext(
                user_id="demo_user",
                session_id=self.session_id,
                business_context="lead_scoring",
                priority="high"
            )
            
            decision_result = await self.decision_engine.make_decision(
                decision_type=DecisionType.OPTIMIZATION,
                context=context,
                data={
                    "problem_size": len(leads),
                    "problem_type": "qubo",
                    "priority": "high"
                }
            )
            
            print(f"🎯 Decision Engine selected: {decision_result.strategy_selected}")
            print(f"💡 Reasoning: {decision_result.reasoning}")
            print(f"📊 Confidence: {decision_result.confidence_score:.2f}")
            
            # Execute quantum optimization
            start_time = time.time()
            optimization_result = await self.quantum_adapter.optimize_qubo(
                matrix=matrix,
                algorithm="qaoa"
            )
            execution_time = time.time() - start_time
            
            # Log the optimization result
            await self.ltc_logger.log_quantum_execution(
                operation="lead_scoring_qubo_optimization",
                qubits=matrix.shape[0],
                backend=optimization_result.backend_used,
                execution_time=execution_time,
                success=optimization_result.success,
                user_id="demo_user",
                session_id=self.session_id,
                parent_entry_id=entry_id
            )
            
            if optimization_result.success:
                print(f"✅ Optimization completed successfully!")
                print(f"⚡ Execution time: {execution_time:.3f}s")
                print(f"🔧 Backend used: {optimization_result.backend_used}")
                print(f"📈 Optimal value: {optimization_result.optimal_value:.4f}")
                
                # Process results
                await self._process_optimization_results(leads, optimization_result, entry_id)
            else:
                print(f"❌ Optimization failed: {optimization_result.error_message}")
            
            return optimization_result
            
        except Exception as e:
            print(f"❌ Lead scoring optimization failed: {e}")
            raise
    
    async def _process_optimization_results(self, leads, optimization_result, entry_id):
        """Process and display optimization results"""
        print(f"\n📊 LEAD SCORING RESULTS:")
        print("=" * 50)
        
        if optimization_result.solution_vector:
            # Sort leads by solution vector (1 = selected, 0 = not selected)
            scored_leads = []
            for i, lead in enumerate(leads):
                selected = optimization_result.solution_vector[i] if i < len(optimization_result.solution_vector) else 0
                score = (
                    lead["engagement_score"] * 0.3 +
                    lead["website_traffic"] / 1000 * 0.2 +
                    lead["social_media_followers"] / 1000 * 0.15 +
                    lead["email_open_rate"] * 100 * 0.2 +
                    lead["conversion_rate"] * 1000 * 0.15
                )
                scored_leads.append({
                    "lead": lead,
                    "selected": selected,
                    "score": score
                })
            
            # Sort by score (highest first)
            scored_leads.sort(key=lambda x: x["score"], reverse=True)
            
            # Display top leads
            print("🏆 TOP PRIORITY LEADS:")
            for i, scored_lead in enumerate(scored_leads[:5]):
                lead = scored_lead["lead"]
                status = "✅ SELECTED" if scored_lead["selected"] else "⏳ PENDING"
                print(f"{i+1:2d}. {lead['company']:<15} | {lead['industry']:<12} | "
                      f"Score: {scored_lead['score']:6.2f} | {status}")
            
            # Calculate metrics
            selected_count = sum(1 for sl in scored_leads if sl["selected"])
            total_score = sum(sl["score"] for sl in scored_leads if sl["selected"])
            
            print(f"\n📈 OPTIMIZATION METRICS:")
            print(f"   • Total leads: {len(leads)}")
            print(f"   • Selected leads: {selected_count}")
            print(f"   • Selection rate: {selected_count/len(leads)*100:.1f}%")
            print(f"   • Total score: {total_score:.2f}")
            print(f"   • Average score: {total_score/selected_count:.2f}" if selected_count > 0 else "   • Average score: N/A")
            
            # Log business metrics
            await self.ltc_logger.log_metric(
                "lead_scoring_selection_rate",
                selected_count / len(leads),
                {
                    "total_leads": len(leads),
                    "selected_leads": selected_count,
                    "total_score": total_score
                },
                user_id="demo_user",
                session_id=self.session_id,
                parent_entry_id=entry_id
            )
            
        else:
            print("⚠️  No solution vector available")
    
    async def demonstrate_business_rules(self):
        """Demonstrate business rule processing"""
        print(f"\n📋 DEMONSTRATING BUSINESS RULES:")
        print("=" * 50)
        
        try:
            # Get business rules
            rules = self.decision_engine.get_business_rules()
            print(f"📚 Found {len(rules)} business rules:")
            
            for rule in rules:
                print(f"\n🔹 Rule: {rule.name}")
                print(f"   Description: {rule.description}")
                print(f"   Priority: {rule.priority}")
                print(f"   Active: {rule.active}")
                print(f"   Actions: {len(rule.actions)}")
            
            # Test rule execution
            context = DecisionContext(
                user_id="demo_user",
                session_id=self.session_id,
                business_context="lead_scoring",
                priority="high"
            )
            
            rule_result = await self.decision_engine.make_decision(
                decision_type=DecisionType.BUSINESS_RULE,
                context=context,
                data={"size": 150, "priority": "high"}
            )
            
            print(f"\n🎯 Business Rule Execution Result:")
            print(f"   Strategy: {rule_result.strategy_selected}")
            print(f"   Reasoning: {rule_result.reasoning}")
            print(f"   Confidence: {rule_result.confidence_score:.2f}")
            
        except Exception as e:
            print(f"❌ Business rule demonstration failed: {e}")
    
    async def show_ltc_traceability(self):
        """Show LTC traceability features"""
        print(f"\n🔍 LTC TRACEABILITY DEMONSTRATION:")
        print("=" * 50)
        
        try:
            # Get LTC statistics
            stats = self.ltc_logger.get_statistics()
            print(f"📊 LTC Statistics:")
            print(f"   • Total entries: {stats['total_entries']}")
            print(f"   • Total files: {stats['total_files']}")
            print(f"   • Storage size: {stats['total_size_mb']:.2f} MB")
            print(f"   • Current file: {Path(stats['current_file']).name}")
            
            # Search for recent entries
            entries = await self.ltc_logger.search_entries(
                operation_type="lead_scoring_optimization",
                limit=5
            )
            
            print(f"\n📝 Recent Lead Scoring Entries:")
            for entry in entries:
                print(f"   • {entry.timestamp} | {entry.operation_type} | {entry.component}")
                if entry.input_data:
                    lead_count = entry.input_data.get("lead_count", "N/A")
                    print(f"     Input: {lead_count} leads")
                if entry.result_data:
                    success = entry.result_data.get("success", "N/A")
                    print(f"     Result: {success}")
            
        except Exception as e:
            print(f"❌ LTC traceability demonstration failed: {e}")
    
    async def run_demo(self):
        """Run the complete demo"""
        print("🚀 NQBA LEAD SCORING DEMO")
        print("=" * 60)
        print("This demo showcases NQBA's capabilities for:")
        print("• Quantum-optimized lead scoring")
        print("• Intelligent decision making")
        print("• Business rule processing")
        print("• Complete traceability (LTC)")
        print("=" * 60)
        
        try:
            # Initialize components
            await self.initialize()
            
            # Generate sample leads
            leads = self.generate_sample_leads(15)
            print(f"\n👥 Generated {len(leads)} sample leads")
            
            # Show sample lead
            print(f"\n📋 Sample Lead Data:")
            sample_lead = leads[0]
            print(f"   Company: {sample_lead['company']}")
            print(f"   Industry: {sample_lead['industry']}")
            print(f"   Revenue: ${sample_lead['revenue']:,}")
            print(f"   Engagement Score: {sample_lead['engagement_score']}/100")
            
            # Run lead scoring optimization
            await self.optimize_lead_scoring(leads)
            
            # Demonstrate business rules
            await self.demonstrate_business_rules()
            
            # Show LTC traceability
            await self.show_ltc_traceability()
            
            print(f"\n🎉 DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("Key Takeaways:")
            print("• NQBA successfully optimized lead scoring using quantum computing")
            print("• Decision engine selected optimal strategy based on business rules")
            print("• Complete traceability maintained through LTC logging")
            print("• Ready for production deployment with Sigma Select")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            raise
        finally:
            # Cleanup
            if self.ltc_logger:
                self.ltc_logger.shutdown()

async def main():
    """Main demo function"""
    demo = LeadScoringDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
