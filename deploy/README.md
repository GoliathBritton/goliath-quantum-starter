# NQBA Ecosystem Deployment Guide

This guide provides comprehensive instructions for deploying the NQBA (Neuromorphic Quantum Business Architecture) ecosystem to production environments.

## 🏗️ Architecture Overview

The NQBA ecosystem is designed as a cloud-native, scalable platform with the following components:

### Infrastructure Layer
- **AWS EKS Cluster**: Kubernetes orchestration for containerized applications
- **VPC with Private/Public Subnets**: Secure network isolation
- **RDS PostgreSQL**: Persistent data storage
- **ElastiCache Redis**: Caching and message queuing
- **Application Load Balancer**: Traffic distribution and SSL termination
- **S3 Buckets**: Static asset storage and backup

### Application Layer
- **NQBA API Server**: Main FastAPI application (3 replicas)
- **Business Units**: FLYFOX AI, Goliath Trade, Sigma Select (2 replicas each)
- **Quantum Integration Hub**: Dynex integration and quantum workflows (2 replicas)
- **Monitoring Stack**: Prometheus + Grafana for observability

### Security Features
- **IAM Roles**: Least-privilege access for EKS pods
- **Security Groups**: Network-level access control
- **Secrets Management**: Kubernetes secrets for sensitive data
- **Private Subnets**: Database and cache isolation

## 🚀 Quick Start Deployment

### Prerequisites

1. **Required Tools**
   ```bash
   # Install required tools
   brew install terraform kubectl awscli docker  # macOS
   # or
   sudo apt-get install terraform kubectl awscli docker.io  # Ubuntu
   ```

2. **AWS Configuration**
   ```bash
   # Configure AWS credentials
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and default region
   ```

3. **Docker Setup**
   ```bash
   # Ensure Docker is running
   docker --version
   docker ps
   ```

### Automated Deployment

The easiest way to deploy is using our automated deployment script:

```bash
# Make the script executable
chmod +x deploy/scripts/deploy.sh

# Deploy to production (default)
./deploy/scripts/deploy.sh

# Deploy to staging
./deploy/scripts/deploy.sh staging

# Deploy to specific region
./deploy/scripts/deploy.sh production eu-west-1
```

### Manual Deployment Steps

If you prefer manual deployment or need to customize specific components:

#### 1. Build Docker Image
```bash
# Build the production image
docker build -t nqba-ecosystem:latest -f deploy/docker/Dockerfile .

# Tag for your registry (if using ECR)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag nqba-ecosystem:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/nqba-ecosystem:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/nqba-ecosystem:latest
```

#### 2. Deploy Infrastructure
```bash
cd deploy/terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="environment=production" -var="aws_region=us-east-1" -out=tfplan

# Apply infrastructure
terraform apply tfplan

# Get outputs
terraform output
```

#### 3. Deploy Application
```bash
# Configure kubectl for EKS
aws eks update-kubeconfig --region us-east-1 --name nqba-cluster-production

# Create namespace
kubectl create namespace nqba-ecosystem

# Apply Kubernetes manifests
kubectl apply -f deploy/kubernetes/nqba-deployment.yaml

# Verify deployment
kubectl get pods -n nqba-ecosystem
kubectl get services -n nqba-ecosystem
```

## 🔧 Configuration

### Environment Variables

The application can be configured through environment variables:

| Variable | Description | Default | Required |
|-----------|-------------|---------|----------|
| `ENVIRONMENT` | Deployment environment | `production` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `REDIS_URL` | Redis connection string | - | Yes |
| `DYNEX_API_KEY` | Dynex API key for quantum computing | - | Yes |
| `SECRET_KEY` | JWT signing key | - | Yes |

### Secrets Management

Sensitive configuration is stored in Kubernetes secrets:

```bash
# Create secrets (replace with actual values)
kubectl create secret generic nqba-secrets \
  --from-literal=dynex-api-key="your-dynex-key" \
  --from-literal=secret-key="your-secret-key" \
  --from-literal=postgres-password="nqba_password" \
  --from-literal=redis-password="nqba_redis_password" \
  -n nqba-ecosystem
```

### Scaling Configuration

The deployment includes automatic scaling:

- **API Server**: 3-10 replicas based on CPU/Memory usage
- **Business Units**: 2 replicas for high availability
- **QIH**: 2 replicas for quantum workload distribution

