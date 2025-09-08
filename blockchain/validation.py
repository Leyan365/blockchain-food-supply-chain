import hashlib
import json

def is_valid_proof(block, difficulty):
    """
    Checks if block hash starts with the correct number of leading zeros.
    """
    return block.hash.startswith('0' * difficulty)

def is_valid_block(current_block, previous_block, difficulty):
    """
    Validates a single block against its predecessor and proof of work.
    """
    if current_block.previous_hash != previous_block.hash:
        return False

    if current_block.hash != current_block.compute_hash():
        return False

    if not is_valid_proof(current_block, difficulty):
        return False

    return True

def is_valid_chain(chain, difficulty):
    """
    Validates the entire blockchain.
    """
    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        if not is_valid_block(current, previous, difficulty):
            return False
    return True
