// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DAOGovernance is Ownable {
    IERC20 public governanceToken;
    uint256 public proposalCount;
    uint256 public minimumQuorum;
    uint256 public votingPeriod;

    struct Proposal {
        uint256 id;
        string description;
        uint256 voteCount;
        uint256 deadline;
        bool executed;
        mapping(address => bool) voters;
    }

    mapping(uint256 => Proposal) public proposals;

    event ProposalCreated(uint256 id, string description, uint256 deadline);
    event Voted(uint256 proposalId, address voter, uint256 votes);
    event ProposalExecuted(uint256 id);

    constructor(address _tokenAddress, uint256 _minimumQuorum, uint256 _votingPeriod, address initialOwner) Ownable(initialOwner) {
        governanceToken = IERC20(_tokenAddress);
        minimumQuorum = _minimumQuorum;
        votingPeriod = _votingPeriod;
    }

    function createProposal(string memory description) public onlyOwner {
        proposalCount++;
        Proposal storage p = proposals[proposalCount];
        p.id = proposalCount;
        p.description = description;
        p.deadline = block.timestamp + votingPeriod;
        p.executed = false;
        emit ProposalCreated(proposalCount, description, p.deadline);
    }

    function vote(uint256 proposalId) public {
        Proposal storage p = proposals[proposalId];
        require(block.timestamp < p.deadline, "Voting period ended");
        require(!p.voters[msg.sender], "Already voted");

        uint256 votes = governanceToken.balanceOf(msg.sender);
        require(votes > 0, "No governance tokens");

        p.voteCount += votes;
        p.voters[msg.sender] = true;
        emit Voted(proposalId, msg.sender, votes);
    }

    function executeProposal(uint256 proposalId) public onlyOwner {
        Proposal storage p = proposals[proposalId];
        require(block.timestamp >= p.deadline, "Voting period not ended");
        require(!p.executed, "Already executed");
        require(p.voteCount >= minimumQuorum, "Quorum not met");

        p.executed = true;
        // Here, execute the proposal action (e.g., upgrade feature)
        emit ProposalExecuted(proposalId);
    }
}