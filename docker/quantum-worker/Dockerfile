# FLYFOX AI - Quantum Worker Dockerfile
# Specialized worker for quantum computing tasks with Dynex integration

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.6.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    cmake \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --only=main --no-root && rm -rf $POETRY_CACHE_DIR

# Install quantum computing packages
RUN poetry run pip install \
    dynex \
    qiskit \
    qiskit-aer \
    qiskit-optimization \
    pennylane \
    pennylane-qiskit \
    cirq \
    pyqubo \
    dimod \
    dwave-ocean-sdk \
    networkx \
    numpy \
    scipy \
    matplotlib \
    sympy \
    cvxpy \
    pulp \
    ortools

# Create non-root user
RUN groupadd -r quantum && useradd -r -g quantum quantum

# Copy application code
COPY --chown=quantum:quantum . .

# Install the application
RUN poetry install --only-root

# Create necessary directories
RUN mkdir -p /app/logs /app/tmp /app/quantum_cache /app/results && \
    chown -R quantum:quantum /app

# Switch to non-root user
USER quantum

# Health check
HEALTHCHECK --interval=120s --timeout=60s --start-period=30s --retries=3 \
    CMD python -c "import dynex; print('Dynex available')" || exit 1

# Production stage
FROM base as production

# Set production environment
ENV ENVIRONMENT=production
ENV LOG_LEVEL=info
ENV QUANTUM_WORKER_CONCURRENCY=1
ENV DYNEX_TIMEOUT=300
ENV QUANTUM_CACHE_SIZE=1000

# Start command
CMD ["poetry", "run", "celery", "worker", "-A", "flyfox.quantum.celery_app", "--loglevel=info", "--concurrency=1", "--queues=quantum,qubo,optimization"]

# Development stage
FROM base as development

# Install development dependencies
RUN poetry install --with=dev

# Install additional development tools
RUN poetry run pip install \
    jupyter \
    ipywidgets \
    qiskit[visualization] \
    pennylane[dev]

# Set development environment
ENV ENVIRONMENT=development
ENV LOG_LEVEL=debug
ENV QUANTUM_WORKER_CONCURRENCY=1
ENV DYNEX_TIMEOUT=60

# Start command for development
CMD ["poetry", "run", "celery", "worker", "-A", "flyfox.quantum.celery_app", "--loglevel=debug", "--concurrency=1", "--reload"]

# Simulation stage for local testing without Dynex
FROM base as simulation

# Install simulation-only packages
RUN poetry run pip install \
    qiskit-aer[gpu] \
    pennylane-lightning[gpu] \
    cirq-simulator

# Set simulation environment
ENV ENVIRONMENT=simulation
ENV LOG_LEVEL=info
ENV QUANTUM_WORKER_CONCURRENCY=2
ENV USE_SIMULATION=true
ENV DYNEX_FALLBACK=classical

# Start command for simulation
CMD ["poetry", "run", "celery", "worker", "-A", "flyfox.quantum.celery_app", "--loglevel=info", "--concurrency=2", "--queues=quantum_sim,qubo_sim"]

# Default to production
FROM production