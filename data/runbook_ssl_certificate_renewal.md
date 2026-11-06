# Runbook: Emergency TLS/SSL Certificate Renewal
**Applies to:** cert-manager & Let's Encrypt on Kubernetes

### Symptoms
- Alert: TLS Certificate Expiring in < 48h or browser ERR_CERT_DATE_INVALID.

### Resolution Steps
1. Check Certificate Status: kubectl get certificate -A and kubectl describe challenge -n ingress.
2. Verify ACME Challenge Reachability: Ensure WAF or security groups allow /.well-known/acme-challenge/.
3. Force Re-issuance: Delete stuck CertificateRequest or trigger renewal using cmctl renew.