import pandas as pd
from nqba_stack.business_pods.sigma_select.sigma_select_dashboard import sigmaeq_score_leads

def test_sigmaeq_score_leads_quantum():
    df = pd.DataFrame([
        {"name": "Alice", "budget": "high", "urgency": "urgent", "pain_points": "energy costs"},
        {"name": "Bob", "budget": "low", "urgency": "normal", "pain_points": "production delays"},
    ])
    scored = sigmaeq_score_leads(df)
    assert "score" in scored.columns
    assert "quantum_enhanced" in scored.columns
    assert scored["quantum_enhanced"].all()
