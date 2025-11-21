# ==============================================================================
# NQBA Framework - Production Dockerfile
# ==============================================================================
# This Dockerfile builds a production-ready container for the NQBA Framework
# API server. It uses a slim Python base image for reduced size and includes
# health checks for container orchestration.
#
# Build: docker build -t nqba-framework:latest .
# Run:   docker run -p 8080:8080 nqba-framework:latest
# ==============================================================================

# Use Python 3.13 slim variant for smaller image size
# Slim variant excludes unnecessary packages while retaining core functionality
FROM python:3.13-slim

# Set metadata labels for the image
LABEL maintainer="NQBA Framework Team <dev@nqba-framework.com>"
LABEL version="1.0.0"
LABEL description="NQBA Framework - Neuromorphic Quantum Business Architecture"

# Set working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
# This way, dependencies are only reinstalled if requirements.txt changes
COPY requirements.txt ./

# Install Python dependencies
# --no-cache-dir: Reduces image size by not caching pip downloads
# --upgrade: Ensures latest compatible versions are installed
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code
# This is done after installing dependencies to optimize build cache
COPY . .

# Create logs directory for application logs
# Ensures the application has a place to write logs
RUN mkdir -p logs && \
    chmod 755 logs

# Expose port 8080 for the API server
# This is the port where uvicorn will listen for HTTP requests
EXPOSE 8080

# Configure health check for container orchestration
# Docker/Kubernetes can use this to determine if the container is healthy
# Checks every 30 seconds with a 30-second timeout
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

# Set environment variables for production
# These can be overridden when running the container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production \
    LOG_LEVEL=INFO

# Start the API server using uvicorn
# --host 0.0.0.0: Listen on all network interfaces
# --port 8080: Use port 8080 (matches EXPOSE above)
# --workers: Number of worker processes (defaults to 1, can be overridden)
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]

# ==============================================================================
# Usage Examples:
#
# Build the image:
#   docker build -t nqba-framework:latest .
#
# Run with environment variables:
#   docker run -p 8080:8080 \
#     -e DYNEX_API_KEY=your_key \
#     -e DATABASE_URL=postgresql://... \
#     nqba-framework:latest
#
# Run with mounted .env file:
#   docker run -p 8080:8080 --env-file .env nqba-framework:latest
#
# Run with volume for logs:
#   docker run -p 8080:8080 -v $(pwd)/logs:/app/logs nqba-framework:latest
# ==============================================================================
