# Goliath Quantum Starter Dockerfile
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose API port
EXPOSE 8080

# Healthcheck (optional, for Compose)
HEALTHCHECK CMD curl --fail http://localhost:8080/healthz || exit 1

# Start API server (production)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
