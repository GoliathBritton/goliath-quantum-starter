"""
IPFS Integration Scaffold
"""
import ipfshttpclient

def add_file(filepath):
    client = ipfshttpclient.connect()
    res = client.add(filepath)
    return res['Hash']
