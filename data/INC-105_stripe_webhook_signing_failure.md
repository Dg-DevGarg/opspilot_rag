# Incident Report: INC-105
## Title: Payment Webhooks Returning 400 Bad Request
**Service:** Billing Integration | **Severity:** P1 (Critical) | **Date:** 2026-07-20

### Summary
Stripe webhook events were failing with 400 Bad Request, preventing paid subscriptions from activating automatically.

### Root Cause
The webhook signing secret (STRIPE_WEBHOOK_SECRET) was rotated in the Stripe dashboard without updating Kubernetes secrets in production.

### Remediation Steps
1. Synced the new signing secret into production Vault / AWS Secrets Manager.
2. Restarted billing service pods to reload environment variables.
3. Replayed failed webhook events directly from the Stripe developer dashboard.