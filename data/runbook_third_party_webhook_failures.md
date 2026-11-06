# Runbook: Diagnosing Stripe & Third-Party Webhook Failures
**Applies to:** Billing Service & Webhook Ingress

### Symptoms
- Customers charged on Stripe, but subscription status remains Pending in app.
- High rate of HTTP 400 or 401 on /webhooks/stripe.

### Triage Checklist
1. Check Signature Verification Logs: Look for SignatureVerificationError in billing service logs.
2. Verify Webhook Secret: Compare STRIPE_WEBHOOK_SECRET in Kubernetes against the active secret in Stripe Dashboard.
3. Ensure Raw Request Body: Ensure middleware does not modify raw JSON before verifying the signature.