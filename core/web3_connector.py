import web3
from web3 import Web3
from pinatapy import PinataPy
import json
import os

class Web3Connector:
    def __init__(self, provider_url: str, contract_address: str):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_address = contract_address
        self.contract = self.w3.eth.contract(address=contract_address, abi=load_abi('MCPNFT'))

    def verify_nft(self, token_id: int, domain: str) -> bool:
        return self.contract.functions.verifyAccess(token_id, domain).call()

    def store_on_ipfs(self, data: dict) -> str:
        pinata = PinataPy(os.getenv("PINATA_API_KEY"), os.getenv("PINATA_SECRET_API_KEY"))
        response = pinata.pin_json_to_ipfs(data)
        return response["IpfsHash"]

    def load_abi(contract_name):
        artifact_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web3', 'hardhat', 'artifacts', 'contracts', f'{contract_name}.sol', f'{contract_name}.json')
        with open(artifact_path) as f:
            return json.load(f)['abi']