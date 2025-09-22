"""
Decentralized Governance System for FLYFOX AI
Enables FLY token holders to vote on platform decisions, upgrades, and proposals
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import hashlib
from web3 import Web3
from eth_account import Account

class ProposalType(Enum):
    """Types of governance proposals"""
    PLATFORM_UPGRADE = "platform_upgrade"
    ALGORITHM_ADDITION = "algorithm_addition"
    TOKENOMICS_CHANGE = "tokenomics_change"
    PARTNERSHIP = "partnership"
    TREASURY_ALLOCATION = "treasury_allocation"
    POLICY_CHANGE = "policy_change"
    EMERGENCY_ACTION = "emergency_action"

class ProposalStatus(Enum):
    """Proposal lifecycle status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    CANCELLED = "cancelled"

class VoteChoice(Enum):
    """Vote choices"""
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"

@dataclass
class Proposal:
    """Governance proposal structure"""
    proposal_id: str
    title: str
    description: str
    proposal_type: ProposalType
    proposer: str
    created_at: datetime
    voting_start: datetime
    voting_end: datetime
    execution_delay: timedelta
    status: ProposalStatus
    
    # Voting requirements
    quorum_required: float  # Percentage of total supply
    approval_threshold: float  # Percentage of votes needed to pass
    
    # Voting results
    votes_for: float
    votes_against: float
    votes_abstain: float
    total_votes: float
    
    # Execution details
    execution_payload: Optional[Dict[str, Any]]
    execution_target: Optional[str]
    executed_at: Optional[datetime]
    
    # Metadata
    tags: List[str]
    discussion_url: Optional[str]
    impact_assessment: Optional[str]

@dataclass
class Vote:
    """Individual vote record"""
    vote_id: str
    proposal_id: str
    voter: str
    choice: VoteChoice
    voting_power: float
    timestamp: datetime
    reason: Optional[str]
    delegate: Optional[str]  # If vote was delegated

@dataclass
class Delegation:
    """Vote delegation record"""
    delegator: str
    delegate: str
    voting_power: float
    created_at: datetime
    expires_at: Optional[datetime]
    active: bool

