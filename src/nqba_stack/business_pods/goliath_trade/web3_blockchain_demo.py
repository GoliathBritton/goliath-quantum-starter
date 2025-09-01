"""
Web3 Blockchain Analytics Demo
NQBA-Powered Blockchain Intelligence & DeFi Optimization
Powered by Q-Cortex Governance and LTC Provenance
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import hashlib
from datetime import datetime, timedelta
import io
import sys
from pathlib import Path

# Add src to path for NQBA imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba import DecisionLogicEngine, QuantumAdapter, LTCLogger
from nqba.q_cortex_parser import create_q_cortex_parser

# Page configuration
st.set_page_config(
    page_title="Web3 Blockchain Analytics - NQBA DeFi Intelligence",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Web3 branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #7c3aed, #a855f7, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .web3-card {
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        border: 1px solid #4338ca;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0f0f23, #1e1b4b);
        border: 1px solid #4338ca;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #a855f7);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #6d28d9, #7c3aed);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .token-high { background-color: #059669; color: white; }
    .token-medium { background-color: #d97706; color: white; }
    .token-low { background-color: #dc2626; color: white; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_nqba():
    """Initialize NQBA components with caching"""
    try:
        # Initialize core components
        decision_engine = DecisionLogicEngine()
        quantum_adapter = QuantumAdapter()
        ltc_logger = LTCLogger()
        q_cortex_parser = create_q_cortex_parser()
        
        return decision_engine, quantum_adapter, ltc_logger, q_cortex_parser
    except Exception as e:
        st.error(f"Failed to initialize NQBA: {str(e)}")
        return None, None, None, None

def generate_sample_blockchain_data():
    """Generate sample blockchain and DeFi data"""
    np.random.seed(42)  # For reproducible results
    
    protocols = [
        "DynexSwap", "Uniswap V3", "SushiSwap", "PancakeSwap", "Curve Finance",
        "Aave V3", "Compound V3", "MakerDAO", "Lido", "Rocket Pool",
        "Balancer", "1inch", "dYdX", "GMX", "Perpetual Protocol"
    ]
    
    categories = ["DEX", "Lending", "Staking", "Derivatives", "Aggregator"]
    
    data = []
    for i in range(15):
        # Protocol metrics
        total_value_locked = np.random.uniform(1000000, 100000000)  # $1M - $100M
        daily_volume = np.random.uniform(100000, 10000000)  # $100K - $10M
        user_count = np.random.randint(1000, 100000)
        
        # Token metrics
        token_price = np.random.uniform(0.01, 100)  # $0.01 - $100
        market_cap = total_value_locked * np.random.uniform(0.5, 2.0)
        circulating_supply = market_cap / token_price
        
        # DeFi metrics
        apy = np.random.uniform(2, 25)  # 2-25% APY
        impermanent_loss = np.random.uniform(0, 5)  # 0-5% IL
        gas_efficiency = np.random.uniform(0.6, 0.95)  # 60-95% efficiency
        
        # NQBA optimization potential
        optimization_score = np.random.uniform(0.3, 0.9)  # 30-90% optimization potential
        potential_apy_improvement = apy * optimization_score * 0.5  # 50% of optimization score
        potential_tvl_improvement = total_value_locked * optimization_score * 0.3  # 30% of optimization score
        
        # Risk metrics
        risk_score = np.random.uniform(0.1, 0.8)  # 10-80% risk
        volatility = np.random.uniform(0.2, 1.5)  # 20-150% volatility
        
        data.append({
            'protocol_id': f'P{i+1:03d}',
            'protocol_name': protocols[i],
            'category': np.random.choice(categories),
            'total_value_locked': round(total_value_locked, 2),
            'daily_volume': round(daily_volume, 2),
            'user_count': user_count,
            'token_price': round(token_price, 4),
            'market_cap': round(market_cap, 2),
            'circulating_supply': round(circulating_supply, 0),
            'apy_percentage': round(apy, 2),
            'impermanent_loss': round(impermanent_loss, 2),
            'gas_efficiency': round(gas_efficiency, 3),
            'optimization_score': round(optimization_score, 3),
            'potential_apy_improvement': round(potential_apy_improvement, 2),
            'potential_tvl_improvement': round(potential_tvl_improvement, 2),
            'risk_score': round(risk_score, 3),
            'volatility': round(volatility, 3),
            'nqba_optimization_priority': 'High' if optimization_score > 0.7 else 'Medium' if optimization_score > 0.4 else 'Low'
        })
    
    return pd.DataFrame(data)

def run_quantum_defi_optimization(protocol_data, quantum_adapter, ltc_logger):
    """Run quantum-enhanced DeFi optimization using NQBA"""
    try:
        # Create optimization context
        optimization_context = {
            "business_unit": "goliath_trade",
            "optimization_type": "defi_portfolio_optimization",
            "protocol_data": protocol_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate quantum optimization (replace with actual quantum_adapter call)
        optimization_result = {
            "optimization_status": "completed",
            "quantum_enhanced": True,
            "execution_time_ms": np.random.randint(150, 400),
            "portfolio_apy_improvement": np.random.uniform(0.15, 0.35),  # 15-35% APY improvement
            "risk_reduction": np.random.uniform(0.20, 0.40),   # 20-40% risk reduction
            "gas_optimization": np.random.uniform(0.25, 0.45), # 25-45% gas optimization
            "tvl_optimization": np.random.uniform(0.10, 0.30), # 10-30% TVL optimization
            "optimization_algorithm": "qubo_defi_portfolio_optimization",
            "quantum_backend": "dynexsolve"
        }
        
        # Log to LTC
        ltc_ref = ltc_logger.log_operation(
            operation_type="defi_optimization_completed",
            operation_data={
                "protocol_count": len(protocol_data),
                "optimization_result": optimization_result,
                "total_potential_improvement": protocol_data['potential_apy_improvement'].sum()
            },
            thread_ref=f"DEFI_OPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        return optimization_result, ltc_ref
        
    except Exception as e:
        st.error(f"Error running quantum DeFi optimization: {str(e)}")
        return None, None

def create_tvl_analysis_chart(df):
    """Create TVL analysis chart"""
    fig = px.bar(
        df,
        x='protocol_name',
        y='total_value_locked',
        color='category',
        title="Total Value Locked (TVL) by Protocol",
        labels={'total_value_locked': 'TVL ($)', 'protocol_name': 'Protocol'},
        height=400
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=True
    )
    
    return fig

def create_apy_analysis_chart(df):
    """Create APY analysis chart"""
    fig = px.scatter(
        df,
        x='risk_score',
        y='apy_percentage',
        size='total_value_locked',
        color='category',
        hover_data=['protocol_name', 'optimization_score'],
        title="APY vs Risk Analysis",
        labels={
            'risk_score': 'Risk Score (0-1)',
            'apy_percentage': 'APY (%)',
            'total_value_locked': 'TVL ($)'
        },
        height=400
    )
    
    return fig

def create_optimization_priority_chart(df):
    """Create optimization priority chart"""
    priority_counts = df['nqba_optimization_priority'].value_counts()
    
    fig = px.pie(
        values=priority_counts.values,
        names=priority_counts.index,
        title="NQBA Optimization Priority Distribution",
        hole=0.4,
        color_discrete_map={
            'High': '#059669',
            'Medium': '#d97706',
            'Low': '#dc2626'
        }
    )
    
    fig.update_layout(height=400)
    return fig

def create_portfolio_optimization_chart(df):
    """Create portfolio optimization analysis chart"""
    # Group by category for analysis
    category_analysis = df.groupby('category').agg({
        'total_value_locked': 'sum',
        'apy_percentage': 'mean',
        'risk_score': 'mean',
        'optimization_score': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('TVL by Category', 'Average APY by Category', 
                       'Risk Profile by Category', 'Optimization Potential by Category'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # TVL by category
    fig.add_trace(
        go.Bar(x=category_analysis['category'], y=category_analysis['total_value_locked'],
               name='TVL', marker_color='#7c3aed'),
        row=1, col=1
    )
    
    # APY by category
    fig.add_trace(
        go.Bar(x=category_analysis['category'], y=category_analysis['apy_percentage'],
               name='APY %', marker_color='#a855f7'),
        row=1, col=2
    )
    
    # Risk by category
    fig.add_trace(
        go.Bar(x=category_analysis['category'], y=category_analysis['risk_score'],
               name='Risk Score', marker_color='#c084fc'),
        row=2, col=1
    )
    
    # Optimization potential by category
    fig.add_trace(
        go.Bar(x=category_analysis['category'], y=category_analysis['optimization_score'],
               name='Optimization Score', marker_color='#ddd6fe'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    return fig

def create_gas_efficiency_chart(df):
    """Create gas efficiency analysis chart"""
    fig = px.scatter(
        df,
        x='gas_efficiency',
        y='daily_volume',
        size='user_count',
        color='category',
        hover_data=['protocol_name', 'apy_percentage'],
        title="Gas Efficiency vs Daily Volume",
        labels={
            'gas_efficiency': 'Gas Efficiency (0-1)',
            'daily_volume': 'Daily Volume ($)',
            'user_count': 'User Count'
        },
        height=400
    )
    
    return fig

def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">🔗 Web3 Blockchain Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### *NQBA-Powered DeFi Intelligence & Portfolio Optimization*")
    
    # Initialize NQBA components
    decision_engine, quantum_adapter, ltc_logger, q_cortex_parser = initialize_nqba()
    
    if not all([decision_engine, quantum_adapter, ltc_logger, q_cortex_parser]):
        st.error("Failed to initialize NQBA components. Please check your configuration.")
        return
    
    # Sidebar controls
    st.sidebar.markdown("## 🎛️ Analytics Controls")
    
    # Quantum enhancement toggle
    quantum_enhanced = st.sidebar.checkbox(
        "Enable Quantum Enhancement",
        value=True,
        help="Use DynexSolve for advanced DeFi optimization"
    )
    
    # Category filter
    all_categories = ["All Categories"] + sorted(df['category'].unique().tolist()) if 'df' in locals() else ["All Categories"]
    selected_category = st.sidebar.selectbox(
        "Filter by Category",
        all_categories
    )
    
    # Optimization priority filter
    optimization_priority = st.sidebar.selectbox(
        "Filter by Optimization Priority",
        ["All Priorities", "High", "Medium", "Low"]
    )
    
    # Risk threshold
    max_risk = st.sidebar.slider(
        "Maximum Risk Threshold",
        min_value=0.1,
        max_value=0.8,
        value=0.5,
        step=0.1,
        help="Filter protocols above this risk level"
    )
    
    # Load sample data
    df = generate_sample_blockchain_data()
    
    # Apply filters
    if selected_category != "All Categories":
        df = df[df['category'] == selected_category]
    
    if optimization_priority != "All Priorities":
        df = df[df['nqba_optimization_priority'] == optimization_priority]
    
    df = df[df['risk_score'] <= max_risk]
    
    # Main dashboard content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_protocols = len(df)
        st.metric("Total Protocols", total_protocols)
    
    with col2:
        total_tvl = df['total_value_locked'].sum()
        st.metric("Total TVL", f"${total_tvl:,.0f}")
    
    with col3:
        avg_apy = df['apy_percentage'].mean()
        st.metric("Average APY", f"{avg_apy:.2f}%")
    
    with col4:
        total_volume = df['daily_volume'].sum()
        st.metric("Daily Volume", f"${total_volume:,.0f}")
    
    # Blockchain overview
    st.markdown("## 📊 Blockchain Protocol Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # TVL analysis chart
        tvl_chart = create_tvl_analysis_chart(df)
        st.plotly_chart(tvl_chart, use_container_width=True)
    
    with col2:
        # APY vs Risk analysis
        apy_chart = create_apy_analysis_chart(df)
        st.plotly_chart(apy_chart, use_container_width=True)
    
    # Protocol analysis table
    st.markdown("## 📋 Protocol Analysis & Optimization Priority")
    
    # Color-code the optimization priority
    def color_optimization_priority(val):
        if val == "High":
            return "background-color: #059669; color: white"  # High priority
        elif val == "Medium":
            return "background-color: #d97706; color: white"  # Medium priority
        else:
            return "background-color: #dc2626; color: white"  # Low priority
    
    # Display table with styling
    display_columns = ['protocol_name', 'category', 'total_value_locked', 'apy_percentage', 
                       'risk_score', 'optimization_score', 'nqba_optimization_priority']
    styled_df = df[display_columns].copy()
    
    st.dataframe(
        styled_df.style.applymap(
            color_optimization_priority, 
            subset=['nqba_optimization_priority']
        ).format({
            'total_value_locked': '${:,.2f}',
            'apy_percentage': '{:.2f}%',
            'risk_score': '{:.3f}',
            'optimization_score': '{:.3f}'
        }),
        use_container_width=True,
        height=400
    )
    
    # Detailed analytics
    st.markdown("## 📈 Detailed Analytics")
    
    # Portfolio optimization charts
    portfolio_chart = create_portfolio_optimization_chart(df)
    st.plotly_chart(portfolio_chart, use_container_width=True)
    
    # Gas efficiency and optimization analysis
    st.markdown("## ⛽ Gas Efficiency & Optimization Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gas_chart = create_gas_efficiency_chart(df)
        st.plotly_chart(gas_chart, use_container_width=True)
    
    with col2:
        # Optimization priority distribution
        priority_chart = create_optimization_priority_chart(df)
        st.plotly_chart(priority_chart, use_container_width=True)
        
        # Optimization metrics
        high_priority_count = len(df[df['nqba_optimization_priority'] == 'High'])
        total_optimization_potential = df['optimization_score'].sum()
        
        st.metric("High Priority Protocols", high_priority_count)
        st.metric("Total Optimization Potential", f"{total_optimization_potential:.3f}")
        st.metric("Average Optimization Score", f"{df['optimization_score'].mean():.3f}")
    
    # Quantum optimization section
    st.markdown("## 🚀 Quantum-Enhanced DeFi Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### NQBA Quantum Optimization")
        if quantum_enhanced and quantum_adapter:
            st.success("✅ Quantum enhancement enabled via DynexSolve")
            st.info("🚀 QUBO portfolio optimization algorithms active")
            st.info("⚡ Real-time quantum annealing for DeFi strategies")
        else:
            st.warning("⚠️ Quantum enhancement disabled")
        
        # Run optimization button
        if st.button("🚀 Run Quantum DeFi Optimization"):
            with st.spinner("Running quantum-enhanced DeFi optimization..."):
                # Run optimization
                optimization_result, ltc_ref = run_quantum_defi_optimization(
                    df, quantum_adapter, ltc_logger
                )
                
                if optimization_result:
                    st.success("✅ Quantum optimization completed!")
                    
                    # Display results
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Portfolio APY Improvement", f"{optimization_result['portfolio_apy_improvement']*100:.1f}%")
                        st.metric("Risk Reduction", f"{optimization_result['risk_reduction']*100:.1f}%")
                    
                    with col_b:
                        st.metric("Gas Optimization", f"{optimization_result['gas_optimization']*100:.1f}%")
                        st.metric("TVL Optimization", f"{optimization_result['tvl_optimization']*100:.1f}%")
                    
                    st.info(f"🔗 LTC Reference: {ltc_ref}")
                    st.info(f"⚡ Execution Time: {optimization_result['execution_time_ms']}ms")
                else:
                    st.error("❌ Optimization failed")
    
    with col2:
        st.markdown("### Q-Cortex Compliance Status")
        if q_cortex_parser:
            st.success("✅ Q-Cortex Active")
            business_rules = q_cortex_parser.get_business_rules()
            st.info(f"📋 {len(business_rules)} Business Rules Active")
            st.info(f"🛡️ DeFi Compliance: Risk Management Standards")
            st.info(f"🔒 Security: Smart Contract Audit Requirements")
        else:
            st.error("❌ Q-Cortex Inactive")
    
    # Tokenization and NFT section
    st.markdown("## 🎨 Tokenization & NFT Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### DynexCoin Integration")
        st.info("🪙 **DynexCoin (DNX)** - Native token for NQBA ecosystem")
        st.info("💰 **Staking Rewards**: Up to 25% APY for NQBA validators")
        st.info("🔗 **Governance**: DNX holders vote on NQBA protocol upgrades")
        st.info("⚡ **PoUW Rewards**: Earn DNX for contributing quantum compute")
        
        # Simulate DNX metrics
        st.markdown("### DNX Token Metrics")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Current Price", "$0.85")
            st.metric("Market Cap", "$42.5M")
        with col_b:
            st.metric("Circulating Supply", "50M DNX")
            st.metric("Total Supply", "100M DNX")
    
    with col2:
        st.markdown("### NFT & Certification Tokens")
        st.info("🏆 **NQBA Certifications**: NFT-based skill certifications")
        st.info("🎓 **Training Tokens**: Earn NFTs for completing Sigma Select courses")
        st.info("🔐 **Access Tokens**: NFT-gated access to premium NQBA features")
        st.info("💎 **Collector Series**: Limited edition NQBA ecosystem NFTs")
        
        # Simulate NFT metrics
        st.markdown("### NFT Market Metrics")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total NFTs Minted", "1,247")
            st.metric("Floor Price", "0.5 ETH")
        with col_b:
            st.metric("Total Volume", "247 ETH")
            st.metric("Unique Holders", "892")
    
    # Export and actions
    st.markdown("## 📤 Export & Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download DeFi Analysis (CSV)",
            data=csv,
            file_name=f"web3_defi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export optimization report
        if st.button("📊 Generate DeFi Report"):
            report_data = {
                "report_timestamp": datetime.now().isoformat(),
                "total_protocols": len(df),
                "total_tvl": df['total_value_locked'].sum(),
                "average_apy": df['apy_percentage'].mean(),
                "total_optimization_potential": df['optimization_score'].sum(),
                "high_priority_count": len(df[df['nqba_optimization_priority'] == 'High']),
                "protocols": df.to_dict('records')
            }
            
            st.json(report_data)
    
    with col3:
        # Schedule consultation
        if st.button("📞 Schedule Web3 Consultation"):
            st.success("✅ Consultation request submitted!")
            st.info("Our DeFi optimization experts will contact you within 24 hours")
            st.info("Expected APY Improvement: 15-35%")
            st.info("Expected Risk Reduction: 20-40%")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280;">
        <p>🔗 <strong>Web3 Blockchain Analytics</strong> - Powered by NQBA Core | Q-Cortex Governance | LTC Provenance</p>
        <p>DeFi Intelligence with Quantum-Enhanced Portfolio Optimization</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
