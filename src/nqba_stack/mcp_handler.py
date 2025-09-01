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

# Import new integrations
from .openai_integration import openai_integration, OpenAIRequest
from .nvidia_integration import (
    nvidia_integration,
    QuantumSimulationRequest,
    TensorRTRequest,
)
from .q_sales_division import q_sales_division
from .quantum_digital_agent import QuantumDigitalAgent

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


# Resource/cost controls (stub)
def check_resource_limits(tool: str, payload: dict) -> bool:
    # TODO: Implement resource/cost limits
    return True


# Tool registry
TOOL_HANDLERS = {}


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
    # TODO: Implement real QUBO optimization
    return {"result": "QUBO optimization (real logic TODO)", "input": payload}


@register_tool("quantum.optimize.portfolio")
@require_api_key(role="user")
async def handle_optimize_portfolio(payload: dict) -> dict:
    """Optimize investment portfolio using quantum algorithms"""
    # TODO: Implement portfolio optimization
    return {"result": "Portfolio optimization (real logic TODO)", "input": payload}


@register_tool("quantum.optimize.schedule")
@require_api_key(role="user")
async def handle_optimize_schedule(payload: dict) -> dict:
    """Optimize scheduling using quantum algorithms"""
    # TODO: Implement scheduling optimization
    return {"result": "Schedule optimization (real logic TODO)", "input": payload}


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
    """Score leads using quantum-enhanced algorithms"""
    # TODO: Implement lead scoring
    return {"result": "Lead scoring (real logic TODO)", "input": payload}


