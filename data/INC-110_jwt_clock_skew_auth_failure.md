# Incident Report: INC-110
## Title: Authentication Rejections (Token used before issued) on Worker Node
**Service:** Identity & Auth Service | **Severity:** P2 (High) | **Date:** 2026-10-01

### Summary
Approximately 15% of login attempts failed immediately after token generation with HTTP 401 ImmatureSignatureError: The token is not yet valid (iat).

### Root Cause
The NTP daemon (chronyd) crashed on one EC2 worker node (ip-10-0-4-22), causing its system clock to drift 45 seconds behind the Auth token issuer node.

### Remediation Steps
1. Cordoned and drained node ip-10-0-4-22.
2. Restarted chronyd service and verified clock sync.
3. Added a 30-second leeway parameter to jwt.decode(..., leeway=30) in the authentication middleware.