class GovernanceSystem:
    """Main governance system for FLYFOX AI"""
    
    def __init__(self, web3_provider: str, fly_token_address: str, governance_contract: str):
        self.web3 = Web3(Web3.HTTPProvider(web3_provider))
        self.fly_token_address = fly_token_address
        self.governance_contract_address = governance_contract
        self.logger = logging.getLogger(__name__)
        
        # Governance parameters
        self.governance_config = {
            'min_proposal_threshold': 100000,  # Minimum FLY tokens to create proposal
            'voting_period_days': 7,
            'execution_delay_days': 2,
            'default_quorum': 0.04,  # 4% of total supply
            'default_approval_threshold': 0.51,  # 51% of votes
            'emergency_quorum': 0.10,  # 10% for emergency proposals
            'emergency_approval_threshold': 0.67,  # 67% for emergency proposals
            'delegation_enabled': True,
            'max_delegation_depth': 3
        }
        
        # Storage
        self.proposals: Dict[str, Proposal] = {}
        self.votes: Dict[str, Vote] = {}
        self.delegations: Dict[str, Delegation] = {}
        self.voting_power_snapshots: Dict[str, Dict[str, float]] = {}
        
        # Load contracts
        self.fly_token_contract = self._load_fly_token_contract()
        self.governance_contract = self._load_governance_contract()
    
    def _load_fly_token_contract(self):
        """Load FLY token contract for voting power calculation"""
        # Simplified ABI
        fly_token_abi = [
            {
                "inputs": [{"name": "account", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        return self.web3.eth.contract(
            address=self.fly_token_address,
            abi=fly_token_abi
        )
    
    def _load_governance_contract(self):
        """Load governance contract for on-chain execution"""
        # Simplified governance contract ABI
        governance_abi = [
            {
                "inputs": [
                    {"name": "proposalId", "type": "bytes32"},
                    {"name": "targets", "type": "address[]"},
                    {"name": "values", "type": "uint256[]"},
                    {"name": "calldatas", "type": "bytes[]"}
                ],
                "name": "execute",
                "outputs": [],
                "type": "function"
            }
        ]
        
        return self.web3.eth.contract(
            address=self.governance_contract_address,
            abi=governance_abi
        )
    
    async def create_proposal(
        self,
        proposer: str,
        title: str,
        description: str,
        proposal_type: ProposalType,
        execution_payload: Optional[Dict[str, Any]] = None,
        execution_target: Optional[str] = None,
        custom_quorum: Optional[float] = None,
        custom_approval_threshold: Optional[float] = None,
        tags: Optional[List[str]] = None,
        discussion_url: Optional[str] = None
    ) -> str:
        """
        Create a new governance proposal
        
        Args:
            proposer: Address of the proposal creator
            title: Proposal title
            description: Detailed proposal description
            proposal_type: Type of proposal
            execution_payload: Data for automatic execution
            execution_target: Target contract for execution
            custom_quorum: Custom quorum requirement
            custom_approval_threshold: Custom approval threshold
            tags: Proposal tags for categorization
            discussion_url: URL for community discussion
            
        Returns:
            Proposal ID
        """
        try:
            # Check proposer has minimum tokens
            proposer_balance = await self._get_voting_power(proposer)
            if proposer_balance < self.governance_config['min_proposal_threshold']:
                raise ValueError(f"Insufficient tokens to create proposal. Required: {self.governance_config['min_proposal_threshold']}")
            
            # Generate proposal ID
            proposal_id = hashlib.sha256(
                f"{proposer}_{title}_{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            # Set voting parameters based on proposal type
            if proposal_type == ProposalType.EMERGENCY_ACTION:
                quorum = custom_quorum or self.governance_config['emergency_quorum']
                approval_threshold = custom_approval_threshold or self.governance_config['emergency_approval_threshold']
                voting_period = timedelta(days=3)  # Shorter for emergency
            else:
                quorum = custom_quorum or self.governance_config['default_quorum']
                approval_threshold = custom_approval_threshold or self.governance_config['default_approval_threshold']
                voting_period = timedelta(days=self.governance_config['voting_period_days'])
            
            # Create proposal
            now = datetime.now()
            proposal = Proposal(
                proposal_id=proposal_id,
                title=title,
                description=description,
                proposal_type=proposal_type,
                proposer=proposer,
                created_at=now,
                voting_start=now + timedelta(hours=24),  # 24-hour delay before voting starts
                voting_end=now + timedelta(hours=24) + voting_period,
                execution_delay=timedelta(days=self.governance_config['execution_delay_days']),
                status=ProposalStatus.DRAFT,
                quorum_required=quorum,
                approval_threshold=approval_threshold,
                votes_for=0.0,
                votes_against=0.0,
                votes_abstain=0.0,
                total_votes=0.0,
                execution_payload=execution_payload,
                execution_target=execution_target,
                executed_at=None,
                tags=tags or [],
                discussion_url=discussion_url,
                impact_assessment=None
            )
            
            self.proposals[proposal_id] = proposal
            
            # Create voting power snapshot at proposal creation
            await self._create_voting_snapshot(proposal_id)
            
            self.logger.info(f"Proposal created: {proposal_id} - {title}")
            return proposal_id
            
        except Exception as e:
            self.logger.error(f"Error creating proposal: {e}")
            raise
    
    async def _create_voting_snapshot(self, proposal_id: str):
        """Create a snapshot of voting power at proposal creation"""
        try:
            # In a real implementation, this would snapshot all token holders
            # For demo, we'll create an empty snapshot that gets populated as users vote
            self.voting_power_snapshots[proposal_id] = {}
            
        except Exception as e:
            self.logger.error(f"Error creating voting snapshot: {e}")
    
    async def cast_vote(
        self,
        voter: str,
        proposal_id: str,
        choice: VoteChoice,
        reason: Optional[str] = None
    ) -> str:
        """
        Cast a vote on a proposal
        
        Args:
            voter: Address of the voter
            proposal_id: ID of the proposal to vote on
            choice: Vote choice (for/against/abstain)
            reason: Optional reason for the vote
            
        Returns:
            Vote ID
        """
        try:
            # Check proposal exists and is active
            if proposal_id not in self.proposals:
                raise ValueError("Proposal not found")
            
            proposal = self.proposals[proposal_id]
            
            if proposal.status != ProposalStatus.ACTIVE:
                if proposal.status == ProposalStatus.DRAFT and datetime.now() >= proposal.voting_start:
                    proposal.status = ProposalStatus.ACTIVE
                else:
                    raise ValueError(f"Proposal not active for voting. Status: {proposal.status}")
            
            # Check voting period
            now = datetime.now()
            if now < proposal.voting_start or now > proposal.voting_end:
                raise ValueError("Voting period not active")
            
            # Check if user already voted
            existing_vote = self._get_user_vote(voter, proposal_id)
            if existing_vote:
                raise ValueError("User has already voted on this proposal")
            
            # Get voting power (including delegated power)
            voting_power = await self._get_effective_voting_power(voter, proposal_id)
            
            if voting_power == 0:
                raise ValueError("No voting power")
            
            # Create vote record
            vote_id = hashlib.sha256(
                f"{voter}_{proposal_id}_{choice.value}_{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            vote = Vote(
                vote_id=vote_id,
                proposal_id=proposal_id,
                voter=voter,
                choice=choice,
                voting_power=voting_power,
                timestamp=now,
                reason=reason,
                delegate=None
            )
            
            self.votes[vote_id] = vote
            
            # Update proposal vote counts
            if choice == VoteChoice.FOR:
                proposal.votes_for += voting_power
            elif choice == VoteChoice.AGAINST:
                proposal.votes_against += voting_power
            elif choice == VoteChoice.ABSTAIN:
                proposal.votes_abstain += voting_power
            
            proposal.total_votes += voting_power
            
            self.logger.info(f"Vote cast: {vote_id} - {voter} voted {choice.value} on {proposal_id}")
            
            # Check if proposal should be finalized
            await self._check_proposal_finalization(proposal_id)
            
            return vote_id
            
        except Exception as e:
            self.logger.error(f"Error casting vote: {e}")
            raise
    
    async def delegate_voting_power(
        self,
        delegator: str,
        delegate: str,
        expires_at: Optional[datetime] = None
    ) -> str:
        """
        Delegate voting power to another address
        
        Args:
            delegator: Address delegating their voting power
            delegate: Address receiving the delegated power
            expires_at: Optional expiration date for delegation
            
        Returns:
            Delegation ID
        """
        try:
            if not self.governance_config['delegation_enabled']:
                raise ValueError("Delegation is not enabled")
            
            if delegator == delegate:
                raise ValueError("Cannot delegate to self")
            
            # Check for delegation loops
            if await self._would_create_delegation_loop(delegator, delegate):
                raise ValueError("Delegation would create a loop")
            
            # Get delegator's voting power
            voting_power = await self._get_voting_power(delegator)
            if voting_power == 0:
                raise ValueError("No voting power to delegate")
            
            # Cancel existing delegation
            await self._cancel_existing_delegation(delegator)
            
            # Create new delegation
            delegation_id = hashlib.sha256(
                f"{delegator}_{delegate}_{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            delegation = Delegation(
                delegator=delegator,
                delegate=delegate,
                voting_power=voting_power,
                created_at=datetime.now(),
                expires_at=expires_at,
                active=True
            )
            
            self.delegations[delegation_id] = delegation
            
            self.logger.info(f"Voting power delegated: {delegator} -> {delegate}")
            return delegation_id
            
        except Exception as e:
            self.logger.error(f"Error delegating voting power: {e}")
            raise
    
    async def _would_create_delegation_loop(self, delegator: str, delegate: str) -> bool:
        """Check if delegation would create a loop"""
        visited = set()
        current = delegate
        depth = 0
        
        while current and depth < self.governance_config['max_delegation_depth']:
            if current in visited or current == delegator:
                return True
            
            visited.add(current)
            
            # Find if current address has delegated to someone else
            current_delegation = self._get_active_delegation_by_delegator(current)
            current = current_delegation.delegate if current_delegation else None
            depth += 1
        
        return False
    
    async def _cancel_existing_delegation(self, delegator: str):
        """Cancel any existing delegation by the delegator"""
        existing = self._get_active_delegation_by_delegator(delegator)
        if existing:
            for delegation_id, delegation in self.delegations.items():
                if delegation.delegator == delegator and delegation.active:
                    delegation.active = False
                    break
    
    def _get_active_delegation_by_delegator(self, delegator: str) -> Optional[Delegation]:
        """Get active delegation by delegator"""
        for delegation in self.delegations.values():
            if (delegation.delegator == delegator and 
                delegation.active and 
                (not delegation.expires_at or delegation.expires_at > datetime.now())):
                return delegation
        return None
    
    async def _get_voting_power(self, address: str) -> float:
        """Get base voting power (FLY token balance)"""
        try:
            balance_wei = self.fly_token_contract.functions.balanceOf(address).call()
            return balance_wei / 10**18
        except Exception as e:
            self.logger.error(f"Error getting voting power: {e}")
            return 0.0
    
    async def _get_effective_voting_power(self, address: str, proposal_id: str) -> float:
        """Get effective voting power including delegated power"""
        try:
            # Base voting power
            base_power = await self._get_voting_power(address)
            
            # Add delegated power
            delegated_power = 0.0
            for delegation in self.delegations.values():
                if (delegation.delegate == address and 
                    delegation.active and 
                    (not delegation.expires_at or delegation.expires_at > datetime.now())):
                    delegated_power += delegation.voting_power
            
            return base_power + delegated_power
            
        except Exception as e:
            self.logger.error(f"Error calculating effective voting power: {e}")
            return 0.0
    
    def _get_user_vote(self, voter: str, proposal_id: str) -> Optional[Vote]:
        """Check if user has already voted on proposal"""
        for vote in self.votes.values():
            if vote.voter == voter and vote.proposal_id == proposal_id:
                return vote
        return None
    
    async def _check_proposal_finalization(self, proposal_id: str):
        """Check if proposal should be finalized based on votes"""
        try:
            proposal = self.proposals[proposal_id]
            
            if proposal.status != ProposalStatus.ACTIVE:
                return
            
            # Check if voting period has ended
            if datetime.now() > proposal.voting_end:
                await self._finalize_proposal(proposal_id)
                return
            
            # Check for early finalization (if quorum and clear majority reached)
            total_supply = await self._get_total_supply()
            current_quorum = proposal.total_votes / total_supply
            
            if current_quorum >= proposal.quorum_required:
                # Check if there's a clear majority that can't be overturned
                remaining_votes = total_supply - proposal.total_votes
                
                if proposal.votes_for > proposal.votes_against + remaining_votes:
                    # Proposal will definitely pass
                    await self._finalize_proposal(proposal_id)
                elif proposal.votes_against > proposal.votes_for + remaining_votes:
                    # Proposal will definitely fail
                    await self._finalize_proposal(proposal_id)
            
        except Exception as e:
            self.logger.error(f"Error checking proposal finalization: {e}")
    
    async def _finalize_proposal(self, proposal_id: str):
        """Finalize proposal voting and determine outcome"""
        try:
            proposal = self.proposals[proposal_id]
            
            # Calculate final results
            total_supply = await self._get_total_supply()
            quorum_met = proposal.total_votes / total_supply >= proposal.quorum_required
            
            if not quorum_met:
                proposal.status = ProposalStatus.REJECTED
                self.logger.info(f"Proposal {proposal_id} rejected: Quorum not met")
                return
            
            # Check approval threshold
            if proposal.total_votes > 0:
                approval_rate = proposal.votes_for / proposal.total_votes
                if approval_rate >= proposal.approval_threshold:
                    proposal.status = ProposalStatus.PASSED
                    self.logger.info(f"Proposal {proposal_id} passed")
                    
                    # Schedule execution if applicable
                    if proposal.execution_payload:
                        await self._schedule_execution(proposal_id)
                else:
                    proposal.status = ProposalStatus.REJECTED
                    self.logger.info(f"Proposal {proposal_id} rejected: Approval threshold not met")
            else:
                proposal.status = ProposalStatus.REJECTED
                self.logger.info(f"Proposal {proposal_id} rejected: No votes")
            
        except Exception as e:
            self.logger.error(f"Error finalizing proposal: {e}")
    
    async def _schedule_execution(self, proposal_id: str):
        """Schedule proposal execution after delay period"""
        # In a real implementation, this would schedule the execution
        # For demo, we'll just log the scheduling
        proposal = self.proposals[proposal_id]
        execution_time = datetime.now() + proposal.execution_delay
        
        self.logger.info(f"Proposal {proposal_id} scheduled for execution at {execution_time}")
    
    async def execute_proposal(self, proposal_id: str, executor: str) -> bool:
        """
        Execute a passed proposal
        
        Args:
            proposal_id: ID of the proposal to execute
            executor: Address executing the proposal
            
        Returns:
            Success status
        """
        try:
            proposal = self.proposals[proposal_id]
            
            if proposal.status != ProposalStatus.PASSED:
                raise ValueError("Proposal not in passed status")
            
            # Check execution delay has passed
            execution_time = proposal.voting_end + proposal.execution_delay
            if datetime.now() < execution_time:
                raise ValueError("Execution delay period not yet passed")
            
            if not proposal.execution_payload:
                raise ValueError("No execution payload defined")
            
            # Execute the proposal (simplified for demo)
            success = await self._execute_proposal_payload(proposal)
            
            if success:
                proposal.status = ProposalStatus.EXECUTED
                proposal.executed_at = datetime.now()
                self.logger.info(f"Proposal {proposal_id} executed successfully")
            else:
                self.logger.error(f"Proposal {proposal_id} execution failed")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error executing proposal: {e}")
            return False
    
    async def _execute_proposal_payload(self, proposal: Proposal) -> bool:
        """Execute the actual proposal payload"""
        try:
            # This would contain the actual execution logic
            # For demo, we'll just simulate execution
            
            payload = proposal.execution_payload
            if not payload:
                return False
            
            # Different execution types based on proposal type
            if proposal.proposal_type == ProposalType.PLATFORM_UPGRADE:
                return await self._execute_platform_upgrade(payload)
            elif proposal.proposal_type == ProposalType.ALGORITHM_ADDITION:
                return await self._execute_algorithm_addition(payload)
            elif proposal.proposal_type == ProposalType.TOKENOMICS_CHANGE:
                return await self._execute_tokenomics_change(payload)
            elif proposal.proposal_type == ProposalType.TREASURY_ALLOCATION:
                return await self._execute_treasury_allocation(payload)
            else:
                # Generic execution
                return True
            
        except Exception as e:
            self.logger.error(f"Error executing proposal payload: {e}")
            return False
    
    async def _execute_platform_upgrade(self, payload: Dict[str, Any]) -> bool:
        """Execute platform upgrade proposal"""
        # Simulate platform upgrade
        self.logger.info(f"Executing platform upgrade: {payload}")
        return True
    
    async def _execute_algorithm_addition(self, payload: Dict[str, Any]) -> bool:
        """Execute algorithm addition proposal"""
        # Simulate algorithm addition
        self.logger.info(f"Adding new algorithm: {payload}")
        return True
    
    async def _execute_tokenomics_change(self, payload: Dict[str, Any]) -> bool:
        """Execute tokenomics change proposal"""
        # Simulate tokenomics change
        self.logger.info(f"Updating tokenomics: {payload}")
        return True
    
    async def _execute_treasury_allocation(self, payload: Dict[str, Any]) -> bool:
        """Execute treasury allocation proposal"""
        # Simulate treasury allocation
        self.logger.info(f"Allocating treasury funds: {payload}")
        return True
    
    async def _get_total_supply(self) -> float:
        """Get total FLY token supply"""
        try:
            supply_wei = self.fly_token_contract.functions.totalSupply().call()
            return supply_wei / 10**18
        except Exception as e:
            self.logger.error(f"Error getting total supply: {e}")
            return 1000000000.0  # Default to 1B tokens
    
    async def get_proposal_details(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed proposal information"""
        if proposal_id not in self.proposals:
            return None
        
        proposal = self.proposals[proposal_id]
        
        # Get vote breakdown
        proposal_votes = [vote for vote in self.votes.values() if vote.proposal_id == proposal_id]
        
        vote_breakdown = {
            'for_votes': [asdict(vote) for vote in proposal_votes if vote.choice == VoteChoice.FOR],
            'against_votes': [asdict(vote) for vote in proposal_votes if vote.choice == VoteChoice.AGAINST],
            'abstain_votes': [asdict(vote) for vote in proposal_votes if vote.choice == VoteChoice.ABSTAIN]
        }
        
        # Calculate participation metrics
        total_supply = await self._get_total_supply()
        participation_rate = proposal.total_votes / total_supply if total_supply > 0 else 0
        
        return {
            'proposal': asdict(proposal),
            'vote_breakdown': vote_breakdown,
            'participation_rate': participation_rate,
            'quorum_progress': participation_rate / proposal.quorum_required if proposal.quorum_required > 0 else 0,
            'time_remaining': max(0, (proposal.voting_end - datetime.now()).total_seconds()) if proposal.status == ProposalStatus.ACTIVE else 0
        }
    
    async def get_user_governance_info(self, user_address: str) -> Dict[str, Any]:
        """Get user's governance participation information"""
        try:
            # Voting power
            voting_power = await self._get_voting_power(user_address)
            
            # Delegation info
            delegation_given = self._get_active_delegation_by_delegator(user_address)
            delegations_received = [
                d for d in self.delegations.values()
                if d.delegate == user_address and d.active
            ]
            
            # Voting history
            user_votes = [vote for vote in self.votes.values() if vote.voter == user_address]
            
            # Proposals created
            user_proposals = [
                proposal for proposal in self.proposals.values()
                if proposal.proposer == user_address
            ]
            
            return {
                'user_address': user_address,
                'voting_power': voting_power,
                'delegation_given': asdict(delegation_given) if delegation_given else None,
                'delegations_received': [asdict(d) for d in delegations_received],
                'vote_count': len(user_votes),
                'proposals_created': len(user_proposals),
                'governance_participation_score': self._calculate_participation_score(user_address)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user governance info: {e}")
            return {}
    
    def _calculate_participation_score(self, user_address: str) -> float:
        """Calculate user's governance participation score"""
        try:
            # Simple scoring based on votes cast and proposals created
            user_votes = len([vote for vote in self.votes.values() if vote.voter == user_address])
            user_proposals = len([p for p in self.proposals.values() if p.proposer == user_address])
            
            # Score out of 100
            vote_score = min(user_votes * 10, 70)  # Max 70 points for voting
            proposal_score = min(user_proposals * 30, 30)  # Max 30 points for proposals
            
            return vote_score + proposal_score
            
        except Exception as e:
            self.logger.error(f"Error calculating participation score: {e}")
            return 0.0

# Example usage
async def main():
    """Example usage of the governance system"""
    # Initialize governance system
    governance = GovernanceSystem(
        web3_provider="http://localhost:8545",
        fly_token_address="0x1234567890123456789012345678901234567890",
        governance_contract="0x0987654321098765432109876543210987654321"
    )
    
    # Example addresses
    proposer = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
    voter1 = "0x1111111111111111111111111111111111111111"
    voter2 = "0x2222222222222222222222222222222222222222"
    
    # Create a proposal
    print("🏛️ Creating governance proposal...")
    proposal_id = await governance.create_proposal(
        proposer=proposer,
        title="Add New Quantum Algorithm: Quantum Approximate Optimization Algorithm (QAOA)",
        description="Proposal to integrate QAOA for enhanced optimization capabilities in the FLYFOX AI platform.",
        proposal_type=ProposalType.ALGORITHM_ADDITION,
        execution_payload={
            "algorithm_name": "QAOA",
            "implementation_path": "/src/quantum/qaoa.py",
            "api_endpoint": "/api/quantum/qaoa"
        },
        tags=["quantum", "algorithm", "optimization"]
    )
    print(f"Proposal created: {proposal_id}")
    
    # Simulate voting period start
    governance.proposals[proposal_id].status = ProposalStatus.ACTIVE
    governance.proposals[proposal_id].voting_start = datetime.now()
    
    # Cast votes
    print("\n🗳️ Casting votes...")
    vote1_id = await governance.cast_vote(voter1, proposal_id, VoteChoice.FOR, "This will enhance our optimization capabilities")
    vote2_id = await governance.cast_vote(voter2, proposal_id, VoteChoice.FOR, "Strongly support quantum improvements")
    
    print(f"Votes cast: {vote1_id}, {vote2_id}")
    
    # Get proposal details
    print("\n📊 Proposal Details:")
    details = await governance.get_proposal_details(proposal_id)
    print(json.dumps(details, indent=2, default=str))
    
    # Get user governance info
    print(f"\n👤 User Governance Info for {voter1}:")
    user_info = await governance.get_user_governance_info(voter1)
    print(json.dumps(user_info, indent=2, default=str))

if __name__ == "__main__":
    asyncio.run(main())