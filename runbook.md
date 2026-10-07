# PHASE 4 — DEPLOY & MONITOR
## Incident Response Runbook

## Incident example

Suppose the system receives an unusual spike:

```text
Hundreds of requests in a short period
       ↓
Rate limiter triggers
       ↓
Security metric increases
       ↓
Security log records the event
       ↓
Operator investigates
```

## Response steps

### 1. Detect
Use:

- Grafana
- Prometheus
- security.log
- audit.log

### 2. Triage
Identify:

- time
- endpoint
- event type
- request volume
- model/action pattern

### 3. Contain
Possible actions:

- block abusive requests
- rotate the API key
- temporarily tighten the rate limit
- restart the affected container

### 4. Investigate
Review:

```text
logs/security.log
logs/audit.log
```

Because only fingerprints are stored, the system avoids retaining the full email body in the security log.

### 5. Recover
- fix the root cause
- redeploy a validated image
- re-run security scans
- monitor again

### 6. Learn
Document:

- what happened
- why it happened
- control that failed
- control that prevented escalation
- improvement to make next time

## Exam wording

> Incident response is not only detection. I detect the event, contain it, investigate the evidence, recover the service, and capture lessons for improving future controls.
