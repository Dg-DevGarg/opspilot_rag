# Incident Report: INC-101
## Title: Payment API HTTP 503 Outage due to Database Connection Exhaustion
**Service:** Payment Service | **Severity:** P1 (Critical) | **Date:** 2026-03-12

### Summary
Between 14:10 and 14:45 UTC, the Payment API returned HTTP 503 Service Unavailable errors to 42% of traffic. Customers experienced failed checkouts.

### Root Cause
A surge in traffic combined with an unclosed database connection leak in the order_status endpoint exhausted the PostgreSQL connection pool limit (max 100 connections). Requests stalled waiting for available pool slots, causing timeout errors.

### Remediation Steps
1. Restarted payment service worker nodes to drop orphaned connections.
2. Increased DB_POOL_MAX from 100 to 250 in production.env.
3. Patched order_status handler to ensure database sessions use Python context managers.
4. Monitored pg_stat_activity to verify connection counts dropped below 60%.