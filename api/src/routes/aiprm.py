"""
Goliath of All Trade - AIPRM Integration Routes
This module provides FastAPI routes for AIPRM integration.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
import os
from src.aiprm.models import (
    PromptTemplate, 
    AIExtension,
    PromptCategory,
    PromptListResponse,
    ExtensionListResponse,
    CreatePromptRequest,
    InstallExtensionRequest,
    AIPromptExecutionRequest,
    AIPromptExecutionResponse
)
from src.aiprm.client import AIPRMClient

router = APIRouter()

# Initialize AIPRM client
AIPRM_API_KEY = os.getenv("AIPRM_API_KEY", "demo_key")
aiprm_client = AIPRMClient(api_key=AIPRM_API_KEY)

@router.get("/prompts", response_model=PromptListResponse)
async def get_prompts(
    category: Optional[PromptCategory] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get AIPRM prompt templates"""
    try:
        # For development, use mock data
        prompts = await aiprm_client.get_mock_prompts(category)
        return PromptListResponse(
            prompts=prompts,
            total=len(prompts),
            page=page,
            page_size=page_size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch prompts: {str(e)}")

@router.post("/prompts", response_model=PromptTemplate)
async def create_prompt(prompt_data: CreatePromptRequest):
    """Create a new AIPRM prompt template"""
    try:
        # In production, this would call the actual AIPRM API
        # For now, return a mock response
        from datetime import datetime
        return PromptTemplate(
            id="new_prompt_id",
            title=prompt_data.title,
            description=prompt_data.description,
            prompt_text=prompt_data.prompt_text,
            category=prompt_data.category,
            tags=prompt_data.tags,
            author="Current User",
            created_at=datetime.now(),
            is_public=prompt_data.is_public,
            quantum_enhanced=prompt_data.quantum_enhanced
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create prompt: {str(e)}")

@router.get("/extensions", response_model=ExtensionListResponse)
async def get_extensions():
    """Get available AIPRM extensions"""
    try:
        # For development, use mock data
        extensions = await aiprm_client.get_mock_extensions()
        return ExtensionListResponse(
            extensions=extensions,
            total=len(extensions)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch extensions: {str(e)}")

@router.post("/extensions/install", response_model=AIExtension)
async def install_extension(request: InstallExtensionRequest):
    """Install an AIPRM extension"""
    try:
        # In production, this would call the actual AIPRM API
        # For now, return a mock response
        extensions = await aiprm_client.get_mock_extensions()
        for ext in extensions:
            if ext.id == request.extension_id:
                ext.config = request.config
                return ext
        raise HTTPException(status_code=404, detail=f"Extension {request.extension_id} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to install extension: {str(e)}")

@router.post("/execute", response_model=AIPromptExecutionResponse)
async def execute_prompt(request: AIPromptExecutionRequest):
    """Execute an AIPRM prompt"""
    try:
        # In production, this would call the actual AIPRM API
        # For now, return a mock response
        import time
        import random
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Mock response based on request
        if request.prompt_id:
            prompts = await aiprm_client.get_mock_prompts()
            prompt = next((p for p in prompts if p.id == request.prompt_id), None)
            if not prompt:
                raise HTTPException(status_code=404, detail=f"Prompt {request.prompt_id} not found")
            
            # Simple template variable replacement
            result = prompt.prompt_text
            for key, value in request.input_variables.items():
                result = result.replace(f"{{{key}}}", str(value))
                
            # Add some AI-generated content
            result += "\n\nAI-generated response based on your prompt:"
            if prompt.category == PromptCategory.QUANTUM_COMPUTING:
                result += "\n- Optimized quantum circuit with reduced gate count"
                result += "\n- Improved coherence time by 35%"
                result += "\n- Enhanced error mitigation techniques applied"
            elif prompt.category == PromptCategory.ENERGY:
                result += "\n- Identified 3 grid optimization opportunities"
                result += "\n- Potential 28% reduction in energy waste"
                result += "\n- Renewable integration improved by 42%"
            elif prompt.category == PromptCategory.FINANCE:
                result += "\n- Risk assessment complete with 95% confidence"
                result += "\n- Portfolio optimization suggestions provided"
                result += "\n- Quantum-enhanced Monte Carlo simulations applied"
        else:
            # Generic response for custom prompt
            result = "AI-generated response for your custom prompt:\n"
            result += "- Analysis complete with quantum-enhanced algorithms\n"
            result += "- Optimization opportunities identified\n"
            result += "- Recommendations generated based on your input"
            
        return AIPromptExecutionResponse(
            result=result,
            execution_time=random.uniform(0.5, 2.0),
            token_usage={"prompt_tokens": random.randint(50, 200), "completion_tokens": random.randint(100, 500)},
            model_used="gpt-4-quantum" if request.quantum_enhanced else "gpt-4",
            prompt_id=request.prompt_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute prompt: {str(e)}")