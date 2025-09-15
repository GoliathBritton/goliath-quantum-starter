#!/usr/bin/env python3
"""
Recipe API Endpoints

FastAPI endpoints for recipe compilation and execution, integrating the
PipelineBuilder frontend with the qsaiCore orchestrator backend.

Author: Goliath Quantum Engineering Team
Version: 0.1.0
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uuid

# Import WebSocket functionality for real-time updates
try:
    from websocket_router import send_pipeline_execution_update
except ImportError:
    # Fallback if websocket_router is not available
    async def send_pipeline_execution_update(*args, **kwargs):
        pass

# Import our core orchestrator
try:
    from core.qsaiCore import (
        QSAICore, create_orchestrator,
        CompileRequest, FlowDefinition, RecipeNode, RecipeEdge,
        OptimizationLevel, TargetRuntime, JobStatus,
        CompiledRecipe, JobExecution
    )
except ImportError:
    # Fallback for development
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from core.qsaiCore import (
        QSAICore, create_orchestrator,
        CompileRequest, FlowDefinition, RecipeNode, RecipeEdge,
        OptimizationLevel, TargetRuntime, JobStatus,
        CompiledRecipe, JobExecution
    )

# Configure logging
logger = logging.getLogger('recipe_api')

# Create router
router = APIRouter(prefix="/api/recipes", tags=["recipes"])

# Global orchestrator instance
orchestrator: Optional[QSAICore] = None


def get_orchestrator() -> QSAICore:
    """Dependency to get orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        orchestrator = create_orchestrator({
            'environment': 'development',
            'max_concurrent_jobs': 10,
            'default_timeout': 300,
        })
    return orchestrator


# Pydantic models for API requests/responses

class NodePosition(BaseModel):
    """Node position in the flow canvas"""
    x: float
    y: float


class NodeData(BaseModel):
    """Node data from PipelineBuilder"""
    label: str
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None


class FlowNode(BaseModel):
    """Flow node from PipelineBuilder"""
    id: str
    type: str
    position: NodePosition
    data: NodeData
    config: Optional[Dict[str, Any]] = None


class FlowEdge(BaseModel):
    """Flow edge from PipelineBuilder"""
    id: str
    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class FlowMetadata(BaseModel):
    """Flow metadata"""
    name: Optional[str] = None
    description: Optional[str] = None
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: Optional[List[str]] = None


class RecipeCompileRequest(BaseModel):
    """Recipe compilation request from PipelineBuilder"""
    nodes: List[FlowNode]
    edges: List[FlowEdge]
    metadata: FlowMetadata
    optimization_level: str = Field(default="optimized", pattern="^(basic|optimized|aggressive)$")
    target_runtime: str = Field(default="python", pattern="^(python|javascript|quantum)$")
    recipe_name: Optional[str] = None
    description: Optional[str] = None


class RecipeCompileResponse(BaseModel):
    """Recipe compilation response"""
    recipe_id: str
    status: str
    compiled_code: Optional[str] = None
    execution_plan: Optional[Dict[str, Any]] = None
    estimated_cost: float
    estimated_duration: int
    warnings: List[str]
    metadata: Dict[str, Any]
    created_at: datetime


class RecipeExecuteRequest(BaseModel):
    """Recipe execution request"""
    recipe_id: str
    input_data: Optional[Dict[str, Any]] = None
    priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")
    timeout: Optional[int] = Field(default=300, ge=30, le=3600)  # 30s to 1h


class RecipeExecuteResponse(BaseModel):
    """Recipe execution response"""
    job_id: str
    recipe_id: str
    status: str
    message: str
    estimated_completion: Optional[datetime] = None


class JobStatusResponse(BaseModel):
    """Job status response"""
    job_id: str
    recipe_id: str
    status: str
    progress: float
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cost: Optional[float] = None
    compute_provider: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class RecipeListResponse(BaseModel):
    """Recipe list response"""
    recipes: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int


class JobListResponse(BaseModel):
    """Job list response"""
    jobs: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int


class PipelineConfigSaveRequest(BaseModel):
    """Pipeline configuration save request"""
    name: str
    description: Optional[str] = None
    nodes: List[FlowNode]
    edges: List[FlowEdge]
    metadata: FlowMetadata
    tags: Optional[List[str]] = None


