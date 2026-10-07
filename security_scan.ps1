Write-Host "=== DevSecMLOps Local Security Scan ===" -ForegroundColor Cyan

if (-not $env:PYTHONPATH) {
    $env:PYTHONPATH = ".\02_DEVELOP_BUILD"
}

Write-Host "`n[1] Tests" -ForegroundColor Yellow
pytest -q .\03_TEST_VERIFY\tests

Write-Host "`n[2] SAST - Bandit" -ForegroundColor Yellow
bandit -r .\02_DEVELOP_BUILD\app -ll

Write-Host "`n[3] SCA - pip-audit" -ForegroundColor Yellow
pip-audit -r requirements.txt

Write-Host "`n[4] Secret Scan - Gitleaks" -ForegroundColor Yellow
gitleaks detect --source .

Write-Host "`n[5] Docker Build" -ForegroundColor Yellow
docker build -t secure-email-gateway .

Write-Host "`n[6] Container Scan - Trivy" -ForegroundColor Yellow
trivy image secure-email-gateway

Write-Host "`nDone." -ForegroundColor Green
