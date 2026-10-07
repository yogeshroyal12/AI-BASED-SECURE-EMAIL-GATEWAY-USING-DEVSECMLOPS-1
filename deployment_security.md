# PHASE 4 — DEPLOY & MONITOR
## Secure Deployment Controls

1. Non-root container user
2. Minimal Python base image
3. `no-new-privileges`
4. Health check on `/health`
5. Environment-based secrets
6. No full email-body logging
7. Runtime rate limiting
8. Prometheus metrics
9. Grafana dashboard
10. Incident-response documentation

## Runtime protection (RASP-like layer)

The application has runtime controls inside the FastAPI process:

```text
Request
  ↓
API authentication
  ↓
Input validation
  ↓
Rate limit
  ↓
Prediction
  ↓
Security action
  ↓
Audit + metrics
```

This is a simple educational RASP implementation. In production, advanced RASP may be provided by specialized agents/gateways.
