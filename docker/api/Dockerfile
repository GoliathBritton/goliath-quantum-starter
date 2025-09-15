# FLYFOX AI - API Service Dockerfile
# Production-ready FastAPI application container

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

# Create non-root user
RUN groupadd -r flyfox && useradd -r -g flyfox flyfox

# Copy application code
COPY --chown=flyfox:flyfox . .

# Install the application
RUN poetry install --only-root

# Create necessary directories
RUN mkdir -p /app/logs /app/tmp && \
    chown -R flyfox:flyfox /app

# Switch to non-root user
USER flyfox

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production stage
FROM base as production

# Set production environment
ENV ENVIRONMENT=production
ENV LOG_LEVEL=info
ENV WORKERS=4

# Start command
CMD ["poetry", "run", "uvicorn", "flyfox.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Development stage
FROM base as development

# Install development dependencies
RUN poetry install --with=dev

# Set development environment
ENV ENVIRONMENT=development
ENV LOG_LEVEL=debug
ENV RELOAD=true

# Start command for development
CMD ["poetry", "run", "uvicorn", "flyfox.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Default to production
FROM production