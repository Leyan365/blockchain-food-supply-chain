import os
import json

from blockchain.blockchain import Blockchain
from blockchain.block import Block
from blockchain.transaction import Transaction
from datetime import datetime

class BlockchainService:
    def __init__(self):
        self.data_file = 'data/blockchain_data.json'
        if os.path.exists(self.data_file):
            print("Loading blockchain from file...")
            self.blockchain = self._load_blockchain_from_file()
        else:
            print("Creating new blockchain...")
            self.blockchain = Blockchain()
            self.save_blockchain_to_file()

    def _load_blockchain_from_file(self):
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            loaded_blockchain = Blockchain()
            loaded_blockchain.chain = []
            for block_data in data['chain']:
                block_instance = Block(
                    index=block_data['index'],
                    transactions=block_data['transactions'],
                    timestamp=block_data['timestamp'],
                    previous_hash=block_data['previous_hash'],
                    nonce=block_data.get('proof', block_data.get('nonce', 0))
                )
                block_instance.hash = block_data['hash']
                loaded_blockchain.chain.append(block_instance)
            loaded_blockchain.pending_transactions = [
                Transaction(**tx_data) for tx_data in data.get('pending_transactions', [])
            ]
            return loaded_blockchain
        except (IOError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading blockchain file: {e}. Starting with a new blockchain.")
            return Blockchain()

    def save_blockchain_to_file(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        data = {
            'chain': [block.to_dict() for block in self.blockchain.chain],
            'pending_transactions': [tx.to_dict() for tx in self.blockchain.pending_transactions]
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("Blockchain saved to file.")

    def add_transaction(self, tx_data):
        """
        Creates a new transaction. If a timestamp is provided in tx_data, it uses it.
        Otherwise, it defaults to the current time.
        """
        
        if "timestamp" not in tx_data or tx_data.get("timestamp") is None:
            tx_data["timestamp"] = datetime.now().timestamp()
        
        
        transaction = Transaction(
            sender=tx_data["sender"],
            recipient=tx_data["recipient"],
            product_id=tx_data["product_id"],
            product_name=tx_data["product_name"],
            location=tx_data["location"],
            temperature=tx_data["temperature"],
            humidity=tx_data["humidity"],
            transport_info=tx_data["transport_info"],
            status=tx_data["status"],
            timestamp=tx_data["timestamp"],
            expiry_date=tx_data.get("expiry_date")
        )
        self.blockchain.add_transaction(transaction)
        
        self.mine_block(miner_address="placeholder_miner_address")
        
        self.save_blockchain_to_file()
        
        return True

    def get_all_transactions(self):
        all_transactions = []
        for block in self.blockchain.chain:
            all_transactions.extend(block.transactions)
        all_transactions.extend([tx.to_dict() for tx in self.blockchain.pending_transactions])
        return all_transactions

    def is_system_transaction(self, tx):
        return tx.get("sender") == "Network" or tx.get("product_id") == "reward"

    def get_supply_chain_transactions(self):
        return [
            tx for tx in self.get_all_transactions()
            if not self.is_system_transaction(tx)
        ]

    def get_latest_tx_for_product(self, product_id):
        for block in reversed(self.blockchain.chain):
            for tx in reversed(block.transactions):
                if tx.get("product_id") == product_id:
                    return tx
        return None

    def mine_block(self, miner_address):
        block = self.blockchain.mine_pending_transactions(miner_address)
        return block

    def get_full_chain(self):
        return self.blockchain.chain

    def get_pending_transactions(self):
        return self.blockchain.pending_transactions

    def get_transaction_history(self, product_id):
        history = []
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.get('product_id') == product_id:
                    history.append(tx)
        return sorted(history, key=lambda tx: tx.get("timestamp", 0))

    def get_product_summaries(self):
        latest_by_product = {}
        for tx in self.get_supply_chain_transactions():
            product_id = tx.get("product_id")
            if not product_id:
                continue
            if product_id not in latest_by_product or tx.get("timestamp", 0) > latest_by_product[product_id].get("timestamp", 0):
                latest_by_product[product_id] = tx
        return sorted(latest_by_product.values(), key=lambda tx: tx.get("timestamp", 0), reverse=True)

    def get_blockchain(self):
        return self.blockchain

blockchain_service = BlockchainService()
