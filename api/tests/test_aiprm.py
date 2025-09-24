"""
Test suite for AIPRM integration functionality.
Goliath of All Trade - AIPRM Integration Tests
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.main import app
from src.aiprm.client import AIPRMClient
from src.aiprm.models import PromptTemplate, AIExtension
from src.aiprm.extensions.manager import extension_manager

client = TestClient(app)

# Mock data for testing
mock_prompts = [
    PromptTemplate(
        id="1",
        title="Energy Market Analysis",
        description="Analyze energy market trends",
        category="energy",
        tags=["energy", "market", "analysis"],
        author="Goliath AI",
        quantum_enhanced=True
    )
]

mock_extensions = [
    AIExtension(
        id="ext1",
        name="Quantum Prompt Enhancer",
        description="Enhances prompts with quantum concepts",
        version="1.0.0",
        author="Goliath AI",
        installed=True
    )
]

@pytest.fixture
def mock_aiprm_client():
    with patch('src.routes.aiprm.AIPRMClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_prompt_templates.return_value = mock_prompts
        mock_instance.get_extensions.return_value = mock_extensions
        mock_client.return_value = mock_instance
        yield mock_instance

def test_get_prompts(mock_aiprm_client):
    """Test retrieving prompt templates"""
    response = client.get("/api/aiprm/prompts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Energy Market Analysis"

def test_get_extensions(mock_aiprm_client):
    """Test retrieving extensions"""
    response = client.get("/api/aiprm/extensions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Quantum Prompt Enhancer"

def test_install_extension(mock_aiprm_client):
    """Test installing an extension"""
    mock_aiprm_client.install_extension.return_value = True
    response = client.post("/api/aiprm/extensions/install/ext2")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_execute_prompt(mock_aiprm_client):
    """Test executing a prompt"""
    mock_aiprm_client.execute_prompt.return_value = "Generated response from AIPRM"
    response = client.post(
        "/api/aiprm/execute",
        json={"prompt_id": "1", "input_text": "Analyze recent energy market trends", "extensions": ["ext1"]}
    )
    assert response.status_code == 200
    assert "Generated response from AIPRM" in response.json()["result"]

def test_extension_manager():
    """Test extension manager functionality"""
    # Test getting available extensions
    extensions = extension_manager.get_available_extensions()
    assert len(extensions) > 0
    
    # Test enabling an extension
    extension_id = extensions[0].id
    extension_manager.enable_extension(extension_id)
    assert extension_manager.is_extension_enabled(extension_id)
    
    # Test applying extensions to a prompt
    prompt = "Analyze quantum computing trends"
    enhanced_prompt = extension_manager.apply_extensions_to_prompt(prompt, [extension_id])
    assert enhanced_prompt != prompt  # The prompt should be modified by the extension