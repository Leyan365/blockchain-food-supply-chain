import hashlib
import json
from time import time

def proof_of_work(block, difficulty):
    """
    Performs the Proof-of-Work algorithm:
    Keep incrementing the nonce until the block hash satisfies the difficulty condition.
    """
    block.nonce = 0
    computed_hash = block.compute_hash()

    while not computed_hash.startswith('0' * difficulty):
        block.nonce += 1
        computed_hash = block.compute_hash()

    return computed_hash
