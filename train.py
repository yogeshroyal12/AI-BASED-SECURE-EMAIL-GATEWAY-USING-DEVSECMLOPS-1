from __future__ import annotations

import csv
import hashlib
import json
import random
from datetime import datetime, timezone
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "02_DEVELOP_BUILD" / "data" / "emails.csv"
MODEL_DIR = ROOT / "02_DEVELOP_BUILD" / "model"
MODEL_PATH = MODEL_DIR / "phishing_email_model.joblib"
META_PATH = MODEL_DIR / "model_metadata.json"
REPORT_DIR = ROOT / "reports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


TEMPLATES = {
    "SAFE": [
        ("Project update", "Hi team, the sprint review is scheduled for tomorrow at 10 AM. Please review the attached notes."),
        ("Meeting reminder", "Reminder: our engineering meeting starts at 2 PM in room 301. Please bring your status update."),
        ("Invoice approved", "The finance team approved invoice INV-1042. The payment will be processed according to the normal schedule."),
        ("Course timetable", "The updated timetable has been shared with the class. Please check the official portal for the latest schedule."),
        ("Travel plan", "Here is the itinerary for the conference. The hotel confirmation and train details are included for your reference."),
        ("Document review", "Please review the design document before Friday and add your comments in the shared workspace."),
        ("Team lunch", "We are planning a team lunch on Thursday at 1 PM. Reply to this message if you can join."),
        ("Assignment feedback", "Your assignment feedback is available in the learning portal. Please review the comments when convenient."),
    ],
    "SPAM": [
        ("Exclusive offer", "Congratulations! You qualify for a limited offer on premium products. Get your discount today."),
        ("You won a prize", "You are selected as a winner in our promotional campaign. Claim your reward while the offer is active."),
        ("Special discount", "Limited time promotion: save 70 percent on selected products. Shop now and enjoy the special deal."),
        ("Free gift", "You have been chosen for a free promotional gift. Complete the short form to claim it."),
        ("Make extra money", "Earn extra income from home with our promotional opportunity. Spaces are limited this week."),
        ("Cash reward", "A cash reward is available for selected customers. Confirm your participation before the campaign closes."),
        ("Flash sale", "Flash sale today only. Huge savings on popular products while supplies last."),
        ("Bonus promotion", "A special bonus has been reserved for you. Take advantage of the promotion before it expires."),
    ],
    "PHISHING": [
        ("Urgent account verification", "Your account has been suspended. Verify your password immediately to avoid permanent closure."),
        ("Security alert", "We detected unusual activity. Click here to verify your account and confirm your login details."),
        ("Password reset required", "Your password expires today. Open the link and sign in to keep access to your account."),
        ("Bank account warning", "Your banking profile is locked. Verify your credentials immediately to restore access."),
        ("Mailbox suspension", "Your mailbox is scheduled for deactivation. Click here and confirm your password to prevent closure."),
        ("Payment verification", "Your payment could not be processed. Sign in now and verify your card information."),
        ("Admin notice", "Your administrator account requires immediate verification. Confirm your login information to continue."),
        ("Final warning", "This is the final warning. Your account will be terminated unless you verify your credentials immediately."),
    ],
}


def build_demo_dataset(path: Path, rows_per_class: int = 100) -> None:
    rng = random.Random(42)
    rows: list[tuple[str, str, str]] = []

    for label, templates in TEMPLATES.items():
        for index in range(rows_per_class):
            subject, body = rng.choice(templates)
            suffix = rng.choice(
                [
                    "",
                    " Please review the details carefully.",
                    " Thank you for your attention.",
                    " This message was generated automatically.",
                    " Regards, Support Team",
                ]
            )
            rows.append((subject, body + suffix, label))

    rng.shuffle(rows)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["subject", "body", "label"])
        writer.writerows(rows)


def main() -> None:
    if not DATA_PATH.exists():
        build_demo_dataset(DATA_PATH)

    rows = []
    with DATA_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(row)

    texts = [f"subject: {row['subject']}\nbody: {row['body']}" for row in rows]
    labels = [row["label"] for row in rows]

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.20,
        random_state=42,
        stratify=labels,
    )

    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True,
                    max_features=8000,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1200,
                    random_state=42,
                ),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    accuracy = accuracy_score(y_test, predictions)
    weighted_f1 = f1_score(y_test, predictions, average="weighted")
    report = classification_report(y_test, predictions, output_dict=True)

    joblib.dump(pipeline, MODEL_PATH)
    digest = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()

    metadata = {
        "version": "1.0.0",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "algorithm": "TF-IDF + Logistic Regression",
        "classes": list(pipeline.classes_),
        "metrics": {
            "accuracy": round(float(accuracy), 4),
            "weighted_f1": round(float(weighted_f1), 4),
            "test_rows": len(y_test),
            "train_rows": len(y_train),
        },
        "classification_report": report,
        "dataset": {
            "path": "02_DEVELOP_BUILD/data/emails.csv",
            "rows": len(rows),
            "source": "Synthetic demo dataset generated for this project",
        },
        "sha256": digest,
    }

    META_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / "model_metrics.json"
    report_path.write_text(json.dumps(metadata["metrics"] | {"classification_report": report}, indent=2), encoding="utf-8")

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metadata saved to: {META_PATH}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Weighted F1: {weighted_f1:.4f}")


if __name__ == "__main__":
    main()
