# Runbook: Redis High Memory & Latency Mitigation
**Applies to:** Redis Cluster / AWS ElastiCache

### Symptoms
- OOM command not allowed when used memory > maxmemory.
- Spike in cache miss rate and downstream database CPU load.

### Triage Steps
1. Inspect Memory Usage: Run redis-cli INFO memory.
2. Find Large Keys: Run redis-cli --bigkeys.
3. Check Eviction Policy: Ensure policy is set to allkeys-lru using redis-cli CONFIG SET maxmemory-policy allkeys-lru.