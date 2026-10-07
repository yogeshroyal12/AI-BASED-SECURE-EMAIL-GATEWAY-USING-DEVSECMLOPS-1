# ML — Develop & Build

## Training

```powershell
$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
python .\02_DEVELOP_BUILD\ml\train.py
```

The current demo uses:

- TF-IDF
- Logistic Regression
- 3 classes: SAFE, SPAM, PHISHING

## Why this is enough

The exam is assessing the DevSecMLOps lifecycle. A compact, explainable NLP model leaves enough time to demonstrate the security pipeline properly.

## Model artifact

The trained model is stored in:

```text
02_DEVELOP_BUILD/model/phishing_email_model.joblib
```

Metadata is stored in:

```text
02_DEVELOP_BUILD/model/model_metadata.json
```
