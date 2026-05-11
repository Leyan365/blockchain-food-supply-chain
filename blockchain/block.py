import time
import hashlib
import json
from .mining import proof_of_work  

class Block:
    def __init__(self, index, transactions, timestamp=None, previous_hash="", nonce=0):
        self.index = index
        self.transactions = transactions  
        self.timestamp = timestamp or time.time()
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        Returns the SHA-256 hash of the block contents.
        """
        block_data = {
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """
        Runs proof_of_work to find a valid hash, then sets self.hash.
        """
        self.hash = proof_of_work(self, difficulty)

    def to_dict(self):
        """
        Converts the block's attributes into a dictionary for serialization.
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions, 
            'proof': self.nonce,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

    @property
    def proof(self):
        return self.nonce
    
    def __repr__(self):
        return f"Block<index: {self.index}, hash: {self.hash[:10]}..., prev_hash: {self.previous_hash[:10]}...>"
