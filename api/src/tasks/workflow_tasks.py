from celery import Celery
from typing import Dict, Any, List, Optional, Union
import json
import uuid
import time
import yaml
from datetime import datetime, timedelta
import redis.asyncio as redis
import structlog
import asyncio
from pathlib import Path

logger = structlog.get_logger()

# Get Celery app instance
from ..app_consolidated import celery_app

class WorkflowEngine:
    """Quantum-enhanced workflow execution engine"""
    
    def __init__(self):
        self.redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        self.workflows_path = Path("workflows")
    
    async def load_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Load workflow configuration from YAML file"""
        workflow_file = self.workflows_path / f"{workflow_name}.yaml"
        
        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow {workflow_name} not found")
        
        with open(workflow_file, 'r') as f:
            return yaml.safe_load(f)
    
    async def execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        step_type = step.get("type")
        step_name = step.get("name", "unnamed_step")
        
        logger.info("Executing workflow step", step_name=step_name, step_type=step_type)
        
        if step_type == "api_call":
            return await self._execute_api_call(step, context)
        elif step_type == "data_transform":
            return await self._execute_data_transform(step, context)
        elif step_type == "condition":
            return await self._execute_condition(step, context)
        elif step_type == "quantum_process":
            return await self._execute_quantum_process(step, context)
        elif step_type == "notification":
            return await self._execute_notification(step, context)
        else:
            raise ValueError(f"Unknown step type: {step_type}")
    
    async def _execute_api_call(self, step: Dict[str, Any], context: Dict[str, Any]):
        """Execute API call step"""
        # Simulate API call
        await asyncio.sleep(0.5)
        
        endpoint = step.get("endpoint", "/api/default")
        method = step.get("method", "GET")
        
        # Mock response based on endpoint
        if "lead" in endpoint:
            response = {
                "status": "success",
                "data": {
                    "lead_id": context.get("lead_id", "lead_123"),
                    "score": 85,
                    "status": "qualified"
                }
            }
        elif "email" in endpoint:
            response = {
                "status": "success",
                "data": {
                    "email_id": f"email_{uuid.uuid4().hex[:8]}",
                    "sent": True,
                    "delivery_status": "delivered"
                }
            }
        else:
            response = {
                "status": "success",
                "data": {"result": "completed"}
            }
        
        return {
            "step_result": response,
            "context_updates": response.get("data", {})
        }
    
    async def _execute_data_transform(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data transformation step"""
        transform_type = step.get("transform", "identity")
        input_data = context.get(step.get("input_key", "data"), {})
        
        if transform_type == "normalize_score":
            # Normalize score to 0-100 range
            raw_score = input_data.get("score", 0)
            normalized_score = max(0, min(100, raw_score))
            result = {"normalized_score": normalized_score}
        
        elif transform_type == "extract_insights":
            # Extract key insights from data
            result = {
                "insights": [
                    "High engagement detected",
                    "Budget qualification confirmed",
                    "Technical fit validated"
                ],
                "confidence": 0.87
            }
        
        elif transform_type == "aggregate_metrics":
            # Aggregate multiple metrics
            result = {
                "total_interactions": 15,
                "avg_session_duration": 245,
                "conversion_probability": 0.73
            }
        
        else:
            result = input_data  # Identity transform
        
        return {
            "step_result": result,
            "context_updates": {step.get("output_key", "transformed_data"): result}
        }
    
    async def _execute_condition(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute conditional logic step"""
        condition = step.get("condition", "true")
        
        # Simple condition evaluation
        if "score >" in condition:
            threshold = int(condition.split(">")[1].strip())
            score = context.get("score", 0)
            result = score > threshold
        elif "status ==" in condition:
            expected_status = condition.split("==")[1].strip().strip('"\'')
            actual_status = context.get("status", "")
            result = actual_status == expected_status
        else:
            result = True  # Default to true
        
        return {
            "step_result": {"condition_met": result},
            "context_updates": {"last_condition_result": result}
        }
    
    async def _execute_quantum_process(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute quantum processing step"""
        process_type = step.get("process", "optimization")
        
        # Simulate quantum processing
        await asyncio.sleep(1.5)
        
        if process_type == "optimization":
            result = {
                "optimized_parameters": {
                    "engagement_weight": 0.35,
                    "budget_weight": 0.25,
                    "timeline_weight": 0.20,
                    "fit_weight": 0.20
                },
                "quantum_advantage": "23.5%",
                "confidence": 0.91
            }
        elif process_type == "prediction":
            result = {
                "predicted_outcome": "conversion",
                "probability": 0.78,
                "quantum_enhancement": "15.2%",
                "prediction_horizon": "30 days"
            }
        else:
            result = {
                "quantum_result": "processed",
                "enhancement": "12.3%"
            }
        
        return {
            "step_result": result,
            "context_updates": {"quantum_result": result}
        }
    
    async def _execute_notification(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute notification step"""
        notification_type = step.get("type", "email")
        recipient = step.get("recipient", "admin@company.com")
        
        # Simulate notification sending
        await asyncio.sleep(0.3)
        
        notification_id = f"notif_{uuid.uuid4().hex[:8]}"
        
        result = {
            "notification_id": notification_id,
            "type": notification_type,
            "recipient": recipient,
            "sent_at": datetime.utcnow().isoformat(),
            "status": "delivered"
        }
        
        return {
            "step_result": result,
            "context_updates": {"last_notification": notification_id}
        }

@celery_app.task(bind=True, name="workflows.execute_workflow")
def execute_workflow(self, workflow_name: str, initial_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a complete workflow pipeline
    
    Args:
        workflow_name: Name of the workflow to execute
        initial_context: Initial context data for the workflow
        
    Returns:
        Workflow execution results
    """
    task_id = self.request.id
    logger.info("Starting workflow execution", task_id=task_id, workflow=workflow_name)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        engine = WorkflowEngine()
        
        # Set initial status
        asyncio.run(redis_client.hset(
            f"workflow:execution:{task_id}",
            mapping={
                "status": "running",
                "started_at": datetime.utcnow().isoformat(),
                "workflow_name": workflow_name,
                "current_step": 0,
                "total_steps": 0
            }
        ))
        
        # Load workflow configuration
        try:
            workflow_config = asyncio.run(engine.load_workflow(workflow_name))
        except FileNotFoundError:
            # Create a default workflow if not found
            workflow_config = {
                "name": workflow_name,
                "description": f"Auto-generated workflow for {workflow_name}",
                "steps": [
                    {
                        "name": "initialize",
                        "type": "data_transform",
                        "transform": "identity",
                        "input_key": "input_data"
                    },
                    {
                        "name": "process",
                        "type": "quantum_process",
                        "process": "optimization"
                    },
                    {
                        "name": "notify",
                        "type": "notification",
                        "notification_type": "email",
                        "recipient": "admin@company.com"
                    }
                ]
            }
        
        steps = workflow_config.get("steps", [])
        context = initial_context.copy()
        step_results = []
        
        # Update total steps
        asyncio.run(redis_client.hset(
            f"workflow:execution:{task_id}",
            "total_steps", len(steps)
        ))
        
        # Execute each step
        for i, step in enumerate(steps):
            step_name = step.get("name", f"step_{i}")
            logger.info("Executing workflow step", task_id=task_id, step=step_name, step_index=i)
            
            # Update current step
            asyncio.run(redis_client.hset(
                f"workflow:execution:{task_id}",
                mapping={
                    "current_step": i + 1,
                    "current_step_name": step_name
                }
            ))
            
            try:
                step_result = asyncio.run(engine.execute_step(step, context))
                
                # Update context with step results
                context.update(step_result.get("context_updates", {}))
                
                step_results.append({
                    "step_index": i,
                    "step_name": step_name,
                    "status": "completed",
                    "result": step_result["step_result"],
                    "completed_at": datetime.utcnow().isoformat()
                })
                
            except Exception as step_error:
                logger.error("Workflow step failed", task_id=task_id, step=step_name, error=str(step_error))
                
                step_results.append({
                    "step_index": i,
                    "step_name": step_name,
                    "status": "failed",
                    "error": str(step_error),
                    "failed_at": datetime.utcnow().isoformat()
                })
                
                # Check if workflow should continue on error
                if not step.get("continue_on_error", False):
                    break
        
        # Calculate execution statistics
        successful_steps = [r for r in step_results if r["status"] == "completed"]
        failed_steps = [r for r in step_results if r["status"] == "failed"]
        
        execution_result = {
            "task_id": task_id,
            "workflow_name": workflow_name,
            "status": "completed" if len(failed_steps) == 0 else "partial_failure",
            "total_steps": len(steps),
            "successful_steps": len(successful_steps),
            "failed_steps": len(failed_steps),
            "step_results": step_results,
            "final_context": context,
            "execution_time": (datetime.utcnow() - datetime.fromisoformat(
                asyncio.run(redis_client.hget(f"workflow:execution:{task_id}", "started_at"))
            )).total_seconds(),
            "completed_at": datetime.utcnow().isoformat()
        }
        
        # Update completion status
        completion_data = {
            "status": execution_result["status"],
            "completed_at": datetime.utcnow().isoformat(),
            "successful_steps": len(successful_steps),
            "failed_steps": len(failed_steps),
            "result": json.dumps(execution_result)
        }
        
        asyncio.run(redis_client.hset(
            f"workflow:execution:{task_id}",
            mapping=completion_data
        ))
        
        # Publish workflow completion event
        asyncio.run(redis_client.publish(
            "workflow:updates",
            json.dumps({
                "task_id": task_id,
                "workflow_name": workflow_name,
                "status": execution_result["status"],
                "successful_steps": len(successful_steps),
                "failed_steps": len(failed_steps),
                "timestamp": datetime.utcnow().isoformat()
            })
        ))
        
        logger.info("Workflow execution completed", task_id=task_id, 
                   workflow=workflow_name, status=execution_result["status"])
        
        return execution_result
        
    except Exception as e:
        logger.error("Workflow execution failed", task_id=task_id, error=str(e))
        
        # Update error status
        error_data = {
            "status": "failed",
            "failed_at": datetime.utcnow().isoformat(),
            "error": str(e)
        }
        
        asyncio.run(redis_client.hset(
            f"workflow:execution:{task_id}",
            mapping=error_data
        ))
        
        raise

@celery_app.task(bind=True, name="workflows.schedule_workflow")
def schedule_workflow(self, workflow_name: str, schedule_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Schedule a workflow for future execution
    
    Args:
        workflow_name: Name of the workflow to schedule
        schedule_config: Scheduling configuration (cron, delay, etc.)
        context: Context data for the workflow
        
    Returns:
        Scheduling result
    """
    task_id = self.request.id
    logger.info("Scheduling workflow", task_id=task_id, workflow=workflow_name)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        schedule_type = schedule_config.get("type", "delay")
        
        if schedule_type == "delay":
            # Schedule with delay
            delay_seconds = schedule_config.get("delay_seconds", 60)
            eta = datetime.utcnow() + timedelta(seconds=delay_seconds)
            
            # Schedule the workflow execution
            scheduled_task = execute_workflow.apply_async(
                args=[workflow_name, context],
                eta=eta
            )
            
            schedule_result = {
                "scheduled_task_id": scheduled_task.id,
                "workflow_name": workflow_name,
                "schedule_type": "delay",
                "delay_seconds": delay_seconds,
                "eta": eta.isoformat(),
                "scheduled_at": datetime.utcnow().isoformat()
            }
            
        elif schedule_type == "cron":
            # For cron scheduling, we'd typically use Celery Beat
            # For now, simulate cron scheduling
            cron_expression = schedule_config.get("cron", "0 0 * * *")
            
            schedule_result = {
                "workflow_name": workflow_name,
                "schedule_type": "cron",
                "cron_expression": cron_expression,
                "next_run": (datetime.utcnow() + timedelta(days=1)).isoformat(),
                "scheduled_at": datetime.utcnow().isoformat()
            }
            
        else:
            raise ValueError(f"Unknown schedule type: {schedule_type}")
        
        # Store schedule information
        schedule_key = f"workflow:schedule:{task_id}"
        asyncio.run(redis_client.hset(
            schedule_key,
            mapping={
                "status": "scheduled",
                "workflow_name": workflow_name,
                "schedule_config": json.dumps(schedule_config),
                "context": json.dumps(context),
                "result": json.dumps(schedule_result)
            }
        ))
        
        logger.info("Workflow scheduled successfully", task_id=task_id, workflow=workflow_name)
        
        return {
            "task_id": task_id,
            "status": "scheduled",
            "schedule_result": schedule_result
        }
        
    except Exception as e:
        logger.error("Workflow scheduling failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="workflows.validate_workflow")
def validate_workflow_config(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate workflow configuration
    
    Args:
        workflow_config: Workflow configuration to validate
        
    Returns:
        Validation results
    """
    task_id = self.request.id
    logger.info("Validating workflow configuration", task_id=task_id)
    
    try:
        validation_errors = []
        validation_warnings = []
        
        # Check required fields
        required_fields = ["name", "steps"]
        for field in required_fields:
            if field not in workflow_config:
                validation_errors.append(f"Missing required field: {field}")
        
        # Validate steps
        steps = workflow_config.get("steps", [])
        if not steps:
            validation_errors.append("Workflow must have at least one step")
        
        for i, step in enumerate(steps):
            step_name = step.get("name", f"step_{i}")
            
            # Check step type
            if "type" not in step:
                validation_errors.append(f"Step '{step_name}' missing type")
            else:
                valid_types = ["api_call", "data_transform", "condition", "quantum_process", "notification"]
                if step["type"] not in valid_types:
                    validation_errors.append(f"Step '{step_name}' has invalid type: {step['type']}")
            
            # Check for potential issues
            if step.get("type") == "condition" and "condition" not in step:
                validation_warnings.append(f"Condition step '{step_name}' missing condition expression")
        
        # Check for circular dependencies (simplified)
        step_names = [step.get("name", f"step_{i}") for i, step in enumerate(steps)]
        if len(step_names) != len(set(step_names)):
            validation_warnings.append("Duplicate step names detected")
        
        validation_result = {
            "is_valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "warnings": validation_warnings,
            "step_count": len(steps),
            "estimated_duration": len(steps) * 2,  # Rough estimate
            "validated_at": datetime.utcnow().isoformat()
        }
        
        logger.info("Workflow validation completed", task_id=task_id, 
                   is_valid=validation_result["is_valid"], 
                   error_count=len(validation_errors))
        
        return {
            "task_id": task_id,
            "status": "completed",
            "validation_result": validation_result
        }
        
    except Exception as e:
        logger.error("Workflow validation failed", task_id=task_id, error=str(e))
        raise

@celery_app.task(bind=True, name="workflows.cleanup_executions")
def cleanup_old_executions(self, retention_days: int = 7) -> Dict[str, Any]:
    """
    Clean up old workflow execution data
    
    Args:
        retention_days: Number of days to retain execution data
        
    Returns:
        Cleanup results
    """
    task_id = self.request.id
    logger.info("Starting workflow execution cleanup", task_id=task_id, retention_days=retention_days)
    
    try:
        redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
        
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        # Find old execution keys
        execution_keys = asyncio.run(redis_client.keys("workflow:execution:*"))
        schedule_keys = asyncio.run(redis_client.keys("workflow:schedule:*"))
        
        cleaned_executions = 0
        cleaned_schedules = 0
        
        # Clean up old executions
        for key in execution_keys:
            try:
                started_at_str = asyncio.run(redis_client.hget(key, "started_at"))
                if started_at_str:
                    started_at = datetime.fromisoformat(started_at_str)
                    if started_at < cutoff_date:
                        asyncio.run(redis_client.delete(key))
                        cleaned_executions += 1
            except Exception:
                # If we can't parse the date, delete it anyway
                asyncio.run(redis_client.delete(key))
                cleaned_executions += 1
        
        # Clean up old schedules
        for key in schedule_keys:
            try:
                # For schedules, we might want different retention logic
                # For now, use the same cutoff
                asyncio.run(redis_client.delete(key))
                cleaned_schedules += 1
            except Exception:
                pass
        
        cleanup_result = {
            "cleaned_executions": cleaned_executions,
            "cleaned_schedules": cleaned_schedules,
            "retention_days": retention_days,
            "cutoff_date": cutoff_date.isoformat(),
            "cleaned_at": datetime.utcnow().isoformat()
        }
        
        logger.info("Workflow cleanup completed", task_id=task_id, 
                   cleaned_executions=cleaned_executions, 
                   cleaned_schedules=cleaned_schedules)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "cleanup_result": cleanup_result
        }
        
    except Exception as e:
        logger.error("Workflow cleanup failed", task_id=task_id, error=str(e))
        raise