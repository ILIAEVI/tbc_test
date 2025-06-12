from pprint import pprint


def calculate_payments(applicants):
    if not isinstance(applicants, list):
        raise TypeError("Input must be a list of applicants.")

    payment_by_currency = {}

    for app in applicants:
        currency = app.get("currency")
        if not currency or not isinstance(currency, str) or currency.strip() == "":
            raise ValueError("Currency must be non empty string and cannot be None.")
        else:
            currency = currency.strip().upper()

        payments = app.get("payments")
        if not isinstance(payments, list):
            raise TypeError("Payments must be a list")
        if not payments:
            raise ValueError("Payments must contain at least one payment.")
        for pay in payments:
            if not isinstance(pay, dict):
                raise TypeError("each payment must be a dict")
            active = pay.get("active", True)

            if not isinstance(active, bool):
                raise TypeError("active must be a bool type")

            if pay.get("active", True):  # gaachnia biznes logikas.
                try:
                    if "base" not in pay:
                        raise KeyError("Missing 'base' in payment.")

                    base = float(pay["base"])
                    if base == 0:
                        raise ZeroDivisionError("Base value cannot be zero.")

                    if "incomeshare" not in pay:
                        raise KeyError("Missing 'incomeshare' in payment.")

                    incomeshare = float(pay.get("incomeshare"))

                    if "amount" not in pay:
                        raise KeyError("Missing 'amount' in payment.")

                    amount = float(pay.get("amount"))

                    if amount < 0:
                        raise ValueError("Amount must be positive.")

                    ratio = incomeshare / base

                    payment_by_currency[currency] = payment_by_currency.get(currency, 0.0) + amount * ratio

                except (ValueError, TypeError) as e:
                    raise ValueError(f"Invalid data type in payment: {pay} — {e}")
                except KeyError as e:
                    raise KeyError(f"Missing key in payment: {e}")
                except ZeroDivisionError as e:
                    raise ZeroDivisionError(f"Payments cannot be divided by zero: {e}")
    return payment_by_currency


applicants = [
    {
        "currency": "USD",
        "payments": [
            {
                "active": True,
                "incomeshare": 0.3,
                "amount": 1000,
                "base": 0.5,
            },
            {
                "active": False,
                "incomeshare": 0.3,
                "amount": 500,
                "base": 0.4
            }
        ]
    },
    {
        "currency": "GEL",
        "payments": [
            {
                "active": True,
                "incomeshare": 0.2,
                "amount": 1000,
                "base": 0.5,
            },
            {
                "active": True,
                "incomeshare": 0.3,
                "amount": 500,
                "base": 0.4
            }
        ]
    }
]

if __name__ == "__main__":
    pprint(calculate_payments(applicants))
