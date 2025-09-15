from typing import List, Dict

PARTNERS = [
    {
        "id": "p_001",
        "company": "FLYFOX AI",
        "tier": "platinum",
        "monthlyRevenue": 152000,
        "commissionRate": 0.30,
        "totalCustomers": 210
    },
    {
        "id": "p_002",
        "company": "Goliath of All Trade Inc",
        "tier": "platinum",
        "monthlyRevenue": 117000,
        "commissionRate": 0.28,
        "totalCustomers": 160
    },
    {
        "id": "p_003",
        "company": "Sigma Select",
        "tier": "gold",
        "monthlyRevenue": 89000,
        "commissionRate": 0.25,
        "totalCustomers": 94
    }
]

LEADS = [
    {
        "id": "l_001",
        "company": "TechCorp Solutions",
        "contact": "Sarah Johnson",
        "email": "sarah.johnson@techcorp.com",
        "status": "qualified",
        "estimatedValue": 45000,
        "source": "website",
        "assignedPartner": "p_001"
    },
    {
        "id": "l_002",
        "company": "DataFlow Industries",
        "contact": "Michael Chen",
        "email": "m.chen@dataflow.com",
        "status": "contacted",
        "estimatedValue": 78000,
        "source": "referral",
        "assignedPartner": "p_002"
    },
    {
        "id": "l_003",
        "company": "Quantum Dynamics",
        "contact": "Dr. Emily Rodriguez",
        "email": "e.rodriguez@quantumdyn.com",
        "status": "proposal",
        "estimatedValue": 125000,
        "source": "conference",
        "assignedPartner": "p_001"
    }
]

quantum_nexus_PREDICTIONS = [
    {
        "id": "pred_001",
        "query": "Market trend analysis for Q1 2024",
        "prediction": "Quantum computing adoption will increase by 35% in enterprise sector",
        "confidence": 0.87,
        "timestamp": "2024-01-15T10:30:00Z",
        "quantumCredits": 150
    },
    {
        "id": "pred_002",
        "query": "Partner revenue optimization",
        "prediction": "FLYFOX AI partnership shows 23% growth potential with expanded service offerings",
        "confidence": 0.92,
        "timestamp": "2024-01-14T14:22:00Z",
        "quantumCredits": 200
    }
]