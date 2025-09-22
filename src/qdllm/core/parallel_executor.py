"""Parallel Executor for qdLLM Platform

This module provides parallel execution capabilities for quantum-enhanced operations,
including batch processing, distributed computing, and resource management.

Author: qdLLM Team
Version: 1.0.0
"""

import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union, Tuple
from enum import Enum
import multiprocessing as mp
import threading
from queue import Queue, Empty
import uuid
import psutil
import numpy as np


class ExecutionMode(Enum):
    """Execution modes for parallel processing"""
    THREAD = "thread"
    PROCESS = "process"
    ASYNC = "async"
    HYBRID = "hybrid"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionTask:
    """Represents a task for parallel execution"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    function: Callable = None
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM
    timeout: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.task_id is None:
            self.task_id = str(uuid.uuid4())

    @property
    def execution_time(self) -> Optional[float]:
        """Calculate task execution time"""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None

    @property
    def total_time(self) -> Optional[float]:
        """Calculate total time from creation to completion"""
        if self.completed_at:
            return self.completed_at - self.created_at
        return None


@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    batch_size: int = 10
    max_concurrent_batches: int = 4
    timeout_per_batch: Optional[float] = None
    retry_failed_tasks: bool = True
    preserve_order: bool = False
    chunk_strategy: str = "size"  # "size" or "count"
    progress_callback: Optional[Callable] = None


@dataclass
class ExecutorConfig:
    """Configuration for parallel executor"""
    max_workers: Optional[int] = None
    execution_mode: ExecutionMode = ExecutionMode.HYBRID
    enable_monitoring: bool = True
    log_level: str = "INFO"
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    queue_size: int = 1000
    heartbeat_interval: float = 5.0


@dataclass
class ExecutionMetrics:
    """Metrics for execution monitoring"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    cancelled_tasks: int = 0
    average_execution_time: float = 0.0
    peak_memory_usage: float = 0.0
    cpu_utilization: float = 0.0
    throughput: float = 0.0  # tasks per second
    error_rate: float = 0.0
    queue_size: int = 0
    active_workers: int = 0


