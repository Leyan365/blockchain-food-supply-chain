import unittest

from services.validation_service import (
    parse_humidity,
    parse_temperature,
    validate_email_like,
    validate_optional_date,
    validate_required_fields,
)


class ValidationServiceTests(unittest.TestCase):
    def test_required_fields_collects_missing_values(self):
        cleaned, errors = validate_required_fields({"name": "  "}, {"name": "Name"})

        self.assertEqual(cleaned["name"], "")
        self.assertEqual(errors, ["Name is required."])

    def test_temperature_must_be_numeric_and_reasonable(self):
        self.assertEqual(parse_temperature("12.5"), (12.5, None))
        self.assertEqual(parse_temperature("hot")[1], "Temperature must be a number.")
        self.assertEqual(parse_temperature("100")[1], "Temperature must be at most 60.")

    def test_humidity_must_be_between_zero_and_one_hundred(self):
        self.assertEqual(parse_humidity("80"), (80.0, None))
        self.assertEqual(parse_humidity("-1")[1], "Humidity must be at least 0.")
        self.assertEqual(parse_humidity("101")[1], "Humidity must be at most 100.")

    def test_email_like_validation(self):
        self.assertIsNone(validate_email_like("demo@example.com", "Recipient"))
        self.assertEqual(
            validate_email_like("not-an-email", "Recipient"),
            "Recipient must be a valid email address.",
        )

    def test_optional_date_validation(self):
        self.assertIsNone(validate_optional_date("", "Expiry date"))
        self.assertIsNone(validate_optional_date("2026-05-20", "Expiry date"))
        self.assertEqual(
            validate_optional_date("20-05-2026", "Expiry date"),
            "Expiry date must use YYYY-MM-DD format.",
        )


if __name__ == "__main__":
    unittest.main()
