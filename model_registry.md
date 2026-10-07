# Lightweight Model Registry

This project uses a simple file-based model registry because it is a mini practical project.

## Model record

`model_metadata.json` stores:

- version
- training timestamp
- algorithm
- classes
- test accuracy
- weighted F1
- dataset information
- model artifact SHA-256

## Why this matters

The application checks the model file hash during startup.

```text
model.joblib
     ↓
SHA-256
     ↓
compare with metadata
     ↓
match → start
mismatch → fail closed
```

## Production extension

A production system could move this into MLflow Model Registry, DVC, a signed model repository, or a managed artifact store.
