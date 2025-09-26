from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes.partners import router as partners_router
from .routes.leads import router as leads_router
from .routes.qnexus import router as qnexus_router
from .routes.diversegy import router as diversegy_router
from .routes.auth import router as auth_router
from .routes.aiprm import router as aiprm_router
from .routes.entitlements import router as entitlements_router
from .routes.security import router as security_router
# from .routes.performance import router as performance_router
from .routes.dynex import router as dynex_router
from .routes.stripe import router as stripe_router
from .routes.diversegy import router as diversegy_router
from .routes.sigma_router import sigma_router
from .security.middleware import SecurityMiddleware
import uvicorn
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src'))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from pathlib import Path
project_root = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.append(str(project_root))
# sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))
# from quantum.reasoning import reversal_reasoning_sync
from typing import Dict, Any
from web3 import Web3
import os
import json
from fastapi import APIRouter, Body
from procedures.mcp_orchestrator import MCPOrchestrator

app = FastAPI(
    title="NQBA Quantum Sales API",
    description="Demo API for Quantum-Enhanced Sales Intelligence",
    version="1.0.0"
)

# Security middleware (should be added first)
# app.add_middleware(
#     SecurityMiddleware,
#     enable_rate_limiting=True,
#     enable_audit_logging=True,
#     enable_ip_filtering=True,
#     enable_compliance_checks=True
# )

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(partners_router, prefix="/api/partners", tags=["partners"])
app.include_router(leads_router, prefix="/api/leads", tags=["leads"])
app.include_router(diversegy_router, prefix="/api/diversegy", tags=["diversegy"])
app.include_router(qnexus_router, prefix="/api/quantum-nexus-engine", tags=["quantum-nexus-engine"])
app.include_router(aiprm_router, prefix="/api/aiprm", tags=["aiprm"])
app.include_router(stripe_router, prefix="/api", tags=["stripe"])
app.include_router(entitlements_router, prefix="/api", tags=["entitlements"])
app.include_router(security_router, prefix="/api/security", tags=["security"])
# app.include_router(performance_router, prefix="/api/performance", tags=["performance"])
app.include_router(dynex_router, prefix="/api/dynex", tags=["dynex"])
app.include_router(sigma_router, prefix="/api/sigma", tags=["sigma"])

# from quantum.quantum_job_manager import QuantumJobManager

from .dynex_client import dynex_client
# from qdllm.core.nuco_client import NucoClient

# nuco_client = NucoClient("test_key")  # FLYFOX AI: Use environment variable for production

# @app.post("/api/compute/submit")
# async def submit_compute(payload: Dict[str, Any]):
#     manager = QuantumJobManager(dynex_client, nuco_client)
#     job_id = manager.submit_job(payload)
#     return {"job_id": job_id, "estimated_cost": "70% < AWS"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "brand": "FLYFOX AI - Goliath of All Trade - Sigma Select"
        }
    )

@app.get("/")
async def root():
    return {
        "message": "NQBA Quantum Sales API",
        "version": "1.0.0",
        "status": "operational",
        "quantum_enhanced": True,
        "brand": "FLYFOX AI - Goliath of All Trade - Sigma Select"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "quantum_core": "operational",
        "dynex_simulation": "active",
        "brand": "FLYFOX AI - Goliath of All Trade - Sigma Select"
    }

@app.websocket("/ws/qdllm-status")
async def qdllm_status_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Example status using reversal_reasoning
            await websocket.send_json({
                "type": "status_update",
                "data": {"status": "operational"}  # Placeholder since quantum.reasoning is unavailable
            })
            await asyncio.sleep(10)  # Update every 10 seconds
    except WebSocketDisconnect:
        print("WebSocket disconnected")

# Web3 Initialization for local Hardhat node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
if not web3.is_connected():
    print("Warning: Web3 not connected to local node")
else:
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    def load_abi(contract_name):
        artifact_path = os.path.join(project_root, 'blockchain', 'hardhat', 'artifacts', 'contracts', f'{contract_name}.sol', f'{contract_name}.json')
        with open(artifact_path) as f:
            return json.load(f)['abi']
    contracts = {}
    contract_list = [
        ('NQBAToken', '0xE6E340D132b5f46d1e472DebcD681B2aBc16e57E'),
        ('MCPWrapper', '0xc3e53F4d16Ae77Db1c982e75a937B9f60FE63690'),
        ('DAOGovernance', '0x84eA74d481Ee0A5332c457a4d796187F6Ba67fEB'),
        ('PennyLaneWrapper', '0x9E545E3C0baAB3E08CdfD552C960A1050f373042'),
        ('AutoGenWrapper', '0xa82fF9aFd8f496c3d6ac40E2a0F282E47488CFc9'),
        ('AkashWrapper', '0x1613beB3B2C4f22Ee086B2b38C1476A3cE7f78E8'),
        ('BubbleWrapper', '0x851356ae760d987E095750cCeb3bC6014560891C'),
        ('MCPNFT', '0xf5059a5D33d5853360D16C683c16e67980206f36'),
    ]
    for name, addr in contract_list:
        abi = load_abi(name)
        contracts[name] = web3.eth.contract(address=addr, abi=abi)

    web3_router = APIRouter(prefix="/web3")

    @app.post("/web3/request-task/{wrapper_name}")
    def request_task(wrapper_name: str, description: str = Body(...)):
        if wrapper_name not in contracts:
            raise HTTPException(status_code=400, detail="Invalid wrapper")
        contract = contracts[wrapper_name]
        if wrapper_name == 'DAOGovernance':
            function_name = "createProposal"
        else:
            function_name = f"request{wrapper_name.replace('Wrapper', '')}Task"
        account_private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
        account = web3.eth.account.from_key(account_private_key)
        nonce = web3.eth.get_transaction_count(account.address)
        if wrapper_name != 'DAOGovernance':
            token = contracts['NQBAToken']
            task_fee = contract.functions.TASK_FEE().call()
            approve_tx = token.functions.approve(contract.address, task_fee).build_transaction({
                'chainId': 31337,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei'),
                'nonce': nonce,
            })
            signed_approve_tx = account.sign_transaction(approve_tx)
            web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
            web3.eth.wait_for_transaction_receipt(signed_approve_tx.hash)
            nonce += 1
        txn = contract.functions[function_name](description).build_transaction({
            'chainId': 31337,
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = account.sign_transaction(txn)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return {"transaction_hash": tx_hash.hex(), "receipt": tx_receipt}

    @web3_router.post("/mint-nft")
    def mint_nft(to: str = Body(...), domain: str = Body(...)):
        contract = contracts['MCPNFT']
        account_private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
        account = web3.eth.account.from_key(account_private_key)
        nonce = web3.eth.get_transaction_count(account.address)
        tx = contract.functions.mint(to, domain).build_transaction({
            'chainId': 31337,
            'gas': 2000000,
            'gasPrice': web3.to_wei('1', 'gwei'),
            'nonce': nonce,
        })
        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # Assuming token ID starts from 1
        return {"transaction_hash": tx_hash.hex(), "status": tx_receipt.status, "token_id": 1}
    app.include_router(web3_router, tags=["web3"])

    mcp_router = APIRouter(prefix="/mcp")
    @mcp_router.post("/orchestrate")
    def orchestrate_content(input_data: str = Body(...), domain: str = "finance", token_id: int = None):
        orchestrator = MCPOrchestrator(framework=contracts['DAOGovernance'])
        return orchestrator.orchestrate_content(input_data, domain, token_id)
    app.include_router(mcp_router, tags=["mcp"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)