# Runbook: Debugging Kubernetes Pod CrashLoopBackOff & OOMKilled
**Applies to:** EKS / GKE Clusters

### Investigation Commands
1. Check Last Termination Reason: kubectl describe pod <pod-name> -n production
   - Exit Code 137 (OOMKilled): Container exceeded memory limit. Increase resources.limits.memory or fix memory leaks.
   - Exit Code 1: Application crash or uncaught exception.
2. Fetch Logs from Previous Crashed Container: kubectl logs <pod-name> -n production --previous
3. Verify Environment Variables & Secrets: Ensure required secrets or configmap keys exist.