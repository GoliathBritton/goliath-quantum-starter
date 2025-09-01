# NQBA Phase 2 Deployment Guide

## Overview
This document provides comprehensive deployment instructions for the NQBA Phase 2 platform, which includes:
- Unified Dashboard (cross-pillar analytics)
- Integrations (UiPath, n8n, Mendix, Prismatic)
- Quantum Security (Dynex-anchored)

## Prerequisites

### System Requirements
- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 15+
- Redis 7+

### Environment Setup
1. Copy `.env.example` to `.env`
2. Fill in required environment variables:
   ```bash
   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   DATABASE_URL=postgresql://postgres:postgres@db:5432/nqba
   REDIS_URL=redis://redis:6379/0
   
   # Dynex Configuration
   DYNEX_API_KEY=your_dynex_api_key
   DYNEX_MAINNET=true
   
   # Security
   JWT_SECRET=your_64_character_jwt_secret
   
   # Third-party Integrations
   UIPATH_API_KEY=your_uipath_key
   N8N_WEBHOOK_SECRET=your_n8n_secret
   MENDIX_APP_KEY=your_mendix_key
   PRISMATIC_API_KEY=your_prismatic_key
   ```

## Quick Start (Docker)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd nqba-phase2
cp .env.example .env
# Edit .env with your configuration
```

### 2. Start Services
```bash
docker-compose -f docker-compose.phase2.yml up --build -d
```

### 3. Verify Deployment
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Local Development

### Backend (FastAPI)
```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)
```bash
cd web
npm install
npm run dev
```

### Database Setup
```bash
# Using Docker
docker run --name nqba-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=nqba -p 5432:5432 -d postgres:15

# Or using local PostgreSQL
createdb nqba
```

## Production Deployment

### AWS ECS Deployment
1. Build and push Docker images to ECR
2. Deploy using provided CloudFormation templates
3. Configure environment variables in ECS task definitions

### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f infra/k8s/

# Check deployment status
kubectl get pods -n nqba-phase2
kubectl get services -n nqba-phase2
```

### Environment Variables (Production)
```bash
# Required for production
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/nqba
REDIS_URL=redis://host:6379/0
JWT_SECRET=your_secure_jwt_secret
DYNEX_API_KEY=your_dynex_key
```

## Integration Setup

### UiPath Integration
1. Obtain UiPath Cloud API credentials
2. Configure in the Integrations page
3. Test connection via the UI

### n8n Integration
1. Set up n8n webhook endpoint
2. Configure API key and base URL
3. Test workflow execution

### Mendix Integration
1. Get Mendix app credentials
2. Configure app ID and environment
3. Test deployment capabilities

### Prismatic Integration
1. Obtain Prismatic API credentials
2. Configure instance URL and organization
3. Test connector creation

## Security Configuration

### Quantum Key Rotation
1. Configure Dynex API key
2. Set up automated key rotation schedule
3. Monitor audit logs for compliance

### Compliance Checks
1. Run initial compliance assessment
2. Configure automated compliance monitoring
3. Set up alerting for compliance violations

## Monitoring and Logging

### Health Checks
- API Health: `GET /health`
- Database Health: `GET /health/db`
- Redis Health: `GET /health/redis`

### Logging
- Application logs: Docker logs or Kubernetes logs
- Audit logs: Available via `/v2/security/audit-logs`
- Performance metrics: Available via dashboard

## Troubleshooting

### Common Issues

#### Database Connection
```bash
# Check database connectivity
docker exec -it nqba-phase2-db-1 psql -U postgres -d nqba -c "SELECT 1;"
```

#### Redis Connection
```bash
# Test Redis connectivity
docker exec -it nqba-phase2-redis-1 redis-cli ping
```

#### API Issues
```bash
# Check API logs
docker logs nqba-phase2-api-1

# Test API health
curl http://localhost:8000/health
```

#### Frontend Issues
```bash
# Check frontend logs
docker logs nqba-phase2-web-1

# Rebuild frontend
docker-compose -f docker-compose.phase2.yml build web
```

### Performance Optimization
1. Enable Redis caching for frequently accessed data
2. Configure database connection pooling
3. Implement CDN for static assets
4. Enable compression for API responses

## Backup and Recovery

### Database Backup
```bash
# Create backup
docker exec nqba-phase2-db-1 pg_dump -U postgres nqba > backup.sql

# Restore backup
docker exec -i nqba-phase2-db-1 psql -U postgres nqba < backup.sql
```

### Configuration Backup
```bash
# Backup environment configuration
cp .env .env.backup

# Backup Docker volumes
docker run --rm -v nqba-phase2_db_data:/data -v $(pwd):/backup alpine tar czf /backup/db_backup.tar.gz -C /data .
```

## Support and Maintenance

### Regular Maintenance Tasks
1. Update dependencies monthly
2. Rotate security keys quarterly
3. Review audit logs weekly
4. Monitor performance metrics daily

### Support Contacts
- Technical Issues: [Support Email]
- Security Issues: [Security Email]
- Documentation: [Documentation URL]

## License
This deployment guide is part of the NQBA Phase 2 platform. See LICENSE file for details.
