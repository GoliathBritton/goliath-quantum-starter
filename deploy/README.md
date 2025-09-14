# Goliath Quantum Division - Deployment Guide

🚀 **Enterprise-Ready Deployment for 10K+ Contact Batch Processing**

## Quick Start

### Windows (Recommended)
```bash
# Simple one-click deployment
.\deploy.bat

# Or specify deployment mode
.\deploy.bat docker    # Full containerized deployment
.\deploy.bat local     # Local development deployment
.\deploy.bat hybrid    # Hybrid cloud-local deployment
```

### PowerShell (Advanced)
```powershell
# Full deployment with all options
.\deploy\deploy.ps1 -Environment production -Mode docker

# Skip tests for faster deployment
.\deploy\deploy.ps1 -Environment production -Mode docker -SkipTests

# Force deployment (skip prerequisite checks)
.\deploy\deploy.ps1 -Environment production -Mode docker -Force
```

### Python (Cross-Platform)
```bash
# Async deployment with full orchestration
python deploy/deploy.py

# With custom configuration
python deploy/deploy.py --config deploy/config/deployment.yaml
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 GOLIATH QUANTUM DIVISION                   │
│                Enterprise Architecture                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Web Frontend  │  │   Main API      │  │  NQBA Engine    │
│   Port: 3000    │◄─┤   Port: 8080    │◄─┤   Port: 8000    │
│   React/Next.js │  │   FastAPI       │  │   Quantum Core  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ High Council    │  │ Quantum Architect│  │ Lead Processor  │
│ Port: 8001      │  │ Port: 8002      │  │ Port: 8003      │
│ Governance      │  │ Orchestration   │  │ Batch Engine    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PostgreSQL    │  │     Redis       │  │   AI Calling    │
│   Port: 5432    │  │   Port: 6379    │  │   Port: 8004    │
│   Database      │  │   Cache/Queue   │  │   Voice AI      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Deployment Modes

### 🐳 Docker Mode (Production)
**Recommended for production environments**

- **Full containerization** with Docker Compose
- **Auto-scaling** with load balancing
- **Built-in monitoring** (Prometheus + Grafana)
- **Enterprise security** with isolated networks
- **Zero-downtime deployments**

```bash
.\deploy.bat docker
```

**Features:**
- ✅ 10K+ contact batch processing
- ✅ Quantum-enhanced lead scoring
- ✅ AI-powered calling agents
- ✅ Real-time monitoring dashboards
- ✅ Automatic failover and recovery

### 🏠 Local Mode (Development)
**Perfect for development and testing**

- **Native Python processes** for debugging
- **Hot reload** for rapid development
- **Direct database access** for testing
- **Simplified configuration**

```bash
.\deploy.bat local
```

**Features:**
- ✅ Fast development iteration
- ✅ Easy debugging and profiling
- ✅ Direct file system access
- ✅ Simplified logging

### ☁️ Hybrid Mode (Enterprise)
**Best of both worlds**

- **Critical services** in containers
- **Development services** running locally
- **Cloud database** connections
- **Flexible scaling**

```bash
.\deploy.bat hybrid
```

## Prerequisites

### System Requirements
- **OS:** Windows 10/11, macOS 10.15+, or Linux
- **RAM:** 16GB minimum, 32GB recommended
- **Storage:** 50GB free space
- **CPU:** 8 cores recommended for 10K+ batches

### Software Dependencies
- **Python 3.8+** (3.11 recommended)
- **Node.js 16+** (for web frontend)
- **Docker 20.0+** (for containerized deployment)
- **Docker Compose 2.0+**
- **PostgreSQL 13+** (or use Docker)
- **Redis 6+** (or use Docker)

### Environment Variables
Create a `.env` file with:

```env
# Required API Keys
DYNEX_API_KEY=your_dynex_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_super_secure_secret_key_here

# Optional: Communication APIs
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Optional: Database (if not using Docker)
DATABASE_URL=postgresql://user:pass@localhost:5432/goliath_quantum
REDIS_URL=redis://localhost:6379/0

