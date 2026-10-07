# PHASE 1 — PLAN & DESIGN
## Data Flow

```text
Email Subject + Email Body
          |
          v
   Pydantic Validation
          |
          v
    Security Checks
   /      |       \
 Auth   Rate      Size
          |
          v
       ML Model
          |
          v
   Prediction + Score
          |
          +------> Explainable indicators
          |
          +------> Security action
          |
          +------> Audit log
          |
          +------> Prometheus metrics
```

### Data minimization

The application does not need to persist the full email body for operational monitoring.

A one-way SHA-256 fingerprint is stored for audit correlation.
