# Service Level Agreements (SLAs)

This document outlines the performance and availability guarantees for the Goliath Quantum Platform.

## Availability Commitments

| Service Tier | Availability Target | Maximum Monthly Downtime | Credits Eligibility |
|--------------|---------------------|--------------------------|---------------------|
| Enterprise   | 99.9%               | 43 minutes               | 10% for <99.9%, 25% for <99.5% |
| Professional | 99.5%               | 3 hours, 36 minutes      | 10% for <99.5%, 25% for <99.0% |
| Standard     | 99.0%               | 7 hours, 12 minutes      | 10% for <99.0% |

## Performance Guarantees

### API Response Times

| Operation Type | Target Response Time | 95th Percentile Guarantee |
|----------------|----------------------|---------------------------|
| Read operations | 200ms | 500ms |
| Write operations | 500ms | 1000ms |
| Batch operations | 1000ms | 2000ms |

### Quantum Job Processing

| Job Complexity | Queue Time | Processing Time |
|----------------|------------|----------------|
| Low (< 50 qubits) | < 5 minutes | < 10 minutes |
| Medium (50-100 qubits) | < 15 minutes | < 30 minutes |
| High (> 100 qubits) | < 30 minutes | < 60 minutes |

## Support Response Times

| Severity | Description | Initial Response | Resolution Target |
|----------|-------------|------------------|-------------------|
| Critical | Service unavailable | 30 minutes | 4 hours |
| High | Major functionality impacted | 2 hours | 8 hours |
| Medium | Limited functionality impacted | 8 hours | 24 hours |
| Low | Minor issues, questions | 24 hours | 72 hours |

## Maintenance Windows

Scheduled maintenance will be performed during the following windows:

- **Americas**: Sundays, 2:00 AM - 6:00 AM EST
- **Europe**: Sundays, 2:00 AM - 6:00 AM CET
- **Asia-Pacific**: Sundays, 2:00 AM - 6:00 AM JST

Customers will be notified at least 72 hours in advance of any scheduled maintenance.

## Disaster Recovery

| Metric | Target |
|--------|--------|
| Recovery Point Objective (RPO) | < 15 minutes |
| Recovery Time Objective (RTO) | < 4 hours |

## SLA Exclusions

The following are excluded from SLA calculations:

1. Scheduled maintenance windows
2. Force majeure events
3. Issues resulting from customer's applications or equipment
4. Suspension of services due to violation of Terms of Service
5. Beta or preview features explicitly marked as such

## SLA Monitoring and Reporting

- Service status is available at status.goliath-quantum.com
- Monthly SLA reports are available in the customer portal
- SLA violations will be automatically credited to eligible accounts

## Requesting SLA Credits

To request SLA credits:

1. Submit a request within 30 days of the incident
2. Include account information and incident details
3. Credits will be applied within two billing cycles

## Contact Information

For SLA-related inquiries:
- Email: sla@goliath-quantum.com
- Phone: +1-555-123-4567