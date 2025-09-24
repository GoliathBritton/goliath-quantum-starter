"""
Goliath of All Trade - AIPRM Integration Client
This module provides a client for interacting with the AIPRM API.
"""

import httpx
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .models import (
    PromptTemplate, 
    AIExtension, 
    PromptCategory,
    PromptCollection
)

logger = logging.getLogger(__name__)

class AIPRMClient:
    """Client for interacting with AIPRM API"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.aiprm.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def get_prompts(self, category: Optional[PromptCategory] = None, 
                         page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Get prompt templates from AIPRM"""
        params = {"page": page, "pageSize": page_size}
        if category:
            params["category"] = category
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/prompts", 
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching prompts: {str(e)}")
                raise
    
    async def get_prompt(self, prompt_id: str) -> Dict[str, Any]:
        """Get a specific prompt template"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/prompts/{prompt_id}", 
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching prompt {prompt_id}: {str(e)}")
                raise
    
    async def create_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new prompt template"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/prompts", 
                    headers=self.headers,
                    json=prompt_data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error creating prompt: {str(e)}")
                raise
    
    async def get_extensions(self) -> List[Dict[str, Any]]:
        """Get available AIPRM extensions"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/extensions", 
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching extensions: {str(e)}")
                raise
    
    async def install_extension(self, extension_id: str, config: Dict[str, Any] = {}) -> Dict[str, Any]:
        """Install an AIPRM extension"""
        payload = {
            "extension_id": extension_id,
            "config": config
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/extensions/install", 
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error installing extension {extension_id}: {str(e)}")
                raise
    
    async def execute_prompt(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an AIPRM prompt"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/execute", 
                    headers=self.headers,
                    json=prompt_data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error executing prompt: {str(e)}")
                raise

    # Mock methods for development/testing
    async def get_mock_prompts(self, category: Optional[PromptCategory] = None) -> List[PromptTemplate]:
        """Get mock prompt templates for development"""
        now = datetime.now()
        prompts = [
            PromptTemplate(
                id="1",
                title="Quantum Algorithm Optimizer",
                description="Optimize quantum algorithms for specific use cases",
                prompt_text="Optimize the following quantum algorithm for {use_case}: {algorithm}",
                category=PromptCategory.QUANTUM_COMPUTING,
                tags=["quantum", "optimization", "algorithm"],
                author="Goliath AI",
                created_at=now,
                quantum_enhanced=True
            ),
            PromptTemplate(
                id="2",
                title="Energy Grid Analysis",
                description="Analyze energy grid data for optimization opportunities",
                prompt_text="Analyze the following energy grid data and identify optimization opportunities: {data}",
                category=PromptCategory.ENERGY,
                tags=["energy", "grid", "optimization"],
                author="Goliath AI",
                created_at=now,
                quantum_enhanced=True
            ),
            PromptTemplate(
                id="3",
                title="Financial Risk Assessment",
                description="Assess financial risk using quantum-enhanced models",
                prompt_text="Assess the financial risk for the following portfolio using quantum-enhanced models: {portfolio}",
                category=PromptCategory.FINANCE,
                tags=["finance", "risk", "quantum"],
                author="Goliath AI",
                created_at=now,
                quantum_enhanced=True
            )
        ]
        
        if category:
            return [p for p in prompts if p.category == category]
        return prompts
    
    async def get_mock_extensions(self) -> List[AIExtension]:
        """Get mock extensions for development"""
        now = datetime.now()
        return [
            AIExtension(
                id="ext1",
                name="Quantum Prompt Enhancer",
                description="Enhances prompts with quantum computing concepts",
                version="1.0.0",
                author="Goliath AI",
                created_at=now,
                compatibility=["default", "quantum"]
            ),
            AIExtension(
                id="ext2",
                name="Energy Domain Knowledge",
                description="Adds energy domain knowledge to prompt responses",
                version="1.0.0",
                author="Goliath AI",
                created_at=now,
                compatibility=["default", "energy"]
            ),
            AIExtension(
                id="ext3",
                name="Financial Analysis Tools",
                description="Adds financial analysis capabilities to prompts",
                version="1.0.0",
                author="Goliath AI",
                created_at=now,
                compatibility=["default", "finance"]
            )
        ]