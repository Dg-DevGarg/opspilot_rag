# Incident Report: INC-109
## Title: Public API Outage Caused by Expired Let's Encrypt TLS Certificate
**Service:** Edge Ingress Controller | **Severity:** P1 (Critical) | **Date:** 2026-09-15

### Summary
Mobile and web clients failed to connect to api.example.com with ERR_CERT_DATE_INVALID SSL handshake errors.

### Root Cause
cert-manager failed to auto-renew the TLS certificate because an updated AWS WAF rule blocked incoming HTTP-01 challenge requests on /.well-known/acme-challenge/*.

### Remediation Steps
1. Added WAF bypass rule allowing traffic to /.well-known/acme-challenge/*.
2. Deleted the stuck CertificateRequest resource in Kubernetes to force immediate renewal.
3. Switched future renewals from HTTP-01 to Route53 DNS-01 validation.