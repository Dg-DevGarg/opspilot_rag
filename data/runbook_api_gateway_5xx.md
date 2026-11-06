# Runbook: Ingress & API Gateway 5xx Error Triaging
**Applies to:** Nginx Ingress, Cloudflare, AWS ALB

### Diagnostic Flow
- HTTP 502 Bad Gateway: Upstream service is dead, crashing, or refusing connections. Check pod restart count.
- HTTP 503 Service Unavailable: Upstream service is overloaded, no healthy pods registered, or connection pool limits reached.
- HTTP 504 Gateway Timeout: Upstream took longer than proxy_read_timeout (60s) to respond. Check DB locks or slow external APIs.