"""
Living Technical Codex (LTC) Logger
Comprehensive logging and traceability for all NQBA operations
Provides audit, compliance, and learning capabilities
"""
import json
import logging
import hashlib
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import threading
from dataclasses import dataclass, asdict
import requests

from .settings import get_settings

logger = logging.getLogger(__name__)

@dataclass
class LTCOperation:
    """LTC Operation record"""
    operation_id: str
    operation_type: str
    operation_data: Dict[str, Any]
    thread_ref: str
    timestamp: datetime
    hash_chain: str
    ipfs_reference: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class LTCLogger:
    """Living Technical Codex Logger"""
    
    def __init__(self):
        """Initialize LTC Logger"""
        self.settings = get_settings()
        self.db_path = self.settings.data_dir / "ltc_operations.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Thread safety
        self.lock = threading.Lock()
        
        # Initialize database
        self._initialize_database()
        
        # Hash chain for integrity
        self.last_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        
        logger.info("LTC Logger initialized successfully")
    
    def _initialize_database(self):
        """Initialize SQLite database for LTC operations"""
        with self.lock:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Create operations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ltc_operations (
                    operation_id TEXT PRIMARY KEY,
                    operation_type TEXT NOT NULL,
                    operation_data TEXT NOT NULL,
                    thread_ref TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    hash_chain TEXT NOT NULL,
                    ipfs_reference TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for efficient querying
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_operation_type 
                ON ltc_operations(operation_type)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON ltc_operations(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_thread_ref 
                ON ltc_operations(thread_ref)
            """)
            
            conn.commit()
            conn.close()
    
    def _generate_operation_id(self, operation_type: str, thread_ref: str) -> str:
        """Generate unique operation ID"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{operation_type}_{thread_ref}_{timestamp}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:16]
    
    def _update_hash_chain(self, operation_data: Dict[str, Any]) -> str:
        """Update hash chain for integrity verification"""
        data_string = json.dumps(operation_data, sort_keys=True, default=str)
        combined = f"{self.last_hash}{data_string}"
        new_hash = hashlib.sha256(combined.encode()).hexdigest()
        self.last_hash = new_hash
        return new_hash
    
    def log_operation(self, 
                     operation_type: str, 
                     operation_data: Dict[str, Any], 
                     thread_ref: str,
                     metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Log an operation to the Living Technical Codex
        
        Args:
            operation_type: Type of operation (e.g., 'task_submitted', 'qubo_optimization')
            operation_data: Operation data dictionary
            thread_ref: Thread reference for tracing
            metadata: Additional metadata
        
        Returns:
            Operation ID for reference
        """
        try:
            # Generate operation ID and hash chain
            operation_id = self._generate_operation_id(operation_type, thread_ref)
            hash_chain = self._update_hash_chain(operation_data)
            
            # Create LTC operation record
            ltc_operation = LTCOperation(
                operation_id=operation_id,
                operation_type=operation_type,
                operation_data=operation_data,
                thread_ref=thread_ref,
                timestamp=datetime.now(),
                hash_chain=hash_chain,
                metadata=metadata
            )
            
            # Store in database
            with self.lock:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO ltc_operations 
                    (operation_id, operation_type, operation_data, thread_ref, timestamp, hash_chain, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    operation_id,
                    operation_type,
                    json.dumps(operation_data),
                    thread_ref,
                    ltc_operation.timestamp.isoformat(),
                    hash_chain,
                    json.dumps(metadata) if metadata else None
                ))
                
                conn.commit()
                conn.close()
            
            # Log to standard logging
            logger.info(f"LTC Operation logged: {operation_type} - {operation_id}")
            
            # Attempt IPFS backup if configured
            if self.settings.ipfs_configured:
                try:
                    ipfs_ref = self._backup_to_ipfs(ltc_operation)
                    if ipfs_ref:
                        self._update_ipfs_reference(operation_id, ipfs_ref)
                except Exception as e:
                    logger.warning(f"IPFS backup failed: {e}")
            
            return operation_id
            
        except Exception as e:
            logger.error(f"Failed to log operation to LTC: {e}")
            # Return a fallback ID
            return f"fallback_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
    
    def _backup_to_ipfs(self, ltc_operation: LTCOperation) -> Optional[str]:
        """Backup operation to IPFS"""
        try:
            # Prepare data for IPFS
            ipfs_data = {
                "operation_id": ltc_operation.operation_id,
                "operation_type": ltc_operation.operation_type,
                "operation_data": ltc_operation.operation_data,
                "thread_ref": ltc_operation.thread_ref,
                "timestamp": ltc_operation.timestamp.isoformat(),
                "hash_chain": ltc_operation.hash_chain,
                "metadata": ltc_operation.metadata,
                "nqba_version": "1.0.0",
                "backup_timestamp": datetime.now().isoformat()
            }
            
            # Convert to JSON
            json_data = json.dumps(ipfs_data, indent=2)
            
            # Upload to IPFS via Infura
            headers = {
                'Authorization': f'Basic {self.settings.ipfs_project_id}:{self.settings.ipfs_project_secret}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f'{self.settings.ipfs_gateway_url}/api/v0/add',
                files={'file': ('ltc_operation.json', json_data, 'application/json')},
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('Hash')
            else:
                logger.warning(f"IPFS upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"IPFS backup error: {e}")
            return None
    
    def _update_ipfs_reference(self, operation_id: str, ipfs_reference: str):
        """Update IPFS reference in database"""
        try:
            with self.lock:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE ltc_operations 
                    SET ipfs_reference = ? 
                    WHERE operation_id = ?
                """, (ipfs_reference, operation_id))
                
                conn.commit()
                conn.close()
                
        except Exception as e:
            logger.error(f"Failed to update IPFS reference: {e}")
    
    def query_operations(self, 
                        operation_type: Optional[str] = None,
                        start_time: Optional[datetime] = None,
                        end_time: Optional[datetime] = None,
                        thread_ref: Optional[str] = None,
                        limit: int = 100) -> List[LTCOperation]:
        """
        Query LTC operations with filters
        
        Args:
            operation_type: Filter by operation type
            start_time: Filter operations after this time
            end_time: Filter operations before this time
            thread_ref: Filter by thread reference
            limit: Maximum number of results
        
        Returns:
            List of LTC operations
        """
        try:
            with self.lock:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                # Build query
                query = "SELECT * FROM ltc_operations WHERE 1=1"
                params = []
                
                if operation_type:
                    query += " AND operation_type = ?"
                    params.append(operation_type)
                
                if start_time:
                    query += " AND timestamp >= ?"
                    params.append(start_time.isoformat())
                
                if end_time:
                    query += " AND timestamp <= ?"
                    params.append(end_time.isoformat())
                
                if thread_ref:
                    query += " AND thread_ref = ?"
                    params.append(thread_ref)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert rows to LTCOperation objects
                operations = []
                for row in rows:
                    operation = LTCOperation(
                        operation_id=row[0],
                        operation_type=row[1],
                        operation_data=json.loads(row[2]),
                        thread_ref=row[3],
                        timestamp=datetime.fromisoformat(row[4]),
                        hash_chain=row[5],
                        ipfs_reference=row[6],
                        metadata=json.loads(row[7]) if row[7] else None
                    )
                    operations.append(operation)
                
                conn.close()
                return operations
                
        except Exception as e:
            logger.error(f"Failed to query LTC operations: {e}")
            return []
    
    def get_operation_by_id(self, operation_id: str) -> Optional[LTCOperation]:
        """Get operation by ID"""
        try:
            with self.lock:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM ltc_operations WHERE operation_id = ?
                """, (operation_id,))
                
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    return LTCOperation(
                        operation_id=row[0],
                        operation_type=row[1],
                        operation_data=json.loads(row[2]),
                        thread_ref=row[3],
                        timestamp=datetime.fromisoformat(row[4]),
                        hash_chain=row[5],
                        ipfs_reference=row[6],
                        metadata=json.loads(row[7]) if row[7] else None
                    )
                return None
                
        except Exception as e:
            logger.error(f"Failed to get operation by ID: {e}")
            return None
    
    def get_hash_chain_integrity(self) -> Dict[str, Any]:
        """Verify hash chain integrity"""
        try:
            with self.lock:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT operation_id, hash_chain, operation_data, timestamp
                    FROM ltc_operations 
                    ORDER BY timestamp ASC
                """)
                
                rows = cursor.fetchall()
                conn.close()
                
                # Verify hash chain
                verified_hash = "0000000000000000000000000000000000000000000000000000000000000000"
                integrity_issues = []
                
                for row in rows:
                    operation_id, stored_hash, operation_data, timestamp = row
                    
                    # Recalculate hash
                    data_string = json.dumps(json.loads(operation_data), sort_keys=True, default=str)
                    calculated_hash = hashlib.sha256(f"{verified_hash}{data_string}".encode()).hexdigest()
                    
                    if calculated_hash != stored_hash:
                        integrity_issues.append({
                            "operation_id": operation_id,
                            "expected_hash": calculated_hash,
                            "stored_hash": stored_hash,
                            "timestamp": timestamp
                        })
                    
                    verified_hash = calculated_hash
                
                return {
                    "total_operations": len(rows),
                    "integrity_verified": len(integrity_issues) == 0,
                    "integrity_issues": integrity_issues,
                    "last_verified_hash": verified_hash,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to verify hash chain integrity: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get LTC statistics"""
        try:
            with self.lock:
                conn = sqlite3.connect(str(self.db_path))
                cursor = conn.cursor()
                
                # Total operations
                cursor.execute("SELECT COUNT(*) FROM ltc_operations")
                total_operations = cursor.fetchone()[0]
                
                # Operations by type
                cursor.execute("""
                    SELECT operation_type, COUNT(*) 
                    FROM ltc_operations 
                    GROUP BY operation_type
                """)
                operations_by_type = dict(cursor.fetchall())
                
                # Recent activity (last 24 hours)
                yesterday = datetime.now() - timedelta(days=1)
                cursor.execute("""
                    SELECT COUNT(*) FROM ltc_operations 
                    WHERE timestamp >= ?
                """, (yesterday.isoformat(),))
                recent_operations = cursor.fetchone()[0]
                
                # IPFS backup status
                cursor.execute("""
                    SELECT COUNT(*) FROM ltc_operations 
                    WHERE ipfs_reference IS NOT NULL
                """)
                ipfs_backed_operations = cursor.fetchone()[0]
                
                conn.close()
                
                return {
                    "total_operations": total_operations,
                    "operations_by_type": operations_by_type,
                    "recent_operations_24h": recent_operations,
                    "ipfs_backed_operations": ipfs_backed_operations,
                    "ipfs_backup_rate": (ipfs_backed_operations / total_operations * 100) if total_operations > 0 else 0,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to get LTC statistics: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def export_operations(self, 
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None,
                         format: str = "json") -> Union[str, bytes]:
        """Export operations in specified format"""
        operations = self.query_operations(start_time=start_time, end_time=end_time, limit=10000)
        
        if format.lower() == "json":
            return json.dumps([asdict(op) for op in operations], indent=2, default=str)
        elif format.lower() == "csv":
            # Simple CSV export
            if not operations:
                return ""
            
            headers = ["operation_id", "operation_type", "thread_ref", "timestamp", "hash_chain"]
            csv_lines = [",".join(headers)]
            
            for op in operations:
                row = [
                    op.operation_id,
                    op.operation_type,
                    op.thread_ref,
                    op.timestamp.isoformat(),
                    op.hash_chain
                ]
                csv_lines.append(",".join(row))
            
            return "\n".join(csv_lines)
        else:
            raise ValueError(f"Unsupported export format: {format}")

# Global LTC Logger instance
ltc_logger = LTCLogger()

# Convenience functions
def get_ltc_logger() -> LTCLogger:
    """Get global LTC logger instance"""
    return ltc_logger

def log_operation(operation_type: str, 
                 operation_data: Dict[str, Any], 
                 thread_ref: str,
                 metadata: Optional[Dict[str, Any]] = None) -> str:
    """Log operation to LTC (convenience function)"""
    return ltc_logger.log_operation(operation_type, operation_data, thread_ref, metadata)
