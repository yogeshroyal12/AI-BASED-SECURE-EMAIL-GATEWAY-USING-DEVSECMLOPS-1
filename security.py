import re
import threading
import time
from collections import defaultdict

from fastapi import Header, HTTPException, Request, status

from .audit import log_security
from .config import settings


class SimpleRateLimiter:
    """
    Lightweight in-memory limiter for an exam/demo project.
    For distributed production systems, use Redis or an API gateway.
    """

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def allow(self, identity: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            hits = [timestamp for timestamp in self._hits[identity] if timestamp >= cutoff]
            if len(hits) >= self.limit:
                self._hits[identity] = hits
                return False
            hits.append(now)
            self._hits[identity] = hits
            return True


rate_limiter = SimpleRateLimiter(
    settings.rate_limit_requests,
    settings.rate_limit_window_seconds,
)

SUSPICIOUS_PATTERNS = {
    "Urgency detected": re.compile(r"\b(urgent|immediately|right away|act now|final warning)\b", re.I),
    "Credential request": re.compile(r"\b(password|passcode|otp|one[- ]time code|login|sign in|verify your account)\b", re.I),
    "Account-threat language": re.compile(r"\b(suspended|locked|deactivated|closed|terminate)\b", re.I),
    "Suspicious link language": re.compile(r"\b(click here|open the link|verify here|follow this link)\b", re.I),
    "Prize/promotion language": re.compile(r"\b(winner|won|prize|free money|claim your reward|limited offer)\b", re.I),
}


def get_client_ip(request: Request) -> str:
    # In a real trusted proxy setup, X-Forwarded-For handling should be restricted
    # to known proxies. For the exam demo we use the direct client address.
    return request.client.host if request.client else "unknown"


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if not settings.auth_required:
        return
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key.",
        )


def check_rate_limit(request: Request) -> None:
    if not rate_limiter.allow(get_client_ip(request)):
        log_security(
            settings.security_log_path,
            {
                "event_type": "RATE_LIMIT_BLOCK",
                "severity": "HIGH",
                "client_ip": get_client_ip(request),
                "path": request.url.path,
                "action": "BLOCKED",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )


def detect_risk_indicators(text: str) -> list[str]:
    return [name for name, pattern in SUSPICIOUS_PATTERNS.items() if pattern.search(text)]
