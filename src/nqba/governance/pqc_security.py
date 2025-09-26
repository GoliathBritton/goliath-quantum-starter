"""Post-Quantum Cryptography Security Module for NQBA Governance

This module provides post-quantum secure signature and key encapsulation using liboqs-python.
"""

import oqs

class PQCSignature:
    def __init__(self, alg="ML-DSA-44"):
        self.alg = alg
        self.signer = oqs.Signature(alg)
        self.verifier = oqs.Signature(alg)
        self.public_key = None
        self.secret_key = None

    def generate_keypair(self):
        self.public_key = self.signer.generate_keypair()
        self.secret_key = self.signer.export_secret_key()
        return self.public_key

    def sign(self, message: bytes) -> bytes:
        return self.signer.sign(message)

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        return self.verifier.verify(message, signature, public_key)

class PQCKeyEncapsulation:
    def __init__(self, alg="ML-KEM-512"):
        self.alg = alg
        self.kem = oqs.KeyEncapsulation(alg)

    def generate_keypair(self):
        return self.kem.generate_keypair()

    def encaps(self, public_key: bytes) -> tuple:
        return self.kem.encaps(public_key)

    def decaps(self, ciphertext: bytes) -> bytes:
        return self.kem.decaps(ciphertext)