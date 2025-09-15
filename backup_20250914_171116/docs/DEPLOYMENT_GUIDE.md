# NQBA Platform - Production Deployment Guide

This comprehensive guide covers the complete deployment process for the NQBA Platform in production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Security Configuration](#security-configuration)
4. [Database Setup](#database-setup)
5. [Application Deployment](#application-deployment)
6. [Monitoring & Logging](#monitoring--logging)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Maintenance & Operations](#maintenance--operations)
9. [Troubleshooting](#troubleshooting)
10. [Rollback Procedures](#rollback-procedures)

## Prerequisites

### Required Tools

```bash
# Install required CLI tools
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Environment Requirements

- **Kubernetes Cluster**: EKS 1.27+ or equivalent
- **Node Requirements**: 
  - Minimum 3 nodes
  - Instance type: t3.large or larger
  - 100GB+ storage per node
- **Database**: PostgreSQL 15+ (RDS recommended)
- **Cache**: Redis 7+ (ElastiCache recommended)
- **Load Balancer**: AWS ALB or equivalent
- **DNS**: Route53 or equivalent
- **SSL Certificates**: ACM or Let's Encrypt

### Access Requirements

- AWS Account with appropriate IAM permissions
- Domain name for the application
- SMTP credentials for email notifications
- Slack workspace for alerts (optional)
- PagerDuty account for critical alerts (optional)

## Infrastructure Setup

### 1. AWS EKS Cluster Setup

```bash
# Create EKS cluster using eksctl
eksctl create cluster \
  --name nqba-production-cluster \
  --version 1.27 \
  --region us-west-2 \
  --nodegroup-name nqba-workers \
  --node-type t3.large \
  --nodes 3 \
  --nodes-min 3 \
  --nodes-max 10 \
  --managed \
  --with-oidc \
  --ssh-access \
  --ssh-public-key your-key-name

# Configure kubectl
aws eks update-kubeconfig --region us-west-2 --name nqba-production-cluster
```

### 2. Storage Classes

```bash
# Apply storage classes
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
EOF
```

### 3. AWS Load Balancer Controller

```bash
# Install AWS Load Balancer Controller
helm repo add eks https://aws.github.io/eks-charts
helm repo update

# Create IAM role for AWS Load Balancer Controller
eksctl create iamserviceaccount \
  --cluster=nqba-production-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::aws:policy/ElasticLoadBalancingFullAccess \
  --approve

# Install the controller
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=nqba-production-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 4. Ingress Controller

```bash
# Install NGINX Ingress Controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"=nlb
```

## Security Configuration

### 1. Create Secrets

```bash
# Create namespace
kubectl create namespace nqba-platform

# Database secrets
kubectl create secret generic nqba-db-secret \
  --from-literal=username=nqba_user \
  --from-literal=password=your-secure-password \
  --from-literal=host=your-rds-endpoint \
  --from-literal=database=nqba_production \
  -n nqba-platform

# Redis secrets
kubectl create secret generic nqba-redis-secret \
  --from-literal=url=redis://your-elasticache-endpoint:6379/0 \
  -n nqba-platform

# Application secrets
kubectl create secret generic nqba-app-secret \
  --from-literal=secret-key=your-django-secret-key \
  --from-literal=jwt-secret=your-jwt-secret \
  --from-literal=encryption-key=your-encryption-key \
  -n nqba-platform

# External service secrets
kubectl create secret generic nqba-external-secret \
  --from-literal=smtp-password=your-smtp-password \
  --from-literal=aws-access-key=your-aws-access-key \
  --from-literal=aws-secret-key=your-aws-secret-key \
  -n nqba-platform

# Monitoring secrets
kubectl create secret generic grafana-secrets \
  --from-literal=admin-password=your-grafana-password \
  --from-literal=secret-key=your-grafana-secret \
  --from-literal=smtp-user=your-smtp-user \
  --from-literal=smtp-password=your-smtp-password \
  -n monitoring

kubectl create secret generic alertmanager-secrets \
  --from-literal=smtp-password=your-smtp-password \
  --from-literal=slack-webhook-url=your-slack-webhook \
  --from-literal=pagerduty-key=your-pagerduty-key \
  -n monitoring
```

### 2. Apply Security Policies

```bash
# Apply security configurations
kubectl apply -f deploy/security/
```

## Database Setup

### 1. RDS PostgreSQL Setup

```bash
# Create RDS instance (using AWS CLI)
aws rds create-db-instance \
  --db-instance-identifier nqba-production-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 15.4 \
  --master-username nqba_admin \
  --master-user-password your-admin-password \
  --allocated-storage 100 \
  --storage-type gp3 \
  --storage-encrypted \
  --vpc-security-group-ids sg-your-security-group \
  --db-subnet-group-name your-db-subnet-group \
  --backup-retention-period 7 \
  --multi-az \
  --deletion-protection
```

### 2. Database Migration

```bash
# Run database migrations
kubectl run migration-job \
  --image=nqba-platform/api:latest \
  --restart=Never \
  --env="DATABASE_URL=postgresql://user:pass@host:5432/db" \
  --command -- python manage.py migrate

# Create superuser
kubectl run create-superuser \
  --image=nqba-platform/api:latest \
  --restart=Never \
  --env="DATABASE_URL=postgresql://user:pass@host:5432/db" \
  --command -- python manage.py createsuperuser --noinput \
  --username admin --email admin@nqba.flyfox.ai
```

### 3. ElastiCache Redis Setup

```bash
# Create Redis cluster
aws elasticache create-replication-group \
  --replication-group-id nqba-production-redis \
  --description "NQBA Production Redis" \
  --node-type cache.t3.medium \
  --engine redis \
  --engine-version 7.0 \
  --num-cache-clusters 2 \
  --security-group-ids sg-your-redis-security-group \
  --subnet-group-name your-cache-subnet-group \
  --at-rest-encryption-enabled \
  --transit-encryption-enabled
```

## Application Deployment

### 1. Build and Push Images

```bash
# Build images
docker build -f deploy/docker/Dockerfile.api -t nqba-platform/api:v1.0.0 .
docker build -f deploy/docker/Dockerfile.worker -t nqba-platform/worker:v1.0.0 .

# Tag for registry
docker tag nqba-platform/api:v1.0.0 your-registry/nqba-platform/api:v1.0.0
docker tag nqba-platform/worker:v1.0.0 your-registry/nqba-platform/worker:v1.0.0

# Push to registry
docker push your-registry/nqba-platform/api:v1.0.0
docker push your-registry/nqba-platform/worker:v1.0.0
```

### 2. Deploy Application

```bash
# Update image tags in manifests
sed -i 's|nqba-platform/api:latest|your-registry/nqba-platform/api:v1.0.0|g' deploy/k8s/api-deployment.yaml
sed -i 's|nqba-platform/worker:latest|your-registry/nqba-platform/worker:v1.0.0|g' deploy/k8s/worker-deployment.yaml

# Apply Kubernetes manifests
kubectl apply -f deploy/k8s/namespace.yaml
kubectl apply -f deploy/k8s/
kubectl apply -f deploy/k8s/production-resources.yaml

# Wait for deployment
kubectl rollout status deployment/nqba-api -n nqba-platform --timeout=300s
kubectl rollout status deployment/nqba-worker -n nqba-platform --timeout=300s
```

### 3. Configure Ingress

```bash
# Apply ingress configuration
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nqba-ingress
  namespace: nqba-platform
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - api.nqba.flyfox.ai
        - nqba.flyfox.ai
      secretName: nqba-tls
  rules:
    - host: api.nqba.flyfox.ai
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nqba-api
                port:
                  number: 8000
    - host: nqba.flyfox.ai
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nqba-frontend
                port:
                  number: 80
EOF
```

## Monitoring & Logging

### 1. Deploy Monitoring Stack

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Deploy Prometheus, Grafana, and AlertManager
kubectl apply -f deploy/monitoring/prometheus-stack.yaml
kubectl apply -f deploy/monitoring/grafana-alertmanager.yaml

# Deploy logging stack
kubectl apply -f deploy/monitoring/logging-stack.yaml

# Wait for deployments
kubectl rollout status deployment/prometheus -n monitoring --timeout=300s
kubectl rollout status deployment/grafana -n monitoring --timeout=300s
kubectl rollout status deployment/loki -n monitoring --timeout=300s
```

### 2. Configure Dashboards

```bash
# Access Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring

# Login with admin credentials and import dashboards
# Default dashboards are automatically provisioned
```

### 3. Set Up Alerts

```bash
# Verify AlertManager is receiving alerts
kubectl port-forward svc/alertmanager 9093:9093 -n monitoring

# Test alert routing
curl -X POST http://localhost:9093/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '[{
    "labels": {
      "alertname": "TestAlert",
      "severity": "warning"
    },
    "annotations": {
      "summary": "Test alert"
    }
  }]'
```

## CI/CD Pipeline

### 1. GitHub Actions Setup

The CI/CD pipeline is automatically configured through the GitHub Actions workflows in `.github/workflows/`.

### 2. Required Secrets

Add these secrets to your GitHub repository:

```bash
# AWS credentials
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_DEV_ACCESS_KEY_ID
AWS_DEV_SECRET_ACCESS_KEY
AWS_PROD_ACCESS_KEY_ID
AWS_PROD_SECRET_ACCESS_KEY

# Container registry
GITHUB_TOKEN  # Automatically provided

# External services
SNYK_TOKEN
CODECOV_TOKEN

# Notifications
SLACK_WEBHOOK_URL
```

### 3. Deployment Environments

- **Development**: Automatic deployment on push to `develop` branch
- **Staging**: Automatic deployment on push to `main` branch
- **Production**: Manual deployment or tag-based deployment

## Maintenance & Operations

### Daily Operations

```bash
# Check cluster health
kubectl get nodes
kubectl get pods --all-namespaces
kubectl top nodes
kubectl top pods -n nqba-platform

# Check application health
kubectl get pods -n nqba-platform
kubectl logs -f deployment/nqba-api -n nqba-platform
kubectl logs -f deployment/nqba-worker -n nqba-platform

# Check monitoring
kubectl get pods -n monitoring
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```

### Weekly Operations

```bash
# Update cluster
eksctl update cluster --name nqba-production-cluster

# Check for security updates
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].image}{"\n"}{end}'

# Review resource usage
kubectl describe nodes
kubectl get pvc --all-namespaces
```

### Monthly Operations

```bash
# Database maintenance
# Connect to RDS and run VACUUM ANALYZE

# Log rotation and cleanup
# Loki automatically handles log retention

# Security audit
# Review IAM roles and permissions
# Update secrets if necessary

# Backup verification
# Test database restore procedures
```

## Troubleshooting

### Common Issues

#### 1. Pod Startup Issues

```bash
# Check pod status
kubectl describe pod <pod-name> -n nqba-platform

# Check logs
kubectl logs <pod-name> -n nqba-platform --previous

# Check events
kubectl get events -n nqba-platform --sort-by='.lastTimestamp'
```

#### 2. Database Connection Issues

```bash
# Test database connectivity
kubectl run db-test --image=postgres:15 --rm -it --restart=Never -- \
  psql postgresql://user:pass@host:5432/db -c "SELECT 1;"

# Check security groups
aws ec2 describe-security-groups --group-ids sg-your-db-security-group
```

#### 3. Performance Issues

```bash
# Check resource usage
kubectl top pods -n nqba-platform
kubectl describe hpa -n nqba-platform

# Check database performance
# Use RDS Performance Insights

# Check Redis performance
aws elasticache describe-cache-clusters --show-cache-node-info
```

#### 4. SSL Certificate Issues

```bash
# Check certificate status
kubectl describe certificate nqba-tls -n nqba-platform

# Check cert-manager logs
kubectl logs -f deployment/cert-manager -n cert-manager

# Manual certificate renewal
kubectl delete certificate nqba-tls -n nqba-platform
kubectl apply -f your-certificate-manifest.yaml
```

### Debugging Commands

```bash
# Get detailed cluster information
kubectl cluster-info dump

# Check resource quotas
kubectl describe resourcequota -n nqba-platform

# Check network policies
kubectl get networkpolicies -n nqba-platform

# Check service endpoints
kubectl get endpoints -n nqba-platform

# Test internal DNS
kubectl run dns-test --image=busybox --rm -it --restart=Never -- \
  nslookup nqba-api.nqba-platform.svc.cluster.local
```

## Rollback Procedures

### Application Rollback

```bash
# Check rollout history
kubectl rollout history deployment/nqba-api -n nqba-platform
kubectl rollout history deployment/nqba-worker -n nqba-platform

# Rollback to previous version
kubectl rollout undo deployment/nqba-api -n nqba-platform
kubectl rollout undo deployment/nqba-worker -n nqba-platform

# Rollback to specific revision
kubectl rollout undo deployment/nqba-api --to-revision=2 -n nqba-platform

# Monitor rollback
kubectl rollout status deployment/nqba-api -n nqba-platform
```

### Database Rollback

```bash
# Create database backup before rollback
kubectl create job --from=cronjob/nqba-backup nqba-backup-$(date +%Y%m%d-%H%M%S) -n nqba-platform

# Restore from backup (if needed)
# This should be done carefully and tested in staging first
pg_restore -h your-rds-endpoint -U nqba_admin -d nqba_production backup_file.sql
```

### Configuration Rollback

```bash
# Rollback ConfigMaps
kubectl rollout restart deployment/nqba-api -n nqba-platform
kubectl rollout restart deployment/nqba-worker -n nqba-platform

# Rollback secrets (create new versions)
kubectl create secret generic nqba-app-secret-v2 \
  --from-literal=secret-key=old-secret-key \
  -n nqba-platform

# Update deployments to use old secrets
kubectl patch deployment nqba-api -n nqba-platform \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"api","envFrom":[{"secretRef":{"name":"nqba-app-secret-v2"}}]}]}}}}'
```

## Emergency Procedures

### Complete System Outage

1. **Assess the situation**
   ```bash
   kubectl get nodes
   kubectl get pods --all-namespaces
   aws eks describe-cluster --name nqba-production-cluster
   ```

2. **Check external dependencies**
   ```bash
   # Check RDS status
   aws rds describe-db-instances --db-instance-identifier nqba-production-db
   
   # Check ElastiCache status
   aws elasticache describe-replication-groups --replication-group-id nqba-production-redis
   ```

3. **Scale up if needed**
   ```bash
   kubectl scale deployment nqba-api --replicas=10 -n nqba-platform
   kubectl scale deployment nqba-worker --replicas=5 -n nqba-platform
   ```

4. **Enable maintenance mode**
   ```bash
   kubectl patch configmap nqba-config -n nqba-platform \
     -p '{"data":{"MAINTENANCE_MODE":"true"}}'
   kubectl rollout restart deployment/nqba-api -n nqba-platform
   ```

### Security Incident

1. **Isolate affected components**
   ```bash
   kubectl scale deployment nqba-api --replicas=0 -n nqba-platform
   kubectl apply -f emergency-network-policy.yaml
   ```

2. **Rotate secrets**
   ```bash
   kubectl delete secret nqba-app-secret -n nqba-platform
   kubectl create secret generic nqba-app-secret \
     --from-literal=secret-key=new-emergency-secret \
     -n nqba-platform
   ```

3. **Review logs**
   ```bash
   kubectl logs -l app=nqba-platform -n nqba-platform --since=1h > incident-logs.txt
   ```

## Performance Optimization

### Database Optimization

```sql
-- Run these queries on your PostgreSQL database

