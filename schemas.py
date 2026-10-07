from typing import Literal

from pydantic import BaseModel, Field, field_validator


class EmailRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1, max_length=10000)

    @field_validator("subject", "body")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.replace("\x00", "").strip()
        if not value:
            raise ValueError("Field cannot be empty.")
        return value


class PredictionResponse(BaseModel):
    request_id: str
    prediction: Literal["SAFE", "SPAM", "PHISHING"]
    probability: float
    risk: Literal["LOW", "MEDIUM", "HIGH"]
    action: Literal["ALLOW", "QUARANTINE", "BLOCK"]
    reasons: list[str]


class HealthResponse(BaseModel):
    status: str
    model_version: str


class StatsResponse(BaseModel):
    total_events: int
    safe: int
    spam: int
    phishing: int
    allowed: int
    quarantined: int
    blocked: int
    security_events: int
    recent_incidents: list[dict]


class ModelInfoResponse(BaseModel):
    version: str
    trained_at: str
    algorithm: str
    classes: list[str]
    metrics: dict
    sha256: str
