import unittest

from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction


class BlockchainTests(unittest.TestCase):
    def test_transaction_preserves_expiry_date(self):
        tx = Transaction(
            sender="retailer@example.com",
            recipient="consumer@example.com",
            product_id="product-1",
            product_name="Tomatoes",
            expiry_date="2026-05-20",
        )

        self.assertEqual(tx.to_dict()["expiry_date"], "2026-05-20")

    def test_mined_chain_is_valid_and_exposes_proof(self):
        chain = Blockchain()
        tx = Transaction(
            sender="farmer@example.com",
            recipient="distributor@example.com",
            product_id="product-1",
            product_name="Tomatoes",
        )

        self.assertTrue(chain.add_transaction(tx))
        mined_block = chain.mine_pending_transactions("miner")

        self.assertTrue(mined_block.hash.startswith("0" * chain.difficulty))
        self.assertEqual(mined_block.proof, mined_block.nonce)
        self.assertTrue(chain.is_chain_valid())


if __name__ == "__main__":
    unittest.main()
