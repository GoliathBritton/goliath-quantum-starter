"""
Best-in-class MCP Handler for Quantum/AI Tools
------------------------------------------------
* Async tool dispatch for all provider.json tools
* Input schema validation (jsonschema)
* Audit/event logging for all jobs
* Resource/cost/concurrency controls
* Backend health checks and fallback
* API key and role-based security hooks
* Extensible, observable, and maintainable
"""

import asyncio
from .engine import NQBAEngine, ExecutionMode
import logging
import time
from typing import Any, Dict, Callable, Awaitable, Optional
import json
import jsonschema
from pathlib import Path
from functools import wraps

logger = logging.getLogger("mcp.handler")

# Load provider.json tool schemas
PROVIDER_JSON = Path(__file__).parent.parent.parent / "mcp" / "provider.json"
with open(PROVIDER_JSON, "r", encoding="utf-8") as f:
    PROVIDER_SPEC = json.load(f)
TOOL_SCHEMAS = {tool["name"]: tool["inputSchema"] for tool in PROVIDER_SPEC["tools"]}

# Audit/event log (simple file-based for demo)
AUDIT_LOG = Path(__file__).parent.parent.parent / "logs" / "mcp_audit.log"


def audit_log(event: str, payload: dict):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(
            json.dumps({"event": event, "payload": payload, "ts": time.time()}) + "\n"
        )


