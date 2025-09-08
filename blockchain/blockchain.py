from .block import Block
from .transaction import Transaction
import time
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2  
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], previous_hash="0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.pending_transactions.append(transaction)
            return True
        return False

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            return False

        new_block = Block(
            index=len(self.chain),
            transactions=[tx.to_dict() for tx in self.pending_transactions],
            previous_hash=self.chain[-1].hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        # Clear pending transactions and reward miner
        reward_tx = Transaction(
            sender="Network",
            recipient=miner_address,
            product_id="reward",
            product_name="Mining Reward",
            location="N/A",
            temperature=0,
            humidity=0,
            transport_info="N/A"
        )
        self.pending_transactions = [reward_tx]
        return new_block

    def get_latest_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def to_dict(self):
        return [block.to_dict() for block in self.chain]