# Optional: Environment
ENVIRONMENT=production
COMPANY_NAME="Your Company Name"
COMPANY_WEBSITE="https://yourcompany.com"
```

## Post-Deployment

### Access URLs
After successful deployment:

- **🌐 Web Frontend:** http://localhost:3000
- **🔧 Main API:** http://localhost:8080
- **⚛️ NQBA Engine:** http://localhost:8000
- **📊 Grafana Dashboard:** http://localhost:3001
- **📈 Prometheus Metrics:** http://localhost:9090
- **🗄️ Database:** localhost:5432
- **🔄 Redis Cache:** localhost:6379

### Default Credentials
- **Grafana:** admin / quantum_admin_2024
- **Database:** goliath_user / quantum_secure_2024

### Batch Processing

#### Upload Contact Lists
```bash
# Upload CSV file
curl -X POST http://localhost:8080/api/v1/leads/upload \
  -F "file=@contacts.csv" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Process batch
curl -X POST http://localhost:8080/api/v1/leads/process \
  -H "Content-Type: application/json" \
  -d '{"batch_size": 1000, "priority": "high"}'
```

#### Monitor Progress
```bash
# Check batch status
curl http://localhost:8080/api/v1/leads/status/BATCH_ID

# View processing metrics
curl http://localhost:8080/api/v1/metrics/processing
```

## Configuration

### Scaling Configuration
Edit `deploy/config/deployment.yaml`:

```yaml
# Scale for larger batches
batch_size: 50000  # Increase for larger batches
quantum_workers: 8  # More quantum processing power
api_workers: 16     # Handle more concurrent requests

# Performance tuning
performance:
  max_concurrent_batches: 10
  quantum_cache_size: 5000
  connection_pool_size: 100
```

## Troubleshooting

### Common Issues

#### 🔴 Port Already in Use
```bash
# Find and kill process using port
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 🔴 Database Connection Failed
```bash
# Check PostgreSQL status
docker-compose -f deploy/docker-compose.yml logs postgres

# Reset database
docker-compose -f deploy/docker-compose.yml down -v
docker-compose -f deploy/docker-compose.yml up -d postgres
```

#### 🔴 Out of Memory
```bash
# Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory > 8GB+

# Or reduce worker count in deployment.yaml
api_workers: 4
quantum_workers: 2
```

### Performance Optimization

#### For 10K+ Contact Batches
1. **Increase worker counts** in deployment.yaml
2. **Enable quantum caching** for repeated QUBO problems
3. **Use SSD storage** for database and cache
4. **Allocate 32GB+ RAM** for large batches
5. **Enable connection pooling** with higher limits

---

**🎉 Ready to deploy? Run `./deploy.bat` and watch the magic happen!**

This directory contains infrastructure-as-code and deployment configurations for the NQBA Platform across multiple environments and cloud providers.

## Directory Structure

```
deploy/
├── README.md                 # This file
├── docker/                   # Docker configurations
│   ├── Dockerfile.api        # API server container
│   ├── Dockerfile.worker     # Background worker container
│   ├── Dockerfile.frontend   # Frontend application container
│   └── docker-compose.yml    # Local development stack
├── kubernetes/               # Kubernetes manifests
│   ├── base/                 # Base configurations
│   ├── overlays/             # Environment-specific overlays
│   │   ├── development/      # Development environment
│   │   ├── staging/          # Staging environment
│   │   └── production/       # Production environment
│   └── helm/                 # Helm charts
├── terraform/                # Terraform/OpenTofu configurations
│   ├── modules/              # Reusable modules
│   ├── environments/         # Environment-specific configs
│   │   ├── dev/              # Development infrastructure
│   │   ├── staging/          # Staging infrastructure
│   │   └── prod/             # Production infrastructure
│   └── providers/            # Cloud provider configurations
│       ├── aws/              # AWS-specific resources
│       ├── azure/            # Azure-specific resources
│       └── gcp/              # Google Cloud-specific resources
├── scripts/                  # Deployment and utility scripts
│   ├── deploy.sh             # Main deployment script
│   ├── setup-env.sh          # Environment setup
│   ├── backup.sh             # Backup procedures
│   └── monitoring.sh         # Monitoring setup
└── configs/                  # Configuration files
    ├── nginx/                # Nginx configurations
    ├── prometheus/           # Monitoring configurations
    └── grafana/              # Dashboard configurations
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (local or cloud)
- Terraform/OpenTofu >= 1.0
- kubectl configured
- Helm >= 3.0

### Local Development

```bash
# Start local development stack
cd deploy/docker
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f
```

### Cloud Deployment

```bash
# Setup environment
./scripts/setup-env.sh <environment>

