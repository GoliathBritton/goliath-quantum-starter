#!/usr/bin/env python3
"""
Advanced Automation & Algorithm Templates Demo
==============================================

Comprehensive demonstration of the platform's advanced capabilities:
- World-class algorithm templates with quantum enhancement
- Advanced automation workflows achieving 90-95% automation
- Configuration management with graceful fallbacks
- Workflow orchestration and performance optimization

This demo showcases the full potential of the quantum automation platform.
"""

import asyncio
import json
import logging
import time
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class AdvancedAutomationDemo:
    """Comprehensive demonstration of advanced automation capabilities"""

    def __init__(self):
        self.demo_results = []
        self.start_time = None
        self.config_manager = None

    async def run_comprehensive_demo(self):
        """Run the complete advanced automation demonstration"""
        self.start_time = datetime.now()
        logger.info("🚀 Starting Advanced Automation & Algorithm Templates Demo")
        logger.info("=" * 60)

        try:
            # Demo 1: Configuration Management
            await self._demo_configuration_management()

            # Demo 2: Advanced Algorithm Templates
            await self._demo_advanced_algorithm_templates()

            # Demo 3: Advanced Automation Workflows
            await self._demo_advanced_automation_workflows()

            # Demo 4: Workflow Orchestration
            await self._demo_workflow_orchestration()

            # Demo 5: Performance & Integration
            await self._demo_performance_integration()

            # Generate final report
            await self._generate_demo_report()

        except Exception as e:
            logger.error(f"❌ Demo execution failed: {e}")
            raise

    async def _demo_configuration_management(self):
        """Demonstrate advanced configuration management capabilities"""
        logger.info("\n🔧 Demo 1: Configuration Management")
        logger.info("-" * 40)

        try:
            # Import configuration manager
            import sys

            sys.path.append(".")

            from src.nqba_stack.core.config_manager import (
                initialize_configuration,
                get_config_manager,
            )

            # Initialize configuration
            self.config_manager = initialize_configuration()

            # Check service status
            operational_status = self.config_manager.get_operational_status()

            logger.info(f"✅ Configuration Manager initialized")
            logger.info(f"📊 Overall Health: {operational_status['overall_health']}")
            logger.info(f"🔌 Services: {len(operational_status['services'])}")

            # Display service details
            for service_name, service_info in operational_status["services"].items():
                status_icon = "✅" if service_info["healthy"] else "❌"
                fallback_icon = "🔄" if service_info["using_fallback"] else "⚡"
                logger.info(
                    f"  {status_icon} {service_name}: {service_info['fallback_mode']} {fallback_icon}"
                )

            # Check degraded features
            degraded_features = self.config_manager.get_degraded_features()
            if degraded_features:
                logger.info(f"⚠️  Degraded Features: {', '.join(degraded_features)}")
            else:
                logger.info("✅ All features operating at full capacity")

            # Create fallback storage
            for service_name in ["dynex", "ipfs", "llm"]:
                self.config_manager.create_fallback_storage(service_name)

            # Save configuration
            self.config_manager.save_configuration()

            demo_result = {
                "demo_name": "Configuration Management",
                "status": "success",
                "overall_health": operational_status["overall_health"],
                "services_configured": len(operational_status["services"]),
                "degraded_features": len(degraded_features),
                "fallback_storage_created": True,
            }

            self.demo_results.append(demo_result)
            logger.info("✅ Configuration Management demo completed successfully")

        except Exception as e:
            logger.error(f"❌ Configuration Management demo failed: {e}")
            self.demo_results.append(
                {
                    "demo_name": "Configuration Management",
                    "status": "failed",
                    "error": str(e),
                }
            )

    async def _demo_advanced_algorithm_templates(self):
        """Demonstrate advanced algorithm template capabilities"""
        logger.info("\n🧠 Demo 2: Advanced Algorithm Templates")
        logger.info("-" * 40)

        try:
            from src.nqba_stack.algorithms.advanced_algorithm_templates import (
                get_algorithm_templates,
                create_algorithm_instance,
            )

            # Get available algorithm templates
            templates = get_algorithm_templates()
            logger.info(f"📊 Available Algorithm Templates: {len(templates)}")

            # Display template information
            for template_name, template in templates.items():
                logger.info(f"\n📋 {template.name}")
                logger.info(f"   Category: {template.category.value}")
                logger.info(f"   Complexity: {template.complexity.value}")
                logger.info(f"   ROI: {template.estimated_roi:.1%}")
                logger.info(
                    f"   Quantum Enhanced: {'✅' if template.quantum_enhancement else '❌'}"
                )
                logger.info(f"   Use Cases: {', '.join(template.use_cases[:3])}...")

            # Create and test algorithm instances
            test_algorithms = []
            for template_name in [
                "quantum_portfolio_optimizer",
                "quantum_fraud_detector",
            ]:
                try:
                    if template_name == "quantum_portfolio_optimizer":
                        config = {
                            "risk_tolerance": 0.6,
                            "target_return": 0.15,
                            "max_positions": 25,
                        }
                    elif template_name == "quantum_fraud_detector":
                        config = {
                            "detection_threshold": 0.8,
                            "false_positive_rate": 0.01,
                            "anomaly_sensitivity": 0.7,
                        }
                    else:
                        config = {}

                    algorithm = create_algorithm_instance(template_name, config)
                    test_algorithms.append(
                        {"name": template_name, "instance": algorithm, "config": config}
                    )

                    logger.info(f"✅ Created {template_name} instance")

                except Exception as e:
                    logger.warning(f"⚠️  Failed to create {template_name}: {e}")

            # Test algorithm validation
            validation_results = []
            for test_algo in test_algorithms:
                try:
                    # Test input validation
                    test_input = {
                        "assets": ["AAPL", "GOOGL", "MSFT", "TSLA"],
                        "returns": [0.12, 0.15, 0.10, 0.25],
                        "covariance": [
                            [0.04, 0.02, 0.01, 0.03],
                            [0.02, 0.06, 0.02, 0.04],
                            [0.01, 0.02, 0.05, 0.02],
                            [0.03, 0.04, 0.02, 0.08],
                        ],
                        "constraints": {"risk_aversion": 0.5, "budget_penalty": 1000},
                    }

                    is_valid = test_algo["instance"].validate_input(test_input)
                    validation_results.append(
                        {
                            "algorithm": test_algo["name"],
                            "validation_passed": is_valid,
                            "input_schema": test_input,
                        }
                    )

                    logger.info(
                        f"✅ {test_algo['name']} input validation: {'PASSED' if is_valid else 'FAILED'}"
                    )

                except Exception as e:
                    logger.warning(
                        f"⚠️  Validation test failed for {test_algo['name']}: {e}"
                    )

            demo_result = {
                "demo_name": "Advanced Algorithm Templates",
                "status": "success",
                "templates_available": len(templates),
                "test_algorithms_created": len(test_algorithms),
                "validation_tests_passed": len(
                    [r for r in validation_results if r["validation_passed"]]
                ),
                "total_validation_tests": len(validation_results),
                "template_categories": list(
                    set(t.category.value for t in templates.values())
                ),
                "quantum_enhanced_count": sum(
                    1 for t in templates.values() if t.quantum_enhancement
                ),
            }

            self.demo_results.append(demo_result)
            logger.info("✅ Advanced Algorithm Templates demo completed successfully")

        except Exception as e:
            logger.error(f"❌ Advanced Algorithm Templates demo failed: {e}")
            self.demo_results.append(
                {
                    "demo_name": "Advanced Algorithm Templates",
                    "status": "failed",
                    "error": str(e),
                }
            )

    async def _demo_advanced_automation_workflows(self):
        """Demonstrate advanced automation workflow capabilities"""
        logger.info("\n⚙️  Demo 3: Advanced Automation Workflows")
        logger.info("-" * 40)

        try:
            from src.nqba_stack.automation.advanced_automation_workflows import (
                create_decision_automation_workflow,
                create_algorithm_optimization_workflow,
                create_deployment_automation_workflow,
            )

            # Create workflow instances
            workflows = {
                "decision": create_decision_automation_workflow(),
                "algorithm": create_algorithm_optimization_workflow(),
                "deployment": create_deployment_automation_workflow(),
            }

            logger.info(f"✅ Created {len(workflows)} workflow instances")

            # Test workflow execution
            workflow_results = {}
            context = {"demo_mode": True, "target_automation": 95.0}

            for workflow_name, workflow in workflows.items():
                logger.info(f"\n📋 Testing {workflow_name.title()} Workflow...")

                try:
                    result = await workflow.execute(context)
                    workflow_results[workflow_name] = result

                    logger.info(
                        f"  Status: {'✅ SUCCESS' if result.overall_success else '❌ FAILED'}"
                    )
                    logger.info(f"  Automation Level: {result.automation_level:.1f}%")
                    logger.info(f"  Steps Completed: {len(result.steps_completed)}")
                    logger.info(f"  Steps Failed: {len(result.steps_failed)}")
                    logger.info(
                        f"  Execution Time: {result.performance_metrics.get('execution_time', 0):.2f}s"
                    )

                except Exception as e:
                    logger.error(f"  ❌ Workflow execution failed: {e}")
                    workflow_results[workflow_name] = {"error": str(e)}

            # Calculate overall workflow performance
            successful_workflows = [
                r
                for r in workflow_results.values()
                if isinstance(r, type(workflow_results["decision"]))
                and r.overall_success
            ]
            avg_automation = (
                np.mean([r.automation_level for r in successful_workflows])
                if successful_workflows
                else 0
            )

            demo_result = {
                "demo_name": "Advanced Automation Workflows",
                "status": "success",
                "workflows_created": len(workflows),
                "workflows_executed": len(workflow_results),
                "successful_workflows": len(successful_workflows),
                "average_automation_level": avg_automation,
                "workflow_details": {
                    name: {
                        "success": isinstance(
                            result, type(workflow_results["decision"])
                        )
                        and result.overall_success,
                        "automation_level": (
                            result.automation_level
                            if isinstance(result, type(workflow_results["decision"]))
                            else 0
                        ),
                        "steps_completed": (
                            len(result.steps_completed)
                            if isinstance(result, type(workflow_results["decision"]))
                            else 0
                        ),
                    }
                    for name, result in workflow_results.items()
                },
            }

            self.demo_results.append(demo_result)
            logger.info("✅ Advanced Automation Workflows demo completed successfully")

        except Exception as e:
            logger.error(f"❌ Advanced Automation Workflows demo failed: {e}")
            self.demo_results.append(
                {
                    "demo_name": "Advanced Automation Workflows",
                    "status": "failed",
                    "error": str(e),
                }
            )

    async def _demo_workflow_orchestration(self):
        """Demonstrate workflow orchestration capabilities"""
        logger.info("\n🎼 Demo 4: Workflow Orchestration")
        logger.info("-" * 40)

        try:
            from src.nqba_stack.automation.advanced_automation_workflows import (
                create_workflow_orchestrator,
                create_decision_automation_workflow,
                create_algorithm_optimization_workflow,
                create_deployment_automation_workflow,
            )

            # Create orchestrator
            orchestrator = create_workflow_orchestrator()
            logger.info("✅ Workflow Orchestrator created")

            # Create and register workflows
            workflows = [
                create_decision_automation_workflow(),
                create_algorithm_optimization_workflow(),
                create_deployment_automation_workflow(),
            ]

            for workflow in workflows:
                orchestrator.register_workflow(workflow)
                logger.info(f"📝 Registered workflow: {workflow.name}")

            # Execute workflow sequence
            context = {"demo_mode": True, "target_automation": 95.0}
            workflow_sequence = [w.workflow_id for w in workflows]

            logger.info(
                f"\n🔄 Executing workflow sequence with {len(workflows)} workflows..."
            )
            sequence_result = await orchestrator.execute_workflow_sequence(
                workflow_sequence, context
            )

            # Display sequence results
            logger.info(f"  Sequence ID: {sequence_result['sequence_id']}")
            logger.info(
                f"  Overall Success: {'✅' if sequence_result['sequence_success'] else '❌'}"
            )
            logger.info(
                f"  Workflows Executed: {sequence_result['workflows_executed']}"
            )
            logger.info(
                f"  Overall Automation: {sequence_result['overall_automation_level']:.1f}%"
            )

            # Get orchestrator summary
            summary = orchestrator.get_orchestration_summary()
            logger.info(f"\n🏆 Orchestrator Summary:")
            logger.info(f"  Total Sequences: {summary['total_sequences']}")
            logger.info(f"  Success Rate: {summary['success_rate']:.1%}")
            logger.info(
                f"  Average Automation: {summary['average_automation_level']:.1f}%"
            )

            demo_result = {
                "demo_name": "Workflow Orchestration",
                "status": "success",
                "orchestrator_created": True,
                "workflows_registered": len(workflows),
                "sequence_executed": True,
                "sequence_success": sequence_result["sequence_success"],
                "overall_automation": sequence_result["overall_automation_level"],
                "orchestrator_summary": summary,
            }

            self.demo_results.append(demo_result)
            logger.info("✅ Workflow Orchestration demo completed successfully")

        except Exception as e:
            logger.error(f"❌ Workflow Orchestration demo failed: {e}")
            self.demo_results.append(
                {
                    "demo_name": "Workflow Orchestration",
                    "status": "failed",
                    "error": str(e),
                }
            )

    async def _demo_performance_integration(self):
        """Demonstrate performance and integration capabilities"""
        logger.info("\n🚀 Demo 5: Performance & Integration")
        logger.info("-" * 40)

        try:
            # Test configuration integration
            config_status = (
                self.config_manager.get_operational_status()
                if self.config_manager
                else {}
            )

            # Test algorithm template integration
            from src.nqba_stack.algorithms.advanced_algorithm_templates import (
                get_algorithm_templates,
            )

            templates = get_algorithm_templates()

            # Test workflow integration
            from src.nqba_stack.automation.advanced_automation_workflows import (
                create_workflow_orchestrator,
            )

            orchestrator = create_workflow_orchestrator()

            # Performance metrics
            total_demo_time = (datetime.now() - self.start_time).total_seconds()
            successful_demos = len(
                [r for r in self.demo_results if r["status"] == "success"]
            )
            total_demos = len(self.demo_results)

            # Calculate overall automation level
            automation_levels = []
            for result in self.demo_results:
                if "average_automation_level" in result:
                    automation_levels.append(result["average_automation_level"])
                elif "overall_automation" in result:
                    automation_levels.append(result["overall_automation"])

            overall_automation = np.mean(automation_levels) if automation_levels else 0

            # Integration status
            integration_status = {
                "configuration_manager": bool(self.config_manager),
                "algorithm_templates": len(templates),
                "workflow_orchestrator": bool(orchestrator),
                "all_components_available": bool(self.config_manager)
                and len(templates) > 0
                and bool(orchestrator),
            }

            logger.info(
                f"✅ Configuration Manager: {'Available' if integration_status['configuration_manager'] else 'Not Available'}"
            )
            logger.info(
                f"✅ Algorithm Templates: {integration_status['algorithm_templates']} available"
            )
            logger.info(
                f"✅ Workflow Orchestrator: {'Available' if integration_status['workflow_orchestrator'] else 'Not Available'}"
            )
            logger.info(
                f"✅ All Components: {'Available' if integration_status['all_components_available'] else 'Not Available'}"
            )

            logger.info(f"\n📊 Performance Metrics:")
            logger.info(f"  Total Demo Time: {total_demo_time:.2f}s")
            logger.info(
                f"  Demo Success Rate: {successful_demos}/{total_demos} ({successful_demos/total_demos*100:.1f}%)"
            )
            logger.info(f"  Overall Automation Level: {overall_automation:.1f}%")

            demo_result = {
                "demo_name": "Performance & Integration",
                "status": "success",
                "total_demo_time": total_demo_time,
                "demo_success_rate": successful_demos / total_demos,
                "overall_automation_level": overall_automation,
                "integration_status": integration_status,
                "performance_metrics": {
                    "total_demos": total_demos,
                    "successful_demos": successful_demos,
                    "failed_demos": total_demos - successful_demos,
                },
            }

            self.demo_results.append(demo_result)
            logger.info("✅ Performance & Integration demo completed successfully")

        except Exception as e:
            logger.error(f"❌ Performance & Integration demo failed: {e}")
            self.demo_results.append(
                {
                    "demo_name": "Performance & Integration",
                    "status": "failed",
                    "error": str(e),
                }
            )

    async def _generate_demo_report(self):
        """Generate comprehensive demo report"""
        logger.info("\n📋 Generating Demo Report")
        logger.info("=" * 60)

        # Calculate summary statistics
        total_demos = len(self.demo_results)
        successful_demos = len(
            [r for r in self.demo_results if r["status"] == "success"]
        )
        failed_demos = total_demos - successful_demos

        # Calculate automation metrics
        automation_levels = []
        for result in self.demo_results:
            if "average_automation_level" in result:
                automation_levels.append(result["average_automation_level"])
            elif "overall_automation" in result:
                automation_levels.append(result["overall_automation"])
            elif "overall_automation_level" in result:
                automation_levels.append(result["overall_automation_level"])

        overall_automation = np.mean(automation_levels) if automation_levels else 0

        # Generate report
        report = {
            "demo_summary": {
                "total_demos": total_demos,
                "successful_demos": successful_demos,
                "failed_demos": failed_demos,
                "success_rate": (
                    successful_demos / total_demos if total_demos > 0 else 0
                ),
                "overall_automation_level": overall_automation,
                "execution_time": (
                    (datetime.now() - self.start_time).total_seconds()
                    if self.start_time
                    else 0
                ),
            },
            "demo_details": self.demo_results,
            "timestamp": datetime.now().isoformat(),
            "platform_version": "2.0.0",
            "capabilities_demonstrated": [
                "Advanced Configuration Management",
                "World-Class Algorithm Templates",
                "Advanced Automation Workflows",
                "Workflow Orchestration",
                "Performance Integration",
            ],
        }

        # Save report to file
        report_filename = f"advanced_automation_demo_report_{int(time.time())}.json"
        try:
            with open(report_filename, "w") as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"📄 Report saved to: {report_filename}")
        except Exception as e:
            logger.warning(f"⚠️  Could not save report to file: {e}")

        # Display summary
        logger.info(f"\n🏆 ADVANCED AUTOMATION DEMO COMPLETED")
        logger.info("=" * 60)
        logger.info(f"📊 Total Demos: {total_demos}")
        logger.info(f"✅ Successful: {successful_demos}")
        logger.info(f"❌ Failed: {failed_demos}")
        logger.info(f"🎯 Success Rate: {successful_demos/total_demos*100:.1f}%")
        logger.info(f"🚀 Overall Automation: {overall_automation:.1f}%")
        logger.info(
            f"⏱️  Total Execution Time: {report['demo_summary']['execution_time']:.2f}s"
        )

        if overall_automation >= 90:
            logger.info("🎉 TARGET ACHIEVED: 90%+ Automation Level!")
        elif overall_automation >= 80:
            logger.info("🎯 EXCELLENT: 80%+ Automation Level!")
        elif overall_automation >= 70:
            logger.info("👍 GOOD: 70%+ Automation Level!")
        else:
            logger.info("📈 PROGRESS: Automation level below target, review needed")

        return report


async def main():
    """Main demo execution"""
    try:
        demo = AdvancedAutomationDemo()
        await demo.run_comprehensive_demo()

    except Exception as e:
        logger.error(f"❌ Demo execution failed: {e}")
        logger.info("\n💡 Make sure all dependencies are installed:")
        logger.info("   pip install numpy pandas pyyaml")
        raise


if __name__ == "__main__":
    asyncio.run(main())
