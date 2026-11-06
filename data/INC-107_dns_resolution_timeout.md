# Incident Report: INC-107
## Title: Intermittent 502 Errors Across Microservices due to CoreDNS Throttling
**Service:** Kubernetes Cluster Infrastructure | **Severity:** P1 (Critical) | **Date:** 2026-08-19

### Summary
Internal service-to-service HTTP calls failed intermittently with Temporary failure in name resolution and HTTP 502 Bad Gateway errors.

### Root Cause
Alpine Linux containers coupled with default Kubernetes ndots:5 settings generated 5 DNS lookups per internal request, overwhelming the 2 CoreDNS pods during peak traffic.

### Remediation Steps
1. Scaled coredns deployment from 2 to 10 replicas.
2. Deployed NodeLocal DNSCache daemonset across all worker nodes.
3. Updated pod specs to set ndots:2 in dnsConfig.