"""
Comprehensive tests for FLYFOX AI Quantum Computing Platform
"""

import pytest
import asyncio
import sys
import os
import tempfile
import json
import yaml
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestConfiguration:
    """Test configuration management"""
    
    def test_config_initialization(self):
        """Test configuration initialization"""
        from utils.config import get_config, config
        
        cfg = get_config()
        assert cfg is not None
        assert cfg.quantum.max_qubits == 32
        assert cfg.quantum.backend == "qiskit"
        assert cfg.dynex.enable_pouw is True
        assert cfg.agent.enable_chatbot is True
    
    def test_config_get_set(self):
        """Test configuration get/set methods"""
        from utils.config import config
        
        # Test get method
        assert config.get("quantum.max_qubits") == 32
        assert config.get("quantum.backend") == "qiskit"
        assert config.get("nonexistent.key", "default") == "default"
        
        # Test set method
        config.set("quantum.max_qubits", 64)
        assert config.quantum.max_qubits == 64
        
        # Test invalid key
        with pytest.raises(KeyError):
            config.set("nonexistent.key", "value")
    
    def test_config_save_load(self):
        """Test configuration save/load functionality"""
        from utils.config import config
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            # Save configuration
            config.save_to_file(temp_path, format="yaml")
            assert os.path.exists(temp_path)
            
            # Load configuration
            config.quantum.max_qubits = 128  # Change value
            config.save_to_file(temp_path, format="yaml")
            
            # Verify file was written
            with open(temp_path, 'r') as f:
                content = f.read()
                assert "max_qubits: 128" in content
                
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

class TestLogging:
    """Test logging functionality"""
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        from utils.logger import get_logger, Logger
        
        logger = get_logger("test_logger")
        assert logger is not None
        assert isinstance(logger, Logger)
        assert logger.name == "test_logger"
    
    def test_logger_methods(self):
        """Test logger methods"""
        from utils.logger import get_logger
        
        logger = get_logger("test_methods")
        
        # Test basic logging methods
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        
        # Test structured logging
        logger.info("Test with extra", extra_field="value", another_field=123)
        
        # Test quantum-specific logging
        logger.log_quantum_execution("test_op", 4, "qiskit", 1.5, True)
        logger.log_dynex_submission("hash1", "hash2", 10.5)
        logger.log_agent_interaction("test_agent", "input", "response", 0.5)

class TestAgents:
    """Test AI agent functionality"""
    
    @pytest.mark.asyncio
    async def test_chatbot_initialization(self):
        """Test chatbot initialization"""
        from agents.chatbot import create_chatbot
        
        chatbot = create_chatbot()
        assert chatbot is not None
        assert chatbot.quantum_enhanced is True
        assert len(chatbot.conversation_history) == 0
    
    @pytest.mark.asyncio
    async def test_chatbot_message_processing(self):
        """Test chatbot message processing"""
        from agents.chatbot import create_chatbot
        
        chatbot = create_chatbot()
        
        # Test basic message processing
        response = await chatbot.process_message("Hello")
        assert response is not None
        assert response.content is not None
        assert response.confidence > 0
        assert response.response_time >= 0
        
        # Test conversation history
        assert len(chatbot.conversation_history) == 2  # user + assistant
    
    @pytest.mark.asyncio
    async def test_voice_agent_initialization(self):
        """Test voice agent initialization"""
        from agents.voice_agent import create_voice_agent
        
        voice_agent = create_voice_agent()
        assert voice_agent is not None
        assert voice_agent.is_voice_enabled == voice_agent.config.enable_voice
    
    @pytest.mark.asyncio
    async def test_digital_human_initialization(self):
        """Test digital human initialization"""
        from agents.digital_human import create_digital_human
        
        digital_human = create_digital_human()
        assert digital_human is not None
        assert digital_human.personality is not None
        assert digital_human.personality["name"] == "Quantum"
    
    @pytest.mark.asyncio
    async def test_digital_human_interaction(self):
        """Test digital human interaction"""
        from agents.digital_human import create_digital_human
        
        digital_human = create_digital_human()
        
        # Test basic interaction
        response = await digital_human.interact("Hello")
        assert response is not None
        assert response.content is not None
        assert response.emotional_expression is not None
        assert response.follow_up_questions is not None
        
        # Test session management
        assert len(digital_human.active_sessions) > 0

