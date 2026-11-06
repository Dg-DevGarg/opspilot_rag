import os

DOCUMENTS = [
    {
        "filename": "INC-101_database_pool_exhaustion.md",
        "content": (
            "# Incident Report: INC-101\n"
            "## Title: Payment API HTTP 503 Outage due to Database Connection Exhaustion\n"
            "**Service:** Payment Service | **Severity:** P1 (Critical) | **Date:** 2026-03-12\n\n"
            "### Summary\n"
            "Between 14:10 and 14:45 UTC, the Payment API returned HTTP 503 Service Unavailable errors "
            "to 42% of traffic. Customers experienced failed checkouts.\n\n"
            "### Root Cause\n"
            "A surge in traffic combined with an unclosed database connection leak in the order_status "
            "endpoint exhausted the PostgreSQL connection pool limit (max 100 connections). Requests stalled "
            "waiting for available pool slots, causing timeout errors.\n\n"
            "### Remediation Steps\n"
            "1. Restarted payment service worker nodes to drop orphaned connections.\n"
            "2. Increased DB_POOL_MAX from 100 to 250 in production.env.\n"
            "3. Patched order_status handler to ensure database sessions use Python context managers.\n"
            "4. Monitored pg_stat_activity to verify connection counts dropped below 60%."
        )
    },
    {
        "filename": "INC-102_redis_cluster_oom.md",
        "content": (
            "# Incident Report: INC-102\n"
            "## Title: User Session Degradation due to Redis Out of Memory (OOM)\n"
            "**Service:** Auth & Session Cache | **Severity:** P2 (High) | **Date:** 2026-04-05\n\n"
            "### Summary\n"
            "Users were randomly logged out of active sessions, and login latency jumped by 400ms across all microservices.\n\n"
            "### Root Cause\n"
            "The session cache cluster reached its 8GB RAM threshold because a recent release removed TTL "
            "(Time-to-Live) expiration on temporary guest shopping carts. Redis began evicting active user authentication keys.\n\n"
            "### Remediation Steps\n"
            "1. Executed emergency memory purge on keys matching guest_cart:*.\n"
            "2. Re-applied default TTL of 7200 seconds (2 hours) across all temporary session keys.\n"
            "3. Updated Redis eviction policy from volatile-lru to allkeys-lru.\n"
            "4. Configured PagerDuty threshold alert at 75% memory utilization."
        )
    },
    {
        "filename": "INC-103_kafka_consumer_lag.md",
        "content": (
            "# Incident Report: INC-103\n"
            "## Title: Order Notification Delays Caused by Kafka Consumer Group Stalled\n"
            "**Service:** Notification Service | **Severity:** P2 (High) | **Date:** 2026-05-18\n\n"
            "### Summary\n"
            "Order confirmation emails and SMS notifications were delayed by up to 2 hours following a flash sale event.\n\n"
            "### Root Cause\n"
            "One partition in the order-events topic contained a malformed JSON payload that triggered an unhandled "
            "serialization exception. The consumer worker repeatedly crashed and restarted in an infinite retry loop.\n\n"
            "### Remediation Steps\n"
            "1. Skipped the poison pill offset using kafka-consumer-groups --reset-offsets.\n"
            "2. Implemented a Dead Letter Queue (DLQ) topic order-events-dlq for messages failing JSON parsing after 3 retries.\n"
            "3. Scaled notification worker pods from 3 to 8 replicas to clear the 120,000 backlogged messages."
        )
    },
    {
        "filename": "INC-104_cors_misconfiguration.md",
        "content": (
            "# Incident Report: INC-104\n"
            "## Title: Frontend Checkout Blocked by Misconfigured CORS Headers\n"
            "**Service:** API Gateway (Kong / Nginx) | **Severity:** P1 (Critical) | **Date:** 2026-06-01\n\n"
            "### Summary\n"
            "Web frontend users encountered blocked API calls during checkout with browser console error: "
            "Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource.\n\n"
            "### Root Cause\n"
            "A deployment to the API Gateway ingress stripped Access-Control-Allow-Origin: https://app.example.com "
            "due to a typo in the Helm chart template variable.\n\n"
            "### Remediation Steps\n"
            "1. Immediately rolled back the API Gateway release to version v2.14.1.\n"
            "2. Validated preflight OPTIONS responses using curl -I -X OPTIONS https://api.example.com/checkout.\n"
            "3. Added automated end-to-end Cypress test checking CORS headers in the staging CI pipeline."
        )
    },
    {
        "filename": "INC-105_stripe_webhook_signing_failure.md",
        "content": (
            "# Incident Report: INC-105\n"
            "## Title: Payment Webhooks Returning 400 Bad Request\n"
            "**Service:** Billing Integration | **Severity:** P1 (Critical) | **Date:** 2026-07-20\n\n"
            "### Summary\n"
            "Stripe webhook events were failing with 400 Bad Request, preventing paid subscriptions from activating automatically.\n\n"
            "### Root Cause\n"
            "The webhook signing secret (STRIPE_WEBHOOK_SECRET) was rotated in the Stripe dashboard without updating "
            "Kubernetes secrets in production.\n\n"
            "### Remediation Steps\n"
            "1. Synced the new signing secret into production Vault / AWS Secrets Manager.\n"
            "2. Restarted billing service pods to reload environment variables.\n"
            "3. Replayed failed webhook events directly from the Stripe developer dashboard."
        )
    },
    {
        "filename": "INC-106_worker_memory_leak.md",
        "content": (
            "# Incident Report: INC-106\n"
            "## Title: Report Generation Service CrashLoopBackOff (OOMKilled)\n"
            "**Service:** Analytics & PDF Export Worker | **Severity:** P2 (High) | **Date:** 2026-08-03\n\n"
            "### Summary\n"
            "Kubernetes pods for pdf-export-worker repeatedly crashed with exit code 137 (OOMKilled), "
            "failing scheduled enterprise financial exports.\n\n"
            "### Root Cause\n"
            "The worker loaded entire multi-gigabyte CSV datasets into pandas DataFrames in memory simultaneously "
            "without chunking or freeing memory references after upload to S3.\n\n"
            "### Remediation Steps\n"
            "1. Temporarily bumped pod memory limit from 2Gi to 6Gi in deployment.yaml.\n"
            "2. Refactored data processing to stream rows in chunks of 50,000 using pd.read_csv(chunksize=50000).\n"
            "3. Added explicit garbage collection calls after each batch completed."
        )
    },
    {
        "filename": "INC-107_dns_resolution_timeout.md",
        "content": (
            "# Incident Report: INC-107\n"
            "## Title: Intermittent 502 Errors Across Microservices due to CoreDNS Throttling\n"
            "**Service:** Kubernetes Cluster Infrastructure | **Severity:** P1 (Critical) | **Date:** 2026-08-19\n\n"
            "### Summary\n"
            "Internal service-to-service HTTP calls failed intermittently with Temporary failure in name resolution "
            "and HTTP 502 Bad Gateway errors.\n\n"
            "### Root Cause\n"
            "Alpine Linux containers coupled with default Kubernetes ndots:5 settings generated 5 DNS lookups per "
            "internal request, overwhelming the 2 CoreDNS pods during peak traffic.\n\n"
            "### Remediation Steps\n"
            "1. Scaled coredns deployment from 2 to 10 replicas.\n"
            "2. Deployed NodeLocal DNSCache daemonset across all worker nodes.\n"
            "3. Updated pod specs to set ndots:2 in dnsConfig."
        )
    },
    {
        "filename": "INC-108_elasticsearch_disk_watermark.md",
        "content": (
            "# Incident Report: INC-108\n"
            "## Title: Product Search Index Read-Only Lock Due to Disk Watermark\n"
            "**Service:** Catalog Search Service | **Severity:** P2 (High) | **Date:** 2026-09-02\n\n"
            "### Summary\n"
            "New products and inventory updates stopped appearing in search results. Updates returned "
            "FORBIDDEN/12/index read-only / allow delete (api).\n\n"
            "### Root Cause\n"
            "Unrotated debug logs filled the Elasticsearch data volume past the 95% flood-stage disk watermark, "
            "triggering Elasticsearch automatic safety mechanism to lock indices into read-only mode.\n\n"
            "### Remediation Steps\n"
            "1. Purged old application log indices older than 14 days.\n"
            "2. Expanded EBS storage volumes on data nodes from 500GB to 1TB.\n"
            "3. Reset the read-only block via PUT /products/_settings setting index.blocks.read_only_allow_delete to null."
        )
    },
    {
        "filename": "INC-109_tls_certificate_expired.md",
        "content": (
            "# Incident Report: INC-109\n"
            "## Title: Public API Outage Caused by Expired Let's Encrypt TLS Certificate\n"
            "**Service:** Edge Ingress Controller | **Severity:** P1 (Critical) | **Date:** 2026-09-15\n\n"
            "### Summary\n"
            "Mobile and web clients failed to connect to api.example.com with ERR_CERT_DATE_INVALID SSL handshake errors.\n\n"
            "### Root Cause\n"
            "cert-manager failed to auto-renew the TLS certificate because an updated AWS WAF rule blocked incoming "
            "HTTP-01 challenge requests on /.well-known/acme-challenge/*.\n\n"
            "### Remediation Steps\n"
            "1. Added WAF bypass rule allowing traffic to /.well-known/acme-challenge/*.\n"
            "2. Deleted the stuck CertificateRequest resource in Kubernetes to force immediate renewal.\n"
            "3. Switched future renewals from HTTP-01 to Route53 DNS-01 validation."
        )
    },
    {
        "filename": "INC-110_jwt_clock_skew_auth_failure.md",
        "content": (
            "# Incident Report: INC-110\n"
            "## Title: Authentication Rejections (Token used before issued) on Worker Node\n"
            "**Service:** Identity & Auth Service | **Severity:** P2 (High) | **Date:** 2026-10-01\n\n"
            "### Summary\n"
            "Approximately 15% of login attempts failed immediately after token generation with HTTP 401 "
            "ImmatureSignatureError: The token is not yet valid (iat).\n\n"
            "### Root Cause\n"
            "The NTP daemon (chronyd) crashed on one EC2 worker node (ip-10-0-4-22), causing its system clock "
            "to drift 45 seconds behind the Auth token issuer node.\n\n"
            "### Remediation Steps\n"
            "1. Cordoned and drained node ip-10-0-4-22.\n"
            "2. Restarted chronyd service and verified clock sync.\n"
            "3. Added a 30-second leeway parameter to jwt.decode(..., leeway=30) in the authentication middleware."
        )
    },
    {
        "filename": "runbook_database_troubleshooting.md",
        "content": (
            "# Runbook: Database Latency and Connection Troubleshooting\n"
            "**Applies to:** PostgreSQL, Aurora DB, MySQL\n\n"
            "### Symptoms\n"
            "- High API latency (>1000ms).\n"
            "- HTTP 503 or 504 gateway timeout errors.\n"
            "- Error logs reporting: could not obtain connection from pool within 5.0 seconds.\n\n"
            "### Investigation Checklist\n"
            "1. Check Active Connections: SELECT state, count(*) FROM pg_stat_activity GROUP BY state;\n"
            "2. Identify Long-Running Queries: Query pg_stat_activity for state != idle running longer than 5 seconds.\n"
            "3. Terminate Blocking Locks: SELECT pg_terminate_backend(pid);\n"
            "4. Emergency Mitigation: Restart application replicas sequentially or increase DB_POOL_MAX ceiling."
        )
    },
    {
        "filename": "runbook_redis_cache_operations.md",
        "content": (
            "# Runbook: Redis High Memory & Latency Mitigation\n"
            "**Applies to:** Redis Cluster / AWS ElastiCache\n\n"
            "### Symptoms\n"
            "- OOM command not allowed when used memory > maxmemory.\n"
            "- Spike in cache miss rate and downstream database CPU load.\n\n"
            "### Triage Steps\n"
            "1. Inspect Memory Usage: Run redis-cli INFO memory.\n"
            "2. Find Large Keys: Run redis-cli --bigkeys.\n"
            "3. Check Eviction Policy: Ensure policy is set to allkeys-lru using redis-cli CONFIG SET maxmemory-policy allkeys-lru."
        )
    },
    {
        "filename": "runbook_kafka_lag_recovery.md",
        "content": (
            "# Runbook: Resolving Kafka Consumer Group Lag\n"
            "**Applies to:** Apache Kafka / AWS MSK\n\n"
            "### Symptoms\n"
            "- Delayed async events (emails, webhooks, analytics updates).\n"
            "- Alert: KafkaConsumerLagHigh (> 50,000 messages).\n\n"
            "### Recovery Procedure\n"
            "1. Inspect Consumer Group Status: kafka-consumer-groups.sh --bootstrap-server $BROKERS --describe --group <group-name>\n"
            "2. Check Consumer Logs for Poison Pill Errors: Look for deserialization exceptions repeating on the same offset.\n"
            "3. Scale Out Consumers: Increase Kubernetes deployment replicas up to the number of topic partitions.\n"
            "4. Skip Corrupted Offset: Stop consumers, run --reset-offsets --shift-by 1 --execute, and restart."
        )
    },
    {
        "filename": "runbook_api_gateway_5xx.md",
        "content": (
            "# Runbook: Ingress & API Gateway 5xx Error Triaging\n"
            "**Applies to:** Nginx Ingress, Cloudflare, AWS ALB\n\n"
            "### Diagnostic Flow\n"
            "- HTTP 502 Bad Gateway: Upstream service is dead, crashing, or refusing connections. Check pod restart count.\n"
            "- HTTP 503 Service Unavailable: Upstream service is overloaded, no healthy pods registered, or connection pool limits reached.\n"
            "- HTTP 504 Gateway Timeout: Upstream took longer than proxy_read_timeout (60s) to respond. Check DB locks or slow external APIs."
        )
    },
    {
        "filename": "runbook_kubernetes_pod_crashloop.md",
        "content": (
            "# Runbook: Debugging Kubernetes Pod CrashLoopBackOff & OOMKilled\n"
            "**Applies to:** EKS / GKE Clusters\n\n"
            "### Investigation Commands\n"
            "1. Check Last Termination Reason: kubectl describe pod <pod-name> -n production\n"
            "   - Exit Code 137 (OOMKilled): Container exceeded memory limit. Increase resources.limits.memory or fix memory leaks.\n"
            "   - Exit Code 1: Application crash or uncaught exception.\n"
            "2. Fetch Logs from Previous Crashed Container: kubectl logs <pod-name> -n production --previous\n"
            "3. Verify Environment Variables & Secrets: Ensure required secrets or configmap keys exist."
        )
    },
    {
        "filename": "runbook_ssl_certificate_renewal.md",
        "content": (
            "# Runbook: Emergency TLS/SSL Certificate Renewal\n"
            "**Applies to:** cert-manager & Let's Encrypt on Kubernetes\n\n"
            "### Symptoms\n"
            "- Alert: TLS Certificate Expiring in < 48h or browser ERR_CERT_DATE_INVALID.\n\n"
            "### Resolution Steps\n"
            "1. Check Certificate Status: kubectl get certificate -A and kubectl describe challenge -n ingress.\n"
            "2. Verify ACME Challenge Reachability: Ensure WAF or security groups allow /.well-known/acme-challenge/.\n"
            "3. Force Re-issuance: Delete stuck CertificateRequest or trigger renewal using cmctl renew."
        )
    },
    {
        "filename": "runbook_elasticsearch_cluster_red.md",
        "content": (
            "# Runbook: Recovering Elasticsearch Cluster Status RED or Read-Only\n"
            "**Applies to:** Elasticsearch / OpenSearch\n\n"
            "### Symptoms\n"
            "- Search endpoints returning HTTP 500 or write operations rejected with FORBIDDEN/12/index read-only.\n\n"
            "### Steps\n"
            "1. Check Cluster Health & Disk Space: GET /_cluster/health and GET /_cat/allocation?v.\n"
            "2. Clear Disk Space: Delete old log indices or increase EBS volume size if disk usage > 90%.\n"
            "3. Unlock Read-Only Indices: PUT /_all/_settings with index.blocks.read_only_allow_delete set to null.\n"
            "4. Reroute Unassigned Shards: POST /_cluster/reroute?retry_failed=true."
        )
    },
    {
        "filename": "runbook_third_party_webhook_failures.md",
        "content": (
            "# Runbook: Diagnosing Stripe & Third-Party Webhook Failures\n"
            "**Applies to:** Billing Service & Webhook Ingress\n\n"
            "### Symptoms\n"
            "- Customers charged on Stripe, but subscription status remains Pending in app.\n"
            "- High rate of HTTP 400 or 401 on /webhooks/stripe.\n\n"
            "### Triage Checklist\n"
            "1. Check Signature Verification Logs: Look for SignatureVerificationError in billing service logs.\n"
            "2. Verify Webhook Secret: Compare STRIPE_WEBHOOK_SECRET in Kubernetes against the active secret in Stripe Dashboard.\n"
            "3. Ensure Raw Request Body: Ensure middleware does not modify raw JSON before verifying the signature."
        )
    },
    {
        "filename": "arch_payment_service.md",
        "content": (
            "# Architecture Overview: Payment & Checkout Service\n"
            "**Owner:** FinTech Core Team\n\n"
            "### Components\n"
            "- API Layer: FastAPI service running on Kubernetes (6 pods default, HPA scales up to 20).\n"
            "- Database: AWS Aurora PostgreSQL (db.r6g.xlarge), max connections 500. Uses SQLAlchemy pooling (DB_POOL_MAX=250).\n"
            "- External Dependencies: Stripe API for card processing and webhook callbacks (/webhooks/stripe).\n"
            "- Failure Modes: If PostgreSQL connection pool saturates, the API returns HTTP 503 after a 5-second timeout."
        )
    },
    {
        "filename": "arch_auth_session_system.md",
        "content": (
            "# Architecture Overview: Authentication & Session Management\n"
            "**Owner:** Platform Security Team\n\n"
            "### Token & Cache Flow\n"
            "- Stateless Auth: Short-lived JWT access tokens (15-minute expiry) signed with RS256. Requires synchronized NTP clocks (30s leeway).\n"
            "- Stateful Cache: Redis Cluster (8GB memory, allkeys-lru eviction) stores refresh tokens, active sessions, and guest carts (2-hour TTL)."
        )
    },
    {
        "filename": "arch_event_driven_pipeline.md",
        "content": (
            "# Architecture Overview: Event-Driven Order & Notification Pipeline\n"
            "**Owner:** Messaging Team\n\n"
            "### Data Flow\n"
            "1. Checkout Service publishes order events to Kafka topic order-events (12 partitions).\n"
            "2. Notification Service consumer group reads from order-events and dispatches emails via SendGrid and SMS via Twilio.\n"
            "3. Fault Tolerance: Messages failing schema validation 3 times are routed to order-events-dlq (Dead Letter Queue)."
        )
    },
    {
        "filename": "arch_api_gateway_ingress.md",
        "content": (
            "# Architecture Overview: Edge API Gateway & Ingress\n"
            "**Owner:** Cloud Infrastructure Team\n\n"
            "### Traffic Routing\n"
            "- Edge Security: AWS WAF -> AWS ALB -> Nginx Ingress Controller.\n"
            "- TLS Termination: Managed automatically by cert-manager via Let's Encrypt DNS-01 challenges.\n"
            "- CORS Policy: Enforces strict Access-Control-Allow-Origin headers for https://app.example.com.\n"
            "- Timeouts: Upstream proxy_read_timeout is 60 seconds; requests exceeding this return HTTP 504."
        )
    },
    {
        "filename": "proc_rollback_procedure.md",
        "content": (
            "# Procedure: Production Deployment Rollback\n"
            "**Applies to:** Kubernetes Deployments (Helm / ArgoCD)\n\n"
            "### Standard Rollback Steps\n"
            "1. Check recent deployment history: kubectl rollout history deployment/<service-name> -n production\n"
            "2. Rollback to previous stable revision: kubectl rollout undo deployment/<service-name> -n production\n"
            "3. Verify pod health: kubectl get pods -l app=<service-name> -n production -w\n"
            "4. Check error rates in Datadog/Prometheus dashboards to ensure 5xx errors decline below 0.1%."
        )
    },
    {
        "filename": "proc_secrets_rotation.md",
        "content": (
            "# Procedure: Zero-Downtime Secret & API Key Rotation\n"
            "**Applies to:** AWS Secrets Manager & Kubernetes ExternalSecrets\n\n"
            "### Rotation Checklist\n"
            "1. Generate new API key/signing secret in the provider dashboard (e.g., Stripe, SendGrid).\n"
            "2. Update the secret value in AWS Secrets Manager.\n"
            "3. Force Kubernetes sync: kubectl annotate externalsecret <name> force-sync=$(date +%s) --overwrite\n"
            "4. Perform rolling restart of the deployment: kubectl rollout restart deployment/<service-name> -n production"
        )
    },
    {
        "filename": "spec_monitoring_alert_thresholds.md",
        "content": (
            "# Specification: Production Alerting & SLO Thresholds\n"
            "**Applies to:** Prometheus / Datadog / PagerDuty\n\n"
            "### Critical P1 Alerts (Immediate Page)\n"
            "- HTTP 5xx Error Rate: > 5% of total requests over a 5-minute window.\n"
            "- Database Connection Pool Utilization: > 85% of max pool capacity.\n"
            "- TLS Certificate Expiry: < 7 days remaining.\n\n"
            "### High P2 Alerts (Slack + On-Call Notification)\n"
            "- Redis Memory Utilization: > 75% of maxmemory.\n"
            "- Kafka Consumer Group Lag: > 50,000 messages for 10 minutes.\n"
            "- Pod Restart Count: > 3 restarts within 15 minutes (CrashLoopBackOff / OOMKilled).\n"
            "- Elasticsearch Disk Usage: > 85% (Low Watermark) or 95% (Flood Stage read-only lock)."
        )
    }
]

os.makedirs("data", exist_ok=True)
for doc in DOCUMENTS:
    filepath = os.path.join("data", doc["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(doc["content"].strip())
    print(f"Created: {filepath}")

print(f"\nSuccessfully generated {len(DOCUMENTS)} documentation files in ./data/")