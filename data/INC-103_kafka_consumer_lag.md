# Incident Report: INC-103
## Title: Order Notification Delays Caused by Kafka Consumer Group Stalled
**Service:** Notification Service | **Severity:** P2 (High) | **Date:** 2026-05-18

### Summary
Order confirmation emails and SMS notifications were delayed by up to 2 hours following a flash sale event.

### Root Cause
One partition in the order-events topic contained a malformed JSON payload that triggered an unhandled serialization exception. The consumer worker repeatedly crashed and restarted in an infinite retry loop.

### Remediation Steps
1. Skipped the poison pill offset using kafka-consumer-groups --reset-offsets.
2. Implemented a Dead Letter Queue (DLQ) topic order-events-dlq for messages failing JSON parsing after 3 retries.
3. Scaled notification worker pods from 3 to 8 replicas to clear the 120,000 backlogged messages.