"""
NQBA Ecosystem - Observability & SRE Package

This package provides comprehensive monitoring, tracing, and incident response
capabilities for the NQBA ecosystem.
"""

from .tracing import (
    TracingConfig,
    NQBATracer,
    TracingMiddleware,
    QuantumJobTracer,
    BusinessUnitTracer,
    get_tracer,
    instrument_fastapi,
    trace_function,
)

from .dashboard import (
    DashboardConfig,
    MetricsCollector,
    DashboardRenderer,
    NQBADashboard,
)

__version__ = "1.0.0"
__author__ = "FLYFOX AI"
__email__ = "hello@flyfoxai.io"

__all__ = [
    # Tracing
    "TracingConfig",
    "NQBATracer",
    "TracingMiddleware",
    "QuantumJobTracer",
    "BusinessUnitTracer",
    "get_tracer",
    "instrument_fastapi",
    "trace_function",
    # Dashboard
    "DashboardConfig",
    "MetricsCollector",
    "DashboardRenderer",
    "NQBADashboard",
]
