# NQBA Ecosystem Production Dockerfile
# Multi-stage build for security and optimization

# Stage 1: Build environment
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production runtime
FROM python:3.11-slim as production

# Create non-root user
RUN groupadd -r nqba && useradd -r -g nqba nqba

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ ./src/
COPY run_benchmarks.py .
COPY integration_test_suite.py .

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/reports && \
    chown -R nqba:nqba /app

# Switch to non-root user
USER nqba

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "-m", "uvicorn", "src.nqba_stack.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