## 📊 Monitoring & Observability

### Prometheus Metrics

The application exposes metrics at `/metrics` endpoints:

- **Application Metrics**: Request rates, response times, error rates
- **Business Metrics**: Quantum job success rates, optimization performance
- **Infrastructure Metrics**: CPU, memory, disk usage

### Grafana Dashboards

Access Grafana dashboards:

```bash
# Port forward Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000

# Access at http://localhost:3000
# Default credentials: admin/admin
```

### Log Aggregation

Logs are collected and can be viewed:

```bash
# View application logs
kubectl logs -f deployment/nqba-api -n nqba-ecosystem

# View business unit logs
kubectl logs -f deployment/nqba-business-units -n nqba-ecosystem
```

## 🔒 Security Considerations

### Network Security
- All database and cache traffic is encrypted in transit
- Private subnets isolate sensitive services
- Security groups restrict access to necessary ports only

### Access Control
- IAM roles provide least-privilege access
- Kubernetes RBAC controls pod permissions
- API authentication via JWT tokens

### Data Protection
- Database encryption at rest
- Secrets stored in Kubernetes secrets (not in code)
- Regular security updates via automated pipelines

## 🚨 Troubleshooting

### Common Issues

#### 1. Pods Not Starting
```bash
# Check pod status
kubectl get pods -n nqba-ecosystem

# Check pod events
kubectl describe pod <pod-name> -n nqba-ecosystem

# Check pod logs
kubectl logs <pod-name> -n nqba-ecosystem
```

#### 2. Database Connection Issues
```bash
# Verify RDS endpoint
terraform output -raw rds_endpoint

# Check security group rules
aws ec2 describe-security-groups --group-ids <sg-id>
```

#### 3. Quantum Integration Problems
```bash
# Check Dynex API key
kubectl get secret nqba-secrets -n nqba-ecosystem -o jsonpath='{.data.dynex-api-key}' | base64 -d

# Test Dynex connectivity
kubectl exec -it <pod-name> -n nqba-ecosystem -- curl -H "Authorization: Bearer $DYNEX_API_KEY" https://api.dynex.com/health
```

### Health Checks

The application includes comprehensive health checks:

```bash
# Check application health
kubectl get endpoints -n nqba-ecosystem

# Test health endpoints
kubectl port-forward -n nqba-ecosystem svc/nqba-api-service 8000:8000
curl http://localhost:8000/health
```

## 📈 Performance Optimization

### Resource Allocation

Recommended resource requests and limits:

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| API Server | 250m | 500m | 512Mi | 1Gi |
| Business Units | 125m | 250m | 256Mi | 512Mi |
| QIH | 500m | 1000m | 1Gi | 2Gi |

### Scaling Policies

Horizontal Pod Autoscaler configuration:

- **CPU Threshold**: 70% utilization
- **Memory Threshold**: 80% utilization
- **Scale Up**: Aggressive (100% increase every 15s)
- **Scale Down**: Conservative (10% decrease every 60s)

## 🔄 CI/CD Integration

### GitHub Actions

The repository includes GitHub Actions workflows:

- **CI Pipeline**: Automated testing and security scanning
- **CD Pipeline**: Automated deployment to staging/production
- **Security Scanning**: Dependency vulnerability checks

### Deployment Pipeline

```yaml
# Example GitHub Actions workflow
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to EKS
      run: |
        aws eks update-kubeconfig --name nqba-cluster-production
        kubectl apply -f deploy/kubernetes/
```

## 📚 Additional Resources

### Documentation
- [NQBA Architecture Overview](../docs/architecture.md)
- [API Documentation](../docs/api.md)
- [Business Unit Integration](../docs/business-units.md)

### Support
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Security**: Private security reports to maintainers

### Contributing
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
- [Development Setup](../docs/development.md)

## 🎯 Next Steps

After successful deployment:

1. **Configure DNS**: Point your domain to the ALB DNS name
2. **SSL Certificates**: Set up HTTPS with AWS Certificate Manager
3. **Monitoring**: Configure alerting and custom dashboards
4. **Backup Strategy**: Implement automated database backups
5. **Disaster Recovery**: Test failover procedures
6. **Performance Testing**: Run benchmarks and load tests
7. **Security Audit**: Conduct penetration testing
8. **Documentation**: Update runbooks and procedures

---

**Need Help?** Check the troubleshooting section above or open a GitHub issue for support.
