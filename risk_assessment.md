# PHASE 1 — PLAN & DESIGN
## Risk Assessment

Risk score = Probability × Impact.

Scale:
- 1–2 Low
- 3–4 Medium
- 5–6 High
- 7–9 Critical

| Risk | Probability | Impact | Score | Level | Mitigation |
|---|---:|---:|---:|---|---|
| Malformed/oversized request | 3 | 3 | 9 | Critical | Validation + size limits |
| API abuse | 3 | 3 | 9 | Critical | Rate limiting |
| Unauthorized API access | 2 | 3 | 6 | High | API key |
| Secret leakage | 2 | 3 | 6 | High | Gitleaks + `.env` |
| Dependency vulnerability | 2 | 3 | 6 | High | pip-audit |
| Container vulnerability | 2 | 3 | 6 | High | Trivy |
| Running API weakness | 2 | 3 | 6 | High | OWASP ZAP |
| Model artifact tampering | 1 | 3 | 3 | Medium | SHA-256 |
| Log privacy leak | 2 | 3 | 6 | High | Fingerprint-only logging |
| Data drift | 2 | 2 | 4 | Medium | Drift check |

## Risk treatment

### High/Critical
Must be mitigated before deployment.

### Medium
Monitor and include in the operational plan.

### Low
Accept with documentation.

## Exam explanation

> I prioritized threats using probability and impact, then mapped the highest risks to specific preventative or detective controls.
