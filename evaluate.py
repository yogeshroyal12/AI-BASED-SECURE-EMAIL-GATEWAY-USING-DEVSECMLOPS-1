from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from train import DATA_PATH, MODEL_PATH


def main() -> None:
    rows = json.loads(
        json.dumps(
            [
                row
                for row in __import__("csv").DictReader(
                    DATA_PATH.open(encoding="utf-8")
                )
            ]
        )
    )

    texts = [f"subject: {row['subject']}\nbody: {row['body']}" for row in rows]
    labels = [row["label"] for row in rows]

    _, x_test, _, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=42, stratify=labels
    )

    model = joblib.load(MODEL_PATH)
    predictions = model.predict(x_test)

    report = classification_report(y_test, predictions, output_dict=True)
    matrix = confusion_matrix(y_test, predictions, labels=list(model.classes_)).tolist()

    output = {
        "classes": list(model.classes_),
        "classification_report": report,
        "confusion_matrix": matrix,
    }

    path = Path("reports") / "evaluation_report.json"
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
