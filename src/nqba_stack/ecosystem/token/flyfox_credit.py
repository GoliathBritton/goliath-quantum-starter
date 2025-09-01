#!/usr/bin/env python3
"""
🚀 FLYFOX Credit (FFC) - AI + Quantum Native Token

FLYFOX Credit is the utility token that powers the NQBA ecosystem,
enabling workflow execution, marketplace access, and ecosystem stickiness.
Built on Dynex blockchain integration with ESG-aligned burn mechanisms.
"""

import asyncio
import hashlib
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from decimal import Decimal

from ..core.ltc_automation import LTCLogger
from ..quantum.adapters.dynex_adapter import DynexAdapter
from ..core.quantum_digital_agents import QuantumDigitalAgent


class TokenType(Enum):
    """Types of FFC tokens"""
    WORKFLOW = "workflow"
    MARKETPLACE = "marketplace"
    PREMIUM = "premium"
    INSURANCE = "insurance"
    ESG = "esg"
    REWARD = "reward"


class TransactionType(Enum):
    """Types of FFC transactions"""
    MINT = "mint"
    BURN = "burn"
    TRANSFER = "transfer"
    WORKFLOW_EXECUTION = "workflow_execution"
    MARKETPLACE_ACCESS = "marketplace_access"
    PREMIUM_FEATURE = "premium_feature"
    INSURANCE_QUOTE = "insurance_quote"
    ESG_DONATION = "esg_donation"
    REWARD_DISTRIBUTION = "reward_distribution"


@dataclass
class FFCWallet:
    """FLYFOX Credit wallet"""
    wallet_id: str
    user_id: str
    balance: Decimal
    total_minted: Decimal
    total_burned: Decimal
    created_at: datetime
    last_updated: datetime
    is_active: bool
    metadata: Dict[str, Any]


@dataclass
class FFCTransaction:
    """FLYFOX Credit transaction record"""
    transaction_id: str
    from_wallet: str
    to_wallet: str
    amount: Decimal
    token_type: TokenType
    transaction_type: TransactionType
    timestamp: datetime
    ltc_hash: str
    quantum_signature: str
    metadata: Dict[str, Any]


@dataclass
class WorkflowPricing:
    """Pricing for workflow execution in FFC"""
    workflow_type: str
    base_cost: Decimal
    quantum_multiplier: float
    complexity_factor: float
    premium_features: List[str]
    ffc_cost: Decimal


