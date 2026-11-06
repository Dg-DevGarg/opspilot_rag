# Architecture Overview: Event-Driven Order & Notification Pipeline
**Owner:** Messaging Team

### Data Flow
1. Checkout Service publishes order events to Kafka topic order-events (12 partitions).
2. Notification Service consumer group reads from order-events and dispatches emails via SendGrid and SMS via Twilio.
3. Fault Tolerance: Messages failing schema validation 3 times are routed to order-events-dlq (Dead Letter Queue).