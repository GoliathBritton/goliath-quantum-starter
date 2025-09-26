from nqba.core.intelligence.qdllm.engine import QuantumDiffusionEngine as QdLLMEngine
from nqba.core.intelligence.qnlp.processor import QNLPProcessor
from nqba.aiprm import ModelContentProtocol
# from dynex import DynexRuntime  # Commented out as DynexRuntime is not available
from core.web3_connector import Web3Connector
import os
from qdllm.core.nuco_client import NucoClient

class MCPOrchestrator:
    def __init__(self, framework):
        self.framework = framework
        self.mcp = ModelContentProtocol()
        self.qdllm = QdLLMEngine(use_simulator=True, qdllm_params=400_000_000_000)
        self.qnlp = QNLPProcessor()
        # self.dynex = DynexRuntime(os.getenv("DYNEX_API_KEY")) if os.getenv("DYNEX_API_KEY") else None
        self.dynex = None  # Temporarily set to None as DynexRuntime is not available
        self.nuco = NucoClient(os.getenv("NUCO_API_KEY")) if os.getenv("NUCO_API_KEY") else None
        self.web3 = Web3Connector(os.getenv("WEB3_PROVIDER_URL"), os.getenv("MCP_NFT_CONTRACT_ADDRESS"))

    def orchestrate_content(self, input_data: str, domain: str = "finance", token_id: int = None) -> dict:
        # Web3: Verify NFT access
        if token_id and not self.web3.verify_nft(token_id, domain):
            return {"error": "Invalid or missing NFT for domain access"}
        
        # MCP processing
        mcp_content = self.mcp.format_content(input_data, domain=domain)
        # Dynamic: Use nuco.cloud if available, fallback to Dynex, then local
        if self.nuco:
            mcp_content = self.nuco.accelerate(mcp_content)
        elif self.dynex:
            mcp_content = self.dynex.accelerate(mcp_content)
        reasoning = self.qdllm.reason(mcp_content["premise"], mcp_content["desired_outcome"])
        sentiment = self.qnlp.analyze_sentiment(mcp_content["text"])
        # Dynamic: Reprocess for high coherence
        if float(reasoning["coherence"].strip("%")) / 100 < 0.9:
            reasoning = self.qdllm.reprocess_with_context(mcp_content["text"] + " [refine]")
        # Store output on IPFS
        ipfs_hash = self.web3.store_on_ipfs(mcp_content)
        return {
            "mcp_output": mcp_content,
            "reasoning": reasoning,
            "sentiment": sentiment,
            "compliance": self.framework.governance.validate(mcp_content),
            "ipfs_hash": ipfs_hash,
            "backend": "nuco" if self.nuco else ("dynex" if self.dynex else "local")
        }