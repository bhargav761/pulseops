import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_incidents():

    response = client.get("/incidents")

    assert response.status_code == 200


def test_trend_analysis():

    response = client.get("/trend-analysis")

    assert response.status_code == 200

    body = response.json()

    assert "total_incidents" in body
    assert "severity_distribution" in body