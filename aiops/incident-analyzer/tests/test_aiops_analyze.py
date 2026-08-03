import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch("main.generate_ai_analysis", new_callable=AsyncMock)
def test_analyze_endpoint(mock_generate):

    mock_generate.return_value = {
        "summary": "Mock AI analysis",
        "root_cause": "Mock root cause",
        "severity": "CRITICAL",
        "recommendations": [
            "Restart deployment",
            "Check logs",
            "Inspect metrics",
        ],
    }

    payload = {
        "service": "backend",
        "severity": "critical",
        "message": "CrashLoopBackOff detected",
    }

    response = client.post("/analyze", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert body["summary"] == "Mock AI analysis"
    assert body["severity"] == "CRITICAL"
    assert len(body["recommendations"]) > 0