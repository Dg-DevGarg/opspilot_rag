# Incident Report: INC-104
## Title: Frontend Checkout Blocked by Misconfigured CORS Headers
**Service:** API Gateway (Kong / Nginx) | **Severity:** P1 (Critical) | **Date:** 2026-06-01

### Summary
Web frontend users encountered blocked API calls during checkout with browser console error: Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource.

### Root Cause
A deployment to the API Gateway ingress stripped Access-Control-Allow-Origin: https://app.example.com due to a typo in the Helm chart template variable.

### Remediation Steps
1. Immediately rolled back the API Gateway release to version v2.14.1.
2. Validated preflight OPTIONS responses using curl -I -X OPTIONS https://api.example.com/checkout.
3. Added automated end-to-end Cypress test checking CORS headers in the staging CI pipeline.