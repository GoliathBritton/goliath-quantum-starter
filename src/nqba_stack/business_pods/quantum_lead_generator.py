"""
Quantum AI Lead Generator: Best-in-class, buyer-intent business leads for your ecosystem and clients.
Automated by Quantum AI Architects.
"""

import pandas as pd
import random
from faker import Faker

fake = Faker()

INDUSTRIES = [
    "Energy",
    "Finance",
    "Manufacturing",
    "Healthcare",
    "Retail",
    "Logistics",
    "AI/ML",
    "Quantum Computing",
]
BUDGETS = ["very high", "high", "medium", "low"]
URGENCIES = ["very urgent", "urgent", "normal", "low"]
PAIN_POINTS = [
    "energy costs",
    "production delays",
    "compliance risk",
    "supply chain",
    "AI adoption",
    "quantum readiness",
    "market volatility",
]
BUYER_INTENT = ["hot", "warm", "cold"]


def generate_leads(n=50):
    leads = []
    for _ in range(n):
        lead = {
            "company": fake.company(),
            "contact": fake.name(),
            "email": fake.company_email(),
            "industry": random.choice(INDUSTRIES),
            "budget": random.choices(BUDGETS, weights=[0.2, 0.4, 0.3, 0.1])[0],
            "urgency": random.choices(URGENCIES, weights=[0.2, 0.4, 0.3, 0.1])[0],
            "pain_points": random.sample(PAIN_POINTS, k=random.randint(1, 3)),
            "buyer_intent": random.choices(BUYER_INTENT, weights=[0.5, 0.3, 0.2])[0],
            "quantum_fit": random.choice([True, False]),
            "notes": fake.sentence(),
        }
        leads.append(lead)
    return pd.DataFrame(leads)


if __name__ == "__main__":
    df = generate_leads(100)
    df.to_csv("quantum_buyer_intent_leads.csv", index=False)
    print(
        "Generated 100 best-in-class quantum buyer intent leads: quantum_buyer_intent_leads.csv"
    )
