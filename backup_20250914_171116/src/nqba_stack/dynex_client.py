"""
Dynex Quantum Backend Client (Stub)
----------------------------------
- Submits QUBO problems to Dynex network
- Supports advanced algorithms (QAOA, VQE, custom)
- Reference: DynexSDK Advanced Examples
"""

import asyncio
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("dynex_client")


class DynexClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "demo"
        self.sampler = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize DynexSDK client with proper configuration."""
        try:
            import dynex
            logger.info("Initializing DynexSDK client...")
            
            # Try with model parameter (newer Dynex SDK versions)
            try:
                self.sampler = dynex.DynexSampler(
                    model="dynex", 
                    mainnet=True, 
                    description="NQBA Platform Quantum Client"
                )
                logger.info("DynexSDK client initialized successfully with model parameter")
            except TypeError:
                # Fallback for older versions without model parameter
                self.sampler = dynex.DynexSampler(
                    mainnet=True, 
                    description="NQBA Platform Quantum Client"
                )
                logger.info("DynexSDK client initialized successfully (legacy mode)")
                
        except ImportError:
            logger.warning("DynexSDK not available, using mock client")
            self.sampler = None
        except Exception as e:
            logger.error(f"Failed to initialize DynexSDK client: {e}")
            self.sampler = None

    # Legacy stub code removed; now uses real Dynex SDK above.
    async def submit_qubo(
        self, qubo: Any, algorithm: str = "qaoa", parameters: Optional[Dict] = None
    ) -> Dict:
        """
        Submit QUBO to Dynex and return result using the real SDK.
        - qubo: QUBO matrix or dimod.BinaryQuadraticModel
        - algorithm: QAOA, VQE, custom, etc. (currently ignored, DynexSampler used)
        - parameters: algorithm-specific params (num_reads, annealing_time, etc.)
        """
        logger.info(f"Submitting QUBO to Dynex: algo={algorithm}, params={parameters}")
        
        # Check if client is properly initialized
        if self.sampler is None:
            logger.warning("DynexSDK client not available, returning mock result")
            return self._mock_result(parameters)
        
        try:
            import dimod
            
            # Accept either a BQM or a dict for QUBO
            if isinstance(qubo, dict):
                linear = qubo.get("linear", {})
                quadratic = qubo.get("quadratic", {})
                offset = qubo.get("offset", 0.0)
                bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.BINARY)
            else:
                bqm = qubo
            
            # Extract parameters
            num_reads = parameters.get("num_reads", 1000) if parameters else 1000
            annealing_time = parameters.get("annealing_time", 100) if parameters else 100
            
            # Submit to Dynex using pre-initialized sampler
            sampleset = await asyncio.to_thread(
                self.sampler.sample, bqm, annealing_time=annealing_time
            )
            
            # Process results
            samples = [dict(s) for s in sampleset.samples()]
            energies = [e for e in sampleset.record.energy]
            
            result = {
                "samples": samples,
                "energies": energies,
                "first_sample": samples[0] if samples else {},
                "first_energy": energies[0] if energies else None,
                "job_id": getattr(sampleset, "job_id", None),
                "parameters": parameters,
                "status": "completed",
                "algorithm": algorithm
            }
            
            logger.info(f"QUBO submission completed successfully, job_id: {result.get('job_id')}")
            return result
            
        except Exception as e:
            logger.error(f"Error submitting QUBO to Dynex: {e}")
            return {
                "samples": [],
                "energies": [],
                "first_sample": {},
                "first_energy": None,
                "job_id": None,
                "parameters": parameters,
                "status": "error",
                "error": str(e),
                "algorithm": algorithm
            }
    
    def _mock_result(self, parameters: Optional[Dict] = None) -> Dict:
        """Return a mock result when DynexSDK is not available."""
        import random
        
        # Generate mock binary solution
        num_vars = 10  # Default number of variables
        mock_sample = {i: random.choice([0, 1]) for i in range(num_vars)}
        mock_energy = random.uniform(-100, 100)
        
        return {
            "samples": [mock_sample],
            "energies": [mock_energy],
            "first_sample": mock_sample,
            "first_energy": mock_energy,
            "job_id": f"mock_{random.randint(1000, 9999)}",
            "parameters": parameters,
            "status": "mock",
            "algorithm": "mock"
        }


# Singleton for handler use
_dynex_client = DynexClient()


def get_dynex_client():
    return _dynex_client
