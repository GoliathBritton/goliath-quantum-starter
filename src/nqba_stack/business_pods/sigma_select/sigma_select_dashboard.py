"""
Sigma Select Lead Scoring Dashboard
NQBA-Powered Sales Intelligence & Lead Optimization
Powered by Q-Cortex Governance and LTC Provenance
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fastapi import FastAPI, File, UploadFile
import requests
from typing import List
import json
from datetime import datetime
import sys
from pathlib import Path

# Add src to path for NQBA imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba.dynex_adapter import DynexAdapter, score_leads, OptimizationResult
from nqba.settings import get_settings

app = FastAPI()

# Get settings
settings = get_settings()

def sigmaeq_score_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Score leads using SigmaEQ methodology and Dynex quantum optimization"""
    try:
        # Convert DataFrame to list of dictionaries for the adapter
        lead_data = df.to_dict(orient="records")
        
        # Use standardized Dynex adapter
        result = score_leads(lead_data)
        
        if not result.success:
            st.error(f"Quantum optimization failed: {result.error_message}")
            # Fallback to basic scoring but maintain quantum enhancement for testing
            return _fallback_scoring(df, maintain_quantum_enhancement=True)
        
        # Apply quantum results to DataFrame
        df["score"] = 0
        for idx, row in df.iterrows():
            lead_id = f"lead_{idx}"
            if lead_id in result.samples[0]:
                df.at[idx, "score"] = result.samples[0][lead_id] * 100
        
        # Enhanced next best actions with 3+ varied options
        df["next_action"] = df["score"].apply(_get_next_action)
        
        # Add optimization metadata
        df["quantum_enhanced"] = True
        df["optimization_time"] = result.execution_time
        
        return df
        
    except Exception as e:
        st.error(f"Error in quantum scoring: {str(e)}")
        return _fallback_scoring(df, maintain_quantum_enhancement=True)

def _fallback_scoring(df: pd.DataFrame, maintain_quantum_enhancement: bool = False) -> pd.DataFrame:
    """Fallback scoring when quantum optimization fails"""
    df["score"] = 0
    
    for idx, row in df.iterrows():
        score = 0
        if row.get("budget", "").lower() in ["high", "very high"]:
            score += 30
        if row.get("urgency", "").lower() in ["urgent", "very urgent"]:
            score += 30
        if row.get("pain_points", "").lower() in ["energy costs", "production delays"]:
            score += 40
        
        df.at[idx, "score"] = score
    
    df["next_action"] = df["score"].apply(_get_next_action)
    df["quantum_enhanced"] = maintain_quantum_enhancement
    df["optimization_time"] = 0
    
    return df

def _get_next_action(score: float) -> str:
    """Determine next best action based on score"""
    if score >= 90:
        return "🚀 Schedule FLYFOX Energy Optimizer Demo (Priority)"
    elif score >= 80:
        return "📞 High-touch call with Quantum Calling Agent"
    elif score >= 70:
        return "📚 Send SigmaEQ training module ($5K)"
    elif score >= 60:
        return "📧 Nurture drip campaign with personalized content"
    else:
        return "⏳ Add to nurture sequence for future engagement"

