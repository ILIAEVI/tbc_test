import re
from collections import defaultdict
import pprint
import json
import time


def process_applicant_transfers(applicants: list):
    if not isinstance(applicants, list):
        raise TypeError("Expected parameter to be a list.")
    if not applicants:
        raise ValueError("Applicants list cannot be empty.")

    result = []

    for idx, applicant in enumerate(applicants):
        applicant_id = validate_applicant(applicant, idx)

        transfers = applicant.get("transfers")

        if transfers is None or not transfers:
            raise ValueError(f"Missing 'transfers', or it is empty for applicant_id: {applicant_id}.")

        if not isinstance(transfers, list):
            raise TypeError(f"'transfers' must be list for applicant_id: {applicant_id}.")

        grouped = defaultdict(lambda: {"amount_gel": 0.0, "sources": set()})

        for transfer in transfers:
            country, period, source, amount_gel = validate_transfer(transfer, applicant_id)

            key = (country, period)
            grouped[key]["amount_gel"] += float(amount_gel)
            grouped[key]["sources"].add(str(source))

        grouped_transfers = [
            {
                "country": country,
                "period": period,
                "amount_gel": round(data["amount_gel"], 2),
                "sources": "/".join(sorted(data["sources"]))
            }
            for (country, period), data in grouped.items()
        ]

        grouped_transfers.sort(key=lambda x: (x["country"], x["period"]))

        result.append({
            "applicant_id": applicant["applicant_id"],
            "transfers": grouped_transfers
        })

    return result


def validate_applicant(applicant, index):
    if not isinstance(applicant, dict):
        raise TypeError(f"Applicant at index {index} must be a dictionary.")

    applicant_id = applicant.get("applicant_id")
    if applicant_id is None:
        raise ValueError(f"Missing 'applicant_id' in applicant at index: {index}.")

    if not isinstance(applicant_id, str):
        raise TypeError(f"'applicant_id' must be a string in applicant at index: {index}.")

    if not re.fullmatch(r"APP_\d+", applicant_id):
        raise ValueError(f"'applicant_id' must match format 'APP_<number>' at index {index}, got '{applicant_id}'.")

    return applicant_id


def validate_transfer(transfer, applicant_id):
    required_fields = ["country", "period", "source", "amountgel"]

    if not isinstance(transfer, dict):
        raise TypeError(f"Transfer for applicant_id: {applicant_id} must be a dictionary.")

    for field in required_fields:
        if field not in transfer:
            raise ValueError(f"Missing '{field}' in transfer for applicant_id: {applicant_id}.")

    country = transfer["country"]
    period = transfer["period"]
    source = transfer["source"]
    amount_gel = transfer["amountgel"]

    if not isinstance(country, str):
        raise TypeError(f"'country' must be a string in transfer for applicant_id: {applicant_id}.")
    if not country:
        raise ValueError(f"'country' cannot be empty in transfer for applicant_id: {applicant_id}.")

    if not isinstance(source, str):
        raise TypeError(f"'source' must be a string in transfer for applicant_id: {applicant_id}.")
    if not source:
        raise ValueError(f"'source' cannot be empty in transfer for applicant_id: {applicant_id}.")

    if not isinstance(period, int):
        raise TypeError(f"'period' must be an integer in transfer for applicant_id: {applicant_id}.")
    if period < 0:
        raise ValueError(f"'period' must be a non-negative integer in transfer for applicant_id: {applicant_id}.")

    if not isinstance(amount_gel, (int, float)):
        raise TypeError(f"'amountgel' must be a number in transfer for applicant_id: {applicant_id}.")
    if amount_gel <= 0:
        raise ValueError(f"'amountgel' must be a positive number in transfer for applicant_id: {applicant_id}.")

    return country, period, source, float(amount_gel)


test_data = [
    {
        "applicant_id": "APP_001",
        "transfers": [
            {"country": "USA", "period": 1, "amountgel": 100.0, "source": "A"},
            {"country": "USA", "period": 1, "amountgel": 50.0, "source": "B"},
            {"country": "GE", "period": 2, "amountgel": 200.0, "source": "M"},
            {"country": "USA", "period": 2, "amountgel": 75.0, "source": "A"},
            {"country": "GE", "period": 1, "amountgel": 120.0, "source": "B"},
        ]
    },
    {
        "applicant_id": "APP_002",
        "transfers": [
            {"country": "UK", "period": 1, "amountgel": 300.0, "source": "C"},
            {"country": "UK", "period": 1, "amountgel": 100.0, "source": "A"},
        ]
    }
]

if __name__ == "__main__":
    start_time = time.time()
    try:
        with open("applicants_data.json", "r") as f:
            applicants = json.load(f)
    except FileNotFoundError:
        applicants = test_data

    result = process_applicant_transfers(applicants)

    with open("processed_data.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"Processed {len(result)} applicants")
