# Runbook: Resolving Kafka Consumer Group Lag
**Applies to:** Apache Kafka / AWS MSK

### Symptoms
- Delayed async events (emails, webhooks, analytics updates).
- Alert: KafkaConsumerLagHigh (> 50,000 messages).

### Recovery Procedure
1. Inspect Consumer Group Status: kafka-consumer-groups.sh --bootstrap-server $BROKERS --describe --group <group-name>
2. Check Consumer Logs for Poison Pill Errors: Look for deserialization exceptions repeating on the same offset.
3. Scale Out Consumers: Increase Kubernetes deployment replicas up to the number of topic partitions.
4. Skip Corrupted Offset: Stop consumers, run --reset-offsets --shift-by 1 --execute, and restart.