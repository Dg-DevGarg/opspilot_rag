# Procedure: Zero-Downtime Secret & API Key Rotation
**Applies to:** AWS Secrets Manager & Kubernetes ExternalSecrets

### Rotation Checklist
1. Generate new API key/signing secret in the provider dashboard (e.g., Stripe, SendGrid).
2. Update the secret value in AWS Secrets Manager.
3. Force Kubernetes sync: kubectl annotate externalsecret <name> force-sync=$(date +%s) --overwrite
4. Perform rolling restart of the deployment: kubectl rollout restart deployment/<service-name> -n production