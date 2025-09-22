// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title FLY Token - FLYFOX AI Ecosystem Token
 * @dev ERC-20 token with ERC-1404 compliance features for regulatory compliance
 * @notice This token powers the FLYFOX AI decentralized ecosystem
 */
contract FLYToken is ERC20, Ownable, ReentrancyGuard, Pausable {
    
    // Token Economics
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18; // 1 billion FLY
    uint256 public constant ECOSYSTEM_ALLOCATION = 400_000_000 * 10**18; // 40%
    uint256 public constant TEAM_ALLOCATION = 150_000_000 * 10**18; // 15%
    uint256 public constant INVESTOR_ALLOCATION = 250_000_000 * 10**18; // 25%
    uint256 public constant FOUNDATION_ALLOCATION = 100_000_000 * 10**18; // 10%
    uint256 public constant COMMUNITY_ALLOCATION = 100_000_000 * 10**18; // 10%
    
    // Staking Variables
    mapping(address => StakeInfo[]) public stakes;
    mapping(address => uint256) public totalStaked;
    mapping(address => uint256) public reputationScore;
    
    // Validation Rewards
    mapping(address => uint256) public validationRewards;
    mapping(address => uint256) public validationCount;
    
    // ERC-1404 Compliance
    mapping(address => bool) public allowedRecipients;
    mapping(address => bool) public restrictedAddresses;
    
    // Governance
    mapping(address => uint256) public votingPower;
    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;
    
    struct StakeInfo {
        uint256 amount;
        uint256 startTime;
        uint256 lockPeriod;
        uint256 multiplier;
        bool active;
    }
    
    struct Proposal {
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 endTime;
        bool executed;
        address proposer;
    }
    
    // Events
    event TokensStaked(address indexed staker, uint256 amount, uint256 lockPeriod);
    event TokensUnstaked(address indexed staker, uint256 amount, uint256 reward);
    event ValidationRewardPaid(address indexed validator, uint256 amount);
    event ProposalCreated(uint256 indexed proposalId, address indexed proposer, string description);
    event VoteCast(uint256 indexed proposalId, address indexed voter, bool support, uint256 weight);
    
    // Lock periods and multipliers (in days and basis points)
    uint256[] public lockPeriods = [30 days, 90 days, 180 days, 365 days];
    uint256[] public multipliers = [10000, 12000, 15000, 20000]; // 1x, 1.2x, 1.5x, 2x
    
    constructor() ERC20("FLY Token", "FLY") {
        _mint(msg.sender, MAX_SUPPLY);
        allowedRecipients[msg.sender] = true;
    }
    
    /**
     * @dev Stake tokens for rewards and governance power
     * @param amount Amount of tokens to stake
     * @param lockPeriodIndex Index of lock period (0-3)
     */
    function stake(uint256 amount, uint256 lockPeriodIndex) external nonReentrant whenNotPaused {
        require(amount > 0, "Amount must be greater than 0");
        require(lockPeriodIndex < lockPeriods.length, "Invalid lock period");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");
        
        _transfer(msg.sender, address(this), amount);
        
        stakes[msg.sender].push(StakeInfo({
            amount: amount,
            startTime: block.timestamp,
            lockPeriod: lockPeriods[lockPeriodIndex],
            multiplier: multipliers[lockPeriodIndex],
            active: true
        }));
        
        totalStaked[msg.sender] += amount;
        votingPower[msg.sender] += (amount * multipliers[lockPeriodIndex]) / 10000;
        
        emit TokensStaked(msg.sender, amount, lockPeriods[lockPeriodIndex]);
    }
    
    /**
     * @dev Unstake tokens and claim rewards
     * @param stakeIndex Index of the stake to unstake
     */
    function unstake(uint256 stakeIndex) external nonReentrant {
        require(stakeIndex < stakes[msg.sender].length, "Invalid stake index");
        StakeInfo storage stakeInfo = stakes[msg.sender][stakeIndex];
        require(stakeInfo.active, "Stake already withdrawn");
        require(block.timestamp >= stakeInfo.startTime + stakeInfo.lockPeriod, "Lock period not ended");
        
        uint256 stakedAmount = stakeInfo.amount;
        uint256 reward = calculateStakingReward(msg.sender, stakeIndex);
        
        stakeInfo.active = false;
        totalStaked[msg.sender] -= stakedAmount;
        votingPower[msg.sender] -= (stakedAmount * stakeInfo.multiplier) / 10000;
        
        _transfer(address(this), msg.sender, stakedAmount + reward);
        
        emit TokensUnstaked(msg.sender, stakedAmount, reward);
    }
    
    /**
     * @dev Calculate staking reward for a specific stake
     * @param staker Address of the staker
     * @param stakeIndex Index of the stake
     * @return reward Calculated reward amount
     */
    function calculateStakingReward(address staker, uint256 stakeIndex) public view returns (uint256 reward) {
        StakeInfo memory stakeInfo = stakes[staker][stakeIndex];
        if (!stakeInfo.active) return 0;
        
        uint256 stakingDuration = block.timestamp - stakeInfo.startTime;
        uint256 annualReward = (stakeInfo.amount * 12) / 100; // 12% APY base
        uint256 multipliedReward = (annualReward * stakeInfo.multiplier) / 10000;
        
        reward = (multipliedReward * stakingDuration) / 365 days;
    }
    
    /**
     * @dev Reward validators for accurate information validation
     * @param validator Address of the validator
     * @param amount Reward amount
     * @param accuracyScore Accuracy score (0-100)
     */
    function rewardValidator(address validator, uint256 amount, uint256 accuracyScore) external onlyOwner {
        require(accuracyScore <= 100, "Invalid accuracy score");
        
        uint256 adjustedReward = (amount * accuracyScore) / 100;
        validationRewards[validator] += adjustedReward;
        validationCount[validator]++;
        
        // Update reputation score
        reputationScore[validator] = (reputationScore[validator] + accuracyScore) / 2;
        
        _mint(validator, adjustedReward);
        
        emit ValidationRewardPaid(validator, adjustedReward);
    }
    
    /**
     * @dev Create a governance proposal
     * @param description Description of the proposal
     * @param votingPeriod Voting period in seconds
     */
    function createProposal(string memory description, uint256 votingPeriod) external {
        require(votingPower[msg.sender] >= 1000 * 10**18, "Insufficient voting power"); // Minimum 1000 FLY voting power
        
        proposalCount++;
        proposals[proposalCount] = Proposal({
            description: description,
            votesFor: 0,
            votesAgainst: 0,
            endTime: block.timestamp + votingPeriod,
            executed: false,
            proposer: msg.sender
        });
        
        emit ProposalCreated(proposalCount, msg.sender, description);
    }
    
    /**
     * @dev Vote on a proposal
     * @param proposalId ID of the proposal
     * @param support True for yes, false for no
     */
    function vote(uint256 proposalId, bool support) external {
        require(proposalId <= proposalCount && proposalId > 0, "Invalid proposal ID");
        require(block.timestamp <= proposals[proposalId].endTime, "Voting period ended");
        require(votingPower[msg.sender] > 0, "No voting power");
        
        uint256 weight = votingPower[msg.sender];
        
        if (support) {
            proposals[proposalId].votesFor += weight;
        } else {
            proposals[proposalId].votesAgainst += weight;
        }
        
        emit VoteCast(proposalId, msg.sender, support, weight);
    }
    
    /**
     * @dev ERC-1404 transfer restriction detection
     * @param from Sender address
     * @param to Recipient address
     * @param value Transfer amount
     * @return restrictionCode 0 for no restriction, >0 for restricted
     */
    function detectTransferRestriction(address from, address to, uint256 value) public view returns (uint8) {
        if (restrictedAddresses[from] || restrictedAddresses[to]) return 1;
        if (!allowedRecipients[to] && !_isContract(to)) return 2;
        return 0;
    }
    
    /**
     * @dev Get restriction message for a restriction code
     * @param restrictionCode The restriction code
     * @return message Human readable restriction message
     */
    function messageForTransferRestriction(uint8 restrictionCode) public pure returns (string memory message) {
        if (restrictionCode == 1) return "Address is restricted";
        if (restrictionCode == 2) return "Recipient not allowed";
        return "No restriction";
    }
    
    /**
     * @dev Override transfer to include ERC-1404 restrictions
     */
    function transfer(address to, uint256 amount) public override returns (bool) {
        uint8 restriction = detectTransferRestriction(msg.sender, to, amount);
        require(restriction == 0, messageForTransferRestriction(restriction));
        return super.transfer(to, amount);
    }
    
    /**
     * @dev Override transferFrom to include ERC-1404 restrictions
     */
    function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
        uint8 restriction = detectTransferRestriction(from, to, amount);
        require(restriction == 0, messageForTransferRestriction(restriction));
        return super.transferFrom(from, to, amount);
    }
    
    // Admin functions
    function addAllowedRecipient(address recipient) external onlyOwner {
        allowedRecipients[recipient] = true;
    }
    
    function removeAllowedRecipient(address recipient) external onlyOwner {
        allowedRecipients[recipient] = false;
    }
    
    function addRestrictedAddress(address addr) external onlyOwner {
        restrictedAddresses[addr] = true;
    }
    
    function removeRestrictedAddress(address addr) external onlyOwner {
        restrictedAddresses[addr] = false;
    }
    
    function pause() external onlyOwner {
        _pause();
    }
    
    function unpause() external onlyOwner {
        _unpause();
    }
    
    // Utility functions
    function _isContract(address account) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(account)
        }
        return size > 0;
    }
    
    /**
     * @dev Get total staking information for an address
     * @param staker Address to query
     * @return totalAmount Total staked amount
     * @return activeStakes Number of active stakes
     * @return totalRewards Total pending rewards
     */
    function getStakingInfo(address staker) external view returns (
        uint256 totalAmount,
        uint256 activeStakes,
        uint256 totalRewards
    ) {
        totalAmount = totalStaked[staker];
        
        for (uint256 i = 0; i < stakes[staker].length; i++) {
            if (stakes[staker][i].active) {
                activeStakes++;
                totalRewards += calculateStakingReward(staker, i);
            }
        }
    }
    
    /**
     * @dev Get proposal information
     * @param proposalId ID of the proposal
     * @return description Proposal description
     * @return votesFor Votes in favor
     * @return votesAgainst Votes against
     * @return endTime Voting end time
     * @return executed Whether proposal was executed
     */
    function getProposal(uint256 proposalId) external view returns (
        string memory description,
        uint256 votesFor,
        uint256 votesAgainst,
        uint256 endTime,
        bool executed
    ) {
        Proposal memory proposal = proposals[proposalId];
        return (
            proposal.description,
            proposal.votesFor,
            proposal.votesAgainst,
            proposal.endTime,
            proposal.executed
        );
    }
}