# Runbook: Database Latency and Connection Troubleshooting
**Applies to:** PostgreSQL, Aurora DB, MySQL

### Symptoms
- High API latency (>1000ms).
- HTTP 503 or 504 gateway timeout errors.
- Error logs reporting: could not obtain connection from pool within 5.0 seconds.

### Investigation Checklist
1. Check Active Connections: SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
2. Identify Long-Running Queries: Query pg_stat_activity for state != idle running longer than 5 seconds.
3. Terminate Blocking Locks: SELECT pg_terminate_backend(pid);
4. Emergency Mitigation: Restart application replicas sequentially or increase DB_POOL_MAX ceiling.