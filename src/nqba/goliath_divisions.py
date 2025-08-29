"""
Goliath of All Trade: Business Divisions and Automated/Demo Workflows
- Each division has its own catalog of automations and demo workflows
"""

from nqba import AUTOMATIONS

DIVISIONS = {
    "flyfox_ai": {
        "label": "FlyFox AI (Quantum Sales & Lead Gen)",
        "automations": [
            "lead_scoring",
            "sales_script",
            "openai_chat",
            "neuro_siphon",
            "q_mirrors",
            "sigma_graph",
        ],
        "demo_workflows": [
            {
                "name": "AI Lead Scoring Demo",
                "description": "Score a lead using quantum/AI policy.",
                "run": lambda: AUTOMATIONS["lead_scoring"](
                    {"lead_score": 0.9, "risk": 0.05}
                ),
            },
            {
                "name": "Sales Script Demo",
                "description": "Generate a personalized sales script.",
                "run": lambda: AUTOMATIONS["sales_script"]({"name": "Demo Customer"}),
            },
            {
                "name": "NeuroSiphon Data Extraction",
                "description": "Extract live data from email/Slack/CRM.",
                "run": lambda: AUTOMATIONS["neuro_siphon"]("email", {"user": "demo"}),
            },
            {
                "name": "Q-Mirrors Shadow DB",
                "description": "Create a quantum-encrypted shadow database.",
                "run": lambda: AUTOMATIONS["q_mirrors"]({"data": "sample"}, "key123"),
            },
            {
                "name": "Sigma Graph Org Chart",
                "description": "Build org chart and compute leverage scores.",
                "run": lambda: AUTOMATIONS["sigma_graph"]({"org": "sample"}),
            },
        ],
    },
    "goliath_trade": {
        "label": "Goliath Trade (Quantum Trading & Optimization)",
        "automations": [
            "quantum_optimize",
            "qubo_optimization",
            "sat_solver",
            "qboost_train",
            "qsvm_train",
            "data_poisoning",
            "dead_drop",
        ],
        "demo_workflows": [
            {
                "name": "Quantum Portfolio Optimization",
                "description": "Optimize a portfolio using QUBO.",
                "run": lambda: AUTOMATIONS["quantum_optimize"](
                    2, [(0, 0, 1.0), (1, 1, -1.0), (0, 1, 0.5)]
                ),
            },
            {
                "name": "Data Poisoning (Reality Distortion)",
                "description": "Distort data using QNLP reality distortion.",
                "run": lambda: AUTOMATIONS["data_poisoning"](
                    {"sales": 100, "risk": 0.2}
                ),
            },
            {
                "name": "Dead Drop Data Trap",
                "description": "Deploy a time-delayed data trap.",
                "run": lambda: AUTOMATIONS["dead_drop"]("targetA", 1),
            },
        ],
    },
    "sigma_select": {
        "label": "Sigma Select (Risk, Insurance, Compliance)",
        "automations": [
            "lead_scoring",
            "openai_embedding",
            "sigma_graph",
            "data_poisoning",
        ],
        "demo_workflows": [
            {
                "name": "Risk Scoring Demo",
                "description": "Score risk for an insurance lead.",
                "run": lambda: AUTOMATIONS["lead_scoring"](
                    {"lead_score": 0.7, "risk": 0.3}
                ),
            },
            {
                "name": "Sigma Graph Org Chart",
                "description": "Build org chart and compute leverage scores.",
                "run": lambda: AUTOMATIONS["sigma_graph"]({"org": "sample"}),
            },
            {
                "name": "Data Poisoning (Revenge Window)",
                "description": "Predict next optimal revenge window.",
                "run": lambda: AUTOMATIONS["data_poisoning"]({"incident": "slight"}),
            },
        ],
    },
    "sfg_insurance": {
        "label": "Symmetry Financial Group (Insurance)",
        "automations": ["lead_scoring", "eclipse_mode"],
        "demo_workflows": [
            {
                "name": "Insurance Lead Scoring",
                "description": "Score a lead for insurance underwriting.",
                "run": lambda: AUTOMATIONS["lead_scoring"](
                    {"lead_score": 0.85, "risk": 0.15}
                ),
            },
            {
                "name": "Eclipse Mode Auto-Purge",
                "description": "Auto-purge related emails for compliance.",
                "run": lambda: AUTOMATIONS["eclipse_mode"]({"type": "compliance"}),
            },
        ],
    },
}