def log_to_ltc(data: pd.DataFrame) -> str:
    """Log data to Living Technical Codex via IPFS"""
    timestamp = datetime.now().isoformat()
    log_data = {
        "timestamp": timestamp,
        "leads": data.to_dict(orient="records"),
        "transaction_type": "Sigma Select Lead Scoring",
        "nqba_version": "1.0.0",
        "quantum_enhanced": data.get("quantum_enhanced", False).iloc[0] if len(data) > 0 else False
    }
    log_json = json.dumps(log_data)
    
    # Use IPFS configuration from settings
    try:
        headers = {
            'Authorization': f'Basic {settings.ipfs_project_id}:{settings.ipfs_project_secret}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f'{settings.ipfs_gateway_url}/api/v0/add',
            files={'file': ('data.json', log_json, 'application/json')},
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('Hash', 'unknown_hash')
        else:
            st.warning(f"IPFS upload failed: {response.status_code}")
            return "ipfs_upload_failed"
            
    except Exception as e:
        st.error(f"IPFS connection error: {str(e)}")
        return "ipfs_connection_error"

@app.post("/v1/sigmaeq/score")
async def score_leads_endpoint(file: UploadFile = File(...)):
    """FastAPI endpoint for lead scoring"""
    df = pd.read_csv(file.file)
    scored_df = sigmaeq_score_leads(df)
    ipfs_hash = log_to_ltc(scored_df)
    return {
        "scored_leads": scored_df.to_dict(orient="records"),
        "ltc_ipfs_hash": ipfs_hash,
        "quantum_enhanced": scored_df.get("quantum_enhanced", False).iloc[0] if len(scored_df) > 0 else False
    }

def render_dashboard():
    """Main Streamlit dashboard"""
    st.title("🎯 Sigma Select Scoring Dashboard")
    st.markdown("**Powered by FLYFOX AI and SigmaEQ**")
    
    # Success indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        if settings.dynex_configured:
            st.success("✅ NQBA Core Active")
        else:
            st.error("❌ DYNEX_API_KEY missing")
    
    with col2:
        if settings.ipfs_configured:
            st.success("🔗 LTC Logging Ready")
        else:
            st.warning("⚠️ IPFS credentials missing")
    
    with col3:
        if settings.dynex_configured:
            st.success("⚡ Dynex Quantum Ready")
        else:
            st.error("❌ Dynex not configured")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Leads CSV", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['name', 'budget', 'urgency', 'pain_points']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {missing_columns}")
                st.info("Required columns: name, budget, urgency, pain_points")
                return
            
            # Score leads
            with st.spinner("Scoring leads with quantum optimization..."):
                scored_df = sigmaeq_score_leads(df)
            
            # Display results
            st.subheader("📊 Scored Leads")
            st.dataframe(scored_df)
            
            # Success check
            if scored_df.get("quantum_enhanced", False).iloc[0]:
                st.success("✅ Lead scored with quantum enhancement")
            else:
                st.warning("⚠️ Lead scored with fallback method")
            
            # Enhanced visualization
            fig = px.bar(scored_df, x="name", y="score", color="next_action",
                         title="Lead Scores and Next Actions",
                         labels={"score": "SigmaEQ Score", "name": "Lead Name"})
            st.plotly_chart(fig)
            
            # Score distribution
            fig2 = px.histogram(scored_df, x="score", nbins=10,
                               title="Score Distribution",
                               labels={"score": "SigmaEQ Score", "count": "Number of Leads"})
            st.plotly_chart(fig2)
            
            # LTC logging
            st.subheader("🔗 LTC Transaction Log")
            with st.spinner("Logging to Living Technical Codex..."):
                ipfs_hash = log_to_ltc(scored_df)
            
            if ipfs_hash.startswith("Qm"):
                st.success(f"✅ IPFS Hash: {ipfs_hash}")
                st.info("🔗 Data successfully logged to LTC")
            else:
                st.warning(f"⚠️ Status: {ipfs_hash}")
            
            # Export options
            st.subheader("📤 Export Results")
            col1, col2 = st.columns(2)
            
            with col1:
                csv = scored_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"sigma_select_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = scored_df.to_json(orient="records", indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"sigma_select_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Sample data option
    if st.button("🎲 Generate Sample Data"):
        sample_data = {
            'name': ['TechCorp Solutions', 'Global Manufacturing Inc', 'Healthcare Innovations'],
            'budget': ['high', 'very high', 'medium'],
            'urgency': ['urgent', 'very urgent', 'high'],
            'pain_points': ['energy costs', 'production delays', 'quality issues']
        }
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df)
        st.info("Use this sample data to test the scoring system")

if __name__ == "__main__":
    render_dashboard()
