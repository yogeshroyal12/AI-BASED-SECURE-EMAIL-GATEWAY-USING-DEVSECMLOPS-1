# PHASE 1 — PLAN & DESIGN
## Threat Modeling

## System

AI-Based Secure Email Gateway

### Assets

| Asset | Why it matters |
|---|---|
| Email content | Potentially sensitive user data |
| ML model | Business logic and decision capability |
| API key | Controls access to prediction endpoints |
| Audit logs | Security evidence |
| Container image | Production deployment artifact |
| Metrics | Availability and security monitoring data |

### Trust boundaries

```text
User / Dashboard
      |
      | HTTP
      v
FastAPI Gateway
      |
      +---- Authentication
      +---- Input Validation
      +---- Rate Limiting
      +---- Audit Logging
      |
      v
ML Model
      |
      +---- Prediction
      +---- Risk decision
      |
      +---- Metrics
      v
Prometheus / Grafana
```

### Main threats

| ID | Threat | Example | Control |
|---|---|---|---|
| T01 | Malformed input | Empty/oversized email | Pydantic validation + request limits |
| T02 | API abuse | Excessive requests | Rate limiter |
| T03 | Unauthorized use | Missing/invalid API key | API-key authentication |
| T04 | Sensitive log exposure | Full email written to disk | Fingerprint-only audit logging |
| T05 | Source vulnerability | Insecure Python code | Bandit |
| T06 | Dependency vulnerability | Known vulnerable package | pip-audit |
| T07 | Secret leakage | Key committed to Git | Gitleaks + .env |
| T08 | Container vulnerability | Vulnerable OS/package | Trivy |
| T09 | Running-app vulnerability | Weak HTTP behavior | OWASP ZAP |
| T10 | Artifact tampering | Modified model file | SHA-256 integrity check |
| T11 | Abnormal runtime behavior | Repeated blocked requests | Metrics + audit logs |
| T12 | Data drift | Input population changes | Drift check |

## Practical exam sentence

> I used threat modeling before coding so that security requirements came from actual risks instead of being added after development.
