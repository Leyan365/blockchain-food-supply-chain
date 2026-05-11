import unittest

from services.user_service import user_service


class UserServiceTests(unittest.TestCase):
    def test_verify_user_password_returns_user_for_valid_password(self):
        user = user_service.verify_user_password("farmer1@example.com", "pass123")

        self.assertIsNotNone(user)
        self.assertEqual(user["role"], "farmer")
        self.assertNotIn("pass123", user.get("password_hash", ""))

    def test_verify_user_password_rejects_invalid_password(self):
        self.assertIsNone(
            user_service.verify_user_password("farmer1@example.com", "wrong")
        )

    def test_user_lookup_is_case_insensitive(self):
        user = user_service.get_user_by_email("FARMER1@EXAMPLE.COM")

        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "farmer1@example.com")


if __name__ == "__main__":
    unittest.main()
