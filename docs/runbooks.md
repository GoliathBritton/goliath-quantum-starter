# NQBA Platform - Operational Runbooks

## Overview

This document provides comprehensive operational procedures for the NQBA Platform, including daily operations, incident response, maintenance procedures, and emergency protocols.

## Table of Contents

1. [Daily Operations](#daily-operations)
2. [Incident Response](#incident-response)
3. [Maintenance Procedures](#maintenance-procedures)
4. [Scaling Operations](#scaling-operations)
5. [Security Procedures](#security-procedures)
6. [Backup and Recovery](#backup-and-recovery)
7. [Performance Tuning](#performance-tuning)
8. [Emergency Procedures](#emergency-procedures)
9. [NQBA-Specific Incidents](#nqba-specific-incidents)

## Incident Severity Levels

- **P0 (Critical)**: Complete system outage, data loss, security breach
- **P1 (High)**: Major functionality degraded, significant performance impact
- **P2 (Medium)**: Minor functionality issues, moderate performance impact
- **P3 (Low)**: Cosmetic issues, minor performance degradation

## Daily Operations

### Morning Health Check

**Frequency**: Daily at 9:00 AM
**Duration**: 15 minutes
**Owner**: Operations Team

#### Checklist

```bash
# 1. Check cluster health
kubectl get nodes
kubectl get pods --all-namespaces | grep -v Running
kubectl top nodes

# 2. Check application status
kubectl get pods -n nqba-platform
kubectl get svc -n nqba-platform
kubectl get ingress -n nqba-platform

# 3. Check HPA status
kubectl get hpa -n nqba-platform

# 4. Check recent deployments
kubectl rollout status deployment/nqba-api -n nqba-platform
kubectl rollout status deployment/nqba-worker -n nqba-platform

# 5. Check monitoring systems
kubectl get pods -n monitoring
curl -s http://prometheus.monitoring.svc.cluster.local:9090/-/healthy
curl -s http://grafana.monitoring.svc.cluster.local:3000/api/health

# 6. Check NQBA-specific services
curl -f https://api.nqba.flyfox.ai/health
curl -f https://api.nqba.flyfox.ai/quantum/status
```

#### Expected Results
- All nodes should be in "Ready" state
- All pods should be "Running" or "Completed"
- CPU/Memory usage should be within normal ranges (< 80%)
- All services should have endpoints
- HPA should show current/desired replica counts
- Monitoring systems should return healthy status
- NQBA API should return 200 status

### Log Review

**Frequency**: Daily at 10:00 AM
**Duration**: 30 minutes
**Owner**: Operations Team

```bash
# 1. Check application logs for errors
kubectl logs -l app=nqba-platform -n nqba-platform --since=24h | grep -i error

# 2. Check worker logs for failed jobs
kubectl logs -l component=worker -n nqba-platform --since=24h | grep -i "failed\|error"

# 3. Check quantum job logs
kubectl logs -l app=nqba-platform -n nqba-platform --since=24h | grep -i "quantum\|dynex"

# 4. Check IPFS logs
kubectl logs -l component=ipfs -n nqba-platform --since=24h | grep -i "pin\|failed"

# 5. Check billing logs
kubectl logs -l app=nqba-platform -n nqba-platform --since=24h | grep -i "billing\|quota"
```

## Incident Response

### P0 - Critical Incident Response

**Response Time**: 15 minutes
**Resolution Time**: 4 hours

#### Immediate Actions (0-15 minutes)

1. **Acknowledge the incident**
   ```bash
   # Create incident channel
   # Post in #incidents Slack channel
   echo "P0 INCIDENT: [Brief description] - Incident Commander: [Name]"
   ```

2. **Assess the scope**
   ```bash
   # Check overall system health
   kubectl get nodes
   kubectl get pods --all-namespaces | grep -v Running
   
   # Check external dependencies
   curl -I https://api.nqba.flyfox.ai/health
   curl -I https://dynex.co/api/health  # Check Dynex status
   
   # Check monitoring dashboards
   # Access Grafana and review system metrics
   ```

3. **Implement immediate mitigation**
   ```bash
   # If API is down, check recent deployments
   kubectl rollout history deployment/nqba-api -n nqba-platform
   
   # If needed, rollback to last known good version
   kubectl rollout undo deployment/nqba-api -n nqba-platform
   
   # Scale up if performance issue
   kubectl scale deployment nqba-api --replicas=10 -n nqba-platform
   
   # Enable quantum fallback if Dynex is down
   kubectl patch configmap nqba-config -n nqba-platform \
     -p '{"data":{"QUANTUM_FALLBACK_ENABLED":"true"}}'
   ```

## Maintenance Procedures

### Weekly Maintenance Window

**Schedule**: Sundays 2:00 AM - 4:00 AM UTC
**Duration**: 2 hours
**Owner**: Operations Team

#### Pre-maintenance Checklist

```bash
# 1. Verify backup completion
kubectl get jobs -n nqba-platform | grep backup
aws rds describe-db-snapshots --db-instance-identifier nqba-production-db

# 2. Check system health
kubectl get pods --all-namespaces | grep -v Running
kubectl top nodes

# 3. Check quantum job queue
kubectl logs -l component=worker -n nqba-platform | grep "queue_size"

# 4. Notify stakeholders
# Send maintenance notification 24 hours in advance

# 5. Prepare rollback plan
kubectl get deployments -n nqba-platform -o yaml > pre-maintenance-state.yaml
```

## Scaling Operations

### Quantum Workload Scaling

```bash
# Check quantum job queue depth
kubectl logs -l component=worker -n nqba-platform | grep "queue_depth"

# Scale quantum workers based on demand
kubectl scale deployment nqba-worker --replicas=10 -n nqba-platform

# Monitor Dynex API rate limits
kubectl logs -l app=nqba-platform -n nqba-platform | grep "rate_limit"
```

## Security Procedures

### Quantum API Key Rotation

```bash
# 1. Generate new Dynex API key
# (Done through Dynex portal)

# 2. Update Kubernetes secret
kubectl create secret generic nqba-quantum-secret-new \
  --from-literal=dynex-api-key=new-api-key \
  -n nqba-platform

# 3. Update deployment
kubectl patch deployment nqba-worker -n nqba-platform \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"worker","envFrom":[{"secretRef":{"name":"nqba-quantum-secret-new"}}]}]}}}}'

# 4. Verify quantum jobs still work
kubectl logs -l component=worker -n nqba-platform | grep "quantum_job_success"
```

## Performance Tuning

### Quantum Job Optimization

```bash
# Monitor quantum job performance
kubectl logs -l component=worker -n nqba-platform | grep "job_duration"

# Adjust quantum worker resources
kubectl patch deployment nqba-worker -n nqba-platform \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"worker","resources":{"requests":{"memory":"4Gi","cpu":"2000m"},"limits":{"memory":"8Gi","cpu":"4000m"}}}]}}}}'

# Tune quantum job batching
kubectl patch configmap nqba-config -n nqba-platform \
  -p '{"data":{"QUANTUM_BATCH_SIZE":"5","QUANTUM_TIMEOUT":"300"}}'
```

## Emergency Procedures

### Dynex Service Outage

```bash
# 1. Enable classical fallback immediately
kubectl patch configmap nqba-config -n nqba-platform \
  -p '{"data":{"QUANTUM_FALLBACK_ENABLED":"true","FALLBACK_SOLVER":"classical"}}'

# 2. Restart workers to pick up new config
kubectl rollout restart deployment/nqba-worker -n nqba-platform

# 3. Update status page
echo "Quantum computing services temporarily using classical fallback due to external provider issues."

# 4. Monitor fallback performance
kubectl logs -l component=worker -n nqba-platform | grep "fallback_job"
```

## NQBA-Specific Incidents

### Runbook Index

1. [Dynex Outage](#dynex-outage)
2. [IPFS Pin Failures](#ipfs-pin-failures)
3. [Quota Exhaustion](#quota-exhaustion)
4. [Delayed Jobs](#delayed-jobs)
5. [Billing Drift](#billing-drift)
6. [API Rate Limit Exceeded](#api-rate-limit-exceeded)
7. [Authentication Failures](#authentication-failures)
8. [Quantum Job Failures](#quantum-job-failures)

---

## Dynex Outage

### Detection
- **Alert**: Dynex API health check fails
- **Symptoms**: Quantum jobs failing, fallback to classical solvers
- **Metrics**: `dynex.health_status = "down"`, `quantum.fallback_rate > 0.5`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P1 or P0 depending on impact
2. **Notify Team**: Alert on-call engineer and quantum specialist
3. **Activate Circuit Breaker**: Automatically route jobs to classical solvers
4. **Update Status Page**: Mark quantum services as degraded

### Investigation (5-30 minutes)
1. **Check Dynex Status Page**: Verify if it's a platform-wide issue
2. **Review Recent Changes**: Check if any deployments affected connectivity
3. **Test Connectivity**: Verify network connectivity to Dynex endpoints
4. **Check Credentials**: Verify API keys and authentication

### Resolution Steps
1. **If Dynex Platform Issue**:
   - Monitor Dynex status page
   - Continue using classical fallback
   - Update customers on expected resolution time

2. **If Network/Configuration Issue**:
   - Check firewall rules and network policies
   - Verify API key rotation hasn't caused issues
   - Test with new API keys if necessary

3. **If Authentication Issue**:
   - Rotate Dynex API keys
   - Update configuration
   - Test connectivity

### Recovery
1. **Verify Quantum Jobs Resume**: Monitor job success rates
2. **Gradual Rollback**: Slowly increase quantum job allocation
3. **Update Documentation**: Document incident and lessons learned
4. **Customer Communication**: Notify customers of resolution

---

## IPFS Pin Failures

### Detection
- **Alert**: IPFS pin operation failures exceed threshold
- **Symptoms**: Content not accessible, LTC verification failures
- **Metrics**: `ipfs.pin_failure_rate > 0.1`, `ltc.verification_failures > 0`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P2
2. **Check IPFS Cluster Health**: Verify cluster status
3. **Activate Backup Pinning**: Use secondary IPFS providers
4. **Pause New Pins**: Temporarily stop new content pinning

### Investigation (5-30 minutes)
1. **Check IPFS Cluster Logs**: Look for error patterns
2. **Verify Storage Capacity**: Check available disk space
3. **Review Network Connectivity**: Ensure IPFS nodes can communicate
4. **Check Authentication**: Verify IPFS cluster authentication

### Resolution Steps
1. **If Storage Full**:
   - Clean up old/unused pins
   - Expand storage capacity
   - Implement pin expiration policies

2. **If Network Issues**:
   - Restart IPFS daemon
   - Check firewall rules
   - Verify cluster configuration

3. **If Authentication Issues**:
   - Rotate IPFS cluster keys
   - Update configuration
   - Restart services

### Recovery
1. **Verify Pinning Resumes**: Test with new content
2. **Repin Failed Content**: Re-pin content that failed during outage
3. **Monitor Success Rates**: Ensure pinning success rate returns to normal
4. **Update LTC Records**: Verify all LTC hashes are properly recorded

---

## Quota Exhaustion

### Detection
- **Alert**: API rate limits exceeded, quota usage > 90%
- **Symptoms**: API calls failing with 429 errors, service degradation
- **Metrics**: `api.quota_usage > 0.9`, `api.rate_limit_exceeded > 0`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P2
2. **Check Quota Status**: Verify current usage across all services
3. **Implement Rate Limiting**: Reduce non-essential API calls
4. **Notify Customers**: Alert customers approaching limits

### Investigation (5-30 minutes)
1. **Analyze Usage Patterns**: Identify high-usage customers/endpoints
2. **Check for Abuse**: Look for potential API abuse or bugs
3. **Review Quota Configuration**: Verify quota settings are appropriate
4. **Check Billing**: Ensure quota increases are properly billed

### Resolution Steps
1. **If Legitimate High Usage**:
   - Increase quota limits for affected customers
   - Implement usage-based billing
   - Optimize API efficiency

2. **If API Abuse**:
   - Implement stricter rate limiting
   - Block abusive IPs/users
   - Review security measures

3. **If Configuration Issue**:
   - Adjust quota settings
   - Update billing configuration
   - Restart quota service

### Recovery
1. **Verify Quota Reset**: Ensure new quotas are active
2. **Monitor Usage**: Track usage patterns post-resolution
3. **Customer Communication**: Notify customers of quota increases
4. **Document Changes**: Update quota policies and procedures

---

## Delayed Jobs

### Detection
- **Alert**: Job queue depth exceeds threshold, processing delays
- **Symptoms**: Jobs taking longer than expected, queue backlog
- **Metrics**: `qih.queue_depth > 100`, `qih.avg_processing_time > 300s`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P2
2. **Check Queue Status**: Verify current queue depth and processing rates
3. **Scale Workers**: Increase worker count if possible
4. **Prioritize Critical Jobs**: Move high-priority jobs to front of queue

### Investigation (5-30 minutes)
1. **Analyze Queue Metrics**: Look for bottlenecks in processing
2. **Check Worker Health**: Verify worker processes are healthy
3. **Review Resource Usage**: Check CPU, memory, and database performance
4. **Identify Stuck Jobs**: Look for jobs that may be blocking the queue

### Resolution Steps
1. **If Worker Bottleneck**:
   - Scale up worker instances
   - Restart stuck workers
   - Optimize job processing logic

2. **If Database Bottleneck**:
   - Check database performance
   - Optimize queries
   - Scale database resources

3. **If Resource Exhaustion**:
   - Scale up infrastructure
   - Implement job prioritization
   - Add circuit breakers for long-running jobs

### Recovery
1. **Monitor Queue Depth**: Ensure queue returns to normal levels
2. **Verify Processing Times**: Confirm job processing times improve
3. **Customer Communication**: Update customers on resolution
4. **Implement Monitoring**: Add better alerting for future incidents

---

## Billing Drift

### Detection
- **Alert**: Billing discrepancies detected, revenue anomalies
- **Symptoms**: Unexpected billing amounts, customer complaints
- **Metrics**: `billing.daily_revenue_variance > 0.2`, `billing.failed_charges > 0`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P1
2. **Pause Billing**: Temporarily stop new charges
3. **Notify Finance Team**: Alert billing and finance personnel
4. **Check Recent Transactions**: Review last 24 hours of billing

### Investigation (5-30 minutes)
1. **Audit Recent Charges**: Verify all charges are legitimate
2. **Check Billing Configuration**: Verify pricing and plan settings
3. **Review Customer Usage**: Confirm usage matches billing
4. **Check Payment Processing**: Verify payment gateway health

### Resolution Steps
1. **If Pricing Error**:
   - Correct pricing configuration
   - Reverse incorrect charges
   - Update customer accounts

2. **If Usage Mismatch**:
   - Reconcile usage data
   - Adjust billing accordingly
   - Update customer records

3. **If Payment Processing Issue**:
   - Check payment gateway status
   - Retry failed charges
   - Update payment methods if needed

### Recovery
1. **Verify Billing Accuracy**: Ensure all charges are correct
2. **Resume Billing**: Restart normal billing operations
3. **Customer Communication**: Notify customers of corrections
4. **Implement Safeguards**: Add billing validation checks

---

## API Rate Limit Exceeded

### Detection
- **Alert**: API rate limits exceeded, 429 errors increasing
- **Symptoms**: API calls failing, service degradation
- **Metrics**: `api.rate_limit_exceeded > 0.1`, `api.error_rate > 0.05`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P2
2. **Check Rate Limit Status**: Verify current rate limit configuration
3. **Implement Throttling**: Reduce non-essential API calls
4. **Notify High-Usage Customers**: Alert customers approaching limits

### Investigation (5-30 minutes)
1. **Analyze Usage Patterns**: Identify high-usage patterns
2. **Check for Abuse**: Look for potential API abuse
3. **Review Rate Limit Settings**: Verify limits are appropriate
4. **Check Customer Plans**: Ensure limits match customer tiers

### Resolution Steps
1. **If Legitimate High Usage**:
   - Increase rate limits for affected customers
   - Implement usage-based billing
   - Optimize API efficiency

2. **If API Abuse**:
   - Implement stricter rate limiting
   - Block abusive IPs/users
   - Review security measures

3. **If Configuration Issue**:
   - Adjust rate limit settings
   - Update customer plans
   - Restart rate limiting service

### Recovery
1. **Verify Rate Limits**: Ensure new limits are active
2. **Monitor Usage**: Track usage patterns post-resolution
3. **Customer Communication**: Notify customers of limit increases
4. **Document Changes**: Update rate limiting policies

---

## Authentication Failures

### Detection
- **Alert**: Authentication failure rate exceeds threshold
- **Symptoms**: Users unable to log in, API authentication errors
- **Metrics**: `auth.failure_rate > 0.1`, `auth.locked_accounts > 0`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P1
2. **Check Authentication Service**: Verify service health
3. **Implement Rate Limiting**: Reduce authentication attempts
4. **Notify Security Team**: Alert security personnel

### Investigation (5-30 minutes)
1. **Analyze Failure Patterns**: Look for attack patterns
2. **Check Service Logs**: Review authentication service logs
3. **Verify Database Connectivity**: Ensure user database is accessible
4. **Check for Brute Force**: Look for multiple failed attempts

### Resolution Steps
1. **If Brute Force Attack**:
   - Implement IP blocking
   - Increase account lockout thresholds
   - Add CAPTCHA for suspicious IPs

2. **If Service Issue**:
   - Restart authentication service
   - Check database connectivity
   - Verify configuration

3. **If Configuration Issue**:
   - Update authentication settings
   - Verify JWT configuration
   - Check password policies

### Recovery
1. **Verify Authentication**: Test login functionality
2. **Monitor Failure Rates**: Ensure failure rates return to normal
3. **Unlock Accounts**: Release legitimate locked accounts
4. **Implement Monitoring**: Add better alerting for future attacks

---

## Quantum Job Failures

### Detection
- **Alert**: Quantum job failure rate exceeds threshold
- **Symptoms**: Jobs failing, customer complaints about results
- **Metrics**: `quantum.failure_rate > 0.2`, `quantum.success_rate < 0.8`

### Immediate Response (0-5 minutes)
1. **Declare Incident**: P2
2. **Check Quantum Service Health**: Verify Dynex and classical solvers
3. **Pause New Jobs**: Temporarily stop new quantum job submissions
4. **Notify Quantum Team**: Alert quantum specialists

### Investigation (5-30 minutes)
1. **Analyze Failure Patterns**: Look for common failure reasons
2. **Check Solver Health**: Verify quantum and classical solver status
3. **Review Job Parameters**: Check if job parameters are valid
4. **Check Resource Availability**: Verify sufficient computational resources

### Resolution Steps
1. **If Solver Issue**:
   - Restart failed solvers
   - Implement fallback to classical solvers
   - Check solver configuration

2. **If Resource Issue**:
   - Scale up computational resources
   - Implement job queuing
   - Add resource monitoring

3. **If Parameter Issue**:
   - Validate job parameters
   - Update job validation logic
   - Implement parameter sanitization

### Recovery
1. **Verify Job Processing**: Test with simple quantum jobs
2. **Monitor Success Rates**: Ensure success rates improve
3. **Resume Job Processing**: Gradually increase job volume
4. **Customer Communication**: Update customers on resolution

---

## Incident Response Checklist

### During Incident
- [ ] Declare incident with appropriate severity
- [ ] Notify relevant team members
- [ ] Implement immediate mitigation
- [ ] Begin investigation
- [ ] Update status page
- [ ] Communicate with customers

### Resolution
- [ ] Implement fix
- [ ] Verify resolution
- [ ] Monitor metrics
- [ ] Update documentation
- [ ] Communicate resolution

### Post-Incident
- [ ] Conduct post-mortem
- [ ] Update runbooks
- [ ] Implement preventive measures
- [ ] Review monitoring and alerting
- [ ] Update incident response procedures

---

## Contact Information

### On-Call Rotation
- **Primary**: [Primary On-Call Engineer]
- **Secondary**: [Secondary On-Call Engineer]
- **Escalation**: [Team Lead/Manager]

### Emergency Contacts
- **Security**: [Security Team Lead]
- **Infrastructure**: [Infrastructure Team Lead]
- **Quantum**: [Quantum Specialist]
- **Management**: [Engineering Manager]

### Communication Channels
- **Slack**: #nqba-incidents
- **Email**: incidents@flyfoxai.io
- **PagerDuty**: [PagerDuty Schedule]
- **Status Page**: [Status Page URL]

---

## Document Version

- **Version**: 1.0
- **Last Updated**: [Current Date]
- **Next Review**: [Next Review Date]
- **Owner**: [Document Owner]
