import unittest

from app import create_app
from services.blockchain_service import blockchain_service


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("dev")
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def test_blockchain_status_api_returns_chain_summary(self):
        response = self.client.get("/api/blockchain/status")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("chain_valid", payload)
        self.assertIn("total_blocks", payload)
        self.assertIn("total_transactions", payload)

    def test_products_api_returns_summaries(self):
        response = self.client.get("/api/products")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("products", payload)
        self.assertEqual(payload["count"], len(payload["products"]))

    def test_product_detail_and_history_api(self):
        summaries = blockchain_service.get_product_summaries()
        if not summaries:
            self.skipTest("No product data available for API test.")

        product_id = summaries[0]["product_id"]
        detail_response = self.client.get(f"/api/products/{product_id}")
        history_response = self.client.get(f"/api/products/{product_id}/history")

        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(history_response.status_code, 200)
        self.assertEqual(detail_response.get_json()["product"]["product_id"], product_id)
        self.assertEqual(history_response.get_json()["product_id"], product_id)
        self.assertGreaterEqual(history_response.get_json()["count"], 1)

    def test_unknown_product_api_returns_404(self):
        response = self.client.get("/api/products/not-a-real-product")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Product not found")


if __name__ == "__main__":
    unittest.main()
