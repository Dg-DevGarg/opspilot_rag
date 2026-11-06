# Incident Report: INC-106
## Title: Report Generation Service CrashLoopBackOff (OOMKilled)
**Service:** Analytics & PDF Export Worker | **Severity:** P2 (High) | **Date:** 2026-08-03

### Summary
Kubernetes pods for pdf-export-worker repeatedly crashed with exit code 137 (OOMKilled), failing scheduled enterprise financial exports.

### Root Cause
The worker loaded entire multi-gigabyte CSV datasets into pandas DataFrames in memory simultaneously without chunking or freeing memory references after upload to S3.

### Remediation Steps
1. Temporarily bumped pod memory limit from 2Gi to 6Gi in deployment.yaml.
2. Refactored data processing to stream rows in chunks of 50,000 using pd.read_csv(chunksize=50000).
3. Added explicit garbage collection calls after each batch completed.