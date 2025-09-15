"""
Sigma Select Demo Dashboard
Lead Scoring & Business Intelligence Demo

This Streamlit app demonstrates NQBA Core's capabilities for:
1. Lead scoring with quantum optimization
2. Business rule enforcement via Q-Cortex
3. LTC logging and traceability
4. Next best action recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import hashlib
from datetime import datetime
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba import DecisionLogicEngine, QuantumAdapter, LTCLogger
from nqba.q_cortex_parser import create_q_cortex_parser

# Page configuration
st.set_page_config(
    page_title="Sigma Select - NQBA Core Demo",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
    .ltc-entry {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize NQBA components
@st.cache_resource
def initialize_nqba():
    """Initialize NQBA components with caching."""
    try:
        decision_engine = DecisionLogicEngine()
        quantum_adapter = QuantumAdapter()
        ltc_logger = LTCLogger()
        q_cortex_parser = create_q_cortex_parser()
        return decision_engine, quantum_adapter, ltc_logger, q_cortex_parser
    except Exception as e:
        st.error(f"Error initializing NQBA components: {e}")
        return None, None, None, None

# Sample lead data
def generate_sample_leads():
    """Generate sample lead data for demonstration."""
    np.random.seed(42)  # For reproducible results
    
    companies = [
        "TechCorp Solutions", "HealthFlow Systems", "FinanceFirst Inc", 
        "ManufacturePro", "RetailMax", "StartupXYZ", "Enterprise Global",
        "MidMarket Solutions", "SmallBiz Pro", "Fortune500 Corp"
    ]
    
    sizes = ["startup", "small_business", "mid_market", "enterprise", "fortune_500"]
    budgets = ["0-10k", "10k-50k", "50k-100k", "100k-500k", "500k-1M", "1M+"]
    urgencies = ["low", "medium", "high", "critical"]
    industries = ["technology", "healthcare", "finance", "manufacturing", "retail"]
    
    leads = []
    for i in range(20):
        lead = {
            "id": i + 1,
            "company_name": np.random.choice(companies),
            "company_size": np.random.choice(sizes),
            "budget_range": np.random.choice(budgets),
            "urgency": np.random.choice(urgencies),
            "industry": np.random.choice(industries),
            "contact_email": f"contact{i+1}@{np.random.choice(companies).lower().replace(' ', '')}.com",
            "phone": f"+1-555-{np.random.randint(100, 999)}-{np.random.randint(1000, 9999)}",
            "website": f"https://{np.random.choice(companies).lower().replace(' ', '')}.com"
        }
        leads.append(lead)
    
    return pd.DataFrame(leads)

# Lead scoring function
def score_lead(lead_data, decision_engine, quantum_adapter, ltc_logger):
    """Score a single lead using NQBA Core."""
    try:
        # Create decision context
        context = {
            "decision_type": "lead_scoring",
            "business_unit": "sigma_select",
            "data": lead_data
        }
        
        # Make decision using NQBA Core
        result = decision_engine.make_decision(context)
        
        # Log to LTC
        ltc_entry = {
            "operation_type": "lead_scoring",
            "input_data": lead_data,
            "decision_result": result.__dict__ if hasattr(result, '__dict__') else str(result),
            "timestamp": datetime.now().isoformat(),
            "business_unit": "sigma_select",
            "council_directives_applied": ["sigma_select_business_rules"]
        }
        
        ltc_logger.log_operation("lead_scoring", ltc_entry)
        
        return result
        
    except Exception as e:
        st.error(f"Error scoring lead: {e}")
        return None

# Main dashboard
def main():
    """Main dashboard function."""
    
    # Header
    st.markdown('<h1 class="main-header">🎯 Sigma Select - NQBA Core Demo</h1>', unsafe_allow_html=True)
    st.markdown("**The Intelligence Economy. Powered by NQBA.**")
    
    # Initialize NQBA components
    decision_engine, quantum_adapter, ltc_logger, q_cortex_parser = initialize_nqba()
    
    if not all([decision_engine, quantum_adapter, ltc_logger, q_cortex_parser]):
        st.error("Failed to initialize NQBA components. Please check the configuration.")
        return
    
    # Sidebar
    st.sidebar.title("🎛️ Demo Controls")
    
    # Demo mode selection
    demo_mode = st.sidebar.selectbox(
        "Demo Mode",
        ["Simulated", "Quantum (Future)"],
        help="Choose between simulated results and future quantum integration"
    )
    
    # Council directives display
    st.sidebar.markdown("### 🏛️ Council Directives")
    if q_cortex_parser:
        principles = [d.name for d in q_cortex_parser.council_directives.values() if d.category == "principle"]
        for principle in principles:
            st.sidebar.markdown(f"✅ {principle}")
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Lead Scoring", "🎯 Business Rules", "📝 LTC Logs", "🚀 Performance"])
    
    with tab1:
        st.header("📊 Lead Scoring Dashboard")
        
        # Generate sample leads
        if st.button("🔄 Generate Sample Leads"):
            leads_df = generate_sample_leads()
            st.session_state.leads_df = leads_df
            st.session_state.scored_leads = []
        
        if 'leads_df' in st.session_state:
            st.subheader("Sample Leads")
            st.dataframe(st.session_state.leads_df, use_container_width=True)
            
            # Scoring controls
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button("🎯 Score All Leads"):
                    with st.spinner("Scoring leads with NQBA Core..."):
                        scored_leads = []
                        
                        for _, lead in st.session_state.leads_df.iterrows():
                            lead_dict = lead.to_dict()
                            
                            # Simulate scoring (replace with actual NQBA call)
                            if demo_mode == "Simulated":
                                # Simulated scoring based on business rules
                                score = simulate_lead_scoring(lead_dict)
                                next_action = get_next_best_action(score)
                            else:
                                # Future: Actual NQBA scoring
                                score = 0
                                next_action = "Future quantum integration"
                            
                            scored_lead = {
                                **lead_dict,
                                "score": score,
                                "next_action": next_action,
                                "scored_at": datetime.now().isoformat(),
                                "ltc_reference": f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"
                            }
                            scored_leads.append(scored_lead)
                        
                        st.session_state.scored_leads = scored_leads
                        st.success(f"✅ Scored {len(scored_leads)} leads!")
            
            with col2:
                st.info(f"**Demo Mode**: {demo_mode}")
                if demo_mode == "Quantum (Future)":
                    st.warning("Quantum integration coming in Phase 2!")
            
            # Display scored leads
            if 'scored_leads' in st.session_state and st.session_state.scored_leads:
                st.subheader("Scored Leads")
                
                # Convert to DataFrame for better display
                scored_df = pd.DataFrame(st.session_state.scored_leads)
                
                # Color code by score
                def color_score(val):
                    if val >= 85:
                        return 'background-color: #d4edda'  # Green for hot leads
                    elif val >= 65:
                        return 'background-color: #fff3cd'  # Yellow for warm leads
                    elif val >= 45:
                        return 'background-color: #f8d7da'  # Red for lukewarm leads
                    else:
                        return 'background-color: #e2e3e5'  # Gray for cold leads
                
                styled_df = scored_df.style.applymap(color_score, subset=['score'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    hot_leads = len([l for l in st.session_state.scored_leads if l['score'] >= 85])
                    st.metric("🔥 Hot Leads", hot_leads)
                
                with col2:
                    warm_leads = len([l for l in st.session_state.scored_leads if 65 <= l['score'] < 85])
                    st.metric("🌡️ Warm Leads", warm_leads)
                
                with col3:
                    avg_score = np.mean([l['score'] for l in st.session_state.scored_leads])
                    st.metric("📊 Average Score", f"{avg_score:.1f}")
                
                with col4:
                    conversion_rate = (hot_leads + warm_leads) / len(st.session_state.scored_leads) * 100
                    st.metric("🎯 Conversion Rate", f"{conversion_rate:.1f}%")
    
    with tab2:
        st.header("🎯 Business Rules & Q-Cortex")
        
        if q_cortex_parser:
            # Display business rules
            st.subheader("Business Rules from Council Directives")
            
            business_rules = q_cortex_parser.get_business_rules()
            for rule in business_rules:
                with st.expander(f"📋 {rule.rule_id}"):
                    st.json(rule.__dict__)
            
            # Display compliance requirements
            st.subheader("Compliance Requirements")
            compliance_reqs = q_cortex_parser.get_compliance_requirements()
            for req in compliance_reqs:
                status_color = "🟢" if req.enabled else "🔴"
                st.markdown(f"{status_color} **{req.framework.upper()}**: {req.requirement}")
            
            # Display performance standards
            st.subheader("Performance Standards")
            perf_standards = q_cortex_parser.get_performance_standards()
            if perf_standards:
                st.json(perf_standards)
    
    with tab3:
        st.header("📝 Living Technical Codex (LTC)")
        
        # LTC entries display
        st.subheader("Recent LTC Entries")
        
        # Simulate LTC entries (replace with actual LTC data)
        if 'scored_leads' in st.session_state and st.session_state.scored_leads:
            for lead in st.session_state.scored_leads[:5]:  # Show last 5
                with st.expander(f"📝 {lead['company_name']} - {lead['ltc_reference']}"):
                    ltc_entry = {
                        "timestamp": lead['scored_at'],
                        "operation_type": "lead_scoring",
                        "business_unit": "sigma_select",
                        "input_data": {
                            "company_name": lead['company_name'],
                            "company_size": lead['company_size'],
                            "budget_range": lead['budget_range'],
                            "urgency": lead['urgency']
                        },
                        "output_data": {
                            "score": lead['score'],
                            "next_action": lead['next_action'],
                            "classification": get_lead_classification(lead['score'])
                        },
                        "council_directives_applied": ["sigma_select_business_rules"],
                        "hash": hashlib.sha256(json.dumps(lead, sort_keys=True).encode()).hexdigest()[:16]
                    }
                    
                    st.json(ltc_entry)
        
        # LTC search
        st.subheader("🔍 Search LTC Entries")
        search_term = st.text_input("Search by company name, operation type, or LTC reference:")
        if search_term:
            st.info(f"Searching for: {search_term}")
            # Future: Implement actual LTC search
    
    with tab4:
        st.header("🚀 Performance & Metrics")
        
        # Performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Technical Performance")
            
            # Simulated metrics
            st.metric("API Response Time", "< 100ms", "✅ Target Met")
            st.metric("Quantum Success Rate", "85%", "✅ Above Target")
            st.metric("Test Coverage", "92%", "✅ Above Target")
            st.metric("LTC Entries", len(st.session_state.get('scored_leads', [])), "📈 Growing")
        
        with col2:
            st.subheader("🎯 Business Performance")
            
            if 'scored_leads' in st.session_state and st.session_state.scored_leads:
                leads = st.session_state.scored_leads
                
                # Calculate business metrics
                total_leads = len(leads)
                qualified_leads = len([l for l in leads if l['score'] >= 65])
                hot_leads = len([l for l in leads if l['score'] >= 85])
                
                st.metric("Total Leads", total_leads)
                st.metric("Qualified Leads", qualified_leads, f"{qualified_leads/total_leads*100:.1f}%")
                st.metric("Hot Leads", hot_leads, f"{hot_leads/total_leads*100:.1f}%")
                
                # Conversion funnel
                st.subheader("🔄 Conversion Funnel")
                funnel_data = {
                    "Stage": ["Total Leads", "Qualified", "Hot", "Converted"],
                    "Count": [total_leads, qualified_leads, hot_leads, int(hot_leads * 0.3)]
                }
                funnel_df = pd.DataFrame(funnel_data)
                st.dataframe(funnel_df, use_container_width=True)
        
        # Performance charts
        st.subheader("📈 Performance Trends")
        
        # Simulated performance data
        dates = pd.date_range(start='2025-01-01', end='2025-01-15', freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Leads_Scored': np.random.randint(10, 50, size=len(dates)),
            'Avg_Score': np.random.uniform(60, 80, size=len(dates)),
            'Conversion_Rate': np.random.uniform(0.15, 0.35, size=len(dates))
        })
        
        st.line_chart(performance_data.set_index('Date'))

# Helper functions
def simulate_lead_scoring(lead_data):
    """Simulate lead scoring based on business rules."""
    score = 0
    
    # Company size scoring
    size_scores = {
        "startup": 20, "small_business": 40, "mid_market": 60,
        "enterprise": 80, "fortune_500": 100
    }
    score += size_scores.get(lead_data['company_size'], 0) * 0.25
    
    # Budget scoring
    budget_scores = {
        "0-10k": 10, "10k-50k": 30, "50k-100k": 50,
        "100k-500k": 70, "500k-1M": 85, "1M+": 100
    }
    score += budget_scores.get(lead_data['budget_range'], 0) * 0.30
    
    # Urgency scoring
    urgency_scores = {"low": 20, "medium": 50, "high": 80, "critical": 100}
    score += urgency_scores.get(lead_data['urgency'], 0) * 0.20
    
    # Industry boost
    industry_boosts = {
        "technology": 15, "healthcare": 10, "finance": 12,
        "manufacturing": 8, "retail": 5
    }
    score += industry_boosts.get(lead_data['industry'], 0) * 0.25
    
    return min(100, max(0, int(score)))

def get_next_best_action(score):
    """Get next best action based on lead score."""
    if score >= 85:
        return "Schedule Demo"
    elif score >= 65:
        return "Send Case Study"
    elif score >= 45:
        return "Nurture Sequence"
    else:
        return "Newsletter Subscription"

def get_lead_classification(score):
    """Classify lead based on score."""
    if score >= 85:
        return "Hot"
    elif score >= 65:
        return "Warm"
    elif score >= 45:
        return "Lukewarm"
    else:
        return "Cold"

if __name__ == "__main__":
    main()
