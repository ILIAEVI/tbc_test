import random
import json

countries = ["USA", "GE", "UK"]
sources = ["A", "B", "C", "M"]
periods = [1, 2, 3]

def generate_transfer():
    return {
        "country": random.choice(countries),
        "period": random.choice(periods),
        "amountgel": round(random.uniform(10.0, 500.0), 2),
        "source": random.choice(sources)
    }

def generate_applicant(index):
    return {
        "applicant_id": f"APP_{str(index).zfill(5)}",
        "transfers": [generate_transfer() for _ in range(random.randint(2, 6))]
    }

applicants = [generate_applicant(i) for i in range(1, 50001)]

with open("applicants_data.json", "w") as f:
    json.dump(applicants, f, indent=2)