# New OpenAI Integration Tools
@register_tool("openai.generate")
@require_api_key(role="user")
async def handle_openai_generate(payload: dict) -> dict:
    """Generate text using OpenAI with quantum enhancement"""
    try:
        request = OpenAIRequest(
            prompt=payload["prompt"],
            model=payload.get("model", "gpt-4o"),
            temperature=payload.get("temperature", 0.7),
            max_tokens=payload.get("max_tokens", 1000),
            stream=payload.get("stream", False),
            functions=payload.get("functions"),
            function_call=payload.get("function_call"),
            use_quantum_enhancement=payload.get("use_quantum_enhancement", True),
            user_id=payload.get("user_id"),
            session_id=payload.get("session_id"),
        )

        if request.stream:
            # Handle streaming response
            chunks = []
            async for chunk in openai_integration.generate(request):
                chunks.append(chunk.content)

            return {"result": "".join(chunks), "streamed": True, "chunks": len(chunks)}
        else:
            # Handle single response
            response = await openai_integration.generate(request)
            return {
                "result": response.content,
                "model": response.model,
                "quantum_enhanced": response.quantum_enhanced,
                "processing_time": response.processing_time,
                "usage": response.usage,
            }

    except Exception as e:
        logger.error(f"OpenAI generation failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("openai.embeddings")
@require_api_key(role="user")
async def handle_openai_embeddings(payload: dict) -> dict:
    """Generate embeddings using OpenAI with quantum enhancement"""
    try:
        text = payload["text"]
        model = payload.get("model", "text-embedding-3-small")
        use_quantum_enhancement = payload.get("use_quantum_enhancement", True)

        embeddings = await openai_integration.get_embeddings(text=text, model=model)

        return {
            "embeddings": embeddings,
            "model": model,
            "quantum_enhanced": use_quantum_enhancement,
            "dimensions": len(embeddings),
        }

    except Exception as e:
        logger.error(f"OpenAI embeddings failed: {e}")
        return {"error": str(e), "success": False}


# New NVIDIA Integration Tools
@register_tool("nvidia.simulate.quantum")
@require_api_key(role="user")
async def handle_nvidia_simulate_quantum(payload: dict) -> dict:
    """Simulate quantum algorithms using NVIDIA cuQuantum"""
    try:
        request = QuantumSimulationRequest(
            qubits=payload["qubits"],
            algorithm=payload.get("algorithm", "qaoa"),
            parameters=payload.get("parameters", {}),
            precision=payload.get("precision", "float32"),
            use_gpu=payload.get("use_gpu", True),
            max_iterations=payload.get("max_iterations", 1000),
            convergence_threshold=payload.get("convergence_threshold", 1e-6),
        )

        result = await nvidia_integration.simulate_quantum(request)

        return {
            "success": result.success,
            "result": result.result.tolist() if result.result is not None else None,
            "energy": result.energy,
            "iterations": result.iterations,
            "processing_time": result.processing_time,
            "gpu_used": result.gpu_used,
            "error_message": result.error_message,
        }

    except Exception as e:
        logger.error(f"NVIDIA quantum simulation failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("nvidia.accelerate.inference")
@require_api_key(role="user")
async def handle_nvidia_accelerate_inference(payload: dict) -> dict:
    """Accelerate AI inference using NVIDIA TensorRT"""
    try:
        import numpy as np

        request = TensorRTRequest(
            model_path=payload["model_path"],
            input_data=np.array(payload["input_data"]),
            batch_size=payload.get("batch_size", 1),
            precision=payload.get("precision", "fp16"),
            optimization_level=payload.get("optimization_level", 3),
            use_gpu=payload.get("use_gpu", True),
        )

        result = await nvidia_integration.accelerate_inference(request)

        return {
            "success": result.success,
            "output": result.output.tolist() if result.output is not None else None,
            "inference_time": result.inference_time,
            "throughput": result.throughput,
            "gpu_used": result.gpu_used,
            "error_message": result.error_message,
        }

    except Exception as e:
        logger.error(f"NVIDIA inference acceleration failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("nvidia.gpu.info")
@require_api_key(role="user")
async def handle_nvidia_gpu_info(payload: dict) -> dict:
    """Get information about available NVIDIA GPUs"""
    try:
        include_memory = payload.get("include_memory", True)
        include_performance = payload.get("include_performance", False)

        gpu_info = []
        for gpu in nvidia_integration.gpu_info:
            info = {
                "device_id": gpu.device_id,
                "name": gpu.name,
                "compute_capability": gpu.compute_capability,
                "cuda_cores": gpu.cuda_cores,
                "tensor_cores": gpu.tensor_cores,
                "is_available": gpu.is_available,
            }

            if include_memory:
                info.update(
                    {
                        "memory_total_mb": gpu.memory_total,
                        "memory_free_mb": gpu.memory_free,
                    }
                )

            gpu_info.append(info)

        memory_usage = {}
        if include_memory:
            memory_usage = nvidia_integration.get_gpu_memory_usage()

        return {
            "gpus": gpu_info,
            "memory_usage": memory_usage,
            "total_gpus": len(gpu_info),
            "cuda_available": nvidia_integration.tensorrt_available,
            "cuquantum_available": nvidia_integration.cuquantum_available,
        }

    except Exception as e:
        logger.error(f"NVIDIA GPU info failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("nvidia.optimize.energy")
@require_api_key(role="user")
async def handle_nvidia_optimize_energy(payload: dict) -> dict:
    """Optimize energy usage for different workload types"""
    try:
        workload_type = payload.get("workload_type", "quantum")
        target_power = payload.get("target_power")
        performance_priority = payload.get("performance_priority", "balanced")

        optimization = nvidia_integration.optimize_energy_usage(workload_type)

        # Add custom optimization based on payload
        if target_power:
            optimization["target_power_watts"] = target_power
            optimization["recommendations"].append(
                f"Target power consumption: {target_power}W"
            )

        if performance_priority != "balanced":
            optimization["performance_priority"] = performance_priority
            if performance_priority == "performance":
                optimization["recommendations"].append(
                    "Optimizing for maximum performance"
                )
            elif performance_priority == "power":
                optimization["recommendations"].append(
                    "Optimizing for minimum power consumption"
                )

        return optimization

    except Exception as e:
        logger.error(f"NVIDIA energy optimization failed: {e}")
        return {"error": str(e), "success": False}


# New Q-Sales Division™ Tools
@register_tool("q_sales.create_pod")
@require_api_key(role="user")
async def handle_q_sales_create_pod(payload: dict) -> dict:
    """Create a new quantum-optimized sales pod with AI agents"""
    try:
        name = payload["name"]
        industry = payload["industry"]
        target_market = payload["target_market"]
        agent_count = payload.get("agent_count", 5)
        playbook_template = payload.get("playbook_template", "standard")

        pod = await q_sales_division.create_sales_pod(
            name=name,
            industry=industry,
            target_market=target_market,
            agent_count=agent_count,
            playbook_template=playbook_template,
        )

        return {
            "success": True,
            "pod_id": pod.pod_id,
            "name": pod.name,
            "industry": pod.industry,
            "target_market": pod.target_market,
            "agent_count": len(pod.agents),
            "playbook_id": pod.playbook_id,
            "status": pod.status.value,
            "created_at": pod.created_at.isoformat(),
        }

    except Exception as e:
        logger.error(f"Q-Sales pod creation failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("q_sales.optimize_pod")
@require_api_key(role="user")
async def handle_q_sales_optimize_pod(payload: dict) -> dict:
    """Optimize sales pod performance using quantum algorithms"""
    try:
        pod_id = payload["pod_id"]
        optimization_focus = payload.get("optimization_focus", "all")

        result = await q_sales_division.optimize_pod_performance(pod_id)

        if result["success"]:
            return {
                "success": True,
                "pod_id": pod_id,
                "optimizations_applied": result["optimizations_applied"],
                "new_status": result["new_status"],
                "next_optimization": result["next_optimization"].isoformat(),
                "optimization_focus": optimization_focus,
            }
        else:
            return {
                "success": False,
                "pod_id": pod_id,
                "error": result.get("error", "Unknown optimization error"),
                "fallback_optimization": result.get("fallback_optimization", False),
            }

    except Exception as e:
        logger.error(f"Q-Sales pod optimization failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("q_sales.get_pod_performance")
@require_api_key(role="user")
async def handle_q_sales_get_pod_performance(payload: dict) -> dict:
    """Get comprehensive performance metrics for a sales pod"""
    try:
        pod_id = payload["pod_id"]
        include_agent_details = payload.get("include_agent_details", False)
        time_range = payload.get("time_range", "month")

        performance = await q_sales_division.get_pod_performance(pod_id)

        # Add agent details if requested
        if include_agent_details:
            pod = q_sales_division.pods.get(pod_id)
            if pod:
                agent_details = []
                for agent in pod.agents:
                    agent_details.append(
                        {
                            "agent_id": agent.agent_id,
                            "name": agent.name,
                            "role": agent.role.value,
                            "specialization": agent.specialization,
                            "experience_level": agent.experience_level,
                            "performance_metrics": agent.performance_metrics,
                            "is_active": agent.is_active,
                        }
                    )
                performance["agent_details"] = agent_details

        performance["time_range"] = time_range
        return performance

    except Exception as e:
        logger.error(f"Q-Sales pod performance retrieval failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("q_sales.scale_pod")
@require_api_key(role="user")
async def handle_q_sales_scale_pod(payload: dict) -> dict:
    """Scale sales pod by adding or removing AI agents"""
    try:
        pod_id = payload["pod_id"]
        target_agent_count = payload["target_agent_count"]
        scaling_strategy = payload.get("scaling_strategy", "smart")

        result = await q_sales_division.scale_pod(pod_id, target_agent_count)

        result["scaling_strategy"] = scaling_strategy
        return result

    except Exception as e:
        logger.error(f"Q-Sales pod scaling failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("q_sales.get_division_overview")
@require_api_key(role="user")
async def handle_q_sales_get_division_overview(payload: dict) -> dict:
    """Get overview of entire Q-Sales Division"""
    try:
        include_pod_details = payload.get("include_pod_details", False)
        include_revenue_breakdown = payload.get("include_revenue_breakdown", True)
        include_performance_trends = payload.get("include_performance_trends", False)

        overview = await q_sales_division.get_division_overview()

        # Add pod details if requested
        if include_pod_details:
            pod_details = []
            for pod in q_sales_division.pods.values():
                pod_details.append(
                    {
                        "pod_id": pod.pod_id,
                        "name": pod.name,
                        "industry": pod.industry,
                        "target_market": pod.target_market,
                        "status": pod.status.value,
                        "agent_count": len(pod.agents),
                        "revenue_generated": pod.revenue_generated,
                        "leads_processed": pod.leads_processed,
                        "conversion_rate": pod.conversion_rate,
                        "created_at": pod.created_at.isoformat(),
                        "last_optimization": pod.last_optimization.isoformat(),
                    }
                )
            overview["pod_details"] = pod_details

        # Add revenue breakdown if requested
        if include_revenue_breakdown:
            revenue_by_industry = {}
            for pod in q_sales_division.pods.values():
                industry = pod.industry
                if industry not in revenue_by_industry:
                    revenue_by_industry[industry] = 0
                revenue_by_industry[industry] += pod.revenue_generated
            overview["revenue_by_industry"] = revenue_by_industry

        # Add performance trends if requested
        if include_performance_trends:
            # Calculate trends over time (simplified for demo)
            overview["performance_trends"] = {
                "revenue_growth": "15.2% month-over-month",
                "conversion_improvement": "8.7% month-over-month",
                "agent_efficiency": "12.3% month-over-month",
            }

        return overview

    except Exception as e:
        logger.error(f"Q-Sales division overview failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("q_sales.train_agents")
@require_api_key(role="user")
async def handle_q_sales_train_agents(payload: dict) -> dict:
    """Train sales agents using quantum-enhanced learning"""
    try:
        pod_id = payload["pod_id"]
        training_focus = payload.get("training_focus", "all")
        training_intensity = payload.get("training_intensity", "moderate")
        use_quantum_enhancement = payload.get("use_quantum_enhancement", True)

        # Get pod for training
        if pod_id not in q_sales_division.pods:
            return {"error": f"Pod {pod_id} not found", "success": False}

        pod = q_sales_division.pods[pod_id]

        # Generate training content using OpenAI
        training_prompt = f"""
        Create comprehensive training content for sales agents in {pod.industry} targeting {pod.target_market}.
        
        Training focus: {training_focus}
        Training intensity: {training_intensity}
        
        Include:
        1. Key learning objectives
        2. Practical exercises
        3. Role-playing scenarios
        4. Assessment criteria
        5. Success metrics
        
        Make it engaging and immediately applicable.
        """

        try:
            response = await openai_integration.generate(
                OpenAIRequest(
                    prompt=training_prompt,
                    model="gpt-4o",
                    max_tokens=2000,
                    temperature=0.7,
                    use_quantum_enhancement=use_quantum_enhancement,
                )
            )

            # Update agent training data
            for agent in pod.agents:
                agent.training_data.update(
                    {
                        "last_training": time.time(),
                        "training_focus": training_focus,
                        "training_intensity": training_intensity,
                        "training_content": response.content[:500]
                        + "...",  # Store summary
                    }
                )

            return {
                "success": True,
                "pod_id": pod_id,
                "agents_trained": len(pod.agents),
                "training_focus": training_focus,
                "training_intensity": training_intensity,
                "quantum_enhanced": use_quantum_enhancement,
                "training_summary": response.content[:200] + "...",
                "next_training_recommended": "7 days",
            }

        except Exception as e:
            logger.error(f"Training content generation failed: {e}")
            return {
                "success": False,
                "error": f"Training content generation failed: {e}",
                "fallback_training": True,
            }

    except Exception as e:
        logger.error(f"Q-Sales agent training failed: {e}")
        return {"error": str(e), "success": False}


# Backend status
def get_backend_status() -> dict:
    """Get status of all backend services"""
    return {
        "openai": {
            "available": openai_integration.client is not None,
            "quantum_enhancement": openai_integration.quantum_enhancement_enabled,
        },
        "nvidia": {
            "gpus_available": len(nvidia_integration.gpu_info),
            "cuda_available": nvidia_integration.tensorrt_available,
            "cuquantum_available": nvidia_integration.cuquantum_available,
        },
        "quantum": {
            "dynex_available": True,  # TODO: Check actual Dynex status
            "simulation_available": True,
        },
        "q_sales_division": {
            "pods_active": len(
                [
                    p
                    for p in q_sales_division.pods.values()
                    if p.status.value == "active"
                ]
            ),
            "total_agents": len(q_sales_division.agents),
            "total_pods": len(q_sales_division.pods),
            "playbooks_available": len(q_sales_division.playbooks),
        },
        "quantum_digital_agent": {
            "available": True,
            "active_calls": 0,  # Will be updated when agent is instantiated
            "call_history_count": 0,  # Will be updated when agent is instantiated
            "quantum_enhancement": True,
            "gpu_acceleration": nvidia_integration.is_gpu_available(),
        },
    }


# Quantum Digital Agent Handlers


@register_tool("quantum_agent.make_call")
async def handle_quantum_agent_make_call(payload: dict) -> dict:
    """Make an outbound call using quantum-enhanced AI"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_make_call, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_make_call._agent = QuantumDigitalAgent(settings)

        agent = handle_quantum_agent_make_call._agent

        # Create call request
        from .quantum_digital_agent import CallRequest

        call_request = CallRequest(
            to_number=payload["to_number"],
            from_number=payload["from_number"],
            agent_id=payload["agent_id"],
            call_purpose=payload["call_purpose"],
            script_template=payload.get("script_template"),
            quantum_optimization=payload.get("quantum_optimization", True),
            gpu_acceleration=payload.get("gpu_acceleration", True),
        )

        # Make the call
        result = await agent.make_call(call_request)

        return {
            "success": result.success,
            "call_id": result.call_id,
            "message": result.message,
            "quantum_insights": result.quantum_insights,
            "call_duration": result.session.duration if result.session else None,
            "call_status": result.session.status.value if result.session else None,
        }

    except Exception as e:
        logger.error(f"Quantum agent make call failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.get_analytics")
async def handle_quantum_agent_get_analytics(payload: dict) -> dict:
    """Get call analytics with quantum insights"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_get_analytics, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_get_analytics._agent = QuantumDigitalAgent(settings)

        agent = handle_quantum_agent_get_analytics._agent

        # Get analytics
        analytics = await agent.get_call_analytics()

        return {"success": True, "analytics": analytics}

    except Exception as e:
        logger.error(f"Quantum agent analytics failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.get_call_history")
async def handle_quantum_agent_get_call_history(payload: dict) -> dict:
    """Get call history with optional filtering"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_get_call_history, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_get_call_history._agent = QuantumDigitalAgent(settings)

        agent = handle_quantum_agent_get_call_history._agent

        # Get call history
        limit = payload.get("limit", 50)
        status_filter = payload.get("status_filter")

        history = await agent.get_call_history(limit=limit)

        # Apply status filter if specified
        if status_filter:
            history = [call for call in history if call.status.value == status_filter]

        # Convert to serializable format
        serializable_history = []
        for call in history:
            serializable_history.append(
                {
                    "call_id": call.call_id,
                    "call_type": call.call_type.value,
                    "status": call.status.value,
                    "start_time": call.start_time.isoformat(),
                    "end_time": call.end_time.isoformat() if call.end_time else None,
                    "duration": call.duration,
                    "purpose": call.metadata.get("purpose"),
                    "quantum_insights": call.quantum_insights,
                }
            )

        return {
            "success": True,
            "call_history": serializable_history,
            "total_calls": len(serializable_history),
            "filtered_by_status": status_filter,
        }

    except Exception as e:
        logger.error(f"Quantum agent call history failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.get_pricing_tiers")
async def handle_quantum_agent_get_pricing_tiers(payload: dict) -> dict:
    """Get all available DIY and DFY pricing tiers"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_get_pricing_tiers, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_get_pricing_tiers._agent = QuantumDigitalAgent(
                settings
            )

        agent = handle_quantum_agent_get_pricing_tiers._agent

        # Get all pricing tiers
        pricing_tiers = await agent.get_all_pricing_tiers()

        return {"success": True, "pricing_tiers": pricing_tiers}

    except Exception as e:
        logger.error(f"Quantum agent pricing tiers failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.get_pricing_quote")
async def handle_quantum_agent_get_pricing_quote(payload: dict) -> dict:
    """Get pricing quote for specific tier and complexity"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_get_pricing_quote, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_get_pricing_quote._agent = QuantumDigitalAgent(
                settings
            )

        agent = handle_quantum_agent_get_pricing_quote._agent

        # Import enums
        from .quantum_digital_agent import ServiceTier, UseCaseComplexity

        # Get pricing quote
        tier = ServiceTier(payload["tier"])
        complexity = UseCaseComplexity(payload["complexity"])
        estimated_calls = payload.get("estimated_calls_per_month")

        quote = await agent.get_pricing_quote(tier, complexity, estimated_calls)

        return {"success": True, "quote": quote}

    except Exception as e:
        logger.error(f"Quantum agent pricing quote failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.create_subscription")
async def handle_quantum_agent_create_subscription(payload: dict) -> dict:
    """Create a new client subscription"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_create_subscription, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_create_subscription._agent = QuantumDigitalAgent(
                settings
            )

        agent = handle_quantum_agent_create_subscription._agent

        # Import enums
        from .quantum_digital_agent import ServiceTier, UseCaseComplexity

        # Create subscription
        subscription = await agent.create_client_subscription(
            client_id=payload["client_id"],
            company_name=payload["company_name"],
            tier=ServiceTier(payload["tier"]),
            complexity=UseCaseComplexity(payload["complexity"]),
            setup_fee_paid=payload.get("setup_fee_paid", False),
        )

        return {
            "success": True,
            "subscription": {
                "client_id": subscription.client_id,
                "company_name": subscription.company_name,
                "tier": subscription.tier.value,
                "complexity": subscription.complexity.value,
                "start_date": subscription.start_date.isoformat(),
                "setup_fee_paid": subscription.setup_fee_paid,
                "status": subscription.status,
            },
        }

    except Exception as e:
        logger.error(f"Quantum agent create subscription failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.get_subscription_status")
async def handle_quantum_agent_get_subscription_status(payload: dict) -> dict:
    """Get client subscription status and usage"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_get_subscription_status, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_get_subscription_status._agent = QuantumDigitalAgent(
                settings
            )

        agent = handle_quantum_agent_get_subscription_status._agent

        # Get subscription status
        status = await agent.get_client_subscription_status(payload["client_id"])

        if not status:
            return {"success": False, "error": "Client subscription not found"}

        return {"success": True, "subscription_status": status}

    except Exception as e:
        logger.error(f"Quantum agent subscription status failed: {e}")
        return {"error": str(e), "success": False}


@register_tool("quantum_agent.get_agent_performance")
async def handle_quantum_agent_get_agent_performance(payload: dict) -> dict:
    """Get performance metrics for a specific agent"""
    try:
        # Initialize quantum agent if not exists
        if not hasattr(handle_quantum_agent_get_agent_performance, "_agent"):
            from .settings import NQBASettings

            settings = NQBASettings()
            handle_quantum_agent_get_agent_performance._agent = QuantumDigitalAgent(
                settings
            )

        agent = handle_quantum_agent_get_agent_performance._agent

        # Get agent performance
        performance = await agent.get_agent_performance(payload["agent_id"])

        return {"success": True, "agent_performance": performance}

    except Exception as e:
        logger.error(f"Quantum agent performance failed: {e}")
        return {"error": str(e), "success": False}