class TestQuantumComponents:
    """Test quantum computing components"""
    
    @pytest.mark.asyncio
    async def test_nqba_engine_import(self):
        """Test NQBA engine import"""
        try:
            from nqba.engine import NQBAEngine
            assert True
        except ImportError:
            pytest.skip("NQBA engine not available")
    
    @pytest.mark.asyncio
    async def test_goliath_quantum_import(self):
        """Test GoliathQuantum import"""
        try:
            from goliath.quantum import GoliathQuantum
            assert True
        except ImportError:
            pytest.skip("GoliathQuantum not available")
    
    @pytest.mark.asyncio
    async def test_sigmaeq_engine_import(self):
        """Test SigmaEQ engine import"""
        try:
            from goliath.quantum.sigmaeq_engine import SigmaEQEngine
            assert True
        except ImportError:
            pytest.skip("SigmaEQ engine not available")

class TestCLI:
    """Test CLI functionality"""
    
    def test_cli_import(self):
        """Test CLI import"""
        try:
            from goliath.quantum.cli import cli
            assert cli is not None
        except ImportError:
            pytest.skip("CLI not available")
    
    def test_cli_commands(self):
        """Test CLI command structure"""
        try:
            from goliath.quantum.cli import cli
            
            # Check that CLI groups exist
            assert hasattr(cli, 'commands')
            
            # Check for quantum commands
            quantum_commands = [cmd.name for cmd in cli.commands if cmd.name == 'quantum']
            assert len(quantum_commands) > 0
            
            # Check for agent commands
            agent_commands = [cmd.name for cmd in cli.commands if cmd.name == 'agents']
            assert len(agent_commands) > 0
            
            # Check for system commands
            system_commands = [cmd.name for cmd in cli.commands if cmd.name == 'system']
            assert len(system_commands) > 0
            
        except ImportError:
            pytest.skip("CLI not available")

class TestIntegration:
    """Test integration scenarios"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test complete workflow from configuration to agent interaction"""
        from utils.config import get_config
        from utils.logger import get_logger
        from agents.chatbot import create_chatbot
        
        # Initialize components
        config = get_config()
        logger = get_logger("test_integration")
        chatbot = create_chatbot()
        
        # Test configuration
        assert config.quantum.max_qubits > 0
        assert config.agent.enable_chatbot is True
        
        # Test logging
        logger.info("Integration test message")
        
        # Test agent
        response = await chatbot.process_message("What is quantum computing?")
        assert response is not None
        assert response.content is not None
    
    def test_configuration_persistence(self):
        """Test configuration persistence across imports"""
        from utils.config import get_config, config
        
        # Get initial config
        initial_config = get_config()
        initial_qubits = initial_config.quantum.max_qubits
        
        # Modify config
        config.quantum.max_qubits = 128
        
        # Get config again
        new_config = get_config()
        assert new_config.quantum.max_qubits == 128
        
        # Verify it's the same instance
        assert initial_config is new_config

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_config_invalid_keys(self):
        """Test configuration with invalid keys"""
        from utils.config import config
        
        # Test getting invalid key
        result = config.get("invalid.key.path", "default_value")
        assert result == "default_value"
        
        # Test setting invalid key
        with pytest.raises(KeyError):
            config.set("invalid.key.path", "value")
    
    @pytest.mark.asyncio
    async def test_agent_error_handling(self):
        """Test agent error handling"""
        from agents.chatbot import create_chatbot
        
        chatbot = create_chatbot()
        
        # Test with empty message
        response = await chatbot.process_message("")
        assert response is not None
        assert response.content is not None
    
    def test_logger_error_handling(self):
        """Test logger error handling"""
        from utils.logger import get_logger
        
        logger = get_logger("test_error_handling")
        
        # Test logging with various data types
        logger.info("Test with dict", data={"key": "value"})
        logger.info("Test with list", data=[1, 2, 3])
        logger.info("Test with None", data=None)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
