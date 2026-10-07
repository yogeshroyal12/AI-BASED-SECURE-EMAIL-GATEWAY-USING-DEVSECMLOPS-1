# PHASE 1 — PLAN & DESIGN
## Secure Architecture

```text
                          USER
                           |
                           v
                +-----------------------+
                | Streamlit Dashboard   |
                +-----------+-----------+
                            |
                            | HTTP
                            v
                +-----------------------+
                | FastAPI Gateway       |
                |-----------------------|
                | API Key Auth          |
                | Pydantic Validation   |
                | Rate Limiting         |
                | Request ID            |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Feature / Text Layer  |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | ML Model              |
                | TF-IDF + Logistic Reg |
                +-----------+-----------+
                            |
                            v
                +-----------------------+
                | Decision Layer        |
                | SAFE → ALLOW          |
                | SPAM → QUARANTINE     |
                | PHISHING → BLOCK      |
                +-----------+-----------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
     +---------------+             +---------------+
     | Audit Logs    |             | Prometheus    |
     +---------------+             +-------+-------+
                                             |
                                             v
                                        +---------+
                                        | Grafana |
                                        +---------+

CI/CD path:

Git Push
   ↓
Pytest
   ↓
Bandit
   ↓
pip-audit
   ↓
Gitleaks
   ↓
Docker Build
   ↓
Trivy
   ↓
Ephemeral API
   ↓
OWASP ZAP
   ↓
Deploy
```

## Security controls by layer

| Layer | Control |
|---|---|
| Client | Dashboard, constrained inputs |
| API | API key authentication |
| Application | Validation, rate limiting, structured errors |
| Model | Version metadata + SHA-256 |
| Source | Bandit |
| Dependencies | pip-audit |
| Repository | Gitleaks |
| Container | Trivy |
| Running service | OWASP ZAP |
| Runtime | Security middleware + audit logging |
| Monitoring | Prometheus + Grafana |
| Response | Incident response runbook |
