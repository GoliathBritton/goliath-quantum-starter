#!/usr/bin/env python3
"""
Simple FastAPI test server for quantum algorithms
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# Import quantum algorithms
from src.quantum.reasoning import reversal_reasoning
from src.quantum.optimization import parallel_qaoa, optimize_qaoa
import numpy as np

app = FastAPI(
    title="Quantum Algorithms Test API",
    description="Test API for Goliath Quantum Algorithms",
    version="1.0.0"
)

# Pydantic models
class ReasoningInput(BaseModel):
    premise: str = Field(..., description="The premise for reasoning")
    conclusion: str = Field(..., description="The conclusion to evaluate")
    coherence_threshold: Optional[float] = Field(0.9, description="Coherence threshold")

class OptimizationInput(BaseModel):
    graph_matrices: List[List[List[float]]] = Field(..., description="List of 2D matrices")
    problem_type: Optional[str] = Field("portfolio", description="Problem type")
    num_workers: Optional[int] = Field(4, description="Number of workers")

class SingleOptimizationInput(BaseModel):
    graph_matrix: List[List[float]] = Field(..., description="2D matrix")
    problem_type: Optional[str] = Field("portfolio", description="Problem type")

@app.get("/")
async def root():
    return {
        "message": "Goliath Quantum Algorithms Test API",
        "status": "active",
        "algorithms": ["reversal_reasoning", "qaoa_optimization"]
    }

@app.post("/quantum/reasoning")
async def quantum_reasoning(input_data: ReasoningInput):
    """Test reversal reasoning algorithm"""
    try:
        result = reversal_reasoning(
            input_data.premise,
            input_data.conclusion,
            input_data.coherence_threshold
        )
        return {
            "success": True,
            "algorithm": "reversal_reasoning",
            "input": {
                "premise": input_data.premise,
                "conclusion": input_data.conclusion,
                "threshold": input_data.coherence_threshold
            },
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "algorithm": "reversal_reasoning"
        }

@app.post("/quantum/optimization/single")
async def single_optimization(input_data: SingleOptimizationInput):
    """Test single QAOA optimization"""
    try:
        # Convert list to numpy array
        graph_matrix = np.array(input_data.graph_matrix)
        params, cost = optimize_qaoa(graph_matrix)
        
        return {
            "success": True,
            "algorithm": "qaoa_single",
            "input": {
                "matrix_shape": graph_matrix.shape,
                "problem_type": input_data.problem_type
            },
            "result": {
                "optimized_parameters": params.tolist(),
                "final_cost": float(cost)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "algorithm": "qaoa_single"
        }

@app.post("/quantum/optimization/parallel")
async def parallel_optimization(input_data: OptimizationInput):
    """Test parallel QAOA optimization"""
    try:
        # Convert lists to numpy arrays
        graph_matrices = [np.array(matrix) for matrix in input_data.graph_matrices]
        results = parallel_qaoa(graph_matrices, input_data.num_workers)
        
        formatted_results = []
        for i, (params, cost) in enumerate(results):
            formatted_results.append({
                "matrix_index": i,
                "optimized_parameters": params.tolist(),
                "final_cost": float(cost)
            })
        
        return {
            "success": True,
            "algorithm": "qaoa_parallel",
            "input": {
                "num_matrices": len(graph_matrices),
                "num_workers": input_data.num_workers,
                "problem_type": input_data.problem_type
            },
            "results": formatted_results
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "algorithm": "qaoa_parallel"
        }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "quantum_algorithms": "operational",
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    print("Starting Quantum Algorithms Test API...")
    print("API Documentation: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)