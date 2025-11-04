# FLYFOX AI Deployment Guide
**Production-Ready Quantum Agent Platform**

This guide provides comprehensive instructions for deploying the FLYFOX AI Quantum Agent Platform in production environments.

---

## ðŸ—ï¸ Architecture Overview

### Production Architecture
`
Internet
    â†“
Load Balancer (Azure Application Gateway)
    â†“
Frontend (Vercel / Azure Static Web Apps)
    â†“
API Gateway (Azure API Management)
    â†“
Backend Services (Azure Container Apps / AKS)
    â†“
Quantum Layer (Dynex SDK + qdLLM)
    â†“
External Services (GoliathCRM, Stripe, Deepgram)
`

### Component Overview
- **Frontend:** Next.js 14 with Vercel AI SDK
- **Backend:** FastAPI with Python 3.11+
- **Quantum Engine:** Dynex SDK with fallback to classical methods
- **Database:** Azure Database for PostgreSQL / Redis Cache
- **Monitoring:** Prometheus, Grafana, Application Insights
- **CI/CD:** GitHub Actions with Azure deployment

---

## ðŸš€ Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### 1. Clone Repository
`ash
git clone https://github.com/GoliathBritton/blank-app-1.git
cd blank-app-1
`

### 2. Environment Setup
`ash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
`

**Required Environment Variables:**
`ash
# Quantum (Dynex primary)
DYNEX_API_KEY=your_dynex_api_key_here
DYNEX_ENDPOINT=https://api.dynex.network/v1

# AI Fallbacks
OPENAI_API_KEY=your_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-azure-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# CRM & Billing
GOLIATHCRM_BASE_URL=https://crm.goliath.local
GOLIATHCRM_API_KEY=your_crm_api_key_here
STRIPE_SECRET_KEY=sk_live_your_stripe_key_here

# Branding
PUBLIC_BRAND=FLYFOX AI
REVERSAL_REASONING=enabled
`

### 3. Start Platform
`ash
# Start all services
docker compose up --build

# Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
`

### 4. Verify Installation
`ash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# Check agent catalog
curl http://localhost:8000/api/v1/agents/catalog
`

---

## â˜ï¸ Production Deployment (Azure)

### Prerequisites
- Azure CLI installed and configured
- Docker Hub or Azure Container Registry access
- GitHub repository with Actions enabled
- Domain name and SSL certificates

### 1. Infrastructure Setup

#### Create Resource Group
`ash
az group create --name flyfox-ai-rg --location eastus
`

#### Create Container Registry
`ash
az acr create --resource-group flyfox-ai-rg \
  --name flyfoxaicr \
  --sku Basic \
  --admin-enabled true
`

#### Create Container Apps Environment
`ash
az containerapp env create \
  --name flyfox-ai-env \
  --resource-group flyfox-ai-rg \
  --location eastus
`

### 2. Backend Deployment

#### Build and Push Backend Image
`ash
# Build backend image
docker build -t flyfoxaicr.azurecr.io/flyfox-ai-backend:latest ./backend

# Push to registry
docker push flyfoxaicr.azurecr.io/flyfox-ai-backend:latest
`

#### Deploy Backend Container App
`ash
az containerapp create \
  --name flyfox-ai-backend \
  --resource-group flyfox-ai-rg \
  --environment flyfox-ai-env \
  --image flyfoxaicr.azurecr.io/flyfox-ai-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server flyfoxaicr.azurecr.io \
  --env-vars \
    DYNEX_API_KEY= \
    OPENAI_API_KEY= \
    AZURE_OPENAI_ENDPOINT= \
    AZURE_OPENAI_API_KEY= \
    DEEPGRAM_API_KEY= \
    GOLIATHCRM_BASE_URL= \
    GOLIATHCRM_API_KEY= \
    STRIPE_SECRET_KEY= \
    PUBLIC_BRAND= \
    REVERSAL_REASONING=
`

### 3. Frontend Deployment (Vercel)

#### Install Vercel CLI
`ash
npm i -g vercel
`

#### Deploy to Vercel
`ash
cd frontend
vercel --prod

# Set environment variables
vercel env add NEXT_PUBLIC_API_BASE
vercel env add NEXT_PUBLIC_BRAND
`

### 4. Database Setup

#### Azure Database for PostgreSQL
`ash
az postgres flexible-server create \
  --resource-group flyfox-ai-rg \
  --name flyfox-ai-db \
  --location eastus \
  --admin-user flyfoxadmin \
  --admin-password  \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32
`

#### Redis Cache
`ash
az redis create \
  --resource-group flyfox-ai-rg \
  --name flyfox-ai-cache \
  --location eastus \
  --sku Basic \
  --vm-size c0
`

---

## ðŸ³ Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (AKS, EKS, or GKE)
- kubectl configured
- Helm 3.x installed

### 1. Create Namespace
`ash
kubectl create namespace flyfox-ai
`

### 2. Deploy Backend
`ash
# Apply backend deployment
kubectl apply -f deploy/k8s/backend-deployment.yaml

# Apply backend service
kubectl apply -f deploy/k8s/backend-service.yaml
`

### 3. Deploy Frontend
`ash
# Apply frontend deployment
kubectl apply -f deploy/k8s/frontend-deployment.yaml

# Apply frontend service
kubectl apply -f deploy/k8s/frontend-service.yaml
`

### 4. Configure Ingress
`ash
# Apply ingress configuration
kubectl apply -f deploy/k8s/ingress.yaml
`

---

## ðŸ“Š Monitoring & Observability

### Prometheus Configuration
`yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flyfox-ai-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    
  - job_name: 'flyfox-ai-frontend'
    static_configs:
      - targets: ['frontend:3000']
`

