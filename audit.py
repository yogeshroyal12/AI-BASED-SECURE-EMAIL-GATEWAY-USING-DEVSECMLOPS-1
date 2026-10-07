import hashlib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path


_lock = threading.Lock()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    with _lock:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def log_audit(path: Path, event: dict) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    _append_jsonl(path, event)


def log_security(path: Path, event: dict) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    _append_jsonl(path, event)


def read_recent(path: Path, limit: int = 25) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows[-limit:][::-1]


def get_stats(audit_path: Path, security_path: Path) -> dict:
    events = read_recent(audit_path, limit=100000)
    total = len(events)
    counts = {
        "SAFE": 0,
        "SPAM": 0,
        "PHISHING": 0,
        "ALLOW": 0,
        "QUARANTINE": 0,
        "BLOCK": 0,
    }
    for event in events:
        for key in counts:
            if event.get("prediction") == key or event.get("action") == key:
                counts[key] += 1

    security_events = read_recent(security_path, limit=100000)
    incidents = [
        row for row in security_events
        if row.get("severity") in {"HIGH", "CRITICAL", "WARNING"}
    ][:20]

    return {
        "total_events": total,
        "safe": counts["SAFE"],
        "spam": counts["SPAM"],
        "phishing": counts["PHISHING"],
        "allowed": counts["ALLOW"],
        "quarantined": counts["QUARANTINE"],
        "blocked": counts["BLOCK"],
        "security_events": len(security_events),
        "recent_incidents": incidents,
    }
