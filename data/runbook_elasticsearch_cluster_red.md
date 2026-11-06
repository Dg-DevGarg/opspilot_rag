# Runbook: Recovering Elasticsearch Cluster Status RED or Read-Only
**Applies to:** Elasticsearch / OpenSearch

### Symptoms
- Search endpoints returning HTTP 500 or write operations rejected with FORBIDDEN/12/index read-only.

### Steps
1. Check Cluster Health & Disk Space: GET /_cluster/health and GET /_cat/allocation?v.
2. Clear Disk Space: Delete old log indices or increase EBS volume size if disk usage > 90%.
3. Unlock Read-Only Indices: PUT /_all/_settings with index.blocks.read_only_allow_delete set to null.
4. Reroute Unassigned Shards: POST /_cluster/reroute?retry_failed=true.