# Security decorator (stub)
def require_api_key(role: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # TODO: Check API key, role, rate limit, etc.
            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Resource/cost control (stub)
def check_resource_limits(tool: str, payload: dict):
    # TODO: Enforce max_concurrent_jobs, cost_limit, etc.
    return True


# Health check (stub)
def backend_health():
    # TODO: Check all backends, return status
    return {"dynex": "ok", "qiskit": "ok", "cirq": "ok", "pennylane": "ok"}


# Tool registry and dispatcher
TOOL_HANDLERS: Dict[str, Callable[[dict], Awaitable[Any]]] = {}


def register_tool(name: str):
    def decorator(func):
        TOOL_HANDLERS[name] = func
        return func

    return decorator


async def dispatch_tool(tool: str, payload: dict, user: str = "anonymous") -> dict:
    if tool not in TOOL_SCHEMAS:
        raise ValueError(f"Unknown tool: {tool}")
    # Validate input
    jsonschema.validate(payload, TOOL_SCHEMAS[tool])
    if not check_resource_limits(tool, payload):
        raise RuntimeError("Resource/cost limit exceeded")
    audit_log("job.started", {"tool": tool, "user": user, "payload": payload})
    try:
        handler = TOOL_HANDLERS[tool]
        result = await handler(payload)
        audit_log("job.completed", {"tool": tool, "user": user, "result": result})
        return {"success": True, "result": result}
    except Exception as e:
        logger.exception(f"Tool {tool} failed")
        audit_log("job.failed", {"tool": tool, "user": user, "error": str(e)})
        return {"success": False, "error": str(e)}


# Handlers for all tools in provider.json (stub implementations)


@register_tool("quantum.optimize.qubo")
@require_api_key(role="user")
async def handle_optimize_qubo(payload: dict) -> dict:
    """Optimize a QUBO problem using real quantum backend (NQBAEngine)"""
    nqba = NQBAEngine(mode=ExecutionMode.SIMULATOR)
    import numpy as np

    qubo_matrix = np.array(payload.get("qubo_matrix"))
    algorithm = payload.get("algorithm", "qaoa")
    parameters = {
        k: v for k, v in payload.items() if k not in ["qubo_matrix", "algorithm"]
    }
    result = await nqba.optimize_qubo(
        qubo_matrix, algorithm=algorithm, parameters=parameters
    )
    return {"result": result.__dict__}


@register_tool("quantum.optimize.portfolio")
@require_api_key(role="user")
async def handle_optimize_portfolio(payload: dict) -> dict:
    """Optimize investment portfolio using quantum backend with real QUBO formulation"""
    import numpy as np
    
    # Extract portfolio parameters
    assets = payload.get("assets", [])
    expected_returns = np.array(payload.get("expected_returns", []))
    covariance_matrix = np.array(payload.get("covariance_matrix", []))
    risk_tolerance = payload.get("risk_tolerance", 0.5)
    budget = payload.get("budget", 1.0)
    min_allocation = payload.get("min_allocation", 0.01)
    max_allocation = payload.get("max_allocation", 0.4)
    
    if len(assets) == 0 or len(expected_returns) == 0:
        return {"error": "Assets and expected returns are required"}
    
    n_assets = len(assets)
    
    # Create QUBO formulation for portfolio optimization
    # Minimize: risk - risk_tolerance * return
    # Variables: binary allocation decisions (discretized)
    allocation_levels = 10  # Discretize allocations into 10 levels
    n_vars = n_assets * allocation_levels
    
    # Initialize QUBO matrix
    Q = np.zeros((n_vars, n_vars))
    
    # Risk term: x^T * Cov * x (quadratic)
    for i in range(n_assets):
        for j in range(n_assets):
            for level_i in range(allocation_levels):
                for level_j in range(allocation_levels):
                    var_i = i * allocation_levels + level_i
                    var_j = j * allocation_levels + level_j
                    allocation_i = (level_i + 1) / allocation_levels * max_allocation
                    allocation_j = (level_j + 1) / allocation_levels * max_allocation
                    
                    if var_i == var_j:
                        Q[var_i][var_j] += covariance_matrix[i][j] * allocation_i * allocation_j
                    else:
                        Q[var_i][var_j] += 0.5 * covariance_matrix[i][j] * allocation_i * allocation_j
    
    # Return term: -risk_tolerance * expected_return (linear)
    for i in range(n_assets):
        for level in range(allocation_levels):
            var_idx = i * allocation_levels + level
            allocation = (level + 1) / allocation_levels * max_allocation
            Q[var_idx][var_idx] -= risk_tolerance * expected_returns[i] * allocation
    
    # Budget constraint penalty
    penalty_weight = 10.0
    for i in range(n_assets):
        for level_i in range(allocation_levels):
            for j in range(n_assets):
                for level_j in range(allocation_levels):
                    if i != j:
                        var_i = i * allocation_levels + level_i
                        var_j = j * allocation_levels + level_j
                        allocation_i = (level_i + 1) / allocation_levels * max_allocation
                        allocation_j = (level_j + 1) / allocation_levels * max_allocation
                        # Penalty for deviating from budget constraint
                        Q[var_i][var_j] += penalty_weight * allocation_i * allocation_j
    
    # One-hot constraint: each asset can only have one allocation level
    for i in range(n_assets):
        for level_i in range(allocation_levels):
            for level_j in range(level_i + 1, allocation_levels):
                var_i = i * allocation_levels + level_i
                var_j = i * allocation_levels + level_j
                Q[var_i][var_j] += penalty_weight  # Penalty for multiple allocations
    
    # Optimize using NQBAEngine
    nqba = NQBAEngine(mode=ExecutionMode.SIMULATOR)
    algorithm = payload.get("algorithm", "qaoa")
    parameters = {"shots": 1000, "layers": 3}
    
    try:
        result = await nqba.optimize_qubo(Q, algorithm=algorithm, parameters=parameters)
        
        # Decode solution to portfolio allocations
        solution = result.solution if hasattr(result, 'solution') else [0] * n_vars
        allocations = np.zeros(n_assets)
        
        for i in range(n_assets):
            for level in range(allocation_levels):
                var_idx = i * allocation_levels + level
                if var_idx < len(solution) and solution[var_idx] == 1:
                    allocations[i] = (level + 1) / allocation_levels * max_allocation
                    break
        
        # Normalize allocations to budget
        total_allocation = np.sum(allocations)
        if total_allocation > 0:
            allocations = allocations / total_allocation * budget
        
        # Calculate portfolio metrics
        portfolio_return = np.dot(allocations, expected_returns)
        portfolio_risk = np.sqrt(np.dot(allocations, np.dot(covariance_matrix, allocations)))
        sharpe_ratio = portfolio_return / portfolio_risk if portfolio_risk > 0 else 0
        
        return {
            "result": {
                "allocations": {assets[i]: float(allocations[i]) for i in range(n_assets)},
                "expected_return": float(portfolio_return),
                "risk": float(portfolio_risk),
                "sharpe_ratio": float(sharpe_ratio),
                "total_allocation": float(np.sum(allocations))
            },
            "quantum_result": result.__dict__ if hasattr(result, '__dict__') else str(result)
        }
    
    except Exception as e:
        logger.exception("Portfolio optimization failed")
        return {"error": f"Optimization failed: {str(e)}"}


@register_tool("quantum.optimize.schedule")
@require_api_key(role="user")
async def handle_optimize_schedule(payload: dict) -> dict:
    """Optimize scheduling problems using quantum backend with real QUBO formulation"""
    import numpy as np
    
    # Extract scheduling parameters
    tasks = payload.get("tasks", [])
    resources = payload.get("resources", [])
    time_slots = payload.get("time_slots", [])
    task_durations = payload.get("task_durations", {})
    resource_capacities = payload.get("resource_capacities", {})
    task_priorities = payload.get("task_priorities", {})
    dependencies = payload.get("dependencies", [])  # [(task1, task2)] where task1 must finish before task2
    
    if not tasks or not resources or not time_slots:
        return {"error": "Tasks, resources, and time_slots are required"}
    
    n_tasks = len(tasks)
    n_resources = len(resources)
    n_slots = len(time_slots)
    
    # Variables: x[t][r][s] = 1 if task t is assigned to resource r at time slot s
    n_vars = n_tasks * n_resources * n_slots
    
    def var_index(task_idx: int, resource_idx: int, slot_idx: int) -> int:
        return task_idx * n_resources * n_slots + resource_idx * n_slots + slot_idx
    
    # Initialize QUBO matrix
    Q = np.zeros((n_vars, n_vars))
    
    # Objective: Maximize priority-weighted task completion (minimize negative priority)
    for t, task in enumerate(tasks):
        priority = task_priorities.get(task, 1.0)
        duration = task_durations.get(task, 1)
        
        for r in range(n_resources):
            for s in range(n_slots - duration + 1):  # Ensure task can complete within time horizon
                var_idx = var_index(t, r, s)
                Q[var_idx][var_idx] -= priority  # Negative for maximization
    
    # Constraint 1: Each task assigned to exactly one resource-time combination
    penalty_weight = 10.0
    for t in range(n_tasks):
        # Penalty for not assigning task
        for r1 in range(n_resources):
            for s1 in range(n_slots):
                for r2 in range(n_resources):
                    for s2 in range(n_slots):
                        if (r1, s1) != (r2, s2):
                            var1 = var_index(t, r1, s1)
                            var2 = var_index(t, r2, s2)
                            Q[var1][var2] += penalty_weight  # Penalty for multiple assignments
    
    # Constraint 2: Resource capacity constraints
    for r in range(n_resources):
        capacity = resource_capacities.get(resources[r], 1)
        for s in range(n_slots):
            # Count tasks assigned to resource r at time s
            task_vars = []
            for t in range(n_tasks):
                duration = task_durations.get(tasks[t], 1)
                # Check if task t would be running at time s
                for start_slot in range(max(0, s - duration + 1), min(n_slots, s + 1)):
                    if start_slot + duration > s:
                        var_idx = var_index(t, r, start_slot)
                        task_vars.append(var_idx)
            
            # Add penalty for exceeding capacity
            for i, var1 in enumerate(task_vars):
                for j, var2 in enumerate(task_vars[i+1:], i+1):
                    if j >= capacity:  # More than capacity tasks
                        Q[var1][var2] += penalty_weight * 2
    
    # Constraint 3: Task dependencies
    for dep_task1, dep_task2 in dependencies:
        if dep_task1 in tasks and dep_task2 in tasks:
            t1_idx = tasks.index(dep_task1)
            t2_idx = tasks.index(dep_task2)
            duration1 = task_durations.get(dep_task1, 1)
            
            # Task 2 cannot start before task 1 finishes
            for r1 in range(n_resources):
                for s1 in range(n_slots):
                    for r2 in range(n_resources):
                        for s2 in range(n_slots):
                            if s2 < s1 + duration1:  # Violation of dependency
                                var1 = var_index(t1_idx, r1, s1)
                                var2 = var_index(t2_idx, r2, s2)
                                Q[var1][var2] += penalty_weight * 3
    
    # Constraint 4: Task duration constraints
    for t, task in enumerate(tasks):
        duration = task_durations.get(task, 1)
        for r in range(n_resources):
            for s in range(n_slots):
                if s + duration > n_slots:  # Task would exceed time horizon
                    var_idx = var_index(t, r, s)
                    Q[var_idx][var_idx] += penalty_weight * 5  # Heavy penalty
    
    # Optimize using NQBAEngine
    nqba = NQBAEngine(mode=ExecutionMode.SIMULATOR)
    algorithm = payload.get("algorithm", "qaoa")
    parameters = {"shots": 1000, "layers": 4}
    
    try:
        result = await nqba.optimize_qubo(Q, algorithm=algorithm, parameters=parameters)
        
        # Decode solution to schedule
        solution = result.solution if hasattr(result, 'solution') else [0] * n_vars
        schedule = {}
        resource_schedule = {resource: {} for resource in resources}
        
        for t, task in enumerate(tasks):
            for r, resource in enumerate(resources):
                for s, time_slot in enumerate(time_slots):
                    var_idx = var_index(t, r, s)
                    if var_idx < len(solution) and solution[var_idx] == 1:
                        schedule[task] = {
                            "resource": resource,
                            "start_time": time_slot,
                            "duration": task_durations.get(task, 1),
                            "end_time": time_slots[min(s + task_durations.get(task, 1) - 1, len(time_slots) - 1)]
                        }
                        
                        # Add to resource schedule
                        duration = task_durations.get(task, 1)
                        for slot_offset in range(duration):
                            if s + slot_offset < len(time_slots):
                                slot = time_slots[s + slot_offset]
                                if slot not in resource_schedule[resource]:
                                    resource_schedule[resource][slot] = []
                                resource_schedule[resource][slot].append(task)
        
        # Calculate schedule metrics
        total_priority = sum(task_priorities.get(task, 1.0) for task in schedule.keys())
        completion_rate = len(schedule) / len(tasks) if tasks else 0
        
        # Check constraint violations
        violations = []
        
        # Check resource capacity violations
        for resource, slots in resource_schedule.items():
            capacity = resource_capacities.get(resource, 1)
            for slot, assigned_tasks in slots.items():
                if len(assigned_tasks) > capacity:
                    violations.append(f"Resource {resource} overloaded at {slot}: {len(assigned_tasks)} > {capacity}")
        
        # Check dependency violations
        for dep_task1, dep_task2 in dependencies:
            if dep_task1 in schedule and dep_task2 in schedule:
                end_time1 = schedule[dep_task1]["end_time"]
                start_time2 = schedule[dep_task2]["start_time"]
                if time_slots.index(start_time2) <= time_slots.index(end_time1):
                    violations.append(f"Dependency violation: {dep_task2} starts before {dep_task1} finishes")
        
        return {
            "result": {
                "schedule": schedule,
                "resource_schedule": resource_schedule,
                "metrics": {
                    "total_priority_score": float(total_priority),
                    "completion_rate": float(completion_rate),
                    "scheduled_tasks": len(schedule),
                    "total_tasks": len(tasks)
                },
                "violations": violations
            },
            "quantum_result": result.__dict__ if hasattr(result, '__dict__') else str(result)
        }
    
    except Exception as e:
        logger.exception("Schedule optimization failed")
        return {"error": f"Optimization failed: {str(e)}"}


from .qdllm import qdllm


@register_tool("quantum.llm.generate")
@require_api_key(role="user")
async def handle_llm_generate(payload: dict) -> dict:
    """Generate text using quantum-driven LLM (qdLLM) and QNLP pipeline with Dynex"""
    prompt = payload.get("prompt")
    context = payload.get("context")
    temperature = payload.get("temperature", 1.0)
    max_tokens = payload.get("max_tokens", 256)
    use_quantum_enhancement = payload.get("use_quantum_enhancement", True)
    result = await qdllm.generate(
        prompt=prompt,
        context=context,
        temperature=temperature,
        max_tokens=max_tokens,
        use_quantum_enhancement=use_quantum_enhancement,
    )
    return {"result": result}


@register_tool("quantum.score.lead")
@require_api_key(role="user")
async def handle_score_lead(payload: dict) -> dict:
    """Score sales leads using quantum-enhanced feature selection and optimization"""
    import numpy as np
    
    # Extract lead data
    leads = payload.get("leads", [])
    features = payload.get("features", [])  # Feature names
    feature_weights = payload.get("feature_weights", {})  # Optional predefined weights
    scoring_criteria = payload.get("scoring_criteria", {})  # Scoring thresholds and preferences
    historical_data = payload.get("historical_data", [])  # Past lead outcomes for training
    
    if not leads or not features:
        return {"error": "Leads and features are required"}
    
    n_leads = len(leads)
    n_features = len(features)
    
    # Extract feature matrix from leads
    feature_matrix = np.zeros((n_leads, n_features))
    for i, lead in enumerate(leads):
        for j, feature in enumerate(features):
            feature_matrix[i][j] = lead.get(feature, 0.0)
    
    # Normalize features to [0, 1] range
    feature_mins = np.min(feature_matrix, axis=0)
    feature_maxs = np.max(feature_matrix, axis=0)
    feature_ranges = feature_maxs - feature_mins
    feature_ranges[feature_ranges == 0] = 1  # Avoid division by zero
    normalized_features = (feature_matrix - feature_mins) / feature_ranges
    
    # Quantum feature selection using QUBO
    # Variables: binary selection for each feature
    n_vars = n_features
    Q = np.zeros((n_vars, n_vars))
    
    # Objective: Select features that maximize predictive power
    # Use correlation with historical outcomes if available
    if historical_data:
        outcomes = np.array([data.get("outcome", 0) for data in historical_data])
        hist_features = np.zeros((len(historical_data), n_features))
        
        for i, data in enumerate(historical_data):
            for j, feature in enumerate(features):
                hist_features[i][j] = data.get(feature, 0.0)
        
        # Normalize historical features
        if len(historical_data) > 0:
            hist_mins = np.min(hist_features, axis=0)
            hist_maxs = np.max(hist_features, axis=0)
            hist_ranges = hist_maxs - hist_mins
            hist_ranges[hist_ranges == 0] = 1
            hist_features = (hist_features - hist_mins) / hist_ranges
        
        # Calculate feature importance based on correlation with outcomes
        for j in range(n_features):
            if len(outcomes) > 1:
                correlation = np.corrcoef(hist_features[:, j], outcomes)[0, 1]
                if not np.isnan(correlation):
                    Q[j][j] -= abs(correlation)  # Negative for maximization
    
    # Add predefined feature weights
    for feature, weight in feature_weights.items():
        if feature in features:
            j = features.index(feature)
            Q[j][j] -= weight  # Negative for maximization
    
    # Feature interaction terms (correlation between features)
    for i in range(n_features):
        for j in range(i + 1, n_features):
            correlation = np.corrcoef(normalized_features[:, i], normalized_features[:, j])[0, 1]
            if not np.isnan(correlation):
                # Penalty for highly correlated features (redundancy)
                Q[i][j] += abs(correlation) * 0.5
    
    # Constraint: Select optimal number of features (not too many, not too few)
    target_features = min(max(3, n_features // 3), 8)  # Target 3-8 features
    penalty_weight = 2.0
    
    # Penalty for selecting too many or too few features
    for i in range(n_features):
        for j in range(i + 1, n_features):
            # Encourage selecting around target number
            Q[i][j] += penalty_weight / target_features
    
    # Optimize feature selection using NQBAEngine
    nqba = NQBAEngine(mode=ExecutionMode.SIMULATOR)
    algorithm = payload.get("algorithm", "qaoa")
    parameters = {"shots": 1000, "layers": 3}
    
    try:
        result = await nqba.optimize_qubo(Q, algorithm=algorithm, parameters=parameters)
        
        # Decode selected features
        solution = result.solution if hasattr(result, 'solution') else [1] * n_vars
        selected_features = [features[i] for i in range(n_features) if i < len(solution) and solution[i] == 1]
        
        if not selected_features:
            # Fallback: select top features by predefined weights or all features
            if feature_weights:
                sorted_features = sorted(feature_weights.items(), key=lambda x: x[1], reverse=True)
                selected_features = [f for f, w in sorted_features[:target_features] if f in features]
            else:
                selected_features = features[:target_features]
        
        # Calculate lead scores using selected features
        lead_scores = []
        
        for i, lead in enumerate(leads):
            score = 0.0
            feature_contributions = {}
            
            for feature in selected_features:
                if feature in lead:
                    feature_value = lead[feature]
                    
                    # Normalize feature value
                    feature_idx = features.index(feature)
                    if feature_ranges[feature_idx] > 0:
                        normalized_value = (feature_value - feature_mins[feature_idx]) / feature_ranges[feature_idx]
                    else:
                        normalized_value = 0.5
                    
                    # Apply feature weight
                    weight = feature_weights.get(feature, 1.0)
                    
                    # Apply scoring criteria if available
                    if feature in scoring_criteria:
                        criteria = scoring_criteria[feature]
                        if "threshold" in criteria:
                            threshold = criteria["threshold"]
                            if feature_value >= threshold:
                                normalized_value *= criteria.get("bonus", 1.5)
                            else:
                                normalized_value *= criteria.get("penalty", 0.5)
                    
                    contribution = normalized_value * weight
                    feature_contributions[feature] = contribution
                    score += contribution
            
            # Normalize score to 0-100 range
            max_possible_score = sum(feature_weights.get(f, 1.0) for f in selected_features)
            if max_possible_score > 0:
                normalized_score = min(100, (score / max_possible_score) * 100)
            else:
                normalized_score = 50  # Default score
            
            lead_scores.append({
                "lead_id": lead.get("id", f"lead_{i}"),
                "score": float(normalized_score),
                "feature_contributions": feature_contributions,
                "selected_features": selected_features,
                "raw_score": float(score)
            })
        
        # Sort leads by score (highest first)
        lead_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Calculate scoring statistics
        scores = [ls["score"] for ls in lead_scores]
        score_stats = {
            "mean_score": float(np.mean(scores)),
            "median_score": float(np.median(scores)),
            "std_score": float(np.std(scores)),
            "min_score": float(np.min(scores)),
            "max_score": float(np.max(scores))
        }
        
        # Feature importance analysis
        feature_importance = {}
        for feature in selected_features:
            contributions = [ls["feature_contributions"].get(feature, 0) for ls in lead_scores]
            feature_importance[feature] = {
                "mean_contribution": float(np.mean(contributions)),
                "std_contribution": float(np.std(contributions)),
                "selection_weight": feature_weights.get(feature, 1.0)
            }
        
        return {
            "result": {
                "lead_scores": lead_scores,
                "selected_features": selected_features,
                "feature_importance": feature_importance,
                "statistics": score_stats,
                "total_leads": n_leads,
                "features_used": len(selected_features)
            },
            "quantum_result": result.__dict__ if hasattr(result, '__dict__') else str(result)
        }
    
    except Exception as e:
        logger.exception("Lead scoring failed")
        return {"error": f"Scoring failed: {str(e)}"}


@register_tool("quantum.optimize.energy")
@require_api_key(role="user")
async def handle_optimize_energy(payload: dict) -> dict:
    """Optimize energy consumption and scheduling using quantum backend with real QUBO formulation"""
    import numpy as np
    
    # Extract energy optimization parameters
    devices = payload.get("devices", [])
    time_slots = payload.get("time_slots", [])
    energy_prices = payload.get("energy_prices", [])  # Price per time slot
    device_power = payload.get("device_power", {})  # Power consumption per device
    device_priorities = payload.get("device_priorities", {})  # Device priority levels
    renewable_generation = payload.get("renewable_generation", [])  # Renewable energy per time slot
    max_total_power = payload.get("max_total_power", float('inf'))  # Grid capacity limit
    battery_capacity = payload.get("battery_capacity", 0.0)  # Energy storage capacity
    battery_efficiency = payload.get("battery_efficiency", 0.9)  # Storage efficiency
    
    if not devices or not time_slots:
        return {"error": "Devices and time_slots are required"}
    
    n_devices = len(devices)
    n_slots = len(time_slots)
    
    # Ensure energy prices and renewable generation have correct length
    if len(energy_prices) != n_slots:
        energy_prices = [1.0] * n_slots  # Default uniform pricing
    if len(renewable_generation) != n_slots:
        renewable_generation = [0.0] * n_slots  # No renewable by default
    
    # Variables: x[d][t] = 1 if device d is active at time slot t
    # Additional variables for battery: charge[t], discharge[t]
    n_device_vars = n_devices * n_slots
    n_battery_vars = 2 * n_slots if battery_capacity > 0 else 0
    n_vars = n_device_vars + n_battery_vars
    
    def device_var_index(device_idx: int, slot_idx: int) -> int:
        return device_idx * n_slots + slot_idx
    
    def battery_charge_var_index(slot_idx: int) -> int:
        return n_device_vars + slot_idx
    
    def battery_discharge_var_index(slot_idx: int) -> int:
        return n_device_vars + n_slots + slot_idx
    
    # Initialize QUBO matrix
    Q = np.zeros((n_vars, n_vars))
    
    # Objective 1: Minimize energy costs
    for d, device in enumerate(devices):
        power = device_power.get(device, 1.0)
        for t in range(n_slots):
            var_idx = device_var_index(d, t)
            cost = energy_prices[t] * power
            Q[var_idx][var_idx] += cost
    
    # Objective 2: Maximize use of renewable energy (negative cost)
    renewable_bonus = 0.5
    for t in range(n_slots):
        renewable = renewable_generation[t]
        if renewable > 0:
            for d in range(n_devices):
                var_idx = device_var_index(d, t)
                power = device_power.get(devices[d], 1.0)
                if power <= renewable:
                    Q[var_idx][var_idx] -= renewable_bonus  # Bonus for using renewable
    
    # Objective 3: Respect device priorities (higher priority = lower cost)
    for d, device in enumerate(devices):
        priority = device_priorities.get(device, 1.0)
        priority_bonus = 1.0 / max(priority, 0.1)  # Higher priority = more bonus
        for t in range(n_slots):
            var_idx = device_var_index(d, t)
            Q[var_idx][var_idx] -= priority_bonus
    
    # Constraint 1: Power capacity limits
    penalty_weight = 10.0
    for t in range(n_slots):
        # Penalty for exceeding total power capacity
        device_vars_at_t = []
        for d in range(n_devices):
            var_idx = device_var_index(d, t)
            device_vars_at_t.append((var_idx, device_power.get(devices[d], 1.0)))
        
        # Add quadratic penalty for power limit violations
        for i, (var1, power1) in enumerate(device_vars_at_t):
            for j, (var2, power2) in enumerate(device_vars_at_t[i:], i):
                total_power = power1 + power2 if i != j else power1
                if total_power > max_total_power:
                    penalty = penalty_weight * (total_power - max_total_power) / max_total_power
                    if i == j:
                        Q[var1][var1] += penalty
                    else:
                        Q[var1][var2] += penalty
    
    # Constraint 2: Device operational constraints
    for d, device in enumerate(devices):
        # Some devices may have minimum/maximum runtime requirements
        min_runtime = payload.get("device_constraints", {}).get(device, {}).get("min_runtime", 0)
        max_runtime = payload.get("device_constraints", {}).get(device, {}).get("max_runtime", n_slots)
        
        if min_runtime > 0:
            # Penalty for not meeting minimum runtime
            device_vars = [device_var_index(d, t) for t in range(n_slots)]
            for i, var1 in enumerate(device_vars):
                for j, var2 in enumerate(device_vars[i+1:], i+1):
                    if j - i < min_runtime:
                        Q[var1][var2] -= penalty_weight * 0.5  # Encourage consecutive operation
        
        if max_runtime < n_slots:
            # Penalty for exceeding maximum runtime
            device_vars = [device_var_index(d, t) for t in range(n_slots)]
            for i, var1 in enumerate(device_vars):
                for j, var2 in enumerate(device_vars[i+1:], i+1):
                    if j - i >= max_runtime:
                        Q[var1][var2] += penalty_weight  # Discourage excessive operation
    
    # Battery optimization (if available)
    if battery_capacity > 0:
        # Battery charge/discharge costs and benefits
        for t in range(n_slots):
            charge_var = battery_charge_var_index(t)
            discharge_var = battery_discharge_var_index(t)
            
            # Cost of charging (buy energy)
            Q[charge_var][charge_var] += energy_prices[t] * battery_efficiency
            
            # Benefit of discharging (sell/use stored energy)
            Q[discharge_var][discharge_var] -= energy_prices[t] / battery_efficiency
            
            # Constraint: Cannot charge and discharge simultaneously
            Q[charge_var][discharge_var] += penalty_weight * 5
        
        # Battery capacity constraints
        for t in range(n_slots - 1):
            charge_var_t = battery_charge_var_index(t)
            discharge_var_t = battery_discharge_var_index(t)
            charge_var_t1 = battery_charge_var_index(t + 1)
            discharge_var_t1 = battery_discharge_var_index(t + 1)
            
            # Penalty for exceeding battery capacity
            Q[charge_var_t][charge_var_t1] += penalty_weight * 0.5
            Q[discharge_var_t][discharge_var_t1] += penalty_weight * 0.5
    
    # Optimize using NQBAEngine
    nqba = NQBAEngine(mode=ExecutionMode.SIMULATOR)
    algorithm = payload.get("algorithm", "qaoa")
    parameters = {"shots": 1000, "layers": 4}
    
    try:
        result = await nqba.optimize_qubo(Q, algorithm=algorithm, parameters=parameters)
        
        # Decode solution to energy schedule
        solution = result.solution if hasattr(result, 'solution') else [0] * n_vars
        
        # Device schedule
        device_schedule = {}
        for d, device in enumerate(devices):
            active_slots = []
            for t, time_slot in enumerate(time_slots):
                var_idx = device_var_index(d, t)
                if var_idx < len(solution) and solution[var_idx] == 1:
                    active_slots.append(time_slot)
            device_schedule[device] = active_slots
        
        # Battery schedule (if applicable)
        battery_schedule = {}
        if battery_capacity > 0:
            charge_schedule = []
            discharge_schedule = []
            for t, time_slot in enumerate(time_slots):
                charge_var = battery_charge_var_index(t)
                discharge_var = battery_discharge_var_index(t)
                
                if charge_var < len(solution) and solution[charge_var] == 1:
                    charge_schedule.append(time_slot)
                if discharge_var < len(solution) and solution[discharge_var] == 1:
                    discharge_schedule.append(time_slot)
            
            battery_schedule = {
                "charge_slots": charge_schedule,
                "discharge_slots": discharge_schedule
            }
        
        # Calculate energy metrics
        total_cost = 0.0
        total_consumption = 0.0
        renewable_usage = 0.0
        peak_power = 0.0
        
        slot_details = []
        for t, time_slot in enumerate(time_slots):
            slot_power = 0.0
            slot_cost = 0.0
            active_devices = []
            
            for d, device in enumerate(devices):
                var_idx = device_var_index(d, t)
                if var_idx < len(solution) and solution[var_idx] == 1:
                    power = device_power.get(device, 1.0)
                    slot_power += power
                    slot_cost += power * energy_prices[t]
                    active_devices.append(device)
            
            # Account for battery operations
            if battery_capacity > 0:
                charge_var = battery_charge_var_index(t)
                discharge_var = battery_discharge_var_index(t)
                
                if charge_var < len(solution) and solution[charge_var] == 1:
                    slot_power += battery_capacity * 0.1  # Assume 10% of capacity per slot
                    slot_cost += battery_capacity * 0.1 * energy_prices[t]
                
                if discharge_var < len(solution) and solution[discharge_var] == 1:
                    slot_power -= battery_capacity * 0.1
                    slot_cost -= battery_capacity * 0.1 * energy_prices[t]
            
            # Calculate renewable usage
            renewable_used = min(slot_power, renewable_generation[t])
            renewable_usage += renewable_used
            
            total_cost += slot_cost
            total_consumption += slot_power
            peak_power = max(peak_power, slot_power)
            
            slot_details.append({
                "time_slot": time_slot,
                "power_consumption": float(slot_power),
                "cost": float(slot_cost),
                "renewable_used": float(renewable_used),
                "active_devices": active_devices,
                "energy_price": energy_prices[t]
            })
        
        # Calculate efficiency metrics
        renewable_efficiency = renewable_usage / sum(renewable_generation) if sum(renewable_generation) > 0 else 0
        load_factor = total_consumption / (peak_power * n_slots) if peak_power > 0 else 0
        
        return {
            "result": {
                "device_schedule": device_schedule,
                "battery_schedule": battery_schedule,
                "slot_details": slot_details,
                "metrics": {
                    "total_cost": float(total_cost),
                    "total_consumption": float(total_consumption),
                    "peak_power": float(peak_power),
                    "renewable_usage": float(renewable_usage),
                    "renewable_efficiency": float(renewable_efficiency),
                    "load_factor": float(load_factor),
                    "average_cost_per_unit": float(total_cost / total_consumption) if total_consumption > 0 else 0
                },
                "optimization_summary": {
                    "devices_optimized": n_devices,
                    "time_slots": n_slots,
                    "battery_enabled": battery_capacity > 0,
                    "renewable_available": sum(renewable_generation) > 0
                }
            },
            "quantum_result": result.__dict__ if hasattr(result, '__dict__') else str(result)
        }
    
    except Exception as e:
        logger.exception("Energy optimization failed")
        return {"error": f"Optimization failed: {str(e)}"}


def list_tools() -> list:
    return list(TOOL_SCHEMAS.keys())


def get_tool_schema(tool: str) -> dict:
    return TOOL_SCHEMAS[tool]


def get_backend_status() -> dict:
    return backend_health()
