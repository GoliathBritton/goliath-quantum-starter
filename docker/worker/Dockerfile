# FLYFOX AI - Worker Service Dockerfile
# Background task processor with GPU support

FROM nvidia/cuda:12.2-runtime-ubuntu22.04 as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive \
    POETRY_VERSION=1.6.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    build-essential \
    curl \
    git \
    libpq-dev \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create symlinks for python
RUN ln -s /usr/bin/python3.11 /usr/bin/python && \
    ln -s /usr/bin/python3.11 /usr/bin/python3

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

# Install additional AI/ML packages
RUN poetry run pip install \
    torch \
    torchvision \
    torchaudio \
    transformers \
    openai \
    anthropic \
    langchain \
    chromadb \
    sentence-transformers \
    numpy \
    scipy \
    scikit-learn \
    pandas \
    matplotlib \
    seaborn \
    plotly \
    jupyter

# Create non-root user
RUN groupadd -r flyfox && useradd -r -g flyfox flyfox

# Copy application code
COPY --chown=flyfox:flyfox . .

# Install the application
RUN poetry install --only-root

# Create necessary directories
RUN mkdir -p /app/logs /app/tmp /app/data /app/models && \
    chown -R flyfox:flyfox /app

# Switch to non-root user
USER flyfox

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=10s --retries=3 \
    CMD python -c "import redis; r=redis.Redis(host='redis', port=6379); r.ping()" || exit 1

# Production stage
FROM base as production

# Set production environment
ENV ENVIRONMENT=production
ENV LOG_LEVEL=info
ENV WORKER_CONCURRENCY=4
ENV WORKER_PREFETCH_MULTIPLIER=1

# Start command
CMD ["poetry", "run", "celery", "worker", "-A", "flyfox.worker.celery_app", "--loglevel=info", "--concurrency=4", "--prefetch-multiplier=1"]

# Development stage
FROM base as development

# Install development dependencies
RUN poetry install --with=dev

# Set development environment
ENV ENVIRONMENT=development
ENV LOG_LEVEL=debug
ENV WORKER_CONCURRENCY=2

# Start command for development
CMD ["poetry", "run", "celery", "worker", "-A", "flyfox.worker.celery_app", "--loglevel=debug", "--concurrency=2", "--reload"]

# GPU stage for CUDA workloads
FROM base as gpu

# Install CUDA-specific packages
RUN poetry run pip install \
    cupy-cuda12x \
    cudf-cu12 \
    cuml-cu12 \
    cugraph-cu12 \
    cuspatial-cu12

# Set GPU environment
ENV ENVIRONMENT=production
ENV LOG_LEVEL=info
ENV WORKER_CONCURRENCY=2
ENV CUDA_VISIBLE_DEVICES=0
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Start command for GPU workers
CMD ["poetry", "run", "celery", "worker", "-A", "flyfox.worker.celery_app", "--loglevel=info", "--concurrency=2", "--queues=gpu,default"]

# Default to production
FROM production