# Deploy infrastructure
cd terraform/environments/<env>
terraform init
terraform plan
terraform apply

# Deploy application
./scripts/deploy.sh <environment>
```

## Environments

### Development
- **Purpose**: Local development and testing
- **Resources**: Minimal, single-node setup
- **Database**: PostgreSQL container
- **Monitoring**: Basic logging

### Staging
- **Purpose**: Pre-production testing and validation
- **Resources**: Production-like but smaller scale
- **Database**: Managed database service
- **Monitoring**: Full observability stack

### Production
- **Purpose**: Live customer-facing environment
- **Resources**: High availability, auto-scaling
- **Database**: Multi-AZ managed database
- **Monitoring**: Enterprise-grade observability

## Security

### Secrets Management
- Kubernetes secrets for sensitive data
- External secret management (AWS Secrets Manager, Azure Key Vault)
- Encrypted at rest and in transit

### Network Security
- Private subnets for application components
- Network policies for pod-to-pod communication
- WAF and DDoS protection

### Access Control
- RBAC for Kubernetes
- IAM roles and policies
- Service mesh for zero-trust networking

## Monitoring & Observability

### Metrics
- Prometheus for metrics collection
- Grafana for visualization
- Custom business metrics

### Logging
- Centralized logging with ELK/EFK stack
- Structured logging format
- Log aggregation and analysis

### Tracing
- Distributed tracing with Jaeger
- Performance monitoring
- Error tracking

### Alerting
- AlertManager for alert routing
- PagerDuty integration
- Slack notifications

## Backup & Disaster Recovery

### Database Backups
- Automated daily backups
- Point-in-time recovery
- Cross-region replication

### Application Backups
- Configuration backups
- Persistent volume snapshots
- Disaster recovery procedures

## Scaling

### Horizontal Pod Autoscaling
- CPU and memory-based scaling
- Custom metrics scaling
- Predictive scaling

### Cluster Autoscaling
- Node auto-scaling based on demand
- Spot instance integration
- Cost optimization

## CI/CD Integration

### GitOps Workflow
- ArgoCD for continuous deployment
- Git-based configuration management
- Automated rollbacks

### Pipeline Integration
- GitHub Actions workflows
- Automated testing and deployment
- Security scanning

## Cost Optimization

### Resource Management
- Resource requests and limits
- Vertical pod autoscaling
- Cluster optimization

### Cloud Cost Management
- Reserved instances
- Spot instances for non-critical workloads
- Cost monitoring and alerting

## Troubleshooting

### Common Issues
- Pod startup failures
- Resource constraints
- Network connectivity

### Debug Commands
```bash
# Check pod status
kubectl get pods -n nqba

# View pod logs
kubectl logs -f <pod-name> -n nqba

# Describe pod for events
kubectl describe pod <pod-name> -n nqba

# Check resource usage
kubectl top pods -n nqba
```

## Support

For deployment issues and questions:
- Documentation: [docs/deployment.md](../docs/deployment.md)
- Issues: [GitHub Issues](https://github.com/flyfox-ai/nqba/issues)
- Support: support@flyfox.ai

---

*Last Updated: January 2025*
*Version: 1.0.0*