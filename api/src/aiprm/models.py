"""
Goliath of All Trade - AIPRM Integration Models
This module defines the data models for AIPRM integration.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class PromptCategory(str, Enum):
    COPYWRITING = "copywriting"
    SEO = "seo"
    CONTENT_STRATEGY = "content_strategy"
    MARKETING = "marketing"
    BUSINESS = "business"
    QUANTUM_COMPUTING = "quantum_computing"
    FINANCE = "finance"
    ENERGY = "energy"
    CUSTOM = "custom"


class PromptTemplate(BaseModel):
    """AIPRM Prompt Template model"""
    id: str
    title: str
    description: str
    prompt_text: str
    category: PromptCategory
    tags: List[str] = []
    author: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    version: str = "1.0"
    is_public: bool = True
    usage_count: int = 0
    rating: float = 0.0
    quantum_enhanced: bool = False


class PromptCollection(BaseModel):
    """Collection of AIPRM prompt templates"""
    id: str
    name: str
    description: str
    owner: str
    prompts: List[str] = []  # List of prompt IDs
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_public: bool = False


class AIExtension(BaseModel):
    """AIPRM Extension model"""
    id: str
    name: str
    description: str
    version: str
    author: str
    enabled: bool = True
    config: Dict[str, Any] = {}
    created_at: datetime
    updated_at: Optional[datetime] = None
    compatibility: List[str] = ["default"]


class UserAIPRMSettings(BaseModel):
    """User settings for AIPRM"""
    user_id: str
    default_prompt_collection: Optional[str] = None
    favorite_prompts: List[str] = []
    enabled_extensions: List[str] = []
    custom_settings: Dict[str, Any] = {}
    created_at: datetime
    updated_at: Optional[datetime] = None


# API Request/Response Models
class CreatePromptRequest(BaseModel):
    """Request model for creating a new prompt template"""
    title: str
    description: str
    prompt_text: str
    category: PromptCategory
    tags: List[str] = []
    is_public: bool = True
    quantum_enhanced: bool = False


class PromptListResponse(BaseModel):
    """Response model for listing prompt templates"""
    prompts: List[PromptTemplate]
    total: int
    page: int
    page_size: int


class ExtensionListResponse(BaseModel):
    """Response model for listing available extensions"""
    extensions: List[AIExtension]
    total: int


class InstallExtensionRequest(BaseModel):
    """Request model for installing an extension"""
    extension_id: str
    config: Dict[str, Any] = {}


class AIPromptExecutionRequest(BaseModel):
    """Request model for executing a prompt"""
    prompt_id: Optional[str] = None
    prompt_text: Optional[str] = None
    input_variables: Dict[str, Any] = {}
    model: str = "default"
    quantum_enhanced: bool = False


class AIPromptExecutionResponse(BaseModel):
    """Response model for prompt execution results"""
    result: str
    execution_time: float
    token_usage: Dict[str, int]
    model_used: str
    prompt_id: Optional[str] = None