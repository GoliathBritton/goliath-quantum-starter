"""
Golden Dashboards for NQBA Ecosystem.
Real-time monitoring, SLO tracking, and performance insights.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
import logging
from typing import Dict, List, Any, Optional
import asyncio
import threading

logger = logging.getLogger(__name__)


class DashboardConfig:
    """Configuration for dashboard components."""

    def __init__(self):
        self.refresh_interval = 30  # seconds
        self.history_hours = 24
        self.quantum_advantage_threshold = 3.4  # 3.4x improvement target
        self.slo_targets = {
            "api_latency_p95": 200,  # ms
            "quantum_success_rate": 0.95,  # 95%
            "workflow_completion_rate": 0.98,  # 98%
            "uptime": 0.999,  # 99.9%
        }


class MetricsCollector:
    """Collects and processes metrics from various sources."""

    def __init__(self):
        self.metrics_cache = {}
        self.last_update = None

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics."""
        # Mock data - replace with actual metrics collection
        return {
            "status": "healthy",
            "uptime": 99.97,
            "active_users": 42,
            "quantum_jobs_running": 8,
            "classical_jobs_running": 12,
            "last_quantum_advantage": 3.2,
            "target_quantum_advantage": 410.7,
        }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance and latency metrics."""
        return {
            "api_latency_p50": 45,
            "api_latency_p95": 180,
            "api_latency_p99": 320,
            "quantum_success_rate": 0.94,
            "classical_success_rate": 0.99,
            "workflow_completion_rate": 0.97,
        }

    def get_business_metrics(self) -> Dict[str, Any]:
        """Get business and revenue metrics."""
        return {
            "arr": 2500000,  # $2.5M ARR
            "cac": 1500,  # Customer Acquisition Cost
            "ltv": 15000,  # Lifetime Value
            "nps": 72,
            "conversion_rate": 0.15,
            "quantum_win_rate": 0.68,
        }

    def get_quantum_metrics(self) -> Dict[str, Any]:
        """Get quantum-specific metrics."""
        return {
            "dynex_qubits_available": 1000000,
            "dynex_qubits_utilized": 750000,
            "quantum_jobs_completed": 1250,
            "quantum_jobs_failed": 75,
            "quantum_advantage_achieved": 3.2,
            "classical_fallback_rate": 0.12,
        }

    def get_workflow_metrics(self) -> List[Dict[str, Any]]:
        """Get workflow execution metrics."""
        workflows = [
            {
                "name": "SigmaEQ Lead Scoring",
                "success_rate": 0.96,
                "avg_time": 2.3,
                "volume": 150,
            },
            {
                "name": "Energy Optimization",
                "success_rate": 0.94,
                "avg_time": 8.7,
                "volume": 89,
            },
            {
                "name": "Portfolio Optimization",
                "success_rate": 0.92,
                "avg_time": 15.2,
                "volume": 67,
            },
            {
                "name": "Insurance Risk Assessment",
                "success_rate": 0.89,
                "avg_time": 4.1,
                "volume": 112,
            },
            {
                "name": "Training Content Generation",
                "success_rate": 0.98,
                "avg_time": 1.8,
                "volume": 203,
            },
        ]
        return workflows


class DashboardRenderer:
    """Renders dashboard components and visualizations."""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector

    def render_header(self):
        """Render dashboard header with key metrics."""
        st.title("🚀 NQBA Ecosystem - Golden Dashboard")
        st.markdown(
            "Real-time monitoring and performance insights for the Quantum Intelligence Economy"
        )

        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            health = self.metrics.get_system_health()
            st.metric("System Status", health["status"].title(), delta="+0.03%")

        with col2:
            st.metric("Uptime", f"{health['uptime']:.2f}%", delta="+0.01%")

        with col3:
            st.metric("Active Users", health["active_users"], delta="+3")

        with col4:
            st.metric("Quantum Jobs", health["quantum_jobs_running"], delta="+2")

    def render_performance_overview(self):
        """Render performance overview section."""
        st.header("📊 Performance Overview")

        # Latency metrics
        perf_metrics = self.metrics.get_performance_metrics()

        col1, col2 = st.columns(2)

        with col1:
            # Latency chart
            latency_data = {
                "Percentile": ["P50", "P95", "P99"],
                "Latency (ms)": [
                    perf_metrics["api_latency_p50"],
                    perf_metrics["api_latency_p95"],
                    perf_metrics["api_latency_p99"],
                ],
            }
            df_latency = pd.DataFrame(latency_data)

            fig = px.bar(
                df_latency,
                x="Percentile",
                y="Latency (ms)",
                title="API Latency Distribution",
                color="Latency (ms)",
                color_continuous_scale="RdYlGn_r",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Success rates
            success_data = {
                "Service": ["Quantum", "Classical", "Workflows"],
                "Success Rate": [
                    perf_metrics["quantum_success_rate"] * 100,
                    perf_metrics["classical_success_rate"] * 100,
                    perf_metrics["workflow_completion_rate"] * 100,
                ],
            }
            df_success = pd.DataFrame(success_data)

            fig = px.pie(
                df_success,
                values="Success Rate",
                names="Service",
                title="Success Rates by Service Type",
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    def render_quantum_advantage(self):
        """Render quantum advantage tracking."""
        st.header("⚛️ Quantum Advantage Tracking")

        quantum_metrics = self.metrics.get_quantum_metrics()
        health = self.metrics.get_system_health()

        # Quantum advantage progress
        current_advantage = quantum_metrics["quantum_advantage_achieved"]
        target_advantage = health["target_quantum_advantage"]
        progress = min(current_advantage / target_advantage, 1.0)

        st.metric("Current Quantum Advantage", f"{current_advantage:.1f}x")
        st.metric("Target Quantum Advantage", f"{target_advantage:.1f}x")

        # Progress bar
        st.progress(progress)
        st.caption(f"Progress: {progress*100:.1f}% towards target")

        # Quantum vs Classical comparison
        col1, col2 = st.columns(2)

        with col1:
            # Quantum utilization
            utilization = (
                quantum_metrics["dynex_qubits_utilized"]
                / quantum_metrics["dynex_qubits_available"]
            ) * 100

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=utilization,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Dynex Qubit Utilization"},
                    delta={"reference": 80},
                    gauge={
                        "axis": {"range": [None, 100]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [0, 50], "color": "lightgray"},
                            {"range": [50, 80], "color": "yellow"},
                            {"range": [80, 100], "color": "green"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 90,
                        },
                    },
                )
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Job completion rates
            quantum_completed = quantum_metrics["quantum_jobs_completed"]
            quantum_failed = quantum_metrics["quantum_jobs_failed"]
            total_quantum = quantum_completed + quantum_failed

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=["Completed", "Failed"],
                        values=[quantum_completed, quantum_failed],
                        hole=0.3,
                        marker_colors=["green", "red"],
                    )
                ]
            )
            fig.update_layout(title="Quantum Job Completion Rate", height=400)
            st.plotly_chart(fig, use_container_width=True)

    def render_business_metrics(self):
        """Render business and revenue metrics."""
        st.header("💰 Business Metrics")

        business_metrics = self.metrics.get_business_metrics()

        # Key business KPIs
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("ARR", f"${business_metrics['arr']:,}", delta="+$125K")

        with col2:
            st.metric(
                "LTV/CAC Ratio",
                f"{business_metrics['ltv']/business_metrics['cac']:.1f}",
                delta="+0.2",
            )

        with col3:
            st.metric("NPS Score", business_metrics["nps"], delta="+3")

        # Revenue and conversion trends
        col1, col2 = st.columns(2)

        with col1:
            # Conversion funnel
            funnel_data = {
                "Stage": ["Visitors", "Leads", "Opportunities", "Customers"],
                "Count": [1000, 150, 75, 11],
            }
            df_funnel = pd.DataFrame(funnel_data)

            fig = px.funnel(df_funnel, x="Count", y="Stage", title="Conversion Funnel")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Quantum win rate over time (mock data)
            dates = pd.date_range(
                start=datetime.now() - timedelta(days=30), end=datetime.now(), freq="D"
            )
            win_rates = [0.65 + 0.03 * i + 0.02 * (i % 7) for i in range(len(dates))]

            fig = px.line(
                x=dates,
                y=win_rates,
                title="Quantum Win Rate Trend",
                labels={"x": "Date", "y": "Win Rate"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    def render_workflow_metrics(self):
        """Render workflow execution metrics."""
        st.header("🔄 Workflow Performance")

        workflows = self.metrics.get_workflow_metrics()
        df_workflows = pd.DataFrame(workflows)

        # Workflow success rates
        fig = px.bar(
            df_workflows,
            x="name",
            y="success_rate",
            title="Workflow Success Rates",
            color="success_rate",
            color_continuous_scale="RdYlGn",
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Workflow volume and performance matrix
        col1, col2 = st.columns(2)

        with col1:
            # Volume vs Success Rate scatter
            fig = px.scatter(
                df_workflows,
                x="volume",
                y="success_rate",
                size="avg_time",
                color="name",
                title="Workflow Volume vs Success Rate",
                labels={"volume": "Daily Volume", "success_rate": "Success Rate"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Average execution time
            fig = px.bar(
                df_workflows,
                x="name",
                y="avg_time",
                title="Average Workflow Execution Time (minutes)",
                color="avg_time",
                color_continuous_scale="RdYlGn_r",
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    def render_slo_dashboard(self):
        """Render SLO (Service Level Objective) dashboard."""
        st.header("🎯 SLO Dashboard")

        perf_metrics = self.metrics.get_performance_metrics()
        config = DashboardConfig()

        # SLO status
        slo_status = []

        for metric, target in config.slo_targets.items():
            if metric == "api_latency_p95":
                current = perf_metrics["api_latency_p95"]
                status = "✅" if current <= target else "❌"
                slo_status.append(
                    {
                        "SLO": "API Latency P95",
                        "Target": f"≤{target}ms",
                        "Current": f"{current}ms",
                        "Status": status,
                    }
                )
            elif metric == "quantum_success_rate":
                current = perf_metrics["quantum_success_rate"]
                status = "✅" if current >= target else "❌"
                slo_status.append(
                    {
                        "SLO": "Quantum Success Rate",
                        "Target": f"≥{target*100}%",
                        "Current": f"{current*100:.1f}%",
                        "Status": status,
                    }
                )
            elif metric == "workflow_completion_rate":
                current = perf_metrics["workflow_completion_rate"]
                status = "✅" if current >= target else "❌"
                slo_status.append(
                    {
                        "SLO": "Workflow Completion Rate",
                        "Target": f"≥{target*100}%",
                        "Current": f"{current*100:.1f}%",
                        "Status": status,
                    }
                )

        df_slo = pd.DataFrame(slo_status)
        st.dataframe(df_slo, use_container_width=True)

        # SLO trend visualization
        st.subheader("SLO Trend (Last 24 Hours)")

        # Mock trend data
        hours = list(range(24))
        latency_trend = [180 + 20 * (i % 6) for i in hours]
        success_trend = [0.94 + 0.02 * (i % 4) for i in hours]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=latency_trend,
                name="API Latency P95 (ms)",
                line=dict(color="red"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[200] * 24,
                name="SLO Target (200ms)",
                line=dict(color="red", dash="dash"),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[x * 1000 for x in success_trend],
                name="Success Rate (%)",
                line=dict(color="green"),
                yaxis="y2",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=hours,
                y=[950] * 24,
                name="SLO Target (95%)",
                line=dict(color="green", dash="dash"),
                yaxis="y2",
            )
        )

        fig.update_layout(
            title="SLO Performance Over Time",
            xaxis_title="Hours Ago",
            yaxis=dict(title="Latency (ms)", side="left"),
            yaxis2=dict(title="Success Rate (%)", side="right", overlaying="y"),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)


class NQBADashboard:
    """Main dashboard application."""

    def __init__(self):
        self.config = DashboardConfig()
        self.metrics = MetricsCollector()
        self.renderer = DashboardRenderer(self.metrics)

    def run(self):
        """Run the dashboard application."""
        st.set_page_config(
            page_title="NQBA Ecosystem Dashboard",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # Sidebar
        st.sidebar.title("🔧 Dashboard Controls")

        # Refresh control
        if st.sidebar.button("🔄 Refresh Metrics"):
            st.rerun()

        # Auto-refresh toggle
        auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)

        # Time range selector
        time_range = st.sidebar.selectbox(
            "Time Range",
            ["Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            index=1,
        )

        # Main dashboard
        self.renderer.render_header()

        # Performance overview
        self.renderer.render_performance_overview()

        # Quantum advantage tracking
        self.renderer.render_quantum_advantage()

        # Business metrics
        self.renderer.render_business_metrics()

        # Workflow metrics
        self.renderer.render_workflow_metrics()

        # SLO dashboard
        self.renderer.render_slo_dashboard()

        # Footer
        st.markdown("---")
        st.markdown(
            "**NQBA Ecosystem Dashboard** | "
            "Built with ❤️ by FLYFOX AI | "
            f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Auto-refresh logic
        if auto_refresh:
            time.sleep(self.config.refresh_interval)
            st.rerun()


def main():
    """Main entry point for the dashboard."""
    dashboard = NQBADashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