class PipelineConfigResponse(BaseModel):
    """Pipeline configuration response"""
    id: str
    name: str
    description: Optional[str] = None
    nodes: List[FlowNode]
    edges: List[FlowEdge]
    metadata: FlowMetadata
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime


class PipelineConfigListResponse(BaseModel):
    """Pipeline configuration list response"""
    pipelines: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int


# API Endpoints

# In-memory storage for pipeline configurations (in production, use a database)
pipeline_configs: Dict[str, Dict[str, Any]] = {}

@router.post("/pipelines", response_model=PipelineConfigResponse)
async def save_pipeline_config(
    request: PipelineConfigSaveRequest
) -> PipelineConfigResponse:
    """
    Save a pipeline configuration for later use
    
    This endpoint saves the raw flow definition from PipelineBuilder
    so users can load and modify their pipelines later.
    """
    try:
        pipeline_id = str(uuid.uuid4())
        now = datetime.now()
        
        pipeline_data = {
            "id": pipeline_id,
            "name": request.name,
            "description": request.description,
            "nodes": [node.dict() for node in request.nodes],
            "edges": [edge.dict() for edge in request.edges],
            "metadata": request.metadata.dict(),
            "tags": request.tags or [],
            "created_at": now,
            "updated_at": now
        }
        
        pipeline_configs[pipeline_id] = pipeline_data
        
        logger.info(f"Pipeline configuration saved: {request.name} (ID: {pipeline_id})")
        
        return PipelineConfigResponse(**pipeline_data)
        
    except Exception as e:
        logger.error(f"Failed to save pipeline configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save pipeline: {str(e)}")


