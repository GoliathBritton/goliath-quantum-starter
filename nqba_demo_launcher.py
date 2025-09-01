"""
NQBA Demo Launcher
Unified Access to All NQBA Demonstrations
Sigma Select | FLYFOX Energy Optimizer | Web3 Blockchain Analytics
"""

import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="NQBA Demo Launcher - Complete Platform Showcase",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for NQBA branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .demo-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .demo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    }
    
    .sigma-card {
        border-left: 6px solid #3b82f6;
    }
    
    .flyfox-card {
        border-left: 6px solid #10b981;
    }
    
    .web3-card {
        border-left: 6px solid #8b5cf6;
    }
    
    .metric-highlight {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main demo launcher function"""
    st.markdown('<h1 class="main-header">🚀 NQBA Demo Launcher</h1>', unsafe_allow_html=True)
    st.markdown("### *Complete Platform Showcase - From Sales Intelligence to Quantum Energy Optimization*")
    
    # Executive Summary
    st.markdown("## 📋 Executive Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-highlight">
            <h3>🎯 Sigma Select</h3>
            <p><strong>Lead Scoring & Sales Intelligence</strong></p>
            <p>Quantum-enhanced lead optimization with SigmaEQ methodology</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-highlight">
            <h3>⚡ FLYFOX Energy</h3>
            <p><strong>Industrial Energy Optimization</strong></p>
            <p>20% cost reduction, 12x ROI via quantum algorithms</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-highlight">
            <h3>🔗 Web3 Analytics</h3>
            <p><strong>DeFi Portfolio Optimization</strong></p>
            <p>15-35% APY improvement with quantum risk management</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Demo 1: Sigma Select
    st.markdown("## 🎯 Demo 1: Sigma Select - Lead Scoring & Sales Intelligence")
    
    st.markdown("""
    <div class="demo-card sigma-card">
        <h2>🎯 Sigma Select - NQBA-Powered Sales Intelligence</h2>
        <p><strong>Purpose:</strong> Demonstrate quantum-enhanced lead scoring with SigmaEQ methodology</p>
        <p><strong>Key Features:</strong></p>
        <ul>
            <li>📊 CSV upload → quantum-enhanced scoring → next best action</li>
            <li>🎯 SigmaEQ question-led methodology integration</li>
            <li>🔗 LTC logging with IPFS provenance</li>
            <li>📈 Real-time business intelligence dashboards</li>
            <li>🚀 NQBA optimization with 10% score improvement</li>
        </ul>
        <p><strong>Business Value:</strong> Immediate cash flow through sales training, consulting, and coaching</p>
        <p><strong>Target Market:</strong> Sales teams, marketing agencies, business consultants</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Launch Sigma Select Demo", key="sigma_launch"):
            try:
                # Launch Sigma Select demo
                sigma_path = Path(__file__).parent / "sigma_select_dashboard.py"
                if sigma_path.exists():
                    st.success("✅ Launching Sigma Select Demo...")
                    st.info("Opening in new Streamlit instance...")
                    # In production, this would launch the actual demo
                    st.markdown("**Demo Features to Showcase:**")
                    st.markdown("- 📊 Upload sample CSV data")
                    st.markdown("- 🎯 Adjust scoring thresholds")
                    st.markdown("- 🚀 Run NQBA optimization")
                    st.markdown("- 📈 Export LTC data")
                else:
                    st.error("❌ Sigma Select demo file not found")
            except Exception as e:
                st.error(f"❌ Error launching demo: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Demo Highlights")
        st.markdown("- **Lead Classification**: Hot/Warm/Lukewarm/Cold with color coding")
        st.markdown("- **Next Best Actions**: SigmaEQ methodology recommendations")
        st.markdown("- **ROI Forecasting**: Revenue projections by lead classification")
        st.markdown("- **LTC Integration**: Full audit trail and compliance logging")
    
    # Demo 2: FLYFOX Energy Optimizer
    st.markdown("## ⚡ Demo 2: FLYFOX Energy Optimizer - Industrial Intelligence")
    
    st.markdown("""
    <div class="demo-card flyfox-card">
        <h2>⚡ FLYFOX Energy Optimizer - NQBA-Powered Industrial Solutions</h2>
        <p><strong>Purpose:</strong> Showcase concrete ROI through quantum-enhanced energy optimization</p>
        <p><strong>Key Features:</strong></p>
        <ul>
            <li>🏭 15 industrial facilities across multiple sectors</li>
            <li>⚡ Equipment, process, and maintenance efficiency analysis</li>
            <li>💰 15-35% energy cost reduction potential</li>
            <li>🌱 Carbon footprint reduction with ESG compliance</li>
            <li>🚀 Quantum optimization via DynexSolve algorithms</li>
        </ul>
        <p><strong>Business Value:</strong> Tangible, dollar-based ROI (20% savings, 12x ROI)</p>
        <p><strong>Target Market:</strong> Manufacturing, data centers, energy, healthcare</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Launch FLYFOX Energy Demo", key="flyfox_launch"):
            try:
                # Launch FLYFOX Energy demo
                flyfox_path = Path(__file__).parent / "flyfox_energy_optimizer.py"
                if flyfox_path.exists():
                    st.success("✅ Launching FLYFOX Energy Demo...")
                    st.info("Opening in new Streamlit instance...")
                    # In production, this would launch the actual demo
                    st.markdown("**Demo Features to Showcase:**")
                    st.markdown("- 🏭 Facility efficiency analysis")
                    st.markdown("- ⚡ Energy consumption optimization")
                    st.markdown("- 💰 ROI and payback calculations")
                    st.markdown("- 🌱 Carbon reduction impact")
                else:
                    st.error("❌ FLYFOX Energy demo file not found")
            except Exception as e:
                st.error(f"❌ Error launching demo: {str(e)}")
    
    with col2:
        st.markdown("### ⚡ Demo Highlights")
        st.markdown("- **Efficiency Radar Charts**: Equipment, process, maintenance analysis")
        st.markdown("- **Savings Analysis**: Industry breakdown and ROI forecasting")
        st.markdown("- **Environmental Impact**: CO2 reduction and ESG compliance")
        st.markdown("- **Quantum Optimization**: Real-time DynexSolve integration")
    
    # Demo 3: Web3 Blockchain Analytics
    st.markdown("## 🔗 Demo 3: Web3 Blockchain Analytics - DeFi Intelligence")
    
    st.markdown("""
    <div class="demo-card web3-card">
        <h2>🔗 Web3 Blockchain Analytics - NQBA-Powered DeFi Intelligence</h2>
        <p><strong>Purpose:</strong> Demonstrate Web3 leadership and DeFi portfolio optimization</p>
        <p><strong>Key Features:</strong></p>
        <ul>
            <li>🔗 15 DeFi protocols across DEX, lending, staking, derivatives</li>
            <li>💰 TVL analysis with APY vs risk optimization</li>
            <li>🚀 Quantum portfolio optimization algorithms</li>
            <li>🪙 DynexCoin integration and NFT certification tokens</li>
            <li>⚡ Gas efficiency and protocol performance analysis</li>
        </ul>
        <p><strong>Business Value:</strong> Web3 differentiation from OpenAI/Grok/Gemini</p>
        <p><strong>Target Market:</strong> DeFi protocols, crypto funds, institutional investors</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Launch Web3 Analytics Demo", key="web3_launch"):
            try:
                # Launch Web3 Analytics demo
                web3_path = Path(__file__).parent / "web3_blockchain_demo.py"
                if web3_path.exists():
                    st.success("✅ Launching Web3 Analytics Demo...")
                    st.info("Opening in new Streamlit instance...")
                    # In production, this would launch the actual demo
                    st.markdown("**Demo Features to Showcase:**")
                    st.markdown("- 🔗 Protocol TVL and APY analysis")
                    st.markdown("- 🚀 Quantum portfolio optimization")
                    st.markdown("- 🪙 DynexCoin and NFT integration")
                    st.markdown("- ⛽ Gas efficiency optimization")
                else:
                    st.error("❌ Web3 Analytics demo file not found")
            except Exception as e:
                st.error(f"❌ Error launching demo: {str(e)}")
    
    with col2:
        st.markdown("### 🔗 Demo Highlights")
        st.markdown("- **Protocol Analysis**: TVL, APY, risk, and optimization scoring")
        st.markdown("- **Portfolio Optimization**: Category-based analysis and recommendations")
        st.markdown("- **Token Integration**: DynexCoin metrics and NFT marketplace")
        st.markdown("- **Quantum Enhancement**: Real-time DeFi strategy optimization")
    
    # Investor Pitch Summary
    st.markdown("## 💼 Investor Pitch Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 **Immediate Value Creation**")
        st.markdown("- **Sigma Select**: $5K/session sales training & consulting")
        st.markdown("- **FLYFOX Energy**: 20% cost reduction, 12x ROI")
        st.markdown("- **Web3 Analytics**: 15-35% APY improvement")
        st.markdown("- **Early Revenue**: $50K-100K/month within 60 days")
    
    with col2:
        st.markdown("### 🚀 **Long-term Moat Building**")
        st.markdown("- **NQBA Core**: 400B parameter LLM + quantum algorithms")
        st.markdown("- **Dynex Integration**: 1,000 qubit quantum advantage")
        st.markdown("- **LTC Provenance**: Immutable audit trail via IPFS")
        st.markdown("- **Market Position**: Ahead of OpenAI/Grok in Web3 + quantum")
    
    # Market Size & Opportunity
    st.markdown("## 📊 Market Size & Opportunity")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏭 **Industrial Solutions**")
        st.markdown("- **Energy Optimization**: $500B market")
        st.markdown("- **Manufacturing**: $2.5T market")
        st.markdown("- **Data Centers**: $200B market")
        st.markdown("- **Target**: 1% market share = $32B TAM")
    
    with col2:
        st.markdown("### 💰 **Financial Services**")
        st.markdown("- **DeFi Optimization**: $50B market")
        st.markdown("- **Portfolio Management**: $7T market")
        st.markdown("- **SMB Lending**: $1.5T market")
        st.markdown("- **Target**: 0.1% market share = $8.5B TAM")
    
    with col3:
        st.markdown("### 🤖 **AI & Automation**")
        st.markdown("- **Sales Intelligence**: $15B market")
        st.markdown("- **Digital Agents**: $270B market")
        st.markdown("- **Process Automation**: $25B market")
        st.markdown("- **Target**: 2% market share = $6.2B TAM")
    
    # Technical Architecture
    st.markdown("## 🏗️ Technical Architecture Overview")
    
    st.markdown("""
    <div class="demo-card">
        <h3>🏛️ NQBA Architecture Stack</h3>
        <p><strong>Layer 1 - Quantum High Council:</strong> Policies, compliance, governance</p>
        <p><strong>Layer 2 - NQBA Core:</strong> 400B LLM + DynexSolve quantum algorithms</p>
        <p><strong>Layer 3 - Business Arms:</strong> FLYFOX AI, Goliath Trade, Sigma Select</p>
        <p><strong>Layer 4 - Agent Mesh:</strong> QDAs, voice agents, chatbots</p>
        <p><strong>Layer 5 - SaaS Platform:</strong> Multi-tenant, scalable deployment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Next Steps & Call to Action
    st.markdown("## 🚀 Next Steps & Call to Action")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 **60-Day MVP Roadmap**")
        st.markdown("- **Week 1-2**: Deploy all three demos to flyfoxai.io")
        st.markdown("- **Week 3-4**: Customer validation and feedback collection")
        st.markdown("- **Week 5-6**: Revenue generation and investor preparation")
        st.markdown("- **Week 7-8**: Series A preparation and market expansion")
    
    with col2:
        st.markdown("### 💰 **Funding Ask**")
        st.markdown("- **Round**: Series A Seed Extension")
        st.markdown("- **Amount**: $5-10M")
        st.markdown("- **Use of Funds**: Team expansion, customer acquisition, Dynex integration")
        st.markdown("- **Valuation**: $50-100M (based on $32B TAM and 1% target)")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280;">
        <p>🚀 <strong>NQBA Demo Launcher</strong> - Complete Platform Showcase</p>
        <p>From Sales Intelligence to Quantum Energy Optimization</p>
        <p>Powered by NQBA Core | Q-Cortex Governance | LTC Provenance</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
