import unittest
from fixed_version import calculate_payments  # Replace with your actual file/module


class TestCalculatePayments(unittest.TestCase):

    def test_single_payment(self):
        applicants = [
            {
                "currency": "usd",
                "payments": [{"amount": 100, "base": 2, "incomeshare": 1, "active": True}]
            }
        ]
        result = calculate_payments(applicants)
        self.assertEqual(result, {"USD": 50.0})

    def test_multiple_applicants_and_currencies(self):
        applicants = [
            {
                "currency": "usd",
                "payments": [
                    {"active": True, "incomeshare": 0.2, "amount": 1000, "base": 0.5}
                ]
            },
            {
                "currency": "gel",
                "payments": [
                    {"active": True, "incomeshare": 0.2, "amount": 500, "base": 0.4}
                ]
            }
        ]
        result = calculate_payments(applicants)
        self.assertEqual(result, {"GEL": 250.0, "USD": 400.0})

    def test_inactive_payments_ignored(self):
        applicants = [
            {
                "currency": "usd",
                "payments": [
                    {"amount": 100, "base": 2, "incomeshare": 1, "active": False},
                    {"amount": 50, "base": 5, "incomeshare": 2}
                ]
            }
        ]
        result = calculate_payments(applicants)
        self.assertEqual(result, {"USD": 20.0})

    def test_missing_currency_raises_error(self):
        applicants = [
            {
                "payments": [
                    {"active": True, "incomeshare": 0.2, "amount": 1000, "base": 0.5}
                ]
            }
        ]
        with self.assertRaises(ValueError):
            calculate_payments(applicants)

    def test_invalid_base_zero(self):
        applicants = [
            {
                "currency": "USD",
                "payments": [
                    {"active": True, "incomeshare": 0.2, "amount": 1000, "base": 0}
                ]
            }
        ]
        with self.assertRaises(ZeroDivisionError):
            calculate_payments(applicants)

    def test_invalid_payment_type(self):
        applicants = [
            {
                "currency": "USD",
                "payments": ["not a dict"]
            }
        ]
        with self.assertRaises(TypeError):
            calculate_payments(applicants)

    def test_negative_amount_raises_error(self):
        applicants = [
            {
                "currency": "USD",
                "payments": [
                    {"active": True, "incomeshare": 0.2, "amount": -500, "base": 0.5}
                ]
            }
        ]
        with self.assertRaises(ValueError):
            calculate_payments(applicants)

    def test_missing_payments_key(self):
        applicants = [
            {
                "currency": "USD"
            }
        ]

        with self.assertRaises(TypeError) as context:
            calculate_payments(applicants)

        self.assertIn("Payments must be a list", str(context.exception))
