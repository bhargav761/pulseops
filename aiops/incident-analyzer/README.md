# PulseOps AI Incident Analyzer

Enterprise-grade AI-powered Incident Intelligence Platform built with FastAPI, Gemini AI, Prometheus and Loki.

---

## Features

- AI Incident Analysis
- Gemini AI Integration
- Prometheus Metrics Collection
- Loki Log Analysis
- SQLite Incident History
- Trend Analysis
- Autonomous Remediation (Simulation)
- Health Monitoring
- Structured Logging
- Request ID Middleware
- Docker Health Checks
- OpenAPI Documentation
- Unit Testing

---

## Tech Stack

- Python 3.12
- FastAPI
- Google Gemini API
- Prometheus
- Loki
- SQLite
- Docker
- GitHub Actions
- Ruff
- Bandit
- Pytest

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Application information |
| GET | /health | Service health |
| GET | /metrics | Monitoring metrics |
| POST | /analyze | AI incident analysis |
| GET | /summary | Executive summary |
| GET | /root-cause | Root cause analysis |
| POST | /remediate | AI remediation |
| GET | /automation-status | Automation capabilities |
| GET | /incidents | Incident history |
| GET | /trend-analysis | Incident trends |
| GET | /ai-status | AI integration status |

---

## Running Locally

```bash
pip install -r requirements.txt

uvicorn main:app --reload --port 8001