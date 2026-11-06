# Specification: Production Alerting & SLO Thresholds
**Applies to:** Prometheus / Datadog / PagerDuty

### Critical P1 Alerts (Immediate Page)
- HTTP 5xx Error Rate: > 5% of total requests over a 5-minute window.
- Database Connection Pool Utilization: > 85% of max pool capacity.
- TLS Certificate Expiry: < 7 days remaining.

### High P2 Alerts (Slack + On-Call Notification)
- Redis Memory Utilization: > 75% of maxmemory.
- Kafka Consumer Group Lag: > 50,000 messages for 10 minutes.
- Pod Restart Count: > 3 restarts within 15 minutes (CrashLoopBackOff / OOMKilled).
- Elasticsearch Disk Usage: > 85% (Low Watermark) or 95% (Flood Stage read-only lock).