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
        # TODO: Initialize DynexSDK client here

        """
        Submit QUBO to Dynex and return result (stub)
        - qubo: QUBO matrix or problem
        - algorithm: QAOA, VQE, custom, etc.
        - parameters: algorithm-specific params
        """

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
        import dimod
        import dynex

        logger.info(f"Submitting QUBO to Dynex: algo={algorithm}, params={parameters}")
        # Accept either a BQM or a dict for QUBO
        if isinstance(qubo, dict):
            linear = qubo.get("linear", {})
            quadratic = qubo.get("quadratic", {})
            offset = qubo.get("offset", 0.0)
            bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, dimod.BINARY)
        else:
            bqm = qubo
        num_reads = parameters.get("num_reads", 1000) if parameters else 1000
        annealing_time = parameters.get("annealing_time", 100) if parameters else 100
        description = (
            parameters.get("description", "DynexClient QUBO job")
            if parameters
            else "DynexClient QUBO job"
        )
        # Initialize DynexSampler with proper model parameter
        try:
            # Try with model parameter (newer Dynex SDK versions)
            sampler = dynex.DynexSampler(
                model="dynex", mainnet=True, description=description
            )
        except TypeError:
            # Fallback for older versions without model parameter
            sampler = dynex.DynexSampler(mainnet=True, description=description)
        sampleset = await asyncio.to_thread(
            sampler.sample, bqm, annealing_time=annealing_time
        )
        samples = [dict(s) for s in sampleset.samples()]
        energies = [e for e in sampleset.record.energy]
        return {
            "samples": samples,
            "energies": energies,
            "first_sample": samples[0] if samples else {},
            "first_energy": energies[0] if energies else None,
            "job_id": getattr(sampleset, "job_id", None),
            "parameters": parameters,
        }


# Singleton for handler use
_dynex_client = DynexClient()


def get_dynex_client():
    return _dynex_client
