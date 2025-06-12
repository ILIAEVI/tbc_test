from pprint import pprint


def calculate_payments(applicants):
    payment_by_currency = {}
    for app in applicants:
        currency = str(app.get("currency", "GEL")).upper()
        payments = app.get("payments")
        for pay in payments:
            if pay.get("active", True):
                incomeshare = float(pay.get('incomeshare') or 1)
                base = pay.get("base")
                ratio = incomeshare / base
                amount = float(pay.get("amount", 0))
                payment_by_currency[currency] = payment_by_currency.get(currency, 0) + amount * ratio
    return payment_by_currency


applicants = [
    {
        "currency": "USD",
        "payments": [
            {
                "active": True,
                "incomeshare": 0.2,
                "amount": 1000,
                "base": 0.5
            },
            {
                "active": False,
                "incomeshare": 0.3,
                "amount": 500,
                "base": 0.4
            }
        ]
    }
]


if __name__ == "__main__":
    pprint(calculate_payments(applicants))