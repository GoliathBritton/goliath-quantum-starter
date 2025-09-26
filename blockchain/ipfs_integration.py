"""
IPFS Integration Scaffold
"""

import ipfshttpclient
import json
import tempfile

def add_file(filepath):
    client = ipfshttpclient.connect()
    res = client.add(filepath)
    return res["Hash"]

def add_json(data: dict) -> str:
    """Add JSON data to IPFS and return CID"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        json.dump(data, tmp)
        tmp_path = tmp.name
    cid = add_file(tmp_path)
    import os
    os.unlink(tmp_path)
    return cid
