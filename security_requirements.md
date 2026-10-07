# PHASE 1 — PLAN & DESIGN
## Security Requirements

### Functional security requirements

1. Every prediction request must be validated.
2. The API must reject empty or oversized email content.
3. Prediction endpoints must require an API key.
4. Requests must be rate limited.
5. Full email bodies must not be stored in audit logs.
6. Dependencies must be scanned before deployment.
7. Source code must undergo SAST.
8. Repository secrets must be scanned.
9. Docker images must be scanned.
10. The running API must undergo DAST.
11. Security events must be observable through metrics and logs.
12. The ML artifact must be integrity-checked at startup.

### Privacy requirement

The audit system stores:

- timestamp
- event type
- action
- predicted class
- confidence
- request/client fingerprint
- email SHA-256 fingerprint

It does **not** store the full email body.

### Availability requirement

The service must reject abusive request bursts using a runtime rate limiter.

### Deployment requirement

The production container runs as a non-root user and uses a minimal Python base image.

### Model requirement

The model must have:

- model version
- training date
- classes
- evaluation metrics
- artifact SHA-256

### Security gates

A deployment should be considered ready only when:

```text
Tests pass
AND
SAST passes
AND
SCA has no unresolved high/critical issue
AND
Secret scan passes
AND
Container scan is acceptable
AND
DAST findings are reviewed
```
