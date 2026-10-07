import os
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "02_DEVELOP_BUILD"))

os.environ["API_KEY"] = "test-api-key"
os.environ["AUTH_REQUIRED"] = "true"
os.environ["RATE_LIMIT_REQUESTS"] = "1000"

@pytest.fixture
def api_key():
    return "test-api-key"
