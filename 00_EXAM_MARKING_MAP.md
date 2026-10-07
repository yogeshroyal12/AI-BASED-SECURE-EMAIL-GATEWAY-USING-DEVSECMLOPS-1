# DevSecMLOps Practical Exam — 30M Mapping

This project is deliberately organized to match the supplied marking table.

| Step | Phase | Marks | Project evidence |
|---|---|---:|---|
| 1 | PLAN & DESIGN | 7 | Threat model, security requirements, secure architecture, risk assessment |
| 2 | DEVELOP & BUILD | 8 | Secure coding, SAST, dependency scanning, secrets management |
| 3 | TEST & VERIFY | 8 | DAST, SCA, container scanning, automated security testing in CI/CD |
| 4 | DEPLOY & MONITOR | 7 | Secure Docker deployment, runtime protection, continuous monitoring, incident response |
| | TOTAL | **30** | |

## Extra highlights

- API-key authentication
- Data/input validation
- Privacy-aware audit trail
- Model integrity hash
- Model metadata/version
- Explainable risk indicators
- Drift detection
- Prometheus + Grafana dashboard
- Streamlit operational dashboard
- Health checks
- CI/CD gates
- Non-root container
- VS Code launch/tasks setup

## One-line story

> Build an ML email classifier, secure every development stage, test every layer, deploy safely, monitor continuously, and respond to incidents.

## Viva definitions

### Threat Modeling
Identify what can go wrong before implementation.

### SAST
Static Application Security Testing — scans source code without running the application.

### SCA
Software Composition Analysis — checks third-party dependencies for known vulnerabilities.

### DAST
Dynamic Application Security Testing — tests the running application.

### Container Scanning
Checks the container image and packages for known vulnerabilities.

### RASP
Runtime Application Self-Protection — runtime controls detect/block suspicious requests while the application is running.

### Incident Response
Detect, contain, investigate, recover and document security incidents.
