"""
Living Technical Codex (LTC) Logger

This module provides comprehensive logging and traceability for all NQBA operations,
creating a living record of decisions, executions, and outcomes for audit,
compliance, and learning purposes.
"""

import asyncio
import logging
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import threading
from queue import Queue
import os

logger = logging.getLogger(__name__)

@dataclass
class LTCEntry:
    """Single entry in the Living Technical Codex"""
    entry_id: str
    timestamp: str
    operation_type: str
    component: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    thread_id: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    execution_context: Optional[Dict[str, Any]] = None
    result_data: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    error_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    hash: Optional[str] = None
    parent_entry_id: Optional[str] = None
    child_entry_ids: Optional[List[str]] = None

@dataclass
class LTCConfig:
    """Configuration for LTC logging"""
    storage_path: str = "./ltc_storage"
    storage_format: str = "jsonl"  # jsonl, json, sqlite
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    max_entries_per_file: int = 10000
    compression_enabled: bool = True
    encryption_enabled: bool = False
    retention_days: int = 365
    async_writing: bool = True
    batch_size: int = 100
    flush_interval: float = 5.0  # seconds

class LTCLogger:
    """Living Technical Codex Logger for comprehensive traceability"""
    
    def __init__(self, config: Optional[LTCConfig] = None):
        """Initialize LTC logger
        
        Args:
            config: LTC configuration, uses defaults if None
        """
        self.config = config or LTCConfig()
        self.storage_path = Path(self.config.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize storage
        self.current_file = None
        self.current_file_entries = 0
        self.entry_counter = 0
        
        # Threading and async support
        self.write_queue = Queue()
        self.write_thread = None
        self.running = False
        
        # Start background writer if async writing is enabled
        if self.config.async_writing:
            self._start_background_writer()
        
        # Initialize current log file
        self._initialize_log_file()
        
        logger.info(f"LTC Logger initialized with storage path: {self.storage_path}")
    
    def _initialize_log_file(self):
        """Initialize the current log file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ltc_{timestamp}.jsonl"
        self.current_file = self.storage_path / filename
        self.current_file_entries = 0
        
        # Create file with header
        with open(self.current_file, 'w') as f:
            f.write(f"# LTC Log File: {filename}\n")
            f.write(f"# Created: {datetime.now().isoformat()}\n")
            f.write(f"# Format: JSON Lines\n\n")
    
    def _start_background_writer(self):
        """Start background thread for async writing"""
        self.running = True
        self.write_thread = threading.Thread(target=self._background_writer_loop, daemon=True)
        self.write_thread.start()
        logger.info("Background LTC writer started")
    
    def _background_writer_loop(self):
        """Background loop for processing write queue"""
        last_flush = time.time()
        batch = []
        
        while self.running:
            try:
                # Process queue with timeout
                try:
                    entry = self.write_queue.get(timeout=1.0)
                    batch.append(entry)
                except:
                    pass
                
                # Flush batch if conditions are met
                current_time = time.time()
                if (len(batch) >= self.config.batch_size or 
                    current_time - last_flush >= self.config.flush_interval):
                    
                    if batch:
                        self._write_entries_sync(batch)
                        batch = []
                        last_flush = current_time
                
            except Exception as e:
                logger.error(f"Background writer error: {e}")
                time.sleep(1)
        
        # Final flush
        if batch:
            self._write_entries_sync(batch)
    
    async def log_operation(self,
                           operation_type: str,
                           component: str,
                           user_id: Optional[str] = None,
                           session_id: Optional[str] = None,
                           input_data: Optional[Dict[str, Any]] = None,
                           execution_context: Optional[Dict[str, Any]] = None,
                           result_data: Optional[Dict[str, Any]] = None,
                           performance_metrics: Optional[Dict[str, Any]] = None,
                           error_data: Optional[Dict[str, Any]] = None,
                           metadata: Optional[Dict[str, Any]] = None,
                           parent_entry_id: Optional[str] = None) -> str:
        """Log an operation to the Living Technical Codex
        
        Args:
            operation_type: Type of operation (e.g., 'quantum_optimization', 'decision_making')
            component: Component performing the operation (e.g., 'quantum_adapter', 'decision_logic')
            user_id: User ID associated with the operation
            session_id: Session ID for the operation
            input_data: Input data for the operation
            execution_context: Context in which operation was executed
            result_data: Results from the operation
            performance_metrics: Performance measurements
            error_data: Error information if operation failed
            metadata: Additional metadata
            parent_entry_id: ID of parent operation if this is a child operation
            
        Returns:
            Entry ID for the logged operation
        """
        
        # Generate entry ID
        entry_id = str(uuid.uuid4())
        
        # Get current thread ID
        thread_id = str(threading.get_ident())
        
        # Create LTC entry
        entry = LTCEntry(
            entry_id=entry_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            operation_type=operation_type,
            component=component,
            user_id=user_id,
            session_id=session_id,
            thread_id=thread_id,
            input_data=input_data,
            execution_context=execution_context,
            result_data=result_data,
            performance_metrics=performance_metrics,
            error_data=error_data,
            metadata=metadata,
            parent_entry_id=parent_entry_id,
            child_entry_ids=[]
        )
        
        # Generate hash for integrity
        entry.hash = self._generate_entry_hash(entry)
        
        # Add to write queue or write directly
        if self.config.async_writing:
            self.write_queue.put(entry)
        else:
            await self._write_entry_async(entry)
        
        # Update parent entry if this is a child
        if parent_entry_id:
            await self._update_parent_entry(parent_entry_id, entry_id)
        
        logger.debug(f"Logged operation {operation_type} with ID: {entry_id}")
        return entry_id
    
    async def log_quantum_execution(self,
                                  operation: str,
                                  qubits: int,
                                  backend: str,
                                  execution_time: float,
                                  success: bool,
                                  **kwargs) -> str:
        """Log quantum execution details
        
        Args:
            operation: Quantum operation performed
            qubits: Number of qubits used
            backend: Quantum backend used
            execution_time: Execution time in seconds
            success: Whether operation succeeded
            **kwargs: Additional quantum-specific data
            
        Returns:
            Entry ID for the logged operation
        """
        
        performance_metrics = {
            "qubits_used": qubits,
            "execution_time": execution_time,
            "backend": backend,
            "success": success
        }
        
        metadata = {
            "quantum_operation": operation,
            "quantum_backend": backend,
            "qubit_count": qubits
        }
        
        if not success:
            error_data = {
                "error_type": "quantum_execution_failure",
                "backend": backend,
                "qubits": qubits
            }
        else:
            error_data = None
        
        return await self.log_operation(
            operation_type="quantum_execution",
            component="quantum_adapter",
            input_data={"operation": operation, "qubits": qubits, "backend": backend},
            result_data={"success": success},
            performance_metrics=performance_metrics,
            error_data=error_data,
            metadata=metadata,
            **kwargs
        )
    
    async def log_decision_making(self,
                                decision_type: str,
                                strategy_selected: str,
                                confidence_score: float,
                                reasoning: str,
                                **kwargs) -> str:
        """Log decision making process
        
        Args:
            decision_type: Type of decision made
            strategy_selected: Strategy that was selected
            confidence_score: Confidence in the decision (0.0-1.0)
            reasoning: Reasoning behind the decision
            **kwargs: Additional decision-specific data
            
        Returns:
            Entry ID for the logged operation
        """
        
        result_data = {
            "decision_type": decision_type,
            "strategy_selected": strategy_selected,
            "confidence_score": confidence_score,
            "reasoning": reasoning
        }
        
        metadata = {
            "decision_engine": "decision_logic",
            "decision_category": decision_type
        }
        
        return await self.log_operation(
            operation_type="decision_making",
            component="decision_logic",
            result_data=result_data,
            metadata=metadata,
            **kwargs
        )
    
    async def log_business_rule_execution(self,
                                        rule_id: str,
                                        rule_name: str,
                                        conditions_matched: bool,
                                        actions_executed: List[str],
                                        **kwargs) -> str:
        """Log business rule execution
        
        Args:
            rule_id: ID of the business rule
            rule_name: Name of the business rule
            conditions_matched: Whether rule conditions were met
            actions_executed: List of actions that were executed
            **kwargs: Additional rule-specific data
            
        Returns:
            Entry ID for the logged operation
        """
        
        input_data = {
            "rule_id": rule_id,
            "rule_name": rule_name,
            "conditions_matched": conditions_matched
        }
        
        result_data = {
            "actions_executed": actions_executed,
            "execution_success": len(actions_executed) > 0
        }
        
        metadata = {
            "business_rule_engine": "decision_logic",
            "rule_priority": kwargs.get("priority", "normal")
        }
        
        return await self.log_operation(
            operation_type="business_rule_execution",
            component="decision_logic",
            input_data=input_data,
            result_data=result_data,
            metadata=metadata,
            **kwargs
        )
    
    async def log_agent_interaction(self,
                                  agent_type: str,
                                  interaction_type: str,
                                  user_input: str,
                                  agent_response: str,
                                  processing_time: float,
                                  **kwargs) -> str:
        """Log AI agent interactions
        
        Args:
            agent_type: Type of agent (chatbot, voice, digital_human)
            interaction_type: Type of interaction (query, command, conversation)
            user_input: User's input
            agent_response: Agent's response
            processing_time: Time taken to process and respond
            **kwargs: Additional interaction-specific data
            
        Returns:
            Entry ID for the logged operation
        """
        
        input_data = {
            "agent_type": agent_type,
            "interaction_type": interaction_type,
            "user_input": user_input[:1000]  # Truncate long inputs
        }
        
        result_data = {
            "agent_response": agent_response[:1000],  # Truncate long responses
            "processing_time": processing_time
        }
        
        performance_metrics = {
            "processing_time": processing_time,
            "input_length": len(user_input),
            "response_length": len(agent_response)
        }
        
        metadata = {
            "ai_agent": agent_type,
            "interaction_category": interaction_type
        }
        
        return await self.log_operation(
            operation_type="agent_interaction",
            component=f"agent_{agent_type}",
            input_data=input_data,
            result_data=result_data,
            performance_metrics=performance_metrics,
            metadata=metadata,
            **kwargs
        )
    
    async def log_metric(self,
                        metric_name: str,
                        metric_value: float,
                        metric_context: Optional[Dict[str, Any]] = None,
                        **kwargs) -> str:
        """Log a performance or business metric
        
        Args:
            metric_name: Name of the metric
            metric_value: Value of the metric
            metric_context: Context for the metric
            **kwargs: Additional metric-specific data
            
        Returns:
            Entry ID for the logged operation
        """
        
        result_data = {
            "metric_name": metric_name,
            "metric_value": metric_value,
            "metric_context": metric_context or {}
        }
        
        metadata = {
            "metric_type": "performance" if "time" in metric_name.lower() else "business",
            "metric_category": kwargs.get("category", "general")
        }
        
        return await self.log_operation(
            operation_type="metric_logging",
            component="metrics_collector",
            result_data=result_data,
            metadata=metadata,
            **kwargs
        )
    
    async def _write_entry_async(self, entry: LTCEntry):
        """Write a single entry asynchronously"""
        try:
            # Check if we need to rotate the log file
            if (self.current_file_entries >= self.config.max_entries_per_file or
                self.current_file.stat().st_size >= self.config.max_file_size):
                self._rotate_log_file()
            
            # Write entry
            entry_json = json.dumps(asdict(entry), default=str)
            with open(self.current_file, 'a') as f:
                f.write(entry_json + '\n')
            
            self.current_file_entries += 1
            self.entry_counter += 1
            
        except Exception as e:
            logger.error(f"Failed to write LTC entry: {e}")
    
    def _write_entries_sync(self, entries: List[LTCEntry]):
        """Write multiple entries synchronously (for background writer)"""
        try:
            # Check if we need to rotate the log file
            if (self.current_file_entries >= self.config.max_entries_per_file or
                self.current_file.stat().st_size >= self.config.max_file_size):
                self._rotate_log_file()
            
            # Write all entries
            with open(self.current_file, 'a') as f:
                for entry in entries:
                    entry_json = json.dumps(asdict(entry), default=str)
                    f.write(entry_json + '\n')
                    self.current_file_entries += 1
                    self.entry_counter += 1
                    
        except Exception as e:
            logger.error(f"Failed to write LTC entries: {e}")
    
    def _rotate_log_file(self):
        """Rotate to a new log file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ltc_{timestamp}.jsonl"
        self.current_file = self.storage_path / filename
        self.current_file_entries = 0
        
        # Create new file with header
        with open(self.current_file, 'w') as f:
            f.write(f"# LTC Log File: {filename}\n")
            f.write(f"# Created: {datetime.now().isoformat()}\n")
            f.write(f"# Format: JSON Lines\n\n")
        
        logger.info(f"Rotated LTC log file to: {filename}")
    
    def _generate_entry_hash(self, entry: LTCEntry) -> str:
        """Generate hash for entry integrity"""
        # Create a copy without the hash field for hashing
        entry_dict = asdict(entry)
        entry_dict['hash'] = None
        
        # Convert to sorted JSON string for consistent hashing
        entry_json = json.dumps(entry_dict, sort_keys=True, default=str)
        
        # Generate SHA-256 hash
        return hashlib.sha256(entry_json.encode()).hexdigest()
    
    async def _update_parent_entry(self, parent_entry_id: str, child_entry_id: str):
        """Update parent entry with child entry ID"""
        # This would update the parent entry in the LTC storage
        # For now, just log the relationship
        logger.debug(f"Child entry {child_entry_id} linked to parent {parent_entry_id}")
    
    async def search_entries(self,
                           operation_type: Optional[str] = None,
                           component: Optional[str] = None,
                           user_id: Optional[str] = None,
                           session_id: Optional[str] = None,
                           start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None,
                           limit: int = 100) -> List[LTCEntry]:
        """Search for LTC entries based on criteria
        
        Args:
            operation_type: Filter by operation type
            component: Filter by component
            user_id: Filter by user ID
            session_id: Filter by session ID
            start_time: Start time for search range
            end_time: End time for search range
            limit: Maximum number of results
            
        Returns:
            List of matching LTC entries
        """
        
        # This is a simplified search implementation
        # In production, this would use a proper database or search engine
        
        results = []
        search_count = 0
        
        # Search through all log files
        for log_file in self.storage_path.glob("ltc_*.jsonl"):
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.startswith('#') or not line.strip():
                            continue
                        
                        try:
                            entry_data = json.loads(line.strip())
                            entry = LTCEntry(**entry_data)
                            
                            # Apply filters
                            if operation_type and entry.operation_type != operation_type:
                                continue
                            if component and entry.component != component:
                                continue
                            if user_id and entry.user_id != user_id:
                                continue
                            if session_id and entry.session_id != session_id:
                                continue
                            
                            # Time range filter
                            if start_time or end_time:
                                entry_time = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
                                if start_time and entry_time < start_time:
                                    continue
                                if end_time and entry_time > end_time:
                                    continue
                            
                            results.append(entry)
                            search_count += 1
                            
                            if search_count >= limit:
                                break
                                
                        except json.JSONDecodeError:
                            continue
                            
                if search_count >= limit:
                    break
                    
            except Exception as e:
                logger.warning(f"Error reading log file {log_file}: {e}")
                continue
        
        return results
    
    async def get_entry_by_id(self, entry_id: str) -> Optional[LTCEntry]:
        """Get a specific LTC entry by ID
        
        Args:
            entry_id: ID of the entry to retrieve
            
        Returns:
            LTC entry if found, None otherwise
        """
        
        # Search through all log files for the specific entry
        for log_file in self.storage_path.glob("ltc_*.jsonl"):
            try:
                with open(log_file, 'r') as f:
                    for line in f:
                        if line.startswith('#') or not line.strip():
                            continue
                        
                        try:
                            entry_data = json.loads(line.strip())
                            if entry_data.get('entry_id') == entry_id:
                                return LTCEntry(**entry_data)
                        except json.JSONDecodeError:
                            continue
                            
            except Exception as e:
                logger.warning(f"Error reading log file {log_file}: {e}")
                continue
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get LTC logging statistics
        
        Returns:
            Dictionary with LTC statistics
        """
        
        total_entries = self.entry_counter
        total_files = len(list(self.storage_path.glob("ltc_*.jsonl")))
        
        # Calculate storage size
        total_size = sum(f.stat().st_size for f in self.storage_path.glob("ltc_*.jsonl"))
        
        return {
            "total_entries": total_entries,
            "total_files": total_files,
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "current_file": str(self.current_file),
            "current_file_entries": self.current_file_entries,
            "background_writer_running": self.running,
            "write_queue_size": self.write_queue.qsize() if self.write_queue else 0
        }
    
    def shutdown(self):
        """Shutdown the LTC logger gracefully"""
        self.running = False
        
        if self.write_thread and self.write_thread.is_alive():
            self.write_thread.join(timeout=5.0)
        
        # Final flush of any remaining entries
        remaining_entries = []
        while not self.write_queue.empty():
            try:
                entry = self.write_queue.get_nowait()
                remaining_entries.append(entry)
            except:
                break
        
        if remaining_entries:
            self._write_entries_sync(remaining_entries)
        
        logger.info("LTC Logger shutdown complete")
