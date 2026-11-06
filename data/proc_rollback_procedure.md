# Procedure: Production Deployment Rollback
**Applies to:** Kubernetes Deployments (Helm / ArgoCD)

### Standard Rollback Steps
1. Check recent deployment history: kubectl rollout history deployment/<service-name> -n production
2. Rollback to previous stable revision: kubectl rollout undo deployment/<service-name> -n production
3. Verify pod health: kubectl get pods -l app=<service-name> -n production -w
4. Check error rates in Datadog/Prometheus dashboards to ensure 5xx errors decline below 0.1%.