### Grafana Dashboards
- **Quantum Agent Performance:** Agent response times, success rates
- **Business Metrics:** Lead generation, conversion rates, ROI
- **System Health:** CPU, memory, network utilization
- **Error Tracking:** Error rates, response codes, failure patterns

### Application Insights Integration
`python
# Add to backend/app/main.py
from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.trace_exporter import AzureExporter

# Configure Application Insights
exporter = AzureExporter(
    connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
)
`

---

## ðŸ”§ Configuration Management

### Environment-Specific Configurations

#### Development
`ash
NODE_ENV=development
PYTHON_ENV=development
LOG_LEVEL=debug
QUANTUM_MODE=mock
`

#### Staging
`ash
NODE_ENV=staging
PYTHON_ENV=staging
LOG_LEVEL=info
QUANTUM_MODE=hybrid
`

#### Production
`ash
NODE_ENV=production
PYTHON_ENV=production
LOG_LEVEL=warning
QUANTUM_MODE=full
`

### Feature Flags
`python
# Feature flag configuration
FEATURE_FLAGS = {
    'quantum_enhancement': True,
    'reversal_reasoning': True,
    'white_label': True,
    'enterprise_features': False
}
`

---

## ðŸ” Security Configuration

### SSL/TLS Setup
`ash
# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout flyfox-ai.key \
  -out flyfox-ai.crt
`

### API Security
`python
# JWT authentication
from fastapi_jwt_auth import AuthJWT

@AuthJWT.load_config
def get_config():
    return Settings()

# Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
`

### Network Security
- VPC/VNet isolation
- Security groups/firewall rules
- WAF (Web Application Firewall)
- DDoS protection

---

## ðŸš€ CI/CD Pipeline

### GitHub Actions Workflow
`yaml
# .github/workflows/deploy.yml
name: Deploy FLYFOX AI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest
          
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build backend
        run: |
          docker build -t flyfox-ai-backend ./backend
      - name: Build frontend
        run: |
          docker build -t flyfox-ai-frontend ./frontend
          
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Azure
        run: |
          az containerapp update \
            --name flyfox-ai-backend \
            --resource-group flyfox-ai-rg \
            --image flyfoxaicr.azurecr.io/flyfox-ai-backend:latest
`

---

## ðŸ“ˆ Scaling & Performance

### Horizontal Scaling
`ash
# Scale backend replicas
kubectl scale deployment flyfox-ai-backend --replicas=5

# Scale frontend replicas
kubectl scale deployment flyfox-ai-frontend --replicas=3
`

### Auto-scaling Configuration
`yaml
# HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flyfox-ai-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flyfox-ai-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
`

### Performance Optimization
- CDN for static assets
- Redis caching for API responses
- Database connection pooling
- Quantum processing optimization

---

## ðŸ”„ Backup & Disaster Recovery

### Database Backups
`ash
# Automated PostgreSQL backups
pg_dump -h flyfox-ai-db.postgres.database.azure.com \
  -U flyfoxadmin \
  -d flyfox_ai \
  --format=custom \
  --file=backup_.dump
`

### Configuration Backups
`ash
# Backup Kubernetes configurations
kubectl get all -o yaml > k8s-backup-.yaml

# Backup environment variables
kubectl get configmap -o yaml > config-backup-.yaml
`

### Disaster Recovery Plan
1. **RTO (Recovery Time Objective):** 4 hours
2. **RPO (Recovery Point Objective):** 1 hour
3. **Backup Frequency:** Daily full, hourly incremental
4. **Testing Schedule:** Monthly DR drills

---

## ðŸ› ï¸ Troubleshooting

### Common Issues

#### Backend Not Starting
`ash
# Check logs
docker logs flyfox-ai-backend

# Check environment variables
docker exec flyfox-ai-backend env | grep -E "(DYNEX|OPENAI|AZURE)"

# Test API connectivity
curl -v http://localhost:8000/health
`

#### Frontend Build Failures
`ash
# Check Node.js version
node --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check build logs
npm run build
`

#### Quantum Processing Issues
`ash
# Check Dynex connectivity
curl -H "Authorization: Bearer " \
  https://api.dynex.network/v1/status

# Verify fallback configuration
curl http://localhost:8000/api/v1/chat/health
`

### Performance Issues
- Check CPU/memory utilization
- Review database query performance
- Analyze network latency
- Monitor quantum processing times

### Security Issues
- Review access logs
- Check SSL certificate validity
- Verify API authentication
- Monitor for unusual traffic patterns

---

## ðŸ“ž Support & Maintenance

### Support Channels
- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/GoliathBritton/blank-app-1/issues)
- **Enterprise Support:** enterprise@flyfox.ai

### Maintenance Schedule
- **Security Updates:** Weekly
- **Feature Updates:** Monthly
- **Major Releases:** Quarterly
- **Infrastructure Maintenance:** As needed

### Monitoring Alerts
- High error rates (>5%)
- Response time degradation (>2s)
- Resource utilization (>80%)
- Quantum processing failures

---

## ðŸŽ¯ Production Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database migrations completed
- [ ] Monitoring configured
- [ ] Backup procedures tested

### Post-Deployment
- [ ] Health checks passing
- [ ] Performance benchmarks met
- [ ] Security scans completed
- [ ] User acceptance testing passed
- [ ] Documentation updated

### Ongoing Operations
- [ ] Daily monitoring review
- [ ] Weekly performance analysis
- [ ] Monthly security assessment
- [ ] Quarterly capacity planning

---

**FLYFOX AI** - Where Emotional Intelligence Meets Quantum Intelligence  
*"They teach tactics. We teach truth."*

**For additional support, contact:** enterprise@flyfox.ai
