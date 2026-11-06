# Incident Report: INC-102
## Title: User Session Degradation due to Redis Out of Memory (OOM)
**Service:** Auth & Session Cache | **Severity:** P2 (High) | **Date:** 2026-04-05

### Summary
Users were randomly logged out of active sessions, and login latency jumped by 400ms across all microservices.

### Root Cause
The session cache cluster reached its 8GB RAM threshold because a recent release removed TTL (Time-to-Live) expiration on temporary guest shopping carts. Redis began evicting active user authentication keys.

### Remediation Steps
1. Executed emergency memory purge on keys matching guest_cart:*.
2. Re-applied default TTL of 7200 seconds (2 hours) across all temporary session keys.
3. Updated Redis eviction policy from volatile-lru to allkeys-lru.
4. Configured PagerDuty threshold alert at 75% memory utilization.