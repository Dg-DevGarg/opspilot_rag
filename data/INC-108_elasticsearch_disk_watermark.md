# Incident Report: INC-108
## Title: Product Search Index Read-Only Lock Due to Disk Watermark
**Service:** Catalog Search Service | **Severity:** P2 (High) | **Date:** 2026-09-02

### Summary
New products and inventory updates stopped appearing in search results. Updates returned FORBIDDEN/12/index read-only / allow delete (api).

### Root Cause
Unrotated debug logs filled the Elasticsearch data volume past the 95% flood-stage disk watermark, triggering Elasticsearch automatic safety mechanism to lock indices into read-only mode.

### Remediation Steps
1. Purged old application log indices older than 14 days.
2. Expanded EBS storage volumes on data nodes from 500GB to 1TB.
3. Reset the read-only block via PUT /products/_settings setting index.blocks.read_only_allow_delete to null.