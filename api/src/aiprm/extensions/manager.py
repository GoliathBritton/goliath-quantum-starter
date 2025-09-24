"""
Goliath of All Trade - AIPRM Extensions Manager
This module provides functionality for managing AIPRM extensions.
"""

from typing import Dict, List, Any, Optional
import logging
from .config import EXTENSION_CONFIG, DEFAULT_EXTENSION_SETTINGS

logger = logging.getLogger(__name__)

class ExtensionManager:
    """Manager for AIPRM extensions"""
    
    def __init__(self):
        self.extensions = EXTENSION_CONFIG
        self.enabled_extensions = {ext_id: ext.get("enabled_by_default", False) 
                                  for ext_id, ext in self.extensions.items()}
        self.extension_settings = {ext_id: {**DEFAULT_EXTENSION_SETTINGS, **ext.get("settings", {})}
                                  for ext_id, ext in self.extensions.items()}
    
    def get_all_extensions(self) -> List[Dict[str, Any]]:
        """Get all available extensions"""
        return [
            {
                "id": ext_id,
                "name": ext_data["name"],
                "description": ext_data["description"],
                "version": ext_data["version"],
                "author": ext_data["author"],
                "enabled": self.enabled_extensions.get(ext_id, False),
                "compatibility": ext_data.get("compatibility", ["default"]),
                "settings": self.extension_settings.get(ext_id, {})
            }
            for ext_id, ext_data in self.extensions.items()
        ]
    
    def get_extension(self, extension_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific extension by ID"""
        if extension_id not in self.extensions:
            return None
            
        ext_data = self.extensions[extension_id]
        return {
            "id": extension_id,
            "name": ext_data["name"],
            "description": ext_data["description"],
            "version": ext_data["version"],
            "author": ext_data["author"],
            "enabled": self.enabled_extensions.get(extension_id, False),
            "compatibility": ext_data.get("compatibility", ["default"]),
            "settings": self.extension_settings.get(extension_id, {})
        }
    
    def enable_extension(self, extension_id: str) -> bool:
        """Enable an extension"""
        if extension_id not in self.extensions:
            return False
            
        self.enabled_extensions[extension_id] = True
        logger.info(f"Extension {extension_id} enabled")
        return True
    
    def disable_extension(self, extension_id: str) -> bool:
        """Disable an extension"""
        if extension_id not in self.extensions:
            return False
            
        self.enabled_extensions[extension_id] = False
        logger.info(f"Extension {extension_id} disabled")
        return True
    
    def update_extension_settings(self, extension_id: str, settings: Dict[str, Any]) -> bool:
        """Update settings for an extension"""
        if extension_id not in self.extensions:
            return False
            
        current_settings = self.extension_settings.get(extension_id, {})
        self.extension_settings[extension_id] = {**current_settings, **settings}
        logger.info(f"Settings updated for extension {extension_id}")
        return True
    
    def get_enabled_extensions(self) -> List[Dict[str, Any]]:
        """Get all enabled extensions"""
        return [
            ext for ext in self.get_all_extensions()
            if ext["enabled"]
        ]
    
    def apply_extensions_to_prompt(self, prompt_text: str, 
                                  context: Dict[str, Any] = {}) -> str:
        """Apply enabled extensions to enhance a prompt"""
        enhanced_prompt = prompt_text
        
        # Apply each enabled extension's enhancements
        for ext_id, enabled in self.enabled_extensions.items():
            if not enabled:
                continue
                
            # In a real implementation, this would call extension-specific enhancement logic
            # For now, we'll just add some mock enhancements
            if ext_id == "quantum_prompt_enhancer" and "quantum" in context.get("categories", []):
                enhanced_prompt += "\n\nApply quantum computing principles to optimize the solution."
                
            elif ext_id == "energy_domain_knowledge" and "energy" in context.get("categories", []):
                enhanced_prompt += "\n\nIncorporate energy grid optimization and renewable integration concepts."
                
            elif ext_id == "financial_analysis_tools" and "finance" in context.get("categories", []):
                enhanced_prompt += "\n\nInclude financial risk assessment and portfolio optimization analysis."
                
            elif ext_id == "diversegy_integration" and "energy" in context.get("categories", []):
                enhanced_prompt += "\n\nConsider Diversegy partner data and energy plan recommendations."
        
        return enhanced_prompt

# Create a singleton instance
extension_manager = ExtensionManager()