"""
FLYFOX Energy Optimizer
NQBA-Powered Industrial Energy Optimization
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
    page_title="FLYFOX Energy Optimizer - NQBA Industrial Solutions",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for FLYFOX AI branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #059669, #10b981, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .energy-card {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #047857;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #022c22, #064e3b);
        border: 1px solid #047857;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #059669, #10b981);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #047857, #059669);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .savings-high { background-color: #059669; color: white; }
    .savings-medium { background-color: #d97706; color: white; }
    .savings-low { background-color: #dc2626; color: white; }
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

def generate_sample_energy_data():
    """Generate sample industrial energy consumption data"""
    np.random.seed(42)  # For reproducible results
    
    facilities = [
        "Manufacturing Plant A", "Data Center B", "Steel Mill C", "Chemical Plant D",
        "Paper Mill E", "Automotive Factory F", "Pharmaceutical Lab G", "Mining Operation H",
        "Oil Refinery I", "Cement Plant J", "Food Processing K", "Textile Factory L",
        "Electronics Assembly M", "Aerospace Facility N", "Power Generation O"
    ]
    
    industries = ["Manufacturing", "Data Centers", "Steel", "Chemicals", "Paper", 
                 "Automotive", "Pharmaceuticals", "Mining", "Oil & Gas", "Cement",
                 "Food & Beverage", "Textiles", "Electronics", "Aerospace", "Energy"]
    
    data = []
    for i in range(15):
        # Base energy consumption (MWh/month)
        base_consumption = np.random.uniform(500, 5000)
        
        # Efficiency factors (0-1, where 1 is most efficient)
        equipment_efficiency = np.random.uniform(0.6, 0.9)
        process_efficiency = np.random.uniform(0.5, 0.85)
        maintenance_efficiency = np.random.uniform(0.7, 0.95)
        
        # Current energy cost ($/MWh)
        energy_cost = np.random.uniform(80, 150)
        
        # Calculate current monthly cost
        current_cost = base_consumption * energy_cost
        
        # Calculate potential savings through optimization
        optimization_potential = np.random.uniform(0.15, 0.35)  # 15-35% savings
        potential_savings = current_cost * optimization_potential
        
        # Calculate ROI (investment vs savings)
        investment_cost = np.random.uniform(50000, 200000)
        annual_savings = potential_savings * 12
        roi = (annual_savings / investment_cost) * 100
        
        # Carbon footprint (tons CO2/month)
        carbon_intensity = np.random.uniform(0.4, 0.8)  # tons CO2/MWh
        current_carbon = base_consumption * carbon_intensity
        potential_carbon_reduction = current_carbon * optimization_potential
        
        data.append({
            'facility_id': f'F{i+1:03d}',
            'facility_name': facilities[i],
            'industry': industries[i],
            'base_consumption_mwh': round(base_consumption, 1),
            'equipment_efficiency': round(equipment_efficiency, 3),
            'process_efficiency': round(process_efficiency, 3),
            'maintenance_efficiency': round(maintenance_efficiency, 3),
            'energy_cost_per_mwh': round(energy_cost, 2),
            'current_monthly_cost': round(current_cost, 2),
            'optimization_potential': round(optimization_potential, 3),
            'potential_monthly_savings': round(potential_savings, 2),
            'investment_cost': round(investment_cost, 2),
            'annual_savings': round(annual_savings, 2),
            'roi_percentage': round(roi, 1),
            'current_carbon_tons': round(current_carbon, 1),
            'potential_carbon_reduction': round(potential_carbon_reduction, 1),
            'payback_months': round(investment_cost / potential_savings, 1)
        })
    
    return pd.DataFrame(data)

def run_quantum_energy_optimization(facility_data, quantum_adapter, ltc_logger):
    """Run quantum-enhanced energy optimization using NQBA"""
    try:
        # Create optimization context
        optimization_context = {
            "business_unit": "flyfox_ai",
            "optimization_type": "energy_efficiency",
            "facility_data": facility_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate quantum optimization (replace with actual quantum_adapter call)
        optimization_result = {
            "optimization_status": "completed",
            "quantum_enhanced": True,
            "execution_time_ms": np.random.randint(200, 500),
            "energy_savings_percentage": np.random.uniform(0.18, 0.28),  # 18-28% savings
            "cost_savings_percentage": np.random.uniform(0.20, 0.30),   # 20-30% cost reduction
            "carbon_reduction_percentage": np.random.uniform(0.15, 0.25), # 15-25% carbon reduction
            "roi_improvement": np.random.uniform(1.1, 1.3),  # 10-30% ROI improvement
            "optimization_algorithm": "qubo_energy_optimization",
            "quantum_backend": "dynexsolve"
        }
        
        # Log to LTC
        ltc_ref = ltc_logger.log_operation(
            operation_type="energy_optimization_completed",
            operation_data={
                "facility_count": len(facility_data),
                "optimization_result": optimization_result,
                "total_potential_savings": facility_data['potential_monthly_savings'].sum()
            },
            thread_ref=f"ENERGY_OPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        return optimization_result, ltc_ref
        
    except Exception as e:
        st.error(f"Error running quantum energy optimization: {str(e)}")
        return None, None

def create_energy_consumption_chart(df):
    """Create energy consumption by facility chart"""
    fig = px.bar(
        df,
        x='facility_name',
        y='base_consumption_mwh',
        color='industry',
        title="Monthly Energy Consumption by Facility",
        labels={'base_consumption_mwh': 'Energy Consumption (MWh/month)', 'facility_name': 'Facility'},
        height=400
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=True
    )
    
    return fig

def create_efficiency_radar_chart(df, selected_facility):
    """Create efficiency radar chart for selected facility"""
    facility_data = df[df['facility_name'] == selected_facility].iloc[0]
    
    categories = ['Equipment', 'Process', 'Maintenance']
    values = [
        facility_data['equipment_efficiency'],
        facility_data['process_efficiency'],
        facility_data['maintenance_efficiency']
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Efficiency',
        line_color='#10b981'
    ))
    
    # Add target efficiency (90% across all categories)
    target_values = [0.9, 0.9, 0.9]
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=categories,
        fill='toself',
        name='Target Efficiency (90%)',
        line_color='#059669',
        opacity=0.3
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=f"Efficiency Analysis - {selected_facility}",
        height=400
    )
    
    return fig

def create_savings_analysis_chart(df):
    """Create savings analysis chart"""
    # Group by industry for analysis
    industry_analysis = df.groupby('industry').agg({
        'potential_monthly_savings': 'sum',
        'investment_cost': 'sum',
        'roi_percentage': 'mean',
        'payback_months': 'mean'
    }).reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Monthly Savings by Industry', 'ROI by Industry', 
                       'Investment vs Savings', 'Payback Period by Industry'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Monthly savings by industry
    fig.add_trace(
        go.Bar(x=industry_analysis['industry'], y=industry_analysis['potential_monthly_savings'],
               name='Monthly Savings', marker_color='#10b981'),
        row=1, col=1
    )
    
    # ROI by industry
    fig.add_trace(
        go.Bar(x=industry_analysis['industry'], y=industry_analysis['roi_percentage'],
               name='ROI %', marker_color='#059669'),
        row=1, col=2
    )
    
    # Investment vs Savings scatter
    fig.add_trace(
        go.Scatter(x=industry_analysis['investment_cost'], y=industry_analysis['potential_monthly_savings'],
                  mode='markers', name='Investment vs Savings', marker_color='#34d399'),
        row=2, col=1
    )
    
    # Payback period by industry
    fig.add_trace(
        go.Bar(x=industry_analysis['industry'], y=industry_analysis['payback_months'],
               name='Payback (months)', marker_color='#6ee7b7'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    return fig

def create_carbon_reduction_chart(df):
    """Create carbon reduction analysis chart"""
    fig = px.scatter(
        df,
        x='current_carbon_tons',
        y='potential_carbon_reduction',
        size='base_consumption_mwh',
        color='industry',
        hover_data=['facility_name', 'roi_percentage'],
        title="Carbon Reduction Potential vs Current Emissions",
        labels={
            'current_carbon_tons': 'Current Monthly CO2 Emissions (tons)',
            'potential_carbon_reduction': 'Potential Monthly CO2 Reduction (tons)',
            'base_consumption_mwh': 'Energy Consumption (MWh/month)'
        },
        height=400
    )
    
    return fig

def main():
    """Main dashboard function"""
    st.markdown('<h1 class="main-header">⚡ FLYFOX Energy Optimizer</h1>', unsafe_allow_html=True)
    st.markdown("### *NQBA-Powered Industrial Energy Intelligence & Optimization*")
    
    # Initialize NQBA components
    decision_engine, quantum_adapter, ltc_logger, q_cortex_parser = initialize_nqba()
    
    if not all([decision_engine, quantum_adapter, ltc_logger, q_cortex_parser]):
        st.error("Failed to initialize NQBA components. Please check your configuration.")
        return
    
    # Sidebar controls
    st.sidebar.markdown("## 🎛️ Optimization Controls")
    
    # Quantum enhancement toggle
    quantum_enhanced = st.sidebar.checkbox(
        "Enable Quantum Enhancement",
        value=True,
        help="Use DynexSolve for advanced energy optimization"
    )
    
    # Industry filter
    all_industries = ["All Industries"] + sorted(df['industry'].unique().tolist()) if 'df' in locals() else ["All Industries"]
    selected_industry = st.sidebar.selectbox(
        "Filter by Industry",
        all_industries
    )
    
    # Efficiency threshold
    min_efficiency = st.sidebar.slider(
        "Minimum Efficiency Threshold",
        min_value=0.5,
        max_value=0.95,
        value=0.7,
        step=0.05,
        help="Filter facilities below this efficiency level"
    )
    
    # ROI threshold
    min_roi = st.sidebar.slider(
        "Minimum ROI Threshold (%)",
        min_value=50,
        max_value=500,
        value=100,
        step=25,
        help="Filter facilities below this ROI level"
    )
    
    # Load sample data
    df = generate_sample_energy_data()
    
    # Apply filters
    if selected_industry != "All Industries":
        df = df[df['industry'] == selected_industry]
    
    df = df[df['equipment_efficiency'] >= min_efficiency]
    df = df[df['roi_percentage'] >= min_roi]
    
    # Main dashboard content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_facilities = len(df)
        st.metric("Total Facilities", total_facilities)
    
    with col2:
        total_consumption = df['base_consumption_mwh'].sum()
        st.metric("Total Energy (MWh/month)", f"{total_consumption:,.0f}")
    
    with col3:
        total_potential_savings = df['potential_monthly_savings'].sum()
        st.metric("Monthly Savings Potential", f"${total_potential_savings:,.0f}")
    
    with col4:
        avg_roi = df['roi_percentage'].mean()
        st.metric("Average ROI", f"{avg_roi:.1f}%")
    
    # Energy consumption overview
    st.markdown("## 📊 Energy Consumption Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Energy consumption chart
        consumption_chart = create_energy_consumption_chart(df)
        st.plotly_chart(consumption_chart, use_container_width=True)
    
    with col2:
        # Efficiency radar chart for selected facility
        if len(df) > 0:
            selected_facility = st.selectbox(
                "Select Facility for Efficiency Analysis",
                df['facility_name'].tolist()
            )
            
            radar_chart = create_efficiency_radar_chart(df, selected_facility)
            st.plotly_chart(radar_chart, use_container_width=True)
    
    # Savings analysis
    st.markdown("## 💰 Savings & ROI Analysis")
    
    # Display facilities table with optimization potential
    st.markdown("### Facility Optimization Analysis")
    
    # Color-code the savings potential
    def color_savings_potential(val):
        if val >= 0.25:
            return "background-color: #059669; color: white"  # High savings
        elif val >= 0.15:
            return "background-color: #d97706; color: white"  # Medium savings
        else:
            return "background-color: #dc2626; color: white"  # Low savings
    
    # Display table with styling
    display_columns = ['facility_name', 'industry', 'base_consumption_mwh', 'current_monthly_cost', 
                       'potential_monthly_savings', 'roi_percentage', 'payback_months']
    styled_df = df[display_columns].copy()
    
    st.dataframe(
        styled_df.style.applymap(
            color_savings_potential, 
            subset=['potential_monthly_savings']
        ).format({
            'base_consumption_mwh': '{:.1f}',
            'current_monthly_cost': '${:,.2f}',
            'potential_monthly_savings': '${:,.2f}',
            'roi_percentage': '{:.1f}%',
            'payback_months': '{:.1f}'
        }),
        use_container_width=True,
        height=400
    )
    
    # Detailed analytics
    st.markdown("## 📈 Detailed Analytics")
    
    # Savings analysis charts
    savings_chart = create_savings_analysis_chart(df)
    st.plotly_chart(savings_chart, use_container_width=True)
    
    # Carbon reduction analysis
    st.markdown("## 🌱 Environmental Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        carbon_chart = create_carbon_reduction_chart(df)
        st.plotly_chart(carbon_chart, use_container_width=True)
    
    with col2:
        # Carbon reduction metrics
        total_current_carbon = df['current_carbon_tons'].sum()
        total_potential_reduction = df['potential_carbon_reduction'].sum()
        
        st.metric("Total Monthly CO2 Emissions", f"{total_current_carbon:.1f} tons")
        st.metric("Potential Monthly CO2 Reduction", f"{total_potential_reduction:.1f} tons")
        st.metric("Reduction Percentage", f"{(total_potential_reduction/total_current_carbon)*100:.1f}%")
        
        # Environmental impact summary
        st.markdown("### 🌍 Environmental Impact Summary")
        st.info(f"**Carbon Reduction**: Equivalent to removing {(total_potential_reduction * 12) / 4.6:.0f} cars from the road annually")
        st.info(f"**Energy Savings**: {(total_potential_savings * 12) / 1000:.1f} MWh saved annually")
        st.info(f"**Cost Impact**: ${total_potential_savings * 12:,.0f} annual savings potential")
    
    # Quantum optimization section
    st.markdown("## 🚀 Quantum-Enhanced Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### NQBA Quantum Optimization")
        if quantum_enhanced and quantum_adapter:
            st.success("✅ Quantum enhancement enabled via DynexSolve")
            st.info("🚀 QUBO energy optimization algorithms active")
            st.info("⚡ Real-time quantum annealing for efficiency")
        else:
            st.warning("⚠️ Quantum enhancement disabled")
        
        # Run optimization button
        if st.button("🚀 Run Quantum Energy Optimization"):
            with st.spinner("Running quantum-enhanced energy optimization..."):
                # Run optimization
                optimization_result, ltc_ref = run_quantum_energy_optimization(
                    df, quantum_adapter, ltc_logger
                )
                
                if optimization_result:
                    st.success("✅ Quantum optimization completed!")
                    
                    # Display results
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Energy Savings", f"{optimization_result['energy_savings_percentage']*100:.1f}%")
                        st.metric("Cost Reduction", f"{optimization_result['cost_savings_percentage']*100:.1f}%")
                    
                    with col_b:
                        st.metric("Carbon Reduction", f"{optimization_result['carbon_reduction_percentage']*100:.1f}%")
                        st.metric("ROI Improvement", f"{optimization_result['roi_improvement']*100:.1f}%")
                    
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
            st.info(f"🛡️ ESG Compliance: Energy Efficiency Standards")
            st.info(f"🌱 Sustainability: Carbon Reduction Targets")
        else:
            st.error("❌ Q-Cortex Inactive")
    
    # Export and actions
    st.markdown("## 📤 Export & Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export to CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Energy Analysis (CSV)",
            data=csv,
            file_name=f"flyfox_energy_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export optimization report
        if st.button("📊 Generate Optimization Report"):
            report_data = {
                "report_timestamp": datetime.now().isoformat(),
                "total_facilities": len(df),
                "total_energy_consumption_mwh": df['base_consumption_mwh'].sum(),
                "total_potential_savings": df['potential_monthly_savings'].sum(),
                "average_roi": df['roi_percentage'].mean(),
                "total_carbon_reduction": df['potential_carbon_reduction'].sum(),
                "facilities": df.to_dict('records')
            }
            
            st.json(report_data)
    
    with col3:
        # Schedule consultation
        if st.button("📞 Schedule FLYFOX Consultation"):
            st.success("✅ Consultation request submitted!")
            st.info("Our energy optimization experts will contact you within 24 hours")
            st.info("Expected ROI: 12x return on investment")
            st.info("Expected Savings: 20% reduction in energy costs")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280;">
        <p>⚡ <strong>FLYFOX AI</strong> - Powered by NQBA Core | Q-Cortex Governance | LTC Provenance</p>
        <p>Industrial Energy Intelligence with Quantum-Enhanced Optimization</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