class ResourceMonitor:
    """Monitor system resources during execution"""
    
    def __init__(self):
        self.process = psutil.Process()
        self.initial_memory = self.process.memory_info().rss
        self.peak_memory = self.initial_memory
        self.cpu_samples = []
        self.monitoring = False
        self._monitor_thread = None
    
    def start_monitoring(self, interval: float = 1.0):
        """Start resource monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2.0)
    
    def _monitor_loop(self, interval: float):
        """Resource monitoring loop"""
        while self.monitoring:
            try:
                # Memory monitoring
                current_memory = self.process.memory_info().rss
                self.peak_memory = max(self.peak_memory, current_memory)
                
                # CPU monitoring
                cpu_percent = self.process.cpu_percent()
                self.cpu_samples.append(cpu_percent)
                
                # Keep only recent samples
                if len(self.cpu_samples) > 60:  # Keep 1 minute of samples
                    self.cpu_samples.pop(0)
                
                time.sleep(interval)
            except Exception as e:
                logging.warning(f"Resource monitoring error: {e}")
    
    def get_metrics(self) -> Dict[str, float]:
        """Get current resource metrics"""
        current_memory = self.process.memory_info().rss
        avg_cpu = np.mean(self.cpu_samples) if self.cpu_samples else 0.0
        
        return {
            "current_memory_mb": current_memory / (1024 * 1024),
            "peak_memory_mb": self.peak_memory / (1024 * 1024),
            "memory_increase_mb": (current_memory - self.initial_memory) / (1024 * 1024),
            "avg_cpu_percent": avg_cpu,
            "current_cpu_percent": self.process.cpu_percent()
        }


class ParallelExecutor:
    """Advanced parallel executor for qdLLM operations"""
    
    def __init__(self, config: Optional[ExecutorConfig] = None):
        self.config = config or ExecutorConfig()
        self.logger = self._setup_logging()
        
        # Execution resources
        self.thread_executor = None
        self.process_executor = None
        self.task_queue = Queue(maxsize=self.config.queue_size)
        self.result_queue = Queue()
        
        # State management
        self.tasks: Dict[str, ExecutionTask] = {}
        self.metrics = ExecutionMetrics()
        self.resource_monitor = ResourceMonitor()
        self.running = False
        self.worker_threads = []
        
        # Synchronization
        self.lock = threading.RLock()
        self.shutdown_event = threading.Event()
        
        # Initialize executors
        self._initialize_executors()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the executor"""
        logger = logging.getLogger(f"ParallelExecutor-{id(self)}")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_executors(self):
        """Initialize thread and process executors"""
        max_workers = self.config.max_workers or min(32, (mp.cpu_count() or 1) + 4)
        
        if self.config.execution_mode in [ExecutionMode.THREAD, ExecutionMode.HYBRID]:
            self.thread_executor = ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix="qdLLM-Thread"
            )
        
        if self.config.execution_mode in [ExecutionMode.PROCESS, ExecutionMode.HYBRID]:
            self.process_executor = ProcessPoolExecutor(
                max_workers=min(max_workers, mp.cpu_count() or 1)
            )
    
    def start(self):
        """Start the parallel executor"""
        if self.running:
            return
        
        self.running = True
        self.shutdown_event.clear()
        
        # Start resource monitoring
        if self.config.enable_monitoring:
            self.resource_monitor.start_monitoring()
        
        # Start worker threads for async execution
        for i in range(min(4, mp.cpu_count() or 1)):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"qdLLM-Worker-{i}",
                daemon=True
            )
            worker.start()
            self.worker_threads.append(worker)
        
        # Start metrics update thread
        metrics_thread = threading.Thread(
            target=self._metrics_loop,
            name="qdLLM-Metrics",
            daemon=True
        )
        metrics_thread.start()
        self.worker_threads.append(metrics_thread)
        
        self.logger.info(f"ParallelExecutor started with {len(self.worker_threads)} workers")
    
    def stop(self, timeout: float = 30.0):
        """Stop the parallel executor"""
        if not self.running:
            return
        
        self.logger.info("Stopping ParallelExecutor...")
        self.running = False
        self.shutdown_event.set()
        
        # Stop resource monitoring
        self.resource_monitor.stop_monitoring()
        
        # Shutdown executors
        if self.thread_executor:
            self.thread_executor.shutdown(wait=True, timeout=timeout/2)
        
        if self.process_executor:
            self.process_executor.shutdown(wait=True, timeout=timeout/2)
        
        # Wait for worker threads
        for worker in self.worker_threads:
            worker.join(timeout=1.0)
        
        self.logger.info("ParallelExecutor stopped")
    
    def submit_task(self, 
                   function: Callable,
                   *args,
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   timeout: Optional[float] = None,
                   max_retries: int = 3,
                   metadata: Optional[Dict[str, Any]] = None,
                   **kwargs) -> str:
        """Submit a task for execution"""
        task = ExecutionTask(
            function=function,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout=timeout,
            max_retries=max_retries,
            metadata=metadata or {}
        )
        
        with self.lock:
            self.tasks[task.task_id] = task
            self.metrics.total_tasks += 1
        
        try:
            self.task_queue.put(task, timeout=1.0)
            self.logger.debug(f"Task {task.task_id} submitted")
        except Exception as e:
            with self.lock:
                task.status = TaskStatus.FAILED
                task.error = e
                self.metrics.failed_tasks += 1
            self.logger.error(f"Failed to submit task {task.task_id}: {e}")
        
        return task.task_id
    
    def submit_batch(self, 
                    tasks: List[Tuple[Callable, Tuple, Dict]],
                    config: Optional[BatchConfig] = None) -> List[str]:
        """Submit a batch of tasks for execution"""
        batch_config = config or BatchConfig()
        task_ids = []
        
        for func, args, kwargs in tasks:
            task_id = self.submit_task(
                func, *args,
                priority=TaskPriority.MEDIUM,
                **kwargs
            )
            task_ids.append(task_id)
        
        return task_ids
    
    async def execute_async_batch(self,
                                 tasks: List[Tuple[Callable, Tuple, Dict]],
                                 config: Optional[BatchConfig] = None) -> List[Any]:
        """Execute a batch of tasks asynchronously"""
        batch_config = config or BatchConfig()
        
        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(batch_config.max_concurrent_batches)
        
        async def execute_task(func, args, kwargs):
            async with semaphore:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(
                    self.thread_executor,
                    lambda: func(*args, **kwargs)
                )
        
        # Create coroutines for all tasks
        coroutines = [
            execute_task(func, args, kwargs)
            for func, args, kwargs in tasks
        ]
        
        # Execute with progress tracking
        if batch_config.progress_callback:
            results = []
            for i, coro in enumerate(asyncio.as_completed(coroutines)):
                result = await coro
                results.append(result)
                batch_config.progress_callback(i + 1, len(coroutines))
            return results
        else:
            return await asyncio.gather(*coroutines, return_exceptions=True)
    
    def get_task_status(self, task_id: str) -> Optional[ExecutionTask]:
        """Get the status of a specific task"""
        with self.lock:
            return self.tasks.get(task_id)
    
    def get_task_result(self, task_id: str, timeout: Optional[float] = None) -> Any:
        """Get the result of a completed task"""
        start_time = time.time()
        
        while True:
            with self.lock:
                task = self.tasks.get(task_id)
                if not task:
                    raise ValueError(f"Task {task_id} not found")
                
                if task.status == TaskStatus.COMPLETED:
                    return task.result
                elif task.status == TaskStatus.FAILED:
                    raise task.error or Exception(f"Task {task_id} failed")
                elif task.status == TaskStatus.CANCELLED:
                    raise Exception(f"Task {task_id} was cancelled")
            
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(f"Timeout waiting for task {task_id}")
            
            time.sleep(0.1)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or running task"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                task.status = TaskStatus.CANCELLED
                self.metrics.cancelled_tasks += 1
                self.logger.info(f"Task {task_id} cancelled")
                return True
            
            return False
    
    def get_metrics(self) -> ExecutionMetrics:
        """Get current execution metrics"""
        with self.lock:
            # Update queue size
            self.metrics.queue_size = self.task_queue.qsize()
            
            # Update resource metrics
            if self.config.enable_monitoring:
                resource_metrics = self.resource_monitor.get_metrics()
                self.metrics.peak_memory_usage = resource_metrics["peak_memory_mb"]
                self.metrics.cpu_utilization = resource_metrics["avg_cpu_percent"]
            
            # Calculate error rate
            if self.metrics.total_tasks > 0:
                self.metrics.error_rate = self.metrics.failed_tasks / self.metrics.total_tasks
            
            return self.metrics
    
    def _worker_loop(self):
        """Main worker loop for processing tasks"""
        while self.running and not self.shutdown_event.is_set():
            try:
                task = self.task_queue.get(timeout=1.0)
                self._execute_task(task)
                self.task_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Worker error: {e}")
    
    def _execute_task(self, task: ExecutionTask):
        """Execute a single task"""
        with self.lock:
            task.status = TaskStatus.RUNNING
            task.started_at = time.time()
        
        try:
            # Choose execution method based on configuration
            if self.config.execution_mode == ExecutionMode.ASYNC:
                # For async tasks, run in thread executor
                future = self.thread_executor.submit(
                    task.function, *task.args, **task.kwargs
                )
            elif self.config.execution_mode == ExecutionMode.PROCESS:
                # For CPU-intensive tasks, use process executor
                future = self.process_executor.submit(
                    task.function, *task.args, **task.kwargs
                )
            else:
                # Default to thread execution
                future = self.thread_executor.submit(
                    task.function, *task.args, **task.kwargs
                )
            
            # Wait for result with timeout
            result = future.result(timeout=task.timeout)
            
            with self.lock:
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = time.time()
                self.metrics.completed_tasks += 1
            
            self.logger.debug(f"Task {task.task_id} completed successfully")
            
        except Exception as e:
            with self.lock:
                task.error = e
                task.completed_at = time.time()
                
                # Retry logic
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.PENDING
                    task.started_at = None
                    
                    # Re-queue the task
                    try:
                        self.task_queue.put(task, timeout=1.0)
                        self.logger.info(f"Task {task.task_id} retry {task.retry_count}/{task.max_retries}")
                    except Exception:
                        task.status = TaskStatus.FAILED
                        self.metrics.failed_tasks += 1
                else:
                    task.status = TaskStatus.FAILED
                    self.metrics.failed_tasks += 1
                    self.logger.error(f"Task {task.task_id} failed after {task.retry_count} retries: {e}")
    
    def _metrics_loop(self):
        """Update metrics periodically"""
        while self.running and not self.shutdown_event.is_set():
            try:
                with self.lock:
                    # Calculate average execution time
                    completed_tasks = [
                        task for task in self.tasks.values()
                        if task.status == TaskStatus.COMPLETED and task.execution_time
                    ]
                    
                    if completed_tasks:
                        total_time = sum(task.execution_time for task in completed_tasks)
                        self.metrics.average_execution_time = total_time / len(completed_tasks)
                    
                    # Calculate throughput (tasks per second)
                    if self.metrics.completed_tasks > 0:
                        runtime = time.time() - min(
                            task.created_at for task in self.tasks.values()
                        )
                        if runtime > 0:
                            self.metrics.throughput = self.metrics.completed_tasks / runtime
                    
                    # Update active workers count
                    self.metrics.active_workers = len([
                        t for t in self.worker_threads if t.is_alive()
                    ])
                
                time.sleep(self.config.heartbeat_interval)
            except Exception as e:
                self.logger.error(f"Metrics update error: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


# Utility functions for common parallel operations

def parallel_map(func: Callable, 
                items: List[Any],
                max_workers: Optional[int] = None,
                execution_mode: ExecutionMode = ExecutionMode.THREAD) -> List[Any]:
    """Parallel map function using the executor"""
    config = ExecutorConfig(
        max_workers=max_workers,
        execution_mode=execution_mode
    )
    
    with ParallelExecutor(config) as executor:
        tasks = [(func, (item,), {}) for item in items]
        task_ids = executor.submit_batch(tasks)
        
        results = []
        for task_id in task_ids:
            try:
                result = executor.get_task_result(task_id, timeout=60.0)
                results.append(result)
            except Exception as e:
                results.append(e)
        
        return results


async def async_parallel_map(func: Callable,
                            items: List[Any],
                            max_concurrent: int = 10) -> List[Any]:
    """Async parallel map function"""
    config = ExecutorConfig(execution_mode=ExecutionMode.ASYNC)
    batch_config = BatchConfig(max_concurrent_batches=max_concurrent)
    
    with ParallelExecutor(config) as executor:
        tasks = [(func, (item,), {}) for item in items]
        return await executor.execute_async_batch(tasks, batch_config)


def parallel_reduce(func: Callable,
                   items: List[Any],
                   initial: Any = None,
                   chunk_size: int = 100) -> Any:
    """Parallel reduce operation"""
    if not items:
        return initial
    
    # Split items into chunks
    chunks = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
    
    # Reduce each chunk in parallel
    def reduce_chunk(chunk):
        result = initial
        for item in chunk:
            result = func(result, item) if result is not None else item
        return result
    
    chunk_results = parallel_map(reduce_chunk, chunks)
    
    # Final reduce of chunk results
    final_result = initial
    for result in chunk_results:
        if isinstance(result, Exception):
            raise result
        final_result = func(final_result, result) if final_result is not None else result
    
    return final_result


# Example usage and testing
if __name__ == "__main__":
    import random
    
    def sample_task(x: int, delay: float = 0.1) -> int:
        """Sample task for testing"""
        time.sleep(delay)
        if random.random() < 0.1:  # 10% failure rate
            raise ValueError(f"Random failure for {x}")
        return x * x
    
    # Test basic execution
    config = ExecutorConfig(
        max_workers=4,
        execution_mode=ExecutionMode.HYBRID,
        enable_monitoring=True
    )
    
    with ParallelExecutor(config) as executor:
        # Submit individual tasks
        task_ids = []
        for i in range(20):
            task_id = executor.submit_task(
                sample_task,
                i,
                delay=random.uniform(0.05, 0.2),
                priority=TaskPriority.HIGH if i % 5 == 0 else TaskPriority.MEDIUM
            )
            task_ids.append(task_id)
        
        # Wait for results
        results = []
        for task_id in task_ids:
            try:
                result = executor.get_task_result(task_id, timeout=10.0)
                results.append(result)
                print(f"Task {task_id}: {result}")
            except Exception as e:
                print(f"Task {task_id} failed: {e}")
                results.append(None)
        
        # Print metrics
        metrics = executor.get_metrics()
        print(f"\nExecution Metrics:")
        print(f"Total tasks: {metrics.total_tasks}")
        print(f"Completed: {metrics.completed_tasks}")
        print(f"Failed: {metrics.failed_tasks}")
        print(f"Average execution time: {metrics.average_execution_time:.3f}s")
        print(f"Throughput: {metrics.throughput:.2f} tasks/sec")
        print(f"Error rate: {metrics.error_rate:.2%}")
        print(f"Peak memory: {metrics.peak_memory_usage:.1f} MB")
        print(f"CPU utilization: {metrics.cpu_utilization:.1f}%")
    
    # Test parallel map
    print("\nTesting parallel_map:")
    numbers = list(range(10))
    squared = parallel_map(lambda x: x * x, numbers, max_workers=4)
    print(f"Squared: {squared}")
    
    # Test parallel reduce
    print("\nTesting parallel_reduce:")
    total = parallel_reduce(lambda a, b: a + b, numbers, initial=0)
    print(f"Sum: {total}")