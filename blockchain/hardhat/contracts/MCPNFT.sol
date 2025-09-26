// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MCPNFT is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    mapping(uint256 => string) private _templateDomains;
    
    constructor() ERC721("NQBA_MCP_Template", "MCPNFT") Ownable(msg.sender) {
        _tokenIdCounter = 0;
    }
    
    function mintNFT(address recipient, string memory domain) public onlyOwner returns (uint256) {
        _tokenIdCounter++;
        uint256 newTokenId = _tokenIdCounter;
        _safeMint(recipient, newTokenId);
        _templateDomains[newTokenId] = domain;
        return newTokenId;
    }
    
    function verifyAccess(uint256 tokenId, string memory domain) public view returns (bool) {
        return keccak256(abi.encodePacked(_templateDomains[tokenId])) == keccak256(abi.encodePacked(domain));
    }
}