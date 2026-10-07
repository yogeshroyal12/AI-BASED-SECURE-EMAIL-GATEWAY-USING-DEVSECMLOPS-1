import time
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .audit import get_stats, log_audit, log_security, read_recent, sha256_text
from .config import settings
from .metrics import REQUESTS, REQUEST_LATENCY, SECURITY_BLOCKS, SECURITY_EVENTS
from .model_service import model_service
from .schemas import (
    EmailRequest,
    HealthResponse,
    ModelInfoResponse,
    PredictionResponse,
    StatsResponse,
)
from .security import (
    check_rate_limit,
    detect_risk_indicators,
    get_client_ip,
    require_api_key,
)


app = FastAPI(
    title="AI-Based Secure Email Gateway",
    version="1.0.0",
    description=(
        "DevSecMLOps mini project: secure email classification using "
        "TF-IDF + Logistic Regression."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    start = time.perf_counter()
    request_id = str(uuid.uuid4())
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        status_code = response.status_code
        return response
    finally:
        elapsed = time.perf_counter() - start
        REQUESTS.labels(
            method=request.method,
            path=request.url.path,
            status_code=str(locals().get("status_code", 500)),
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
        ).observe(elapsed)


@app.get("/health", response_model=HealthResponse)
def health() -> dict:
    return {"status": "healthy", "model_version": model_service.version}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(
        generate_latest().decode("utf-8"),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post(
    "/analyze-email",
    response_model=PredictionResponse,
    dependencies=[Depends(require_api_key), Depends(check_rate_limit)],
)
def analyze_email(payload: EmailRequest, request: Request) -> dict:
    request_id = str(uuid.uuid4())
    combined_text = f"{payload.subject}\n{payload.body}"

    try:
        result = model_service.predict(payload.subject, payload.body)
        reasons = detect_risk_indicators(combined_text)

        if result["prediction"] == "PHISHING" and result["action"] == "BLOCK":
            if not reasons:
                reasons = ["Model confidence indicates phishing."]
            event_type = "PHISHING_BLOCK"
            severity = "HIGH"
        elif result["prediction"] == "SPAM" and result["action"] == "QUARANTINE":
            if not reasons:
                reasons = ["Model confidence indicates spam."]
            event_type = "SPAM_QUARANTINE"
            severity = "MEDIUM"
        else:
            event_type = "EMAIL_ALLOWED"
            severity = "LOW"

        log_audit(
            settings.audit_log_path,
            {
                "request_id": request_id,
                "event_type": event_type,
                "prediction": result["prediction"],
                "probability": result["probability"],
                "risk": result["risk"],
                "action": result["action"],
                "client_ip": get_client_ip(request),
                "email_sha256": sha256_text(combined_text),
            },
        )

        if result["action"] == "BLOCK":
            SECURITY_BLOCKS.labels(reason=event_type).inc()
            SECURITY_EVENTS.labels(event_type=event_type).inc()
            log_security(
                settings.security_log_path,
                {
                    "request_id": request_id,
                    "event_type": event_type,
                    "severity": severity,
                    "client_ip": get_client_ip(request),
                    "action": "BLOCKED",
                },
            )

        return {
            "request_id": request_id,
            **result,
            "reasons": reasons,
        }
    except Exception as exc:
        log_security(
            settings.security_log_path,
            {
                "request_id": request_id,
                "event_type": "PREDICTION_ERROR",
                "severity": "HIGH",
                "error_type": type(exc).__name__,
                "action": "REVIEW",
            },
        )
        SECURITY_EVENTS.labels(event_type="PREDICTION_ERROR").inc()
        raise HTTPException(status_code=500, detail="Prediction service error.") from exc


@app.get(
    "/admin/stats",
    response_model=StatsResponse,
    dependencies=[Depends(require_api_key)],
)
def admin_stats() -> dict:
    return get_stats(settings.audit_log_path, settings.security_log_path)


@app.get(
    "/admin/audit",
    dependencies=[Depends(require_api_key)],
)
def admin_audit(limit: int = 25) -> list[dict]:
    limit = max(1, min(limit, 100))
    return read_recent(settings.audit_log_path, limit)


@app.get(
    "/admin/security-events",
    dependencies=[Depends(require_api_key)],
)
def admin_security_events(limit: int = 25) -> list[dict]:
    limit = max(1, min(limit, 100))
    return read_recent(settings.security_log_path, limit)


@app.get(
    "/admin/model-info",
    response_model=ModelInfoResponse,
    dependencies=[Depends(require_api_key)],
)
def admin_model_info() -> dict:
    return model_service.info
