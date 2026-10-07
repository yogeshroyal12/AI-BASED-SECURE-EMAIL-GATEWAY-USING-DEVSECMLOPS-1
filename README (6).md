# DAST — OWASP ZAP

## Purpose

DAST tests the running application instead of the source code.

## Local PowerShell command

Start FastAPI first:

```powershell
$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
uvicorn app.main:app --reload --port 8000
```

Then:

```powershell
docker run --rm --network host `
  -t ghcr.io/zaproxy/zaproxy:stable `
  zap-baseline.py `
  -t http://127.0.0.1:8000/docs `
  -r zap-report.html
```

## Exam wording

> I use OWASP ZAP for DAST because it probes the running HTTP application for issues that may not be visible from static source analysis alone.

For a deeper authenticated DAST engagement, configure ZAP to inject `X-API-Key` into requests and target `/analyze-email`.
