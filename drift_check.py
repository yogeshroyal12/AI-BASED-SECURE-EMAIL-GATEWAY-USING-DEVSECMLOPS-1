from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "02_DEVELOP_BUILD" / "data" / "emails.csv"
CURRENT = Path(__file__).resolve().parent / "current_batch.csv"
OUTPUT = Path(__file__).resolve().parent / "drift_report.json"


def lengths(frame: pd.DataFrame) -> pd.Series:
    return (frame["subject"].fillna("") + " " + frame["body"].fillna("")).str.len()


def psi(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    expected = expected.astype(float).to_numpy()
    actual = actual.astype(float).to_numpy()

    low = min(expected.min(), actual.min())
    high = max(expected.max(), actual.max())
    edges = np.linspace(low, high + 1e-9, bins + 1)

    expected_counts, _ = np.histogram(expected, bins=edges)
    actual_counts, _ = np.histogram(actual, bins=edges)

    expected_pct = expected_counts / max(expected_counts.sum(), 1)
    actual_pct = actual_counts / max(actual_counts.sum(), 1)

    expected_pct = np.clip(expected_pct, 1e-6, None)
    actual_pct = np.clip(actual_pct, 1e-6, None)

    return float(np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct)))


def main() -> None:
    baseline = pd.read_csv(BASELINE)
    current = pd.read_csv(CURRENT)

    score = psi(lengths(baseline), lengths(current))
    status = "DRIFT_DETECTED" if score >= 0.20 else "NO_DRIFT"

    report = {
        "status": status,
        "psi_email_length": round(score, 4),
        "threshold": 0.20,
        "baseline_rows": len(baseline),
        "current_rows": len(current),
        "note": "Illustrative batch drift check for the practical project.",
    }

    OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
