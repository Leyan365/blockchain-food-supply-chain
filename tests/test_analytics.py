import unittest

from app import create_app
from services.analytics_service import analytics_service


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app("dev")
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def test_service_defaults_to_all_supply_chain_data(self):
        all_payload = analytics_service.get_dashboard_analytics(filters={"status": "Registered"})
        payload = analytics_service.get_dashboard_analytics(
            filters={"status": "Registered"},
            username="farmer1@example.com",
            role="farmer",
        )

        self.assertIn("kpis", payload)
        self.assertIn("insights", payload)
        self.assertIn("available_filters", payload)
        self.assertIn("status_chart", payload["charts"])
        self.assertEqual(payload["scope"], "All supply-chain activity")
        self.assertEqual(payload["kpis"]["total_transactions"], all_payload["kpis"]["total_transactions"])

    def test_service_can_filter_to_logged_in_user_activity(self):
        all_payload = analytics_service.get_dashboard_analytics(
            username="farmer1@example.com",
            role="farmer",
        )
        mine_payload = analytics_service.get_dashboard_analytics(
            filters={"data_scope": "mine"},
            username="farmer1@example.com",
            role="farmer",
        )

        self.assertEqual(mine_payload["scope"], "My Farmer activity")
        self.assertLessEqual(
            mine_payload["kpis"]["total_transactions"],
            all_payload["kpis"]["total_transactions"],
        )

    def test_analytics_page_renders_for_logged_in_user_with_filters(self):
        self.client.post(
            "/auth/login",
            data={"username": "farmer1@example.com", "password": "pass123"},
        )

        response = self.client.get("/analytics/overview?data_scope=mine&status=Registered&anomalies_only=1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Supply Chain Analytics", response.data)
        self.assertIn(b"My activity", response.data)
        self.assertIn(b"Key Insights", response.data)
        self.assertIn(b"Temperature Anomaly Report", response.data)


if __name__ == "__main__":
    unittest.main()
