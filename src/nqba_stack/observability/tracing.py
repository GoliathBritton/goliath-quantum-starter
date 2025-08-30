"""
OpenTelemetry tracing system for NQBA ecosystem.
Provides end-to-end tracing from frontend through API to quantum solvers.
"""

import os
import logging
from typing import Optional, Dict, Any, Callable
from contextlib import contextmanager
from datetime import datetime, timezone
import time

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.trace import Span, Status, StatusCode
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    TRACING_AVAILABLE = True
except ImportError:
    TRACING_AVAILABLE = False
    trace = None
    Span = None
    Status = None
    StatusCode = None

logger = logging.getLogger(__name__)


class TracingConfig:
    """Configuration for OpenTelemetry tracing."""

    def __init__(self):
        self.enabled = os.getenv("NQBA_TRACING_ENABLED", "true").lower() == "true"
        self.service_name = os.getenv("NQBA_SERVICE_NAME", "nqba-ecosystem")
        self.service_version = os.getenv("NQBA_SERVICE_VERSION", "1.0.0")
        self.environment = os.getenv("NQBA_ENVIRONMENT", "development")

        # Exporters
        self.jaeger_endpoint = os.getenv(
            "NQBA_JAEGER_ENDPOINT", "http://localhost:14268/api/traces"
        )
        self.otlp_endpoint = os.getenv("NQBA_OTLP_ENDPOINT", "http://localhost:4317")
        self.console_export = os.getenv("NQBA_CONSOLE_EXPORT", "true").lower() == "true"

        # Sampling
        self.sample_rate = float(os.getenv("NQBA_SAMPLE_RATE", "1.0"))

        # Resource attributes
        self.resource_attributes = {
            "service.name": self.service_name,
            "service.version": self.service_version,
            "deployment.environment": self.environment,
            "nqba.ecosystem": "true",
            "nqba.quantum_backend": "dynex",
        }


