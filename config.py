import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("API_KEY", "change-me")
    auth_required: bool = os.getenv("AUTH_REQUIRED", "true").lower() == "true"
    max_subject_chars: int = int(os.getenv("MAX_SUBJECT_CHARS", "200"))
    max_body_chars: int = int(os.getenv("MAX_BODY_CHARS", "10000"))
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "30"))
    rate_limit_window_seconds: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    allowed_origins: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    )
    model_path: Path = PROJECT_ROOT / "02_DEVELOP_BUILD" / "model" / "phishing_email_model.joblib"
    model_metadata_path: Path = PROJECT_ROOT / "02_DEVELOP_BUILD" / "model" / "model_metadata.json"
    audit_log_path: Path = PROJECT_ROOT / "logs" / "audit.log"
    security_log_path: Path = PROJECT_ROOT / "logs" / "security.log"


settings = Settings()
settings.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
