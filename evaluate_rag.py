from rag_engine import collection, index_documents

# Ground-truth evaluation benchmark: 10 realistic queries mapped to expected source files
EVAL_DATASET = [
    {
        "query": "Payment API returning HTTP 503 and PostgreSQL connection pool exhausted",
        "expected_source": "INC-101_database_pool_exhaustion.md"
    },
    {
        "query": "Users logged out randomly and Redis cluster out of memory OOM",
        "expected_source": "INC-102_redis_cluster_oom.md"
    },
    {
        "query": "Order confirmation emails delayed due to Kafka consumer lag poison pill",
        "expected_source": "INC-103_kafka_consumer_lag.md"
    },
    {
        "query": "Browser console blocking checkout API due to missing CORS Access-Control-Allow-Origin header",
        "expected_source": "INC-104_cors_misconfiguration.md"
    },
    {
        "query": "Stripe billing webhooks failing with HTTP 400 signature verification error",
        "expected_source": "INC-105_stripe_webhook_signing_failure.md"
    },
    {
        "query": "PDF export worker crashing with exit code 137 OOMKilled on large CSV files",
        "expected_source": "INC-106_worker_memory_leak.md"
    },
    {
        "query": "Microservices failing with temporary failure in name resolution and CoreDNS throttling",
        "expected_source": "INC-107_dns_resolution_timeout.md"
    },
    {
        "query": "Product catalog search index locked in read-only mode due to 95% disk watermark",
        "expected_source": "INC-108_elasticsearch_disk_watermark.md"
    },
    {
        "query": "Public API failing with ERR_CERT_DATE_INVALID expired Let's Encrypt SSL certificate",
        "expected_source": "INC-109_tls_certificate_expired.md"
    },
    {
        "query": "Login failing with HTTP 401 ImmatureSignatureError token used before issued clock skew",
        "expected_source": "INC-110_jwt_clock_skew_auth_failure.md"
    }
]


def evaluate_retrieval(k: int = 3):
    index_documents()
    hits = 0
    reciprocal_ranks = []

    print(f"Running RAG Retrieval Benchmark (Top-{k}) across {len(EVAL_DATASET)} test cases...\n")

    for idx, item in enumerate(EVAL_DATASET, 1):
        results = collection.query(query_texts=[item["query"]], n_results=k)
        retrieved_files = [m["source"] for m in results["metadatas"][0]]

        # Calculate Recall@K and Reciprocal Rank
        expected = item["expected_source"]
        if expected in retrieved_files:
            hits += 1
            rank = retrieved_files.index(expected) + 1
            rr = 1.0 / rank
            status = f"PASS (Rank #{rank})"
        else:
            rr = 0.0
            status = "FAIL"

        reciprocal_ranks.append(rr)
        print(f"[{idx:02d}] {status} | Expected: {expected} | Retrieved: {retrieved_files}")

    recall_at_k = (hits / len(EVAL_DATASET)) * 100
    mrr = sum(reciprocal_ranks) / len(EVAL_DATASET)

    print("\n" + "=" * 55)
    print(f"FINAL EVALUATION METRICS (K={k}):")
    print(f"- Recall@{k}: {recall_at_k:.1f}% ({hits}/{len(EVAL_DATASET)} incidents matched)")
    print(f"- Mean Reciprocal Rank (MRR): {mrr:.3f}")
    print("=" * 55)


if __name__ == "__main__":
    evaluate_retrieval(k=3)