class FlyfoxCredit:
    """
    FLYFOX Credit (FFC) Token System
    
    The utility token that powers the NQBA ecosystem, enabling:
    - Workflow execution and marketplace access
    - Premium features and insurance quotes
    - ESG-aligned burn mechanisms
    - Ecosystem stickiness and recurring revenue
    """
    
    def __init__(self):
        self.wallets: Dict[str, FFCWallet] = {}
        self.transactions: List[FFCTransaction] = []
        self.ltc_logger = LTCLogger()
        self.dynex_adapter = DynexAdapter()
        self.quantum_agent = QuantumDigitalAgent()
        
        # Token economics
        self.total_supply = Decimal("1000000000")  # 1 billion FFC
        self.circulating_supply = Decimal("0")
        self.burned_supply = Decimal("0")
        
        # Pricing configuration
        self.workflow_pricing = {
            "energy_optimization": WorkflowPricing(
                workflow_type="energy_optimization",
                base_cost=Decimal("10.0"),
                quantum_multiplier=1.5,
                complexity_factor=1.2,
                premium_features=["real_time_monitoring", "predictive_analytics"],
                ffc_cost=Decimal("18.0")
            ),
            "portfolio_optimization": WorkflowPricing(
                workflow_type="portfolio_optimization",
                base_cost=Decimal("25.0"),
                quantum_multiplier=2.0,
                complexity_factor=1.5,
                premium_features=["risk_assessment", "market_analysis"],
                ffc_cost=Decimal("75.0")
            ),
            "lead_scoring": WorkflowPricing(
                workflow_type="lead_scoring",
                base_cost=Decimal("5.0"),
                quantum_multiplier=1.3,
                complexity_factor=1.1,
                premium_features=["advanced_segmentation", "conversion_prediction"],
                ffc_cost=Decimal("7.15")
            )
        }
        
        # ESG burn configuration
        self.esg_burn_rate = Decimal("0.05")  # 5% of transactions burned for ESG
        self.charity_director_address = "charity_director.nqba.com"
        
        # Marketplace access pricing
        self.marketplace_access_cost = Decimal("50.0")  # 50 FFC for marketplace access
        
        # Premium feature pricing
        self.premium_features = {
            "quantum_advantage_boost": Decimal("100.0"),
            "real_time_monitoring": Decimal("75.0"),
            "advanced_analytics": Decimal("150.0"),
            "custom_algorithms": Decimal("500.0")
        }
    
    async def create_wallet(self, user_id: str, initial_balance: Decimal = Decimal("0")) -> str:
        """Create a new FFC wallet for a user"""
        wallet_id = str(uuid.uuid4())
        
        wallet = FFCWallet(
            wallet_id=wallet_id,
            user_id=user_id,
            balance=initial_balance,
            total_minted=initial_balance,
            total_burned=Decimal("0"),
            created_at=datetime.utcnow(),
            last_updated=datetime.utcnow(),
            is_active=True,
            metadata={}
        )
        
        self.wallets[wallet_id] = wallet
        self.circulating_supply += initial_balance
        
        # Log wallet creation to LTC
        await self.ltc_logger.log_event(
            event_type="ffc_wallet_created",
            event_data={
                "wallet_id": wallet_id,
                "user_id": user_id,
                "initial_balance": float(initial_balance),
                "circulating_supply": float(self.circulating_supply)
            }
        )
        
        return wallet_id
    
    async def mint_tokens(self, wallet_id: str, amount: Decimal, reason: str = "") -> bool:
        """Mint new FFC tokens to a wallet"""
        if wallet_id not in self.wallets:
            return False
        
        wallet = self.wallets[wallet_id]
        
        # Check if minting would exceed total supply
        if self.circulating_supply + amount > self.total_supply:
            return False
        
        wallet.balance += amount
        wallet.total_minted += amount
        wallet.last_updated = datetime.utcnow()
        
        self.circulating_supply += amount
        
        # Create transaction record
        transaction = FFCTransaction(
            transaction_id=str(uuid.uuid4()),
            from_wallet="system_mint",
            to_wallet=wallet_id,
            amount=amount,
            token_type=TokenType.WORKFLOW,
            transaction_type=TransactionType.MINT,
            timestamp=datetime.utcnow(),
            ltc_hash="",
            quantum_signature="",
            metadata={"reason": reason}
        )
        
        # Log minting to LTC
        ltc_hash = await self.ltc_logger.log_event(
            event_type="ffc_tokens_minted",
            event_data={
                "wallet_id": wallet_id,
                "amount": float(amount),
                "reason": reason,
                "circulating_supply": float(self.circulating_supply)
            }
        )
        
        transaction.ltc_hash = ltc_hash
        self.transactions.append(transaction)
        
        return True
    
    async def burn_tokens(self, wallet_id: str, amount: Decimal, reason: str = "") -> bool:
        """Burn FFC tokens from a wallet (ESG alignment)"""
        if wallet_id not in self.wallets:
            return False
        
        wallet = self.wallets[wallet_id]
        
        if wallet.balance < amount:
            return False
        
        wallet.balance -= amount
        wallet.total_burned += amount
        wallet.last_updated = datetime.utcnow()
        
        self.circulating_supply -= amount
        self.burned_supply += amount
        
        # Create transaction record
        transaction = FFCTransaction(
            transaction_id=str(uuid.uuid4()),
            from_wallet=wallet_id,
            to_wallet="system_burn",
            amount=amount,
            token_type=TokenType.ESG,
            transaction_type=TransactionType.BURN,
            timestamp=datetime.utcnow(),
            ltc_hash="",
            quantum_signature="",
            metadata={"reason": reason}
        )
        
        # Log burning to LTC
        ltc_hash = await self.ltc_logger.log_event(
            event_type="ffc_tokens_burned",
            event_data={
                "wallet_id": wallet_id,
                "amount": float(amount),
                "reason": reason,
                "burned_supply": float(self.burned_supply)
            }
        )
        
        transaction.ltc_hash = ltc_hash
        self.transactions.append(transaction)
        
        return True
    
    async def execute_workflow(self, wallet_id: str, workflow_type: str, 
                             complexity: float = 1.0, premium_features: List[str] = None) -> Dict[str, Any]:
        """Execute a workflow using FFC tokens"""
        if wallet_id not in self.wallets:
            raise ValueError("Wallet not found")
        
        if workflow_type not in self.workflow_pricing:
            raise ValueError("Workflow type not supported")
        
        wallet = self.wallets[wallet_id]
        pricing = self.workflow_pricing[workflow_type]
        
        # Calculate FFC cost
        base_cost = pricing.ffc_cost
        complexity_cost = base_cost * Decimal(str(complexity))
        
        # Add premium feature costs
        premium_cost = Decimal("0")
        if premium_features:
            for feature in premium_features:
                if feature in self.premium_features:
                    premium_cost += self.premium_features[feature]
        
        total_cost = complexity_cost + premium_cost
        
        # Check wallet balance
        if wallet.balance < total_cost:
            raise ValueError("Insufficient FFC balance")
        
        # Deduct tokens
        wallet.balance -= total_cost
        wallet.last_updated = datetime.utcnow()
        
        # Calculate ESG burn amount
        esg_burn_amount = total_cost * self.esg_burn_rate
        
        # Execute workflow (simulated)
        workflow_result = await self._execute_quantum_workflow(workflow_type, complexity, premium_features)
        
        # Create transaction record
        transaction = FFCTransaction(
            transaction_id=str(uuid.uuid4()),
            from_wallet=wallet_id,
            to_wallet="workflow_execution",
            amount=total_cost,
            token_type=TokenType.WORKFLOW,
            transaction_type=TransactionType.WORKFLOW_EXECUTION,
            timestamp=datetime.utcnow(),
            ltc_hash="",
            quantum_signature="",
            metadata={
                "workflow_type": workflow_type,
                "complexity": complexity,
                "premium_features": premium_features or [],
                "esg_burn_amount": float(esg_burn_amount)
            }
        )
        
        # Log workflow execution to LTC
        ltc_hash = await self.ltc_logger.log_event(
            event_type="ffc_workflow_executed",
            event_data={
                "wallet_id": wallet_id,
                "workflow_type": workflow_type,
                "ffc_cost": float(total_cost),
                "esg_burn_amount": float(esg_burn_amount),
                "result": workflow_result
            }
        )
        
        transaction.ltc_hash = ltc_hash
        self.transactions.append(transaction)
        
        # Burn ESG tokens
        if esg_burn_amount > 0:
            await self.burn_tokens(wallet_id, esg_burn_amount, "ESG alignment - workflow execution")
        
        return {
            "success": True,
            "workflow_type": workflow_type,
            "ffc_cost": float(total_cost),
            "esg_burn_amount": float(esg_burn_amount),
            "result": workflow_result,
            "transaction_id": transaction.transaction_id,
            "ltc_hash": ltc_hash
        }
    
    async def _execute_quantum_workflow(self, workflow_type: str, complexity: float, 
                                      premium_features: List[str]) -> Dict[str, Any]:
        """Execute quantum workflow using Dynex"""
        try:
            # Create QUBO problem for workflow
            qubo_data = {
                "description": f"FFC Workflow: {workflow_type}",
                "variables": ["efficiency", "accuracy", "speed", "cost"],
                "constraints": {
                    "min_efficiency": 0.8,
                    "max_complexity": complexity * 1000,
                    "min_accuracy": 0.9
                },
                "objective": f"optimize_{workflow_type}",
                "premium_features": premium_features or []
            }
            
            # Submit to Dynex
            job_id = await self.dynex_adapter.submit_qubo(qubo_data)
            
            # Wait for results
            await asyncio.sleep(1)
            
            # Get results
            results = await self.dynex_adapter.get_job_results(job_id)
            
            return {
                "job_id": job_id,
                "workflow_type": workflow_type,
                "complexity": complexity,
                "premium_features": premium_features or [],
                "quantum_advantage": self._calculate_workflow_advantage(results),
                "execution_time": "1.2s",
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    def _calculate_workflow_advantage(self, results: Dict[str, Any]) -> float:
        """Calculate quantum advantage for workflow execution"""
        if "samples" in results and results["samples"]:
            energies = [sample.get("energy", 0) for sample in results["samples"]]
            if energies:
                min_energy = min(energies)
                return max(1.0, 3.0 / (abs(min_energy) + 1))
        return 1.0
    
    async def grant_marketplace_access(self, wallet_id: str) -> Dict[str, Any]:
        """Grant marketplace access using FFC tokens"""
        if wallet_id not in self.wallets:
            raise ValueError("Wallet not found")
        
        wallet = self.wallets[wallet_id]
        
        if wallet.balance < self.marketplace_access_cost:
            raise ValueError("Insufficient FFC balance for marketplace access")
        
        # Deduct tokens
        wallet.balance -= self.marketplace_access_cost
        wallet.last_updated = datetime.utcnow()
        
        # Create transaction record
        transaction = FFCTransaction(
            transaction_id=str(uuid.uuid4()),
            from_wallet=wallet_id,
            to_wallet="marketplace_access",
            amount=self.marketplace_access_cost,
            token_type=TokenType.MARKETPLACE,
            transaction_type=TransactionType.MARKETPLACE_ACCESS,
            timestamp=datetime.utcnow(),
            ltc_hash="",
            quantum_signature="",
            metadata={"access_type": "marketplace", "duration": "30_days"}
        )
        
        # Log marketplace access to LTC
        ltc_hash = await self.ltc_logger.log_event(
            event_type="ffc_marketplace_access_granted",
            event_data={
                "wallet_id": wallet_id,
                "ffc_cost": float(self.marketplace_access_cost),
                "access_type": "marketplace"
            }
        )
        
        transaction.ltc_hash = ltc_hash
        self.transactions.append(transaction)
        
        return {
            "success": True,
            "access_granted": True,
            "access_type": "marketplace",
            "duration": "30 days",
            "ffc_cost": float(self.marketplace_access_cost),
            "transaction_id": transaction.transaction_id,
            "ltc_hash": ltc_hash
        }
    
    async def get_wallet_balance(self, wallet_id: str) -> Optional[Decimal]:
        """Get FFC balance for a wallet"""
        if wallet_id in self.wallets:
            return self.wallets[wallet_id].balance
        return None
    
    async def get_token_economics(self) -> Dict[str, Any]:
        """Get comprehensive token economics data"""
        return {
            "total_supply": float(self.total_supply),
            "circulating_supply": float(self.circulating_supply),
            "burned_supply": float(self.burned_supply),
            "burn_rate": float(self.esg_burn_rate),
            "active_wallets": len([w for w in self.wallets.values() if w.is_active]),
            "total_transactions": len(self.transactions),
            "charity_director_address": self.charity_director_address
        }
    
    async def transfer_tokens(self, from_wallet_id: str, to_wallet_id: str, 
                            amount: Decimal) -> bool:
        """Transfer FFC tokens between wallets"""
        if from_wallet_id not in self.wallets or to_wallet_id not in self.wallets:
            return False
        
        from_wallet = self.wallets[from_wallet_id]
        to_wallet = self.wallets[to_wallet_id]
        
        if from_wallet.balance < amount:
            return False
        
        # Execute transfer
        from_wallet.balance -= amount
        to_wallet.balance += amount
        
        from_wallet.last_updated = datetime.utcnow()
        to_wallet.last_updated = datetime.utcnow()
        
        # Create transaction record
        transaction = FFCTransaction(
            transaction_id=str(uuid.uuid4()),
            from_wallet=from_wallet_id,
            to_wallet=to_wallet_id,
            amount=amount,
            token_type=TokenType.WORKFLOW,
            transaction_type=TransactionType.TRANSFER,
            timestamp=datetime.utcnow(),
            ltc_hash="",
            quantum_signature="",
            metadata={}
        )
        
        # Log transfer to LTC
        ltc_hash = await self.ltc_logger.log_event(
            event_type="ffc_tokens_transferred",
            event_data={
                "from_wallet": from_wallet_id,
                "to_wallet": to_wallet_id,
                "amount": float(amount)
            }
        )
        
        transaction.ltc_hash = ltc_hash
        self.transactions.append(transaction)
        
        return True


# FFC API endpoints
class FFCTokenAPI:
    """API endpoints for FLYFOX Credit token system"""
    
    def __init__(self):
        self.ffc_system = FlyfoxCredit()
    
    async def create_wallet_endpoint(self, user_id: str, initial_balance: float = 0.0) -> Dict[str, Any]:
        """API endpoint for wallet creation"""
        try:
            wallet_id = await self.ffc_system.create_wallet(user_id, Decimal(str(initial_balance)))
            return {
                "success": True,
                "wallet_id": wallet_id,
                "initial_balance": initial_balance
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_workflow_endpoint(self, wallet_id: str, workflow_type: str, 
                                      complexity: float = 1.0, premium_features: List[str] = None) -> Dict[str, Any]:
        """API endpoint for workflow execution"""
        try:
            result = await self.ffc_system.execute_workflow(wallet_id, workflow_type, complexity, premium_features)
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_balance_endpoint(self, wallet_id: str) -> Dict[str, Any]:
        """API endpoint for wallet balance"""
        try:
            balance = await self.ffc_system.get_wallet_balance(wallet_id)
            if balance is not None:
                return {
                    "success": True,
                    "balance": float(balance)
                }
            else:
                return {
                    "success": False,
                    "error": "Wallet not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_economics_endpoint(self) -> Dict[str, Any]:
        """API endpoint for token economics"""
        try:
            economics = await self.ffc_system.get_token_economics()
            return {
                "success": True,
                "data": economics
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Example usage and testing
async def demo_ffc_system():
    """Demonstrate the FLYFOX Credit token system"""
    ffc_system = FlyfoxCredit()
    
    # Create wallets
    wallet1_id = await ffc_system.create_wallet("user_001", Decimal("1000.0"))
    wallet2_id = await ffc_system.create_wallet("user_002", Decimal("500.0"))
    
    print(f"Wallet 1 created: {wallet1_id}")
    print(f"Wallet 2 created: {wallet2_id}")
    
    # Execute workflow
    workflow_result = await ffc_system.execute_workflow(
        wallet1_id, 
        "energy_optimization", 
        complexity=1.5, 
        premium_features=["real_time_monitoring"]
    )
    
    print(f"Workflow executed: {workflow_result}")
    
    # Get balances
    balance1 = await ffc_system.get_wallet_balance(wallet1_id)
    balance2 = await ffc_system.get_wallet_balance(wallet2_id)
    
    print(f"Wallet 1 balance: {balance1}")
    print(f"Wallet 2 balance: {balance2}")
    
    # Get token economics
    economics = await ffc_system.get_token_economics()
    print(f"Token economics: {economics}")


if __name__ == "__main__":
    asyncio.run(demo_ffc_system())
