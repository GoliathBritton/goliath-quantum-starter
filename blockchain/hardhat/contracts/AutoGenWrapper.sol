// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AutoGenWrapper {
    event AutoGenTaskRequested(uint256 taskId, string description);
    event AutoGenResultReceived(uint256 taskId, string result);

    mapping(uint256 => string) public taskResults;
    uint256 public taskCounter;

    address public owner;
    IERC20 public nqbaToken;
    uint256 public constant TASK_FEE = 10 * 10**18; // 10 NQBA tokens, assuming 18 decimals

    constructor(address _tokenAddress) {
        owner = msg.sender;
        nqbaToken = IERC20(_tokenAddress);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    function requestAutoGenTask(string memory description) public {
        require(nqbaToken.transferFrom(msg.sender, address(this), TASK_FEE), "Payment failed");
        taskCounter++;
        emit AutoGenTaskRequested(taskCounter, description);
        // In production, this would integrate with an oracle to trigger AutoGen agents off-chain
    }

    function fulfillAutoGenTask(uint256 taskId, string memory result) public onlyOwner {
        taskResults[taskId] = result;
        emit AutoGenResultReceived(taskId, result);
    }

    function getTaskResult(uint256 taskId) public view returns (string memory) {
        return taskResults[taskId];
    }
}