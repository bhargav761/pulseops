import sys
from pathlib import Path

# Add aiops/incident-analyzer to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert "status" in body
    assert "services" in body