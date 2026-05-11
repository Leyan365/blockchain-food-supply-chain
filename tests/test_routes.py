import unittest

from app import create_app
from services.blockchain_service import blockchain_service


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("dev")
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def test_consumer_dashboard_loads(self):
        response = self.client.get("/consumer/dashboard")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Track a Product", response.data)

    def test_short_tracking_link_redirects_to_consumer_tracking(self):
        summaries = blockchain_service.get_product_summaries()
        if not summaries:
            self.skipTest("No product data available for route test.")

        product_id = summaries[0]["product_id"]
        response = self.client.get(f"/track/{product_id}")

        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/consumer/track/{product_id}", response.headers["Location"])

    def test_product_tracking_page_shows_known_history(self):
        summaries = blockchain_service.get_product_summaries()
        if not summaries:
            self.skipTest("No product data available for route test.")

        product_id = summaries[0]["product_id"]
        response = self.client.get(f"/consumer/track/{product_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(product_id.encode(), response.data)
        self.assertIn(b"Journey History", response.data)

    def test_role_dashboard_requires_login(self):
        response = self.client.get("/farmer/dashboard", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/auth/login", response.headers["Location"])

    def test_wrong_role_cannot_access_farmer_dashboard(self):
        self.client.post(
            "/auth/login",
            data={"username": "dist1@example.com", "password": "pass123"},
        )

        response = self.client.get("/farmer/dashboard", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/distributor/dashboard", response.headers["Location"])

    def test_wrong_role_cannot_access_distributor_dashboard(self):
        self.client.post(
            "/auth/login",
            data={"username": "retail1@example.com", "password": "pass123"},
        )

        response = self.client.get("/distributor/dashboard", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/retailer/dashboard", response.headers["Location"])

    def test_wrong_role_cannot_access_retailer_dashboard(self):
        self.client.post(
            "/auth/login",
            data={"username": "farmer1@example.com", "password": "pass123"},
        )

        response = self.client.get("/retailer/dashboard", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/farmer/dashboard", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
