import concurrent.futures
import os
import psutil
import logging
from typing import List, Dict, Any
import numpy as np
from .optimization import parallel_qaoa_sync  # Assuming parallel_qaoa_sync is available

logger = logging.getLogger(__name__)

class ParallelManager:
    def __init__(self, max_workers: int = None, adaptive_scaling: bool = True):
        self.max_workers = max_workers or os.cpu_count()
        self.adaptive_scaling = adaptive_scaling
        self.performance_history = []

    def _determine_worker_count(self, num_tasks: int) -> int:
        if not self.adaptive_scaling:
            return self.max_workers
        
        # Dynamic scaling based on system resources and task count
        available_cores = os.cpu_count()
        available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB
        
        # Simple heuristic: max workers = min(available_cores, num_tasks, memory-limited)
        memory_per_task = 500  # Assume 500MB per task
        memory_limited = available_memory // memory_per_task
        
        workers = min(available_cores, num_tasks, max(1, int(memory_limited)))
        logger.info(f"Determined {workers} workers for {num_tasks} tasks")
        return workers

    def execute_parallel_qaoa(self, graph_matrices: List[np.ndarray], problem_type: str = "portfolio") -> List[Dict[str, Any]]:
        num_tasks = len(graph_matrices)
        num_workers = self._determine_worker_count(num_tasks)
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                # Split tasks into chunks for better load balancing
                chunk_size = max(1, num_tasks // num_workers)
                chunks = [graph_matrices[i:i + chunk_size] for i in range(0, num_tasks, chunk_size)]
                
                futures = [executor.submit(parallel_qaoa_sync, chunk, problem_type) for chunk in chunks]
                
                results = []
                for future in concurrent.futures.as_completed(futures):
                    chunk_results = future.result()
                    results.extend(chunk_results)
                
                return results
                
        except Exception as e:
            logger.error(f"Parallel execution failed: {str(e)}")
            raise

    def get_performance_stats(self) -> Dict[str, Any]:
        return {
            "max_workers": self.max_workers,
            "adaptive_scaling": self.adaptive_scaling,
            "history": self.performance_history
        }