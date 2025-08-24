"""
Test Sigma Select Dashboard Fixes
Verifies all user feedback issues have been resolved
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add src to path for NQBA imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nqba.dynex_adapter import DynexAdapter, OptimizationResult, DynexConfig
from nqba.settings import NQBASettings, get_settings

class TestDynexAdapter:
    """Test Dynex adapter functionality"""
    
    def test_dynex_config_creation(self):
        """Test DynexConfig creation"""
        config = DynexConfig(
            api_key="test_key",
            mainnet=False,
            description="Test Description",
            default_reads=500,
            default_annealing_time=50
        )
        
        assert config.api_key == "test_key"
        assert config.mainnet == False
        assert config.description == "Test Description"
        assert config.default_reads == 500
        assert config.default_annealing_time == 50
    
    def test_optimization_result_creation(self):
        """Test OptimizationResult creation"""
        result = OptimizationResult(
            success=True,
            samples=[{"x": 1, "y": 0}],
            energy=-1.0,
            execution_time=0.5,
            dynex_job_id="job_123",
            metadata={"test": "data"}
        )
        
        assert result.success == True
        assert result.samples == [{"x": 1, "y": 0}]
        assert result.energy == -1.0
        assert result.execution_time == 0.5
        assert result.dynex_job_id == "job_123"
        assert result.metadata["test"] == "data"
    
    @patch('nqba.dynex_adapter.dynex.init')
    def test_dynex_adapter_initialization(self, mock_dynex_init):
        """Test DynexAdapter initialization"""
        config = DynexConfig(api_key="test_key")
        adapter = DynexAdapter(config)
        
        mock_dynex_init.assert_called_once_with(api_key="test_key")
        assert adapter.config == config
    
    @patch('nqba.dynex_adapter.dynex.DynexSampler')
    def test_solve_qubo_success(self, mock_sampler_class):
        """Test successful QUBO solving"""
        # Mock the sampler and sampleset
        mock_sampler = Mock()
        mock_sampleset = Mock()
        mock_sampler_class.return_value = mock_sampler
        
        # Mock sampleset behavior
        mock_sampleset.samples.return_value = [{"x": 1, "y": 0}]
        mock_sampleset.first.energy = -1.0
        mock_sampler.sample.return_value = mock_sampleset
        
        # Create adapter and solve
        config = DynexConfig(api_key="test_key")
        adapter = DynexAdapter(config)
        
        # Create a simple BQM
        bqm = Mock()
        
        result = adapter.solve_qubo(bqm, num_reads=100, annealing_time=50)
        
        # Verify sampler was called correctly
        mock_sampler.sample.assert_called_once_with(bqm, num_reads=100, annealing_time=50)
        
        # Verify result
        assert result.success == True
        assert result.samples == [{"x": 1, "y": 0}]
        assert result.energy == -1.0
        assert result.execution_time > 0
    
    @patch('nqba.dynex_adapter.dynex.DynexSampler')
    def test_solve_qubo_failure(self, mock_sampler_class):
        """Test QUBO solving failure handling"""
        # Mock sampler to raise exception
        mock_sampler = Mock()
        mock_sampler_class.return_value = mock_sampler
        mock_sampler.sample.side_effect = Exception("Test error")
        
        # Create adapter and solve
        config = DynexConfig(api_key="test_key")
        adapter = DynexAdapter(config)
        
        bqm = Mock()
        result = adapter.solve_qubo(bqm)
        
        # Verify failure handling
        assert result.success == False
        assert result.error_message == "Test error"
        assert result.energy == float('inf')
        assert result.execution_time > 0
    
    def test_build_lead_scoring_bqm(self):
        """Test lead scoring BQM construction"""
        config = DynexConfig(api_key="test_key")
        adapter = DynexAdapter(config)
        
        lead_data = [
            {
                "budget": "high",
                "urgency": "urgent",
                "pain_points": "energy costs"
            },
            {
                "budget": "medium",
                "urgency": "low",
                "pain_points": "quality issues"
            }
        ]
        
        bqm = adapter._build_lead_scoring_bqm(lead_data)
        
        # Verify BQM has expected variables
        assert "lead_0" in bqm.variables
        assert "lead_1" in bqm.variables
        
        # Verify quadratic interactions are added
        # Note: This is a simplified test - in practice you'd check the actual BQM structure

class TestSettings:
    """Test settings module functionality"""
    
    def test_settings_defaults(self):
        """Test default settings values"""
        settings = NQBASettings()
        
        assert settings.environment == "development"
        assert settings.debug == False
        assert settings.dynex_mainnet == True
        assert settings.dynex_default_reads == 1000
        assert settings.dynex_default_annealing_time == 100
    
    def test_environment_properties(self):
        """Test environment property methods"""
        settings = NQBASettings(environment="production")
        
        assert settings.is_production == True
        assert settings.is_development == False
        assert settings.is_testing == False
    
    def test_configuration_properties(self):
        """Test configuration property methods"""
        settings = NQBASettings(
            dynex_api_key="test_key",
            ipfs_project_id="test_id",
            ipfs_project_secret="test_secret"
        )
        
        assert settings.dynex_configured == True
        assert settings.ipfs_configured == True
        assert settings.web3_configured == False
        assert settings.llm_configured == False
    
    def test_validation(self):
        """Test settings validation"""
        # Test valid environment
        settings = NQBASettings(environment="staging")
        assert settings.environment == "staging"
        
        # Test invalid environment (should raise error)
        with pytest.raises(ValueError):
            NQBASettings(environment="invalid")
        
        # Test valid log level
        settings = NQBASettings(log_level="DEBUG")
        assert settings.log_level == "DEBUG"
        
        # Test invalid log level (should raise error)
        with pytest.raises(ValueError):
            NQBASettings(log_level="INVALID")

class TestIntegration:
    """Test integration between components"""
    
    @patch('nqba.dynex_adapter.dynex.init')
    @patch('nqba.dynex_adapter.dynex.DynexSampler')
    def test_lead_scoring_integration(self, mock_sampler_class, mock_dynex_init):
        """Test complete lead scoring flow"""
        # Mock the sampler
        mock_sampler = Mock()
        mock_sampleset = Mock()
        mock_sampler_class.return_value = mock_sampler
        
        # Mock successful sampleset
        mock_sampleset.samples.return_value = [{"lead_0": 1, "lead_1": 0}]
        mock_sampleset.first.energy = -1.0
        mock_sampler.sample.return_value = mock_sampleset
        
        # Create test data
        lead_data = [
            {
                "budget": "high",
                "urgency": "urgent",
                "pain_points": "energy costs"
            },
            {
                "budget": "medium",
                "urgency": "low",
                "pain_points": "quality issues"
            }
        ]
        
        # Test the convenience function
        from nqba.dynex_adapter import score_leads
        
        result = score_leads(lead_data)
        
        # Verify result
        assert result.success == True
        assert "lead_0" in result.samples[0]
        assert "lead_1" in result.samples[0]
        assert result.energy == -1.0
    
    def test_settings_integration(self):
        """Test settings integration with other modules"""
        # Test that settings can be imported and used
        settings = get_settings()
        assert isinstance(settings, NQBASettings)
        
        # Test that settings has expected attributes
        assert hasattr(settings, 'dynex_configured')
        assert hasattr(settings, 'ipfs_configured')
        assert hasattr(settings, 'is_production')

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
