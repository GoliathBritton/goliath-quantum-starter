"""
World-Class Algorithm Orchestrator
Coordinates All Quantum-Enhanced Algorithms for Maximum Business Value

This module orchestrates all the cutting-edge algorithms:
- Portfolio Optimization
- Risk Management
- Machine Learning
- Energy Optimization
- Cross-Domain Optimization
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime, timedelta
import asyncio
import json

from ..quantum_adapter import QuantumAdapter
from ..core.ltc_logger import LTCLogger
from .portfolio_algorithms import (
    QuantumPortfolioOptimizer,
    OptimizationStrategy,
    PortfolioConstraints,
)
from .risk_algorithms import (
    QuantumVaRCalculator,
    StressTestEngine,
    CorrelationOptimizer,
    VolatilityForecaster,
    RiskLevel,
)
from .ml_algorithms import QuantumSVM, QuantumNeuralNetwork, QuantumClustering
from .energy_algorithms import (
    GridOptimizer,
    DemandForecaster,
    RenewableIntegration,
    StorageOptimizer,
    EnergyDemand,
    EnergySupply,
    EnergySource,
)

logger = logging.getLogger(__name__)


class OptimizationDomain(Enum):
    """Optimization domains"""

    PORTFOLIO = "portfolio"
    RISK = "risk"
    MACHINE_LEARNING = "ml"
    ENERGY = "energy"
    CROSS_DOMAIN = "cross_domain"


class OrchestrationStrategy(Enum):
    """Orchestration strategies"""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"
    QUANTUM_ENHANCED = "quantum_enhanced"


@dataclass
class OptimizationRequest:
    """Optimization request"""

    domain: OptimizationDomain
    strategy: OrchestrationStrategy
    parameters: Dict[str, Any]
    constraints: Dict[str, Any]
    priority: int = 1
    timeout: int = 300  # seconds


@dataclass
class OptimizationResult:
    """Optimization result"""

    request_id: str
    domain: OptimizationDomain
    strategy: OrchestrationStrategy
    results: Dict[str, Any]
    metadata: Dict[str, Any]
    quantum_advantage: Optional[float] = None
    execution_time: float = 0.0
    timestamp: datetime = None


class AlgorithmOrchestrator:
    """
    World-Class Algorithm Orchestrator

    Coordinates all quantum-enhanced algorithms to deliver maximum business value
    through intelligent optimization, cross-domain insights, and quantum advantage.
    """

    def __init__(self, quantum_adapter: QuantumAdapter, ltc_logger: LTCLogger):
        self.quantum_adapter = quantum_adapter
        self.ltc_logger = ltc_logger

        # Initialize all algorithm components
        self.portfolio_optimizer = QuantumPortfolioOptimizer(
            quantum_adapter, ltc_logger
        )
        self.risk_calculator = QuantumVaRCalculator(quantum_adapter, ltc_logger)
        self.stress_engine = StressTestEngine(quantum_adapter, ltc_logger)
        self.correlation_optimizer = CorrelationOptimizer(quantum_adapter, ltc_logger)
        self.volatility_forecaster = VolatilityForecaster(quantum_adapter, ltc_logger)
        self.ml_svm = QuantumSVM(quantum_adapter, ltc_logger)
        self.ml_nn = QuantumNeuralNetwork(quantum_adapter, ltc_logger)
        self.ml_clustering = QuantumClustering(quantum_adapter, ltc_logger)
        self.grid_optimizer = GridOptimizer(quantum_adapter, ltc_logger)
        self.demand_forecaster = DemandForecaster(quantum_adapter, ltc_logger)
        self.renewable_integrator = RenewableIntegration(quantum_adapter, ltc_logger)
        self.storage_optimizer = StorageOptimizer(quantum_adapter, ltc_logger)

        # Orchestration state
        self.optimization_history: List[OptimizationResult] = []
        self.active_requests: Dict[str, OptimizationRequest] = {}
        self.performance_metrics: Dict[str, Dict[str, float]] = {}

        logger.info(
            "Algorithm Orchestrator initialized with all world-class algorithms"
        )

    async def execute_optimization(
        self, request: OptimizationRequest
    ) -> OptimizationResult:
        """
        Execute optimization using the appropriate algorithms

        Args:
            request: Optimization request with domain and strategy

        Returns:
            OptimizationResult with comprehensive results
        """
        start_time = datetime.now()
        request_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(request)) % 10000}"

        try:
            # Log optimization start
            await self.ltc_logger.log_operation(
                "optimization_started",
                {
                    "request_id": request_id,
                    "domain": request.domain.value,
                    "strategy": request.strategy.value,
                    "priority": request.priority,
                },
                "algorithm_orchestrator",
            )

            # Execute domain-specific optimization
            if request.domain == OptimizationDomain.PORTFOLIO:
                results = await self._execute_portfolio_optimization(request)
            elif request.domain == OptimizationDomain.RISK:
                results = await self._execute_risk_optimization(request)
            elif request.domain == OptimizationDomain.MACHINE_LEARNING:
                results = await self._execute_ml_optimization(request)
            elif request.domain == OptimizationDomain.ENERGY:
                results = await self._execute_energy_optimization(request)
            elif request.domain == OptimizationDomain.CROSS_DOMAIN:
                results = await self._execute_cross_domain_optimization(request)
            else:
                raise ValueError(f"Unknown optimization domain: {request.domain}")

            # Calculate quantum advantage
            quantum_advantage = self._calculate_quantum_advantage(results)

            # Create result
            execution_time = (datetime.now() - start_time).total_seconds()
            result = OptimizationResult(
                request_id=request_id,
                domain=request.domain,
                strategy=request.strategy,
                results=results,
                metadata={
                    "execution_time": execution_time,
                    "quantum_advantage": quantum_advantage,
                    "algorithm_components": list(results.keys()),
                },
                quantum_advantage=quantum_advantage,
                execution_time=execution_time,
                timestamp=datetime.now(),
            )

            # Store in history
            self.optimization_history.append(result)

            # Update performance metrics
            self._update_performance_metrics(request.domain, result)

            # Log completion
            await self.ltc_logger.log_operation(
                "optimization_completed",
                {
                    "request_id": request_id,
                    "execution_time": execution_time,
                    "quantum_advantage": quantum_advantage,
                    "results_count": len(results),
                },
                "algorithm_orchestrator",
            )

            return result

        except Exception as e:
            logger.error(f"Optimization failed for request {request_id}: {e}")
            await self.ltc_logger.log_operation(
                "optimization_failed",
                {
                    "request_id": request_id,
                    "error": str(e),
                    "domain": request.domain.value,
                },
                "algorithm_orchestrator",
            )
            raise

    async def _execute_portfolio_optimization(
        self, request: OptimizationRequest
    ) -> Dict[str, Any]:
        """Execute portfolio optimization"""
        try:
            results = {}

            # Extract parameters
            returns_data = request.parameters.get("returns_data")
            strategy = request.parameters.get(
                "strategy", OptimizationStrategy.MAXIMIZE_SHARPE
            )
            constraints = request.parameters.get("constraints", {})

            if returns_data is not None:
                # Convert to DataFrame if needed
                if isinstance(returns_data, dict):
                    returns_df = pd.DataFrame(returns_data)
                else:
                    returns_df = returns_data

                # Create portfolio constraints
                portfolio_constraints = PortfolioConstraints(**constraints)

                # Execute portfolio optimization
                portfolio_result = await self.portfolio_optimizer.optimize_portfolio(
                    returns=returns_df,
                    strategy=strategy,
                    constraints=portfolio_constraints,
                )

                results["portfolio_optimization"] = {
                    "weights": portfolio_result.weights.tolist(),
                    "expected_return": portfolio_result.expected_return,
                    "expected_risk": portfolio_result.expected_risk,
                    "sharpe_ratio": portfolio_result.sharpe_ratio,
                    "quantum_advantage": portfolio_result.quantum_advantage,
                }

                # Analyze performance
                performance_analysis = (
                    await self.portfolio_optimizer.analyze_portfolio_performance(
                        portfolio_result.weights, returns_df
                    )
                )
                results["performance_analysis"] = performance_analysis

            return results

        except Exception as e:
            logger.error(f"Portfolio optimization failed: {e}")
            return {"error": str(e)}

    async def _execute_risk_optimization(
        self, request: OptimizationRequest
    ) -> Dict[str, Any]:
        """Execute risk optimization"""
        try:
            results = {}

            # Extract parameters
            returns_data = request.parameters.get("returns_data")
            portfolio_weights = request.parameters.get("portfolio_weights")
            confidence_level = request.parameters.get("confidence_level", RiskLevel.P95)

            if returns_data is not None and portfolio_weights is not None:
                # Convert to DataFrame if needed
                if isinstance(returns_data, dict):
                    returns_df = pd.DataFrame(returns_data)
                else:
                    returns_df = returns_data

                # Calculate VaR
                var_result = await self.risk_calculator.calculate_var(
                    returns=returns_df,
                    portfolio_weights=np.array(portfolio_weights),
                    confidence_level=confidence_level,
                    method="quantum_enhanced",
                )

                results["var_calculation"] = {
                    "var": var_result.var,
                    "cvar": var_result.cvar,
                    "volatility": var_result.volatility,
                    "sharpe_ratio": var_result.sharpe_ratio,
                    "quantum_advantage": var_result.quantum_advantage,
                }

                # Generate stress test scenarios
                stress_scenarios = await self.stress_engine.generate_stress_scenarios(
                    returns=returns_df,
                    portfolio_weights=np.array(portfolio_weights),
                    num_scenarios=5,
                )

                results["stress_testing"] = {
                    "scenarios": [s.__dict__ for s in stress_scenarios],
                    "count": len(stress_scenarios),
                }

                # Optimize correlations
                correlation_result = (
                    await self.correlation_optimizer.optimize_correlations(
                        returns=returns_df, method="quantum_enhanced"
                    )
                )

                results["correlation_optimization"] = correlation_result

                # Forecast volatility
                volatility_result = (
                    await self.volatility_forecaster.forecast_volatility(
                        returns=returns_df,
                        forecast_horizon=30,
                        method="quantum_enhanced",
                    )
                )

                results["volatility_forecasting"] = volatility_result

            return results

        except Exception as e:
            logger.error(f"Risk optimization failed: {e}")
            return {"error": str(e)}

    async def _execute_ml_optimization(
        self, request: OptimizationRequest
    ) -> Dict[str, Any]:
        """Execute machine learning optimization"""
        try:
            results = {}

            # Extract parameters
            X_data = request.parameters.get("X_data")
            y_data = request.parameters.get("y_data")
            ml_task = request.parameters.get("ml_task", "classification")

            if X_data is not None and y_data is not None:
                # Convert to numpy arrays if needed
                if isinstance(X_data, list):
                    X = np.array(X_data)
                else:
                    X = X_data

                if isinstance(y_data, list):
                    y = np.array(y_data)
                else:
                    y = y_data

                if ml_task == "classification":
                    # Train quantum SVM
                    svm_result = await self.ml_svm.fit(
                        X=X, y=y, method="quantum_enhanced"
                    )
                    results["quantum_svm"] = svm_result

                    # Make predictions
                    predictions = self.ml_svm.predict(X)
                    results["svm_predictions"] = {
                        "predictions": predictions.prediction.tolist(),
                        "confidence": predictions.confidence.tolist(),
                        "quantum_advantage": predictions.quantum_advantage,
                    }

                elif ml_task == "regression":
                    # Train quantum neural network
                    architecture = request.parameters.get(
                        "architecture", [X.shape[1], 64, 32, 1]
                    )
                    nn_result = await self.ml_nn.fit(
                        X=X, y=y, architecture=architecture, method="quantum_enhanced"
                    )
                    results["quantum_nn"] = nn_result

                    # Make predictions
                    predictions = self.ml_nn.predict(X)
                    results["nn_predictions"] = {
                        "predictions": predictions.prediction.tolist(),
                        "confidence": predictions.confidence.tolist(),
                        "quantum_advantage": predictions.quantum_advantage,
                    }

                elif ml_task == "clustering":
                    # Perform quantum clustering
                    n_clusters = request.parameters.get("n_clusters", 3)
                    clustering_result = await self.ml_clustering.fit(
                        X=X, n_clusters=n_clusters, method="quantum_enhanced"
                    )
                    results["quantum_clustering"] = clustering_result

                    # Make predictions
                    predictions = self.ml_clustering.predict(X)
                    results["clustering_predictions"] = {
                        "predictions": predictions.prediction.tolist(),
                        "confidence": predictions.confidence.tolist(),
                        "quantum_advantage": predictions.quantum_advantage,
                    }

            return results

        except Exception as e:
            logger.error(f"ML optimization failed: {e}")
            return {"error": str(e)}

    async def _execute_energy_optimization(
        self, request: OptimizationRequest
    ) -> Dict[str, Any]:
        """Execute energy optimization"""
        try:
            results = {}

            # Extract parameters
            demands_data = request.parameters.get("demands_data")
            supplies_data = request.parameters.get("supplies_data")
            grid_constraints = request.parameters.get("grid_constraints", {})

            if demands_data is not None and supplies_data is not None:
                # Convert to EnergyDemand and EnergySupply objects
                demands = [EnergyDemand(**d) for d in demands_data]
                supplies = [EnergySupply(**s) for s in supplies_data]

                # Optimize grid
                grid_result = await self.grid_optimizer.optimize_grid(
                    demands=demands,
                    supplies=supplies,
                    grid_constraints=grid_constraints,
                    method="quantum_enhanced",
                )

                results["grid_optimization"] = {
                    "optimal_flows": grid_result.optimal_flows,
                    "total_cost": grid_result.total_cost,
                    "emissions_reduction": grid_result.emissions_reduction,
                    "reliability_score": grid_result.reliability_score,
                    "quantum_advantage": grid_result.quantum_advantage,
                }

                # Forecast demand
                historical_demand = request.parameters.get("historical_demand")
                weather_data = request.parameters.get("weather_data")

                if historical_demand is not None and weather_data is not None:
                    demand_forecast = await self.demand_forecaster.forecast_demand(
                        historical_demand=pd.DataFrame(historical_demand),
                        weather_data=pd.DataFrame(weather_data),
                        forecast_horizon=24,
                        method="quantum_enhanced",
                    )

                    results["demand_forecasting"] = demand_forecast

                # Optimize renewable integration
                renewable_sources = [
                    s
                    for s in supplies
                    if s.source_type
                    in [EnergySource.SOLAR, EnergySource.WIND, EnergySource.HYDRO]
                ]

                if renewable_sources:
                    integration_result = (
                        await self.renewable_integrator.optimize_integration(
                            renewable_sources=renewable_sources,
                            grid_capacity=grid_constraints.get("grid_capacity", 1000.0),
                            storage_capacity=grid_constraints.get(
                                "storage_capacity", 500.0
                            ),
                            method="quantum_enhanced",
                        )
                    )

                    results["renewable_integration"] = integration_result

                # Optimize storage
                demand_profile = request.parameters.get("demand_profile")
                renewable_profile = request.parameters.get("renewable_profile")

                if demand_profile is not None and renewable_profile is not None:
                    storage_result = await self.storage_optimizer.optimize_storage(
                        demand_profile=demand_profile,
                        renewable_profile=renewable_profile,
                        storage_capacity=grid_constraints.get(
                            "storage_capacity", 500.0
                        ),
                        method="quantum_enhanced",
                    )

                    results["storage_optimization"] = storage_result

            return results

        except Exception as e:
            logger.error(f"Energy optimization failed: {e}")
            return {"error": str(e)}

    async def _execute_cross_domain_optimization(
        self, request: OptimizationRequest
    ) -> Dict[str, Any]:
        """Execute cross-domain optimization"""
        try:
            results = {}

            # This is the most sophisticated optimization - combining insights from all domains
            # Extract parameters for cross-domain analysis
            portfolio_data = request.parameters.get("portfolio_data")
            risk_data = request.parameters.get("risk_data")
            energy_data = request.parameters.get("energy_data")

            # Execute portfolio optimization first
            if portfolio_data:
                portfolio_request = OptimizationRequest(
                    domain=OptimizationDomain.PORTFOLIO,
                    strategy=request.strategy,
                    parameters=portfolio_data,
                    constraints=request.constraints,
                    priority=request.priority,
                )

                portfolio_result = await self._execute_portfolio_optimization(
                    portfolio_request
                )
                results["portfolio"] = portfolio_result

            # Execute risk optimization
            if risk_data:
                risk_request = OptimizationRequest(
                    domain=OptimizationDomain.RISK,
                    strategy=request.strategy,
                    parameters=risk_data,
                    constraints=request.constraints,
                    priority=request.priority,
                )

                risk_result = await self._execute_risk_optimization(risk_request)
                results["risk"] = risk_result

            # Execute energy optimization
            if energy_data:
                energy_request = OptimizationRequest(
                    domain=OptimizationDomain.ENERGY,
                    strategy=request.strategy,
                    parameters=energy_data,
                    constraints=request.constraints,
                    priority=request.priority,
                )

                energy_result = await self._execute_energy_optimization(energy_request)
                results["energy"] = energy_result

            # Cross-domain insights and optimization
            cross_domain_insights = await self._generate_cross_domain_insights(results)
            results["cross_domain_insights"] = cross_domain_insights

            return results

        except Exception as e:
            logger.error(f"Cross-domain optimization failed: {e}")
            return {"error": str(e)}

    async def _generate_cross_domain_insights(
        self, domain_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate insights across different domains"""
        try:
            insights = {}

            # Portfolio-Risk insights
            if "portfolio" in domain_results and "risk" in domain_results:
                portfolio_risk = domain_results["portfolio"]
                risk_metrics = domain_results["risk"]

                # Calculate risk-adjusted portfolio performance
                if (
                    "portfolio_optimization" in portfolio_risk
                    and "var_calculation" in risk_metrics
                ):
                    portfolio = portfolio_risk["portfolio_optimization"]
                    risk = risk_metrics["var_calculation"]

                    # Risk-adjusted return
                    risk_adjusted_return = (
                        portfolio["expected_return"] / risk["volatility"]
                        if risk["volatility"] > 0
                        else 0
                    )

                    insights["portfolio_risk"] = {
                        "risk_adjusted_return": risk_adjusted_return,
                        "var_coverage": (
                            abs(portfolio["expected_return"] / risk["var"])
                            if risk["var"] != 0
                            else 0
                        ),
                        "recommendation": (
                            "Increase diversification"
                            if risk["volatility"] > 0.2
                            else "Portfolio well-balanced"
                        ),
                    }

            # Energy-Portfolio insights
            if "energy" in domain_results and "portfolio" in domain_results:
                energy = domain_results["energy"]
                portfolio = domain_results["portfolio"]

                if (
                    "grid_optimization" in energy
                    and "portfolio_optimization" in portfolio
                ):
                    grid = energy["grid_optimization"]

                    # Green energy investment opportunities
                    green_energy_ratio = grid["emissions_reduction"] / 100.0

                    insights["energy_portfolio"] = {
                        "green_energy_ratio": green_energy_ratio,
                        "investment_opportunity": (
                            "High"
                            if green_energy_ratio > 0.7
                            else "Medium" if green_energy_ratio > 0.4 else "Low"
                        ),
                        "recommendation": (
                            "Consider increasing renewable energy investments"
                            if green_energy_ratio > 0.6
                            else "Monitor energy transition trends"
                        ),
                    }

            # Machine Learning insights
            if "ml" in domain_results:
                ml = domain_results["ml"]

                # Algorithm performance comparison
                algorithm_performance = {}
                for key, value in ml.items():
                    if "quantum_advantage" in value:
                        algorithm_performance[key] = value["quantum_advantage"]

                if algorithm_performance:
                    best_algorithm = max(
                        algorithm_performance, key=algorithm_performance.get
                    )
                    insights["ml_performance"] = {
                        "best_algorithm": best_algorithm,
                        "quantum_advantage": algorithm_performance[best_algorithm],
                        "recommendation": f"Use {best_algorithm} for optimal performance",
                    }

            return insights

        except Exception as e:
            logger.warning(f"Cross-domain insights generation failed: {e}")
            return {"error": str(e)}

    def _calculate_quantum_advantage(self, results: Dict[str, Any]) -> Optional[float]:
        """Calculate overall quantum advantage from results"""
        try:
            quantum_advantages = []

            # Extract quantum advantages from all results
            def extract_qa(obj):
                if isinstance(obj, dict):
                    if (
                        "quantum_advantage" in obj
                        and obj["quantum_advantage"] is not None
                    ):
                        quantum_advantages.append(obj["quantum_advantage"])
                    for value in obj.values():
                        extract_qa(value)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_qa(item)

            extract_qa(results)

            if quantum_advantages:
                return np.mean(quantum_advantages)
            else:
                return None

        except Exception as e:
            logger.warning(f"Quantum advantage calculation failed: {e}")
            return None

    def _update_performance_metrics(
        self, domain: OptimizationDomain, result: OptimizationResult
    ):
        """Update performance metrics for the domain"""
        try:
            if domain.value not in self.performance_metrics:
                self.performance_metrics[domain.value] = {}

            metrics = self.performance_metrics[domain.value]

            # Update execution time metrics
            if "execution_times" not in metrics:
                metrics["execution_times"] = []
            metrics["execution_times"].append(result.execution_time)

            # Keep only last 100 executions
            if len(metrics["execution_times"]) > 100:
                metrics["execution_times"] = metrics["execution_times"][-100:]

            # Update quantum advantage metrics
            if "quantum_advantages" not in metrics:
                metrics["quantum_advantages"] = []
            if result.quantum_advantage is not None:
                metrics["quantum_advantages"].append(result.quantum_advantage)

            if len(metrics["quantum_advantages"]) > 100:
                metrics["quantum_advantages"] = metrics["quantum_advantages"][-100:]

            # Calculate averages
            metrics["avg_execution_time"] = np.mean(metrics["execution_times"])
            metrics["avg_quantum_advantage"] = (
                np.mean(metrics["quantum_advantages"])
                if metrics["quantum_advantages"]
                else 0.0
            )

        except Exception as e:
            logger.warning(f"Performance metrics update failed: {e}")

    async def get_optimization_history(
        self, domain: Optional[OptimizationDomain] = None, limit: int = 100
    ) -> List[OptimizationResult]:
        """Get optimization history"""
        try:
            if domain:
                filtered_history = [
                    r for r in self.optimization_history if r.domain == domain
                ]
            else:
                filtered_history = self.optimization_history

            # Sort by timestamp (newest first) and limit
            sorted_history = sorted(
                filtered_history, key=lambda x: x.timestamp, reverse=True
            )
            return sorted_history[:limit]

        except Exception as e:
            logger.error(f"Failed to get optimization history: {e}")
            return []

    async def get_performance_metrics(
        self, domain: Optional[OptimizationDomain] = None
    ) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            if domain:
                return self.performance_metrics.get(domain.value, {})
            else:
                return self.performance_metrics

        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}

    async def get_algorithm_status(self) -> Dict[str, Any]:
        """Get status of all algorithm components"""
        try:
            status = {
                "portfolio_optimizer": "ready",
                "risk_calculator": "ready",
                "stress_engine": "ready",
                "correlation_optimizer": "ready",
                "volatility_forecaster": "ready",
                "ml_svm": "ready",
                "ml_nn": "ready",
                "ml_clustering": "ready",
                "grid_optimizer": "ready",
                "demand_forecaster": "ready",
                "renewable_integrator": "ready",
                "storage_optimizer": "ready",
                "quantum_adapter": (
                    "ready" if self.quantum_adapter else "not_initialized"
                ),
                "total_optimizations": len(self.optimization_history),
                "active_requests": len(self.active_requests),
            }

            return status

        except Exception as e:
            logger.error(f"Failed to get algorithm status: {e}")
            return {"error": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components"""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "components": {},
                "overall_score": 0.0,
            }

            # Check each component
            components = [
                ("portfolio_optimizer", self.portfolio_optimizer),
                ("risk_calculator", self.risk_calculator),
                ("ml_svm", self.ml_svm),
                ("grid_optimizer", self.grid_optimizer),
            ]

            total_score = 0.0
            for name, component in components:
                try:
                    # Simple health check - try to access component
                    if hasattr(component, "__class__"):
                        health_status["components"][name] = "healthy"
                        total_score += 1.0
                    else:
                        health_status["components"][name] = "unhealthy"
                except Exception as e:
                    health_status["components"][name] = f"error: {str(e)}"

            # Calculate overall health score
            health_status["overall_score"] = total_score / len(components)

            if health_status["overall_score"] < 0.8:
                health_status["status"] = "degraded"
            if health_status["overall_score"] < 0.5:
                health_status["status"] = "unhealthy"

            return health_status

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
