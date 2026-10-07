import hashlib
import json
from pathlib import Path

import joblib

from .audit import log_audit, sha256_text
from .config import settings
from .metrics import ACTIONS, PREDICTIONS


class ModelService:
    def __init__(self) -> None:
        self.model = joblib.load(settings.model_path)
        self.metadata = json.loads(settings.model_metadata_path.read_text(encoding="utf-8"))
        self._verify_integrity()

    def _verify_integrity(self) -> None:
        digest = hashlib.sha256(settings.model_path.read_bytes()).hexdigest()
        expected = self.metadata.get("sha256")
        if expected and expected != digest:
            raise RuntimeError(
                "Model integrity check failed: SHA-256 does not match model metadata."
            )

    def predict(self, subject: str, body: str) -> dict:
        text = f"subject: {subject}\nbody: {body}"
        probabilities = self.model.predict_proba([text])[0]
        classes = list(self.model.classes_)
        best_index = int(probabilities.argmax())
        prediction = str(classes[best_index])
        probability = float(probabilities[best_index])

        if probability >= 0.80:
            risk = "HIGH"
        elif probability >= 0.55:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        if prediction == "PHISHING" and probability >= 0.60:
            action = "BLOCK"
        elif prediction == "SPAM" and probability >= 0.60:
            action = "QUARANTINE"
        else:
            action = "ALLOW"

        PREDICTIONS.labels(prediction=prediction).inc()
        ACTIONS.labels(action=action).inc()

        return {
            "prediction": prediction,
            "probability": round(probability, 4),
            "risk": risk,
            "action": action,
        }

    @property
    def version(self) -> str:
        return self.metadata["version"]

    @property
    def info(self) -> dict:
        return self.metadata


model_service = ModelService()
