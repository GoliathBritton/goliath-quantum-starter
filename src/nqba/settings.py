"""
NQBA Settings - Core module imports
Imports from nqba_stack.core.settings for compatibility
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "nqba_stack", "core"))

try:
    from settings import (
        NQBASettings,
        get_settings,
        is_production,
        is_development,
        is_testing,
    )
except ImportError:
    # Fallback if nqba_stack is not available
    from typing import Dict, Any, Optional
    from pathlib import Path

    class NQBASettings:
        """Fallback NQBASettings class"""

        def __init__(self):
            self.environment = "development"
            self.debug = False
            self.company_name = "NQBA Core"
            self.business_unit = "NQBA Core"
            self.dynex_api_key = None
            self.data_dir = Path("./data")
            self.log_dir = Path("./logs")
            self.cache_dir = Path("./cache")
            self.api_host = "0.0.0.0"
            self.api_port = 8000
            self.quantum_backend = "mock"

        def setup_directories(self):
            """Setup directories (fallback)"""
            pass

        def get_credential_status(self) -> Dict[str, str]:
            """Get credential status (fallback)"""
            return {
                "dynex": "not_configured",
                "ipfs": "not_configured",
                "web3": "not_configured",
                "llm": "not_configured",
            }

    def get_settings() -> NQBASettings:
        """Get settings instance (fallback)"""
        return NQBASettings()

    def is_production() -> bool:
        """Check if production (fallback)"""
        return False

    def is_development() -> bool:
        """Check if development (fallback)"""
        return True

    def is_testing() -> bool:
        """Check if testing (fallback)"""
        return False
