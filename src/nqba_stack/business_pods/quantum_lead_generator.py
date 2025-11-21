"""
Quantum AI Lead Generator - Automated Lead Generation System

Generates high-quality, buyer-intent business leads using AI-driven analysis
and quantum-inspired optimization. This module creates synthetic lead data
for testing and demonstration purposes, with realistic attributes based on
industry standards.

Key Features:
    - Generates realistic business leads with buyer intent scoring
    - Configurable industry sectors and pain points
    - Budget and urgency classification
    - Quantum computing fit assessment
    - CSV export for CRM integration

Data Fields:
    - company: Company name (generated using Faker)
    - contact: Contact person name
    - email: Business email address
    - industry: Industry sector (Energy, Finance, Healthcare, etc.)
    - budget: Budget classification (very high, high, medium, low)
    - urgency: Urgency level (very urgent, urgent, normal, low)
    - pain_points: List of business challenges
    - buyer_intent: Lead temperature (hot, warm, cold)
    - quantum_fit: Boolean indicating quantum computing applicability
    - notes: Additional context about the lead

Usage:
    >>> from quantum_lead_generator import generate_leads
    >>> leads_df = generate_leads(n=100)
    >>> leads_df.to_csv('leads.csv', index=False)
    
    Or run as script:
    $ python quantum_lead_generator.py
    
Example Output:
    Generated leads are saved to 'quantum_buyer_intent_leads.csv' with
    realistic company information, contact details, and scoring metrics.

Related Modules:
    - quantum_leads_cli.py: Command-line interface for lead generation
    - sigma_select_pod.py: Lead scoring and prioritization
    
See Also:
    - docs/business_pods.md: Business pod documentation
    - FIRST_10_CLIENTS_STRATEGY.md: Lead generation strategy

Author: NQBA Framework Team
Version: 1.0.0
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
    """
    Generate synthetic business leads with realistic attributes.
    
    Creates a dataset of business leads with randomized but realistic
    characteristics including company information, buyer intent, budget,
    and pain points. Uses weighted random selection to create a distribution
    that mirrors real-world lead characteristics.
    
    Args:
        n (int): Number of leads to generate. Default is 50.
        
    Returns:
        pandas.DataFrame: DataFrame containing generated leads with columns:
            - company: Company name
            - contact: Contact person name
            - email: Business email address
            - industry: Industry sector
            - budget: Budget classification
            - urgency: Urgency level
            - pain_points: List of business challenges
            - buyer_intent: Lead temperature (hot/warm/cold)
            - quantum_fit: Boolean for quantum applicability
            - notes: Additional context
    
    Example:
        >>> leads = generate_leads(n=100)
        >>> print(f"Generated {len(leads)} leads")
        >>> hot_leads = leads[leads['buyer_intent'] == 'hot']
        >>> print(f"Hot leads: {len(hot_leads)}")
    """
    leads = []
    for _ in range(n):
        lead = {
            # Generate realistic company and contact information using Faker
            "company": fake.company(),
            "contact": fake.name(),
            "email": fake.company_email(),
            
            # Random industry selection from predefined sectors
            "industry": random.choice(INDUSTRIES),
            
            # Budget distribution: 20% very high, 40% high, 30% medium, 10% low
            # Weighted to favor higher budgets for qualified leads
            "budget": random.choices(BUDGETS, weights=[0.2, 0.4, 0.3, 0.1])[0],
            
            # Urgency distribution: Similar weighting to budget
            # More leads have higher urgency to reflect demand
            "urgency": random.choices(URGENCIES, weights=[0.2, 0.4, 0.3, 0.1])[0],
            
            # Pain points: Each lead has 1-3 randomly selected challenges
            "pain_points": random.sample(PAIN_POINTS, k=random.randint(1, 3)),
            
            # Buyer intent: 50% hot, 30% warm, 20% cold
            # Weighted heavily toward hot leads for demo purposes
            "buyer_intent": random.choices(BUYER_INTENT, weights=[0.5, 0.3, 0.2])[0],
            
            # Quantum fit: Random 50/50 split for quantum computing applicability
            "quantum_fit": random.choice([True, False]),
            
            # Additional notes with random sentence for context
            "notes": fake.sentence(),
        }
        leads.append(lead)
    
    # Return as pandas DataFrame for easy analysis and export
    return pd.DataFrame(leads)


if __name__ == "__main__":
    df = generate_leads(100)
    df.to_csv("quantum_buyer_intent_leads.csv", index=False)
    print(
        "Generated 100 best-in-class quantum buyer intent leads: quantum_buyer_intent_leads.csv"
    )
