# Architecture Overview: Payment & Checkout Service
**Owner:** FinTech Core Team

### Components
- API Layer: FastAPI service running on Kubernetes (6 pods default, HPA scales up to 20).
- Database: AWS Aurora PostgreSQL (db.r6g.xlarge), max connections 500. Uses SQLAlchemy pooling (DB_POOL_MAX=250).
- External Dependencies: Stripe API for card processing and webhook callbacks (/webhooks/stripe).
- Failure Modes: If PostgreSQL connection pool saturates, the API returns HTTP 503 after a 5-second timeout.