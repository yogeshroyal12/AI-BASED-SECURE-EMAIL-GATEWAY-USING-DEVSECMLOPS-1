Write-Host "Starting Secure Email Gateway in VS Code..." -ForegroundColor Cyan

if (-not (Test-Path ".\.venv")) {
    py -3.11 -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

if (-not (Test-Path ".\.env")) {
    Copy-Item .env.example .env
}

$env:PYTHONPATH = ".\02_DEVELOP_BUILD"

Write-Host "Training model..." -ForegroundColor Yellow
python .\02_DEVELOP_BUILD\ml\train.py

Write-Host "Starting FastAPI on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Open another terminal for Streamlit:"
Write-Host "streamlit run .\02_DEVELOP_BUILD\dashboard\streamlit_app.py"

uvicorn app.main:app --reload --port 8000
