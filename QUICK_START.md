# Quick Start — VS Code

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env

$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
python .\02_DEVELOP_BUILD\ml\train.py

# Terminal 1
$env:PYTHONPATH = ".\02_DEVELOP_BUILD"
uvicorn app.main:app --reload --port 8000

# Terminal 2
streamlit run .\02_DEVELOP_BUILD\dashboard\streamlit_app.py

# Tests
pytest -q .\03_TEST_VERIFY\tests
```

Then open:

```text
http://localhost:8501
```

## Docker

```powershell
docker compose up --build
```

Then open:

```text
http://localhost:8501
http://localhost:3000
```