-- Check slow queries
SELECT query, mean_time, calls, total_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE schemaname = 'public' 
ORDER BY n_distinct DESC;

-- Vacuum and analyze
VACUUM ANALYZE;
```

### Application Optimization

```bash
# Check HPA status
kubectl get hpa -n nqba-platform

# Adjust resource limits based on usage
kubectl patch deployment nqba-api -n nqba-platform \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"api","resources":{"requests":{"memory":"1Gi","cpu":"500m"},"limits":{"memory":"2Gi","cpu":"1000m"}}}]}}}}'

# Enable CPU-based autoscaling
kubectl autoscale deployment nqba-api --cpu-percent=70 --min=3 --max=20 -n nqba-platform
```

## Backup and Recovery

### Automated Backups

```bash
# Database backups are handled by RDS automatic backups
# Additional manual backup
kubectl create job manual-backup-$(date +%Y%m%d) \
  --from=cronjob/nqba-backup -n nqba-platform

# Application data backup
kubectl create job app-data-backup-$(date +%Y%m%d) \
  --image=nqba-platform/api:latest \
  --restart=Never \
  -- python manage.py dumpdata > /backup/app-data-$(date +%Y%m%d).json
```

### Recovery Testing

```bash
# Test database restore in staging
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier nqba-staging-restore-test \
  --db-snapshot-identifier nqba-production-snapshot-$(date +%Y%m%d)

# Test application restore
kubectl apply -f staging-restore-test.yaml
```

---

## Support and Contacts

- **Operations Team**: ops-team@nqba.flyfox.ai
- **Development Team**: dev-team@nqba.flyfox.ai
- **Security Team**: security@nqba.flyfox.ai
- **Emergency Hotline**: +1-XXX-XXX-XXXX

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [NQBA Platform Architecture](./ARCHITECTURE.md)
- [Security Guidelines](./SECURITY.md)

---

**Last Updated**: $(date +%Y-%m-%d)
**Version**: 1.0.0
**Maintained by**: NQBA DevOps Team