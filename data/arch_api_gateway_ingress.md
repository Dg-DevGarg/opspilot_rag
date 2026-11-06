# Architecture Overview: Edge API Gateway & Ingress
**Owner:** Cloud Infrastructure Team

### Traffic Routing
- Edge Security: AWS WAF -> AWS ALB -> Nginx Ingress Controller.
- TLS Termination: Managed automatically by cert-manager via Let's Encrypt DNS-01 challenges.
- CORS Policy: Enforces strict Access-Control-Allow-Origin headers for https://app.example.com.
- Timeouts: Upstream proxy_read_timeout is 60 seconds; requests exceeding this return HTTP 504.