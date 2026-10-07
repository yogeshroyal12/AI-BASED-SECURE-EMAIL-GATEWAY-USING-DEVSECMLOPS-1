# Secure Email Gateway — AI + DevSecMLOps Mini Project

A VS Code-ready mini project for a DevSecMLOps practical exam.

## What the system does

The application accepts an email subject and body, classifies the message as:

- SAFE
- SPAM
- PHISHING

It then assigns a risk level and security action:

- SAFE → ALLOW
- SPAM → QUARANTINE
- PHISHING → BLOCK

The ML model uses **TF-IDF + Logistic Regression**. The application is served through **FastAPI** and demonstrated through a polished **Streamlit dashboard**.

## Why this project is strong for the practical

It deliberately separates the exam work into four folders:

| Exam Section | Folder | Marks | Main Evidence |
|---|---|---:|---|
| Phase 1 | `01_PLAN_DESIGN` | 7 | Threat model, requirements, architecture, risk matrix |
| Phase 2 | `02_DEVELOP_BUILD` | 8 | Secure FastAPI code, ML, Bandit, pip-audit, Gitleaks |
| Phase 3 | `03_TEST_VERIFY` | 8 | Pytest, DAST with OWASP ZAP, Trivy, automated CI tests |
| Phase 4 | `04_DEPLOY_MONITOR` | 7 | Docker, runtime protection, Prometheus, Grafana, incident response |

### Extra project highlights

These are not strictly required by the supplied 30-mark table, but make the project more professional:

1. API-key authentication
2. Request-size validation
3. In-memory rate limiting
4. Privacy-aware audit logging using an email fingerprint instead of storing the full body
5. Model artifact SHA-256 integrity verification
6. Model metadata/version information
7. Explainable risk indicators
8. Basic data-drift check for batch monitoring
9. VS Code launch/tasks configuration
10. Docker health checks and non-root containers

## Project flow

```text
                        ┌────────────────────────┐
                        │ Streamlit Dashboard    │
                        │ Live Analysis + Metrics │
                        └────────────┬───────────┘
                                     │ HTTP
                                     ▼
                        ┌────────────────────────┐
                        │ FastAPI Secure Gateway │
                        │ Auth • Validation       │
                        │ Rate Limit • Audit Log  │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │ ML Prediction Service   │
                        │ TF-IDF + Logistic Reg.  │
                        └────────────┬───────────┘
                                     │
                       SAFE / SPAM / PHISHING
                                     │
                                     ▼
                         ALLOW / QUARANTINE / BLOCK
                                     │
                          ┌──────────┴──────────┐
                          ▼                     ▼
                     Audit Logs          Prometheus
                                                │
                                                ▼
                                             Grafana
```

## 1. Run in VS Code — Windows PowerShell

Open the extracted project folder in VS Code.

### Create a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy the environment file:

```powershell
Copy-Item .env.example .env
```

The included `.env.example` uses a demo key. Change it before real use.

### Train / refresh the model

```powershell
$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
python .\02_DEVELOP_BUILD\ml\train.py
```

The training script creates/refreshes:

```text
02_DEVELOP_BUILD/model/phishing_email_model.joblib
02_DEVELOP_BUILD/model/model_metadata.json
reports/model_metrics.json
```

### Start the FastAPI backend

```powershell
$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
http://127.0.0.1:8000/metrics
```

### Start the dashboard

Open a second VS Code terminal:

```powershell
streamlit run .\02_DEVELOP_BUILD\dashboard\streamlit_app.py
```

Open:

```text
http://localhost:8501
```

The dashboard uses the same API key from `.env`.

## 2. Docker deployment

Make sure Docker Desktop is running.

```powershell
docker compose up --build
```

Services:

| Service | URL |
|---|---|
| FastAPI | http://localhost:8000 |
| FastAPI Swagger | http://localhost:8000/docs |
| Streamlit | http://localhost:8501 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

Default Grafana credentials are controlled by `GRAFANA_ADMIN_USER` and `GRAFANA_ADMIN_PASSWORD` in `.env`.

To stop:

```powershell
docker compose down
```

## 3. Security tools — local demonstration

Run unit/security tests:

```powershell
$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
pytest -q .\03_TEST_VERIFY\tests
```

SAST:

```powershell
bandit -r .\02_DEVELOP_BUILD\app -ll
```