@router.get("/pipelines", response_model=PipelineConfigListResponse)
async def list_pipeline_configs(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None
) -> PipelineConfigListResponse:
    """
    List saved pipeline configurations
    
    Returns a paginated list of saved pipeline configurations.
    """
    try:
        # Filter pipelines based on search term
        filtered_pipelines = []
        for pipeline in pipeline_configs.values():
            if search:
                if (search.lower() in pipeline["name"].lower() or 
                    (pipeline["description"] and search.lower() in pipeline["description"].lower())):
                    filtered_pipelines.append(pipeline)
            else:
                filtered_pipelines.append(pipeline)
        
        # Sort by updated_at descending
        filtered_pipelines.sort(key=lambda x: x["updated_at"], reverse=True)
        
        # Paginate
        total = len(filtered_pipelines)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_pipelines = filtered_pipelines[start_idx:end_idx]
        
        # Convert datetime objects to strings for JSON serialization
        for pipeline in paginated_pipelines:
            pipeline["created_at"] = pipeline["created_at"].isoformat()
            pipeline["updated_at"] = pipeline["updated_at"].isoformat()
        
        return PipelineConfigListResponse(
            pipelines=paginated_pipelines,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to list pipeline configurations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list pipelines: {str(e)}")


@router.get("/pipelines/{pipeline_id}", response_model=PipelineConfigResponse)
async def get_pipeline_config(
    pipeline_id: str
) -> PipelineConfigResponse:
    """
    Get a specific pipeline configuration by ID
    
    Returns the full pipeline configuration for loading into PipelineBuilder.
    """
    try:
        if pipeline_id not in pipeline_configs:
            raise HTTPException(status_code=404, detail=f"Pipeline not found: {pipeline_id}")
        
        pipeline_data = pipeline_configs[pipeline_id].copy()
        
        # Convert datetime objects to strings for JSON serialization
        pipeline_data["created_at"] = pipeline_data["created_at"].isoformat()
        pipeline_data["updated_at"] = pipeline_data["updated_at"].isoformat()
        
        return PipelineConfigResponse(**pipeline_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get pipeline configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get pipeline: {str(e)}")


@router.put("/pipelines/{pipeline_id}", response_model=PipelineConfigResponse)
async def update_pipeline_config(
    pipeline_id: str,
    request: PipelineConfigSaveRequest
) -> PipelineConfigResponse:
    """
    Update an existing pipeline configuration
    
    Updates the pipeline configuration with new data while preserving the ID and created_at timestamp.
    """
    try:
        if pipeline_id not in pipeline_configs:
            raise HTTPException(status_code=404, detail=f"Pipeline not found: {pipeline_id}")
        
        existing_pipeline = pipeline_configs[pipeline_id]
        now = datetime.now()
        
        updated_pipeline = {
            "id": pipeline_id,
            "name": request.name,
            "description": request.description,
            "nodes": [node.dict() for node in request.nodes],
            "edges": [edge.dict() for edge in request.edges],
            "metadata": request.metadata.dict(),
            "tags": request.tags or [],
            "created_at": existing_pipeline["created_at"],
            "updated_at": now
        }
        
        pipeline_configs[pipeline_id] = updated_pipeline
        
        logger.info(f"Pipeline configuration updated: {request.name} (ID: {pipeline_id})")
        
        # Convert datetime objects to strings for JSON serialization
        response_data = updated_pipeline.copy()
        response_data["created_at"] = response_data["created_at"].isoformat()
        response_data["updated_at"] = response_data["updated_at"].isoformat()
        
        return PipelineConfigResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update pipeline configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update pipeline: {str(e)}")


@router.delete("/pipelines/{pipeline_id}")
async def delete_pipeline_config(
    pipeline_id: str
) -> JSONResponse:
    """
    Delete a pipeline configuration
    
    Removes a saved pipeline configuration from the system.
    """
    try:
        if pipeline_id not in pipeline_configs:
            raise HTTPException(status_code=404, detail=f"Pipeline not found: {pipeline_id}")
        
        pipeline_name = pipeline_configs[pipeline_id]["name"]
        del pipeline_configs[pipeline_id]
        
        logger.info(f"Pipeline configuration deleted: {pipeline_name} (ID: {pipeline_id})")
        
        return JSONResponse(
            content={"message": f"Pipeline configuration {pipeline_id} has been deleted"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete pipeline configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete pipeline: {str(e)}")


@router.post("/compile", response_model=RecipeCompileResponse)
async def compile_recipe(
    request: RecipeCompileRequest,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> RecipeCompileResponse:
    """
    Compile a drag/drop recipe from PipelineBuilder into executable format
    
    This endpoint receives the flow definition from the PipelineBuilder frontend
    and compiles it into an executable recipe using the qsaiCore orchestrator.
    """
    try:
        logger.info(f"Compiling recipe: {request.recipe_name or 'Unnamed'}")
        
        # Generate a temporary recipe ID for WebSocket updates
        temp_recipe_id = str(uuid.uuid4())
        
        # Send compilation started update
        await send_pipeline_execution_update(
            temp_recipe_id, 
            "compiling", 
            progress=0.0, 
            message="Starting recipe compilation..."
        )
        
        # Convert Pydantic models to qsaiCore models
        await send_pipeline_execution_update(
            temp_recipe_id, 
            "compiling", 
            progress=0.2, 
            message="Converting flow definition..."
        )
        
        nodes = [
            RecipeNode(
                id=node.id,
                type=node.type,
                position={"x": node.position.x, "y": node.position.y},
                data=node.data.dict(),
                config=node.config
            )
            for node in request.nodes
        ]
        
        edges = [
            RecipeEdge(
                id=edge.id,
                source=edge.source,
                target=edge.target,
                source_handle=edge.source_handle,
                target_handle=edge.target_handle,
                data=edge.data
            )
            for edge in request.edges
        ]
        
        flow_definition = FlowDefinition(
            nodes=nodes,
            edges=edges,
            metadata=request.metadata.dict()
        )
        
        # Send validation update
        await send_pipeline_execution_update(
            temp_recipe_id, 
            "compiling", 
            progress=0.4, 
            message="Validating flow definition..."
        )
        
        # Create compilation request
        compile_request = CompileRequest(
            flow_definition=flow_definition,
            optimization_level=OptimizationLevel(request.optimization_level),
            target_runtime=TargetRuntime(request.target_runtime),
            recipe_name=request.recipe_name,
            description=request.description
        )
        
        # Send optimization update
        await send_pipeline_execution_update(
            temp_recipe_id, 
            "compiling", 
            progress=0.6, 
            message="Optimizing execution plan..."
        )
        
        # Compile the recipe
        compiled_recipe = await orchestrator.compile_recipe(compile_request)
        
        # Send completion update
        await send_pipeline_execution_update(
            temp_recipe_id, 
            "completed", 
            progress=1.0, 
            message="Recipe compilation completed successfully!",
            result={"recipe_id": compiled_recipe.recipe_id}
        )
        
        # Return response
        return RecipeCompileResponse(
            recipe_id=compiled_recipe.recipe_id,
            status="success",
            compiled_code=compiled_recipe.compiled_code,
            execution_plan={
                "steps": compiled_recipe.execution_plan.steps,
                "dependencies": compiled_recipe.execution_plan.dependencies,
                "resource_requirements": compiled_recipe.execution_plan.resource_requirements,
                "parallelizable_steps": compiled_recipe.execution_plan.parallelizable_steps
            },
            estimated_cost=compiled_recipe.estimated_cost,
            estimated_duration=compiled_recipe.estimated_duration,
            warnings=compiled_recipe.warnings,
            metadata=compiled_recipe.metadata,
            created_at=compiled_recipe.created_at
        )
        
    except ValueError as e:
        logger.error(f"Validation error during compilation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Compilation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Compilation failed: {str(e)}")


@router.post("/execute", response_model=RecipeExecuteResponse)
async def execute_recipe(
    request: RecipeExecuteRequest,
    background_tasks: BackgroundTasks,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> RecipeExecuteResponse:
    """
    Execute a compiled recipe
    
    Starts execution of a previously compiled recipe with optional input data.
    The execution runs in the background and can be monitored via the job status endpoint.
    """
    try:
        logger.info(f"Executing recipe: {request.recipe_id}")
        
        # Check if recipe exists
        recipe = orchestrator.get_recipe(request.recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"Recipe not found: {request.recipe_id}")
        
        # Start execution
        job_id = await orchestrator.execute_recipe(
            request.recipe_id,
            request.input_data
        )
        
        # Calculate estimated completion time
        estimated_completion = None
        if recipe.estimated_duration:
            estimated_completion = datetime.utcnow().replace(
                microsecond=0
            ) + timedelta(seconds=recipe.estimated_duration)
        
        return RecipeExecuteResponse(
            job_id=job_id,
            recipe_id=request.recipe_id,
            status="started",
            message=f"Recipe execution started with job ID: {job_id}",
            estimated_completion=estimated_completion
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@router.get("/jobs/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> JobStatusResponse:
    """
    Get the status of a recipe execution job
    
    Returns the current status, progress, and results (if completed) of a job.
    """
    try:
        job = orchestrator.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
        
        return JobStatusResponse(
            job_id=job.job_id,
            recipe_id=job.recipe_id,
            status=job.status.value,
            progress=job.progress,
            result=job.result,
            error=job.error,
            started_at=job.started_at,
            completed_at=job.completed_at,
            cost=job.cost,
            compute_provider=job.compute_provider.value if job.compute_provider else None,
            metadata=job.metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get job status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get job status: {str(e)}")


@router.get("/jobs/{job_id}/cancel")
async def cancel_job(
    job_id: str,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> JSONResponse:
    """
    Cancel a running job
    
    Attempts to cancel a job that is currently queued or running.
    """
    try:
        job = orchestrator.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
        
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            return JSONResponse(
                status_code=400,
                content={"message": f"Job {job_id} cannot be cancelled (status: {job.status.value})"}
            )
        
        # Update job status to cancelled
        job.status = JobStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        
        return JSONResponse(
            content={"message": f"Job {job_id} has been cancelled"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel job: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel job: {str(e)}")


@router.get("/", response_model=RecipeListResponse)
async def list_recipes(
    page: int = 1,
    page_size: int = 20,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> RecipeListResponse:
    """
    List all compiled recipes
    
    Returns a paginated list of all compiled recipes with their metadata.
    """
    try:
        recipes = orchestrator.list_recipes()
        total = len(recipes)
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_recipes = recipes[start_idx:end_idx]
        
        # Convert to dict format
        recipe_dicts = []
        for recipe in paginated_recipes:
            recipe_dict = {
                "recipe_id": recipe.recipe_id,
                "estimated_cost": recipe.estimated_cost,
                "estimated_duration": recipe.estimated_duration,
                "warnings": recipe.warnings,
                "metadata": recipe.metadata,
                "created_at": recipe.created_at,
                "node_count": recipe.metadata.get("node_count", 0),
                "edge_count": recipe.metadata.get("edge_count", 0)
            }
            recipe_dicts.append(recipe_dict)
        
        return RecipeListResponse(
            recipes=recipe_dicts,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to list recipes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list recipes: {str(e)}")


@router.get("/jobs", response_model=JobListResponse)
async def list_jobs(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> JobListResponse:
    """
    List jobs with optional status filtering
    
    Returns a paginated list of jobs, optionally filtered by status.
    """
    try:
        # Parse status filter
        status_filter = None
        if status:
            try:
                status_filter = JobStatus(status)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        jobs = orchestrator.list_jobs(status_filter)
        total = len(jobs)
        
        # Apply pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_jobs = jobs[start_idx:end_idx]
        
        # Convert to dict format
        job_dicts = []
        for job in paginated_jobs:
            job_dict = {
                "job_id": job.job_id,
                "recipe_id": job.recipe_id,
                "status": job.status.value,
                "progress": job.progress,
                "started_at": job.started_at,
                "completed_at": job.completed_at,
                "cost": job.cost,
                "compute_provider": job.compute_provider.value if job.compute_provider else None,
                "has_result": job.result is not None,
                "has_error": job.error is not None
            }
            job_dicts.append(job_dict)
        
        return JobListResponse(
            jobs=job_dicts,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to list jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")


# Health check endpoint
@router.get("/health")
async def health_check(
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> JSONResponse:
    """
    Health check for the recipe API
    
    Returns the current status of the recipe compilation and execution system.
    """
    try:
        recipes = orchestrator.list_recipes()
        jobs = orchestrator.list_jobs()
        
        running_jobs = [job for job in jobs if job.status == JobStatus.RUNNING]
        completed_jobs = [job for job in jobs if job.status == JobStatus.COMPLETED]
        failed_jobs = [job for job in jobs if job.status == JobStatus.FAILED]
        
        return JSONResponse(
            content={
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "statistics": {
                    "total_recipes": len(recipes),
                    "total_jobs": len(jobs),
                    "running_jobs": len(running_jobs),
                    "completed_jobs": len(completed_jobs),
                    "failed_jobs": len(failed_jobs)
                },
                "orchestrator": {
                    "version": "0.1.0",
                    "environment": orchestrator.config.get("environment", "unknown")
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        )


@router.get("/test")
async def test_endpoint():
    """Simple test endpoint without dependencies"""
    return {"message": "Recipe router is working!", "timestamp": datetime.now().isoformat()}


@router.get("/{recipe_id}", response_model=Dict[str, Any])
async def get_recipe(
    recipe_id: str,
    include_code: bool = False,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> Dict[str, Any]:
    """
    Get a specific recipe by ID
    
    Returns the details of a compiled recipe, optionally including the compiled code.
    """
    try:
        recipe = orchestrator.get_recipe(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"Recipe not found: {recipe_id}")
        
        recipe_dict = {
            "recipe_id": recipe.recipe_id,
            "estimated_cost": recipe.estimated_cost,
            "estimated_duration": recipe.estimated_duration,
            "warnings": recipe.warnings,
            "metadata": recipe.metadata,
            "created_at": recipe.created_at,
            "execution_plan": {
                "steps": recipe.execution_plan.steps,
                "dependencies": recipe.execution_plan.dependencies,
                "resource_requirements": recipe.execution_plan.resource_requirements,
                "parallelizable_steps": recipe.execution_plan.parallelizable_steps
            }
        }
        
        if include_code:
            recipe_dict["compiled_code"] = recipe.compiled_code
        
        return recipe_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get recipe: {str(e)}")


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: str,
    orchestrator: QSAICore = Depends(get_orchestrator)
) -> JSONResponse:
    """
    Delete a recipe
    
    Removes a compiled recipe from the system. Active jobs using this recipe will continue running.
    """
    try:
        recipe = orchestrator.get_recipe(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"Recipe not found: {recipe_id}")
        
        # Remove from orchestrator
        del orchestrator.recipes[recipe_id]
        
        return JSONResponse(
            content={"message": f"Recipe {recipe_id} has been deleted"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete recipe: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete recipe: {str(e)}")


# Export router for inclusion in main FastAPI app
__all__ = ["router"]