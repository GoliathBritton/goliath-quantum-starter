"""
Prometheus Metrics and OpenTelemetry Tracing Scaffold
"""

from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from starlette.responses import Response
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total API Requests", ["endpoint"])


@app.middleware("http")
async def prometheus_middleware(request, call_next):
    endpoint = request.url.path
    REQUEST_COUNT.labels(endpoint=endpoint).inc()
    response = await call_next(request)
    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# OpenTelemetry setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
