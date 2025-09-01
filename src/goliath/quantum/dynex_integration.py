"""Dynex Integration - Blockchain integration and PoUW for FLYFOX AI Quantum Platform"""

import asyncio
import logging
import hashlib
import json
import time
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import aiohttp
import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

logger = logging.getLogger(__name__)

class DynexNetwork(Enum):
    """Dynex network types"""
    MAINNET = "mainnet"
    TESTNET = "testnet"
    DEVNET = "devnet"

class PoUWType(Enum):
    """Types of Proof of Useful Work"""
    QUBO_OPTIMIZATION = "qubo_optimization"
    QUANTUM_ML = "quantum_ml"
    CIRCUIT_OPTIMIZATION = "circuit_optimization"
    CRYPTOGRAPHIC_VERIFICATION = "cryptographic_verification"

@dataclass
class PoUWReceipt:
    """Proof of Useful Work receipt"""
    receipt_id: str
    work_type: PoUWType
    timestamp: float
    green_credits: int
    difficulty: float
    solution_hash: str
    metadata: Dict[str, Any]
    signature: Optional[str] = None

@dataclass
class DynexTransaction:
    """Dynex blockchain transaction"""
    tx_hash: str
    from_address: str
    to_address: str
    amount: float
    fee: float
    timestamp: float
    block_height: int
    confirmations: int
    status: str