SCA:

```powershell
pip-audit -r requirements.txt
```

Secret scanning:

```powershell
gitleaks detect --source .
```

Container scan:

```powershell
docker build -t secure-email-gateway .
trivy image secure-email-gateway
```

## 4. DAST — OWASP ZAP

Start FastAPI first.

For a simple baseline scan:

```powershell
docker run --rm --network host `
  -t ghcr.io/zaproxy/zaproxy:stable `
  zap-baseline.py `
  -t http://127.0.0.1:8000/docs `
  -r zap-report.html
```

For the practical exam, explain:

> SAST analyzes the source code. DAST analyzes the running application from the attacker's perspective.

## 5. CI/CD

The workflow is in:

```text
.github/workflows/devsecmlops.yml
```

The pipeline is:

```text
Git Push
   ↓
Install
   ↓
Pytest
   ↓
Bandit (SAST)
   ↓
pip-audit (SCA)
   ↓
Gitleaks
   ↓
Docker Build
   ↓
Trivy Container Scan
   ↓
Start temporary API
   ↓
OWASP ZAP DAST
```

The DAST job uses an ephemeral CI environment with authentication disabled only for scanning. Production configuration keeps API-key authentication enabled.

Current workflow actions are intentionally pinned to current major/release lines available when this project was packaged, including checkout v7, setup-python v7, Gitleaks v3 and Trivy action v0.36.0.

## 6. Exam demonstration order

### PHASE 1 — PLAN & DESIGN — 7 marks

Show:

1. `01_PLAN_DESIGN/threat_model.md`
2. `01_PLAN_DESIGN/security_requirements.md`
3. `01_PLAN_DESIGN/architecture.md`
4. `01_PLAN_DESIGN/risk_assessment.md`

Say:

> I first identified threats, defined security requirements, designed a secure architecture, and prioritized the risks before implementation.

### PHASE 2 — DEVELOP & BUILD — 8 marks

Show:

1. FastAPI code
2. ML training code/model
3. input validation
4. authentication
5. audit logging
6. Bandit
7. pip-audit
8. Gitleaks

Say:

> Security controls are built into development instead of being added at the end.

### PHASE 3 — TEST & VERIFY — 8 marks

Run:

```powershell
pytest -q .\03_TEST_VERIFY\tests
bandit -r .\02_DEVELOP_BUILD\app -ll
pip-audit -r requirements.txt
docker build -t secure-email-gateway .
trivy image secure-email-gateway
```

Then demonstrate OWASP ZAP.

### PHASE 4 — DEPLOY & MONITOR — 7 marks

Show:

```text
Docker
   ↓
FastAPI
   ↓
Runtime protection
   ↓
Audit logs
   ↓
Prometheus
   ↓
Grafana
   ↓
Incident response runbook
```

## 7. Dashboard demo

The Streamlit dashboard contains four main tabs:

- **Live Email Analysis** — paste an email and see prediction, probability, risk, action and reasons
- **Security Dashboard** — live request/prediction/security counts
- **Audit & Incidents** — recent blocked/quarantined events
- **Model & Drift** — model version, training metrics, artifact hash and drift-check summary

## 8. Files you should be ready to explain

### Plan & Design
`01_PLAN_DESIGN/*`

### Develop & Build
`02_DEVELOP_BUILD/app/*`
`02_DEVELOP_BUILD/ml/*`
`02_DEVELOP_BUILD/model/*`

### Test & Verify
`03_TEST_VERIFY/tests/*`
`03_TEST_VERIFY/zap/*`

### Deploy & Monitor
`04_DEPLOY_MONITOR/prometheus/*`
`04_DEPLOY_MONITOR/grafana/*`
`04_DEPLOY_MONITOR/monitoring/*`
`04_DEPLOY_MONITOR/incident_response/*`

## 9. Important note about the dataset

The repository includes a small **synthetic demo dataset** so the project is self-contained and does not require downloading a third-party dataset just to run the practical.

For a stronger academic version, replace `02_DEVELOP_BUILD/data/emails.csv` with a documented public dataset and retrain the model.

## 10. Suggested project title

**AI-Based Secure Email Gateway with DevSecMLOps**

or

**Secure Intelligent Email Classification and Threat Prevention System using DevSecMLOps**
