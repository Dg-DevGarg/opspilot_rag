# Architecture Overview: Authentication & Session Management
**Owner:** Platform Security Team

### Token & Cache Flow
- Stateless Auth: Short-lived JWT access tokens (15-minute expiry) signed with RS256. Requires synchronized NTP clocks (30s leeway).
- Stateful Cache: Redis Cluster (8GB memory, allkeys-lru eviction) stores refresh tokens, active sessions, and guest carts (2-hour TTL).