class NQBATracer:
    """NQBA-specific tracing wrapper around OpenTelemetry."""

    def __init__(self, config: TracingConfig):
        self.config = config
        self.tracer_provider = None
        self.tracer = None

        if TRACING_AVAILABLE and config.enabled:
            self._initialize_tracing()
        else:
            logger.warning(
                "OpenTelemetry not available or disabled. Tracing will be no-op."
            )

    def _initialize_tracing(self):
        """Initialize OpenTelemetry tracing."""
        try:
            # Create resource
            resource = Resource.create(attributes=self.config.resource_attributes)

            # Create tracer provider
            self.tracer_provider = TracerProvider(resource=resource)

            # Add exporters
            if self.config.console_export:
                console_exporter = ConsoleSpanExporter()
                self.tracer_provider.add_span_processor(
                    BatchSpanProcessor(console_exporter)
                )

            # Add Jaeger exporter if configured
            if self.config.jaeger_endpoint:
                jaeger_exporter = JaegerExporter(
                    collector_endpoint=self.config.jaeger_endpoint
                )
                self.tracer_provider.add_span_processor(
                    BatchSpanProcessor(jaeger_exporter)
                )

            # Add OTLP exporter if configured
            if self.config.otlp_endpoint:
                otlp_exporter = OTLPSpanExporter(endpoint=self.config.otlp_endpoint)
                self.tracer_provider.add_span_processor(
                    BatchSpanProcessor(otlp_exporter)
                )

            # Set global tracer provider
            trace.set_tracer_provider(self.tracer_provider)

            # Create tracer
            self.tracer = trace.get_tracer(self.config.service_name)

            logger.info("OpenTelemetry tracing initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize OpenTelemetry tracing: {e}")
            self.tracer = None

    def start_span(
        self, name: str, attributes: Optional[Dict[str, Any]] = None
    ) -> Optional["Span"]:
        """Start a new span."""
        if not self.tracer:
            return None

        try:
            span = self.tracer.start_span(name, attributes=attributes or {})
            return span
        except Exception as e:
            logger.error(f"Failed to start span '{name}': {e}")
            return None

    @contextmanager
    def span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Context manager for automatic span management."""
        span = self.start_span(name, attributes)
        if not span:
            yield
            return

        try:
            yield span
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            raise
        finally:
            span.end()

    def add_event(
        self,
        span: Optional[Span],
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        """Add an event to a span."""
        if span:
            try:
                span.add_event(name, attributes or {})
            except Exception as e:
                logger.error(f"Failed to add event '{name}' to span: {e}")

    def set_attribute(self, span: Optional[Span], key: str, value: Any):
        """Set an attribute on a span."""
        if span:
            try:
                span.set_attribute(key, value)
            except Exception as e:
                logger.error(f"Failed to set attribute '{key}' on span: {e}")

    def set_status(self, span: Optional[Span], status: Status):
        """Set the status of a span."""
        if span:
            try:
                span.set_status(status)
            except Exception as e:
                logger.error(f"Failed to set status on span: {e}")


class TracingMiddleware:
    """FastAPI middleware for automatic tracing."""

    def __init__(self, tracer: NQBATracer):
        self.tracer = tracer

    async def __call__(self, request, call_next):
        if not self.tracer.tracer:
            return await call_next(request)

        # Extract span context from headers
        span_context = trace.get_current_span().get_span_context()

        with self.tracer.span("http_request") as span:
            # Set request attributes
            self.tracer.set_attribute(span, "http.method", request.method)
            self.tracer.set_attribute(span, "http.url", str(request.url))
            self.tracer.set_attribute(
                span, "http.user_agent", request.headers.get("user-agent", "")
            )
            self.tracer.set_attribute(
                span, "http.request_id", request.headers.get("x-request-id", "")
            )

            # Add business context
            self.tracer.set_attribute(
                span, "nqba.user_id", request.headers.get("x-user-id", "")
            )
            self.tracer.set_attribute(
                span, "nqba.org_id", request.headers.get("x-org-id", "")
            )

            start_time = time.time()

            try:
                response = await call_next(request)

                # Set response attributes
                self.tracer.set_attribute(
                    span, "http.status_code", response.status_code
                )
                self.tracer.set_attribute(
                    span, "http.response_time_ms", (time.time() - start_time) * 1000
                )

                return response

            except Exception as e:
                self.tracer.set_status(span, Status(StatusCode.ERROR, str(e)))
                self.tracer.add_event(
                    span, "exception", {"error": str(e), "type": type(e).__name__}
                )
                raise


class QuantumJobTracer:
    """Specialized tracer for quantum job execution."""

    def __init__(self, tracer: NQBATracer):
        self.tracer = tracer

    def trace_job_submission(self, job_id: str, user_id: str, solver_type: str):
        """Trace quantum job submission."""
        return self.tracer.span("quantum_job_submission")

    def trace_job_execution(self, job_id: str, solver_type: str, problem_size: int):
        """Trace quantum job execution."""
        return self.tracer.span("quantum_job_execution")

    def trace_solver_fallback(
        self, job_id: str, from_solver: str, to_solver: str, reason: str
    ):
        """Trace solver fallback events."""
        return self.tracer.span("quantum_solver_fallback")


class BusinessUnitTracer:
    """Specialized tracer for business unit operations."""

    def __init__(self, tracer: NQBATracer):
        self.tracer = tracer

    def trace_bu_operation(self, bu_name: str, operation: str, user_id: str):
        """Trace business unit operations."""
        return self.tracer.span("business_unit_operation")

    def trace_workflow_execution(self, workflow_id: str, bu_name: str, step_count: int):
        """Trace workflow execution."""
        return self.tracer.span("workflow_execution")


def get_tracer() -> NQBATracer:
    """Get the global tracer instance."""
    config = TracingConfig()
    return NQBATracer(config)


def instrument_fastapi(app, tracer: NQBATracer):
    """Instrument FastAPI with OpenTelemetry."""
    if not TRACING_AVAILABLE or not tracer.tracer:
        return

    try:
        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)

        # Instrument Redis if available
        try:
            RedisInstrumentor().instrument()
        except Exception:
            pass

        # Instrument requests if available
        try:
            RequestsInstrumentor().instrument()
        except Exception:
            pass

        logger.info("FastAPI instrumented with OpenTelemetry")

    except Exception as e:
        logger.error(f"Failed to instrument FastAPI: {e}")


def trace_function(name: str, attributes: Optional[Dict[str, Any]] = None):
    """Decorator for tracing function execution."""

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            with tracer.span(name, attributes) as span:
                try:
                    result = func(*args, **kwargs)
                    tracer.set_attribute(
                        span, "function.result_type", type(result).__name__
                    )
                    return result
                except Exception as e:
                    tracer.set_status(span, Status(StatusCode.ERROR, str(e)))
                    tracer.add_event(
                        span, "exception", {"error": str(e), "type": type(e).__name__}
                    )
                    raise

        return wrapper

    return decorator