class DynexAPI:
    """Dynex blockchain API integration"""
    
    def __init__(self, 
                 network: DynexNetwork = DynexNetwork.TESTNET,
                 api_key: Optional[str] = None,
                 wallet_address: Optional[str] = None):
        self.network = network
        self.api_key = api_key
        self.wallet_address = wallet_address
        
        # API endpoints
        self.base_url = self._get_base_url()
        self.session = None
        
        # PoUW tracking
        self.pow_receipts: List[PoUWReceipt] = []
        self.transaction_history: List[DynexTransaction] = []
        
        # Network status
        self.network_status = {
            "connected": False,
            "last_check": 0,
            "block_height": 0,
            "difficulty": 0.0
        }
        
        logger.info(f"Dynex API initialized for {network.value}")
    
    def _get_base_url(self) -> str:
        """Get base URL for the selected network"""
        if self.network == DynexNetwork.MAINNET:
            return "https://api.dynexcoin.org"
        elif self.network == DynexNetwork.TESTNET:
            return "https://testnet-api.dynexcoin.org"
        else:
            return "https://devnet-api.dynexcoin.org"
    
    async def connect(self) -> bool:
        """Connect to Dynex network"""
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession(
                    headers={"User-Agent": "Goliath-Quantum/1.0"}
                )
            
            # Test connection
            async with self.session.get(f"{self.base_url}/status") as response:
                if response.status == 200:
                    status_data = await response.json()
                    self.network_status.update({
                        "connected": True,
                        "last_check": time.time(),
                        "block_height": status_data.get("block_height", 0),
                        "difficulty": status_data.get("difficulty", 0.0)
                    })
                    logger.info("Connected to Dynex network")
                    return True
                else:
                    logger.error(f"Failed to connect to Dynex network: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Connection to Dynex network failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Dynex network"""
        if self.session:
            await self.session.close()
            self.session = None
        self.network_status["connected"] = False
        logger.info("Disconnected from Dynex network")
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        if not self.network_status["connected"]:
            await self.connect()
        
        return self.network_status.copy()
    
    async def submit_pouw(self, 
                          work_type: PoUWType,
                          solution_data: Dict[str, Any],
                          difficulty: float = 1.0) -> Optional[PoUWReceipt]:
        """Submit Proof of Useful Work to Dynex network"""
        try:
            if not self.network_status["connected"]:
                await self.connect()
            
            # Create PoUW receipt
            receipt = self._create_pouw_receipt(work_type, solution_data, difficulty)
            
            # Submit to network
            submission_result = await self._submit_to_network(receipt)
            
            if submission_result.get("success"):
                receipt.signature = submission_result.get("signature")
                self.pow_receipts.append(receipt)
                logger.info(f"PoUW submitted successfully: {receipt.receipt_id}")
                return receipt
            else:
                logger.error(f"PoUW submission failed: {submission_result.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"PoUW submission failed: {e}")
            return None
    
    async def verify_pouw(self, receipt_id: str) -> bool:
        """Verify a PoUW receipt on the blockchain"""
        try:
            if not self.network_status["connected"]:
                await self.connect()
            
            # Query blockchain for receipt
            verification_result = await self._query_blockchain_receipt(receipt_id)
            
            if verification_result.get("verified"):
                logger.info(f"PoUW verified: {receipt_id}")
                return True
            else:
                logger.warning(f"PoUW verification failed: {receipt_id}")
                return False
                
        except Exception as e:
            logger.error(f"PoUW verification failed: {e}")
            return False
    
    async def get_green_credits(self, address: Optional[str] = None) -> int:
        """Get green credits balance for an address"""
        try:
            target_address = address or self.wallet_address
            if not target_address:
                logger.error("No wallet address specified")
                return 0
            
            if not self.network_status["connected"]:
                await self.connect()
            
            # Query balance
            balance_result = await self._query_balance(target_address)
            
            if balance_result.get("success"):
                green_credits = balance_result.get("green_credits", 0)
                logger.info(f"Green credits balance: {green_credits}")
                return green_credits
            else:
                logger.error(f"Failed to get balance: {balance_result.get('error')}")
                return 0
                
        except Exception as e:
            logger.error(f"Failed to get green credits: {e}")
            return 0
    
    async def transfer_green_credits(self, 
                                   to_address: str, 
                                   amount: int,
                                   fee: int = 1) -> Optional[str]:
        """Transfer green credits to another address"""
        try:
            if not self.wallet_address:
                logger.error("No wallet address configured")
                return None
            
            if not self.network_status["connected"]:
                await self.connect()
            
            # Create transaction
            transaction = {
                "from_address": self.wallet_address,
                "to_address": to_address,
                "amount": amount,
                "fee": fee,
                "timestamp": time.time()
            }
            
            # Submit transaction
            tx_result = await self._submit_transaction(transaction)
            
            if tx_result.get("success"):
                tx_hash = tx_result.get("transaction_hash")
                logger.info(f"Transaction submitted: {tx_hash}")
                
                # Record transaction
                self._record_transaction(transaction, tx_hash)
                
                return tx_hash
            else:
                logger.error(f"Transaction failed: {tx_result.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return None
    
    async def get_transaction_status(self, tx_hash: str) -> Optional[DynexTransaction]:
        """Get status of a transaction"""
        try:
            if not self.network_status["connected"]:
                await self.connect()
            
            # Query transaction
            tx_result = await self._query_transaction(tx_hash)
            
            if tx_result.get("success"):
                tx_data = tx_result.get("transaction", {})
                transaction = DynexTransaction(
                    tx_hash=tx_hash,
                    from_address=tx_data.get("from_address", ""),
                    to_address=tx_data.get("to_address", ""),
                    amount=tx_data.get("amount", 0.0),
                    fee=tx_data.get("fee", 0.0),
                    timestamp=tx_data.get("timestamp", 0.0),
                    block_height=tx_data.get("block_height", 0),
                    confirmations=tx_data.get("confirmations", 0),
                    status=tx_data.get("status", "unknown")
                )
                return transaction
            else:
                logger.error(f"Failed to get transaction: {tx_result.get('error')}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get transaction status: {e}")
            return None
    
    def _create_pouw_receipt(self, 
                            work_type: PoUWType,
                            solution_data: Dict[str, Any],
                            difficulty: float) -> PoUWReceipt:
        """Create a PoUW receipt"""
        # Generate receipt ID
        receipt_id = hashlib.sha256(
            f"{work_type.value}_{time.time()}_{json.dumps(solution_data)}".encode()
        ).hexdigest()[:16]
        
        # Calculate green credits based on difficulty and work type
        base_credits = {
            PoUWType.QUBO_OPTIMIZATION: 100,
            PoUWType.QUANTUM_ML: 150,
            PoUWType.CIRCUIT_OPTIMIZATION: 80,
            PoUWType.CRYPTOGRAPHIC_VERIFICATION: 200
        }
        
        green_credits = int(base_credits.get(work_type, 100) * difficulty)
        
        # Create solution hash
        solution_hash = hashlib.sha256(
            json.dumps(solution_data, sort_keys=True).encode()
        ).hexdigest()
        
        receipt = PoUWReceipt(
            receipt_id=receipt_id,
            work_type=work_type,
            timestamp=time.time(),
            green_credits=green_credits,
            difficulty=difficulty,
            solution_hash=solution_hash,
            metadata=solution_data
        )
        
        return receipt
    
    async def _submit_to_network(self, receipt: PoUWReceipt) -> Dict[str, Any]:
        """Submit PoUW receipt to Dynex network"""
        try:
            if not self.session:
                return {"success": False, "error": "No active session"}
            
            # Prepare submission data
            submission_data = {
                "receipt_id": receipt.receipt_id,
                "work_type": receipt.work_type.value,
                "timestamp": receipt.timestamp,
                "green_credits": receipt.green_credits,
                "difficulty": receipt.difficulty,
                "solution_hash": receipt.solution_hash,
                "metadata": receipt.metadata
            }
            
            # Submit to network
            async with self.session.post(
                f"{self.base_url}/pouw/submit",
                json=submission_data,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {"success": True, "signature": result.get("signature")}
                else:
                    error_text = await response.text()
                    return {"success": False, "error": error_text}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _query_blockchain_receipt(self, receipt_id: str) -> Dict[str, Any]:
        """Query blockchain for PoUW receipt verification"""
        try:
            if not self.session:
                return {"verified": False, "error": "No active session"}
            
            async with self.session.get(
                f"{self.base_url}/pouw/verify/{receipt_id}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {"verified": result.get("verified", False)}
                else:
                    return {"verified": False, "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"verified": False, "error": str(e)}
    
    async def _query_balance(self, address: str) -> Dict[str, Any]:
        """Query balance for an address"""
        try:
            if not self.session:
                return {"success": False, "error": "No active session"}
            
            async with self.session.get(
                f"{self.base_url}/balance/{address}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "green_credits": result.get("green_credits", 0),
                        "dynex_coins": result.get("dynex_coins", 0.0)
                    }
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _submit_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a transaction to the network"""
        try:
            if not self.session:
                return {"success": False, "error": "No active session"}
            
            # Submit transaction
            async with self.session.post(
                f"{self.base_url}/transaction/submit",
                json=transaction,
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "transaction_hash": result.get("transaction_hash")
                    }
                else:
                    error_text = await response.text()
                    return {"success": False, "error": error_text}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _query_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Query transaction details"""
        try:
            if not self.session:
                return {"success": False, "error": "No active session"}
            
            async with self.session.get(
                f"{self.base_url}/transaction/{tx_hash}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return {"success": True, "transaction": result}
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _record_transaction(self, transaction: Dict[str, Any], tx_hash: str):
        """Record a transaction in local history"""
        tx_record = DynexTransaction(
            tx_hash=tx_hash,
            from_address=transaction["from_address"],
            to_address=transaction["to_address"],
            amount=transaction["amount"],
            fee=transaction["fee"],
            timestamp=transaction["timestamp"],
            block_height=0,  # Will be updated when confirmed
            confirmations=0,
            status="pending"
        )
        
        self.transaction_history.append(tx_record)
        
        # Keep only last 100 transactions
        if len(self.transaction_history) > 100:
            self.transaction_history.pop(0)
    
    def get_pouw_history(self) -> List[PoUWReceipt]:
        """Get PoUW submission history"""
        return self.pow_receipts.copy()
    
    def get_transaction_history(self) -> List[DynexTransaction]:
        """Get transaction history"""
        return self.transaction_history.copy()
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        return {
            "network": self.network.value,
            "base_url": self.base_url,
            "wallet_address": self.wallet_address,
            "connected": self.network_status["connected"],
            "last_check": self.network_status["last_check"],
            "block_height": self.network_status["block_height"],
            "difficulty": self.network_status["difficulty"]
        }

class DynexPoUWManager:
    """Manager for Proof of Useful Work operations"""
    
    def __init__(self, dynex_api: DynexAPI):
        self.dynex_api = dynex_api
        self.work_queue: List[Dict[str, Any]] = []
        self.completed_work: List[PoUWReceipt] = []
        
        logger.info("Dynex PoUW Manager initialized")
    
    async def submit_qubo_optimization(self, 
                                     qubo_matrix: np.ndarray,
                                     solution: np.ndarray,
                                     optimal_value: float,
                                     execution_time: float) -> Optional[PoUWReceipt]:
        """Submit QUBO optimization as PoUW"""
        try:
            # Prepare solution data
            solution_data = {
                "problem_type": "qubo_optimization",
                "matrix_size": qubo_matrix.shape[0],
                "solution": solution.tolist(),
                "optimal_value": optimal_value,
                "execution_time": execution_time,
                "difficulty_factor": self._calculate_difficulty_factor(qubo_matrix)
            }
            
            # Submit PoUW
            receipt = await self.dynex_api.submit_pouw(
                PoUWType.QUBO_OPTIMIZATION,
                solution_data,
                difficulty=solution_data["difficulty_factor"]
            )
            
            if receipt:
                self.completed_work.append(receipt)
                logger.info(f"QUBO optimization PoUW submitted: {receipt.receipt_id}")
            
            return receipt
            
        except Exception as e:
            logger.error(f"Failed to submit QUBO PoUW: {e}")
            return None
    
    async def submit_quantum_ml_work(self, 
                                   algorithm: str,
                                   data_shape: tuple,
                                   accuracy: float,
                                   training_time: float) -> Optional[PoUWReceipt]:
        """Submit quantum ML work as PoUW"""
        try:
            # Prepare solution data
            solution_data = {
                "problem_type": "quantum_ml",
                "algorithm": algorithm,
                "data_shape": data_shape,
                "accuracy": accuracy,
                "training_time": training_time,
                "difficulty_factor": self._calculate_ml_difficulty(data_shape, algorithm)
            }
            
            # Submit PoUW
            receipt = await self.dynex_api.submit_pouw(
                PoUWType.QUANTUM_ML,
                solution_data,
                difficulty=solution_data["difficulty_factor"]
            )
            
            if receipt:
                self.completed_work.append(receipt)
                logger.info(f"Quantum ML PoUW submitted: {receipt.receipt_id}")
            
            return receipt
            
        except Exception as e:
            logger.error(f"Failed to submit quantum ML PoUW: {e}")
            return None
    
    def _calculate_difficulty_factor(self, qubo_matrix: np.ndarray) -> float:
        """Calculate difficulty factor for QUBO optimization"""
        size = qubo_matrix.shape[0]
        sparsity = 1.0 - (np.count_nonzero(qubo_matrix) / (size * size))
        
        # Difficulty increases with size and sparsity
        difficulty = (size / 100.0) * (1.0 + sparsity)
        return min(difficulty, 10.0)  # Cap at 10.0
    
    def _calculate_ml_difficulty(self, data_shape: tuple, algorithm: str) -> float:
        """Calculate difficulty factor for quantum ML work"""
        data_size = np.prod(data_shape)
        
        # Algorithm-specific difficulty multipliers
        algorithm_multipliers = {
            "qsvm": 1.0,
            "qgan": 1.5,
            "vqe": 1.2,
            "qnn": 1.3
        }
        
        base_difficulty = (data_size / 1000.0) * algorithm_multipliers.get(algorithm, 1.0)
        return min(base_difficulty, 10.0)  # Cap at 10.0
    
    def get_work_statistics(self) -> Dict[str, Any]:
        """Get statistics about completed work"""
        if not self.completed_work:
            return {"total_work": 0}
        
        total_green_credits = sum(receipt.green_credits for receipt in self.completed_work)
        work_types = {}
        
        for receipt in self.completed_work:
            work_type = receipt.work_type.value
            work_types[work_type] = work_types.get(work_type, 0) + 1
        
        return {
            "total_work": len(self.completed_work),
            "total_green_credits": total_green_credits,
            "work_types": work_types,
            "average_difficulty": np.mean([receipt.difficulty for receipt in self.completed_work])
        }
