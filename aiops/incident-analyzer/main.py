import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import google.generativeai as genai
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from logging_config import logger
from pydantic import BaseModel

# ==================================================
# Load Environment Variables
# ==================================================

load_dotenv()

# ==================================================
# SQLite Database
# ==================================================

DB_PATH = Path("pulseops.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")

conn.commit()

# ==================================================
# Environment Variables
# ==================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://localhost:9090",
)
LOKI_URL = os.getenv(
    "LOKI_URL",
    "http://localhost:3100",
)

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found in .env"
    )

# ==================================================
# Gemini
# ==================================================

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==================================================
# FastAPI
# ==================================================

app = FastAPI(
    title="PulseOps AI Incident Analyzer",
    description="""
Enterprise-grade AI-powered AIOps platform.

## Features

- AI Incident Analysis (Gemini)
- Prometheus Metrics Integration
- Loki Log Analysis
- Incident History (SQLite)
- Trend Analysis
- Autonomous Remediation (Simulation)
- Kubernetes Observability

Developed as part of the PulseOps platform.
""",
    version="4.0.0",
    contact={
        "name": "Bhargava R",
        "url": "https://github.com/bhargav761",
    },
    license_info={
        "name": "MIT License",
    },
)
# ==================================================
# Request ID Middleware
# ==================================================

@app.middleware("http")
async def add_request_id(request: Request, call_next):

    request_id = str(uuid.uuid4())

    logger.info(
        f"Request ID={request_id} Method={request.method} Path={request.url.path}"
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response

# ==================================================
# Models
# ==================================================

class Incident(BaseModel):
    service: str
    severity: str
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "service": "backend",
                "severity": "critical",
                "message": "CrashLoopBackOff detected",
            }
        }
    }


class LogRequest(BaseModel):
    logs: List[str]


class AIResponse(BaseModel):
    summary: str
    root_cause: str
    severity: str
    recommendations: List[str]


class RemediationResponse(BaseModel):
    incident: str
    recommended_action: str
    automation_possible: bool
    commands: List[str]
    risk_level: str

# ==================================================
# Health
# ==================================================

@app.get(
    "/",
    tags=["General"],
    summary="Application information",
    description="Returns basic information about the PulseOps AI Incident Analyzer service.",
)
def home():
    return {
        "project": "PulseOps",
        "service": "AI Incident Analyzer",
        "version": "4.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Service health check",
    description=(
        "Checks the health of the AI Incident Analyzer and its "
        "dependencies including SQLite, Gemini AI, Prometheus and Loki."
    ),
)
async def health():

    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {},
    }

    # ... rest of your function ...

    # -----------------------------
    # Database
    # -----------------------------
    try:
        cursor.execute("SELECT 1")
        health_status["services"]["database"] = "connected"
    except Exception:
        health_status["services"]["database"] = "disconnected"
        health_status["status"] = "degraded"

    # -----------------------------
    # Gemini
    # -----------------------------
    health_status["services"]["gemini"] = (
        "configured" if GEMINI_API_KEY else "missing"
    )

    # -----------------------------
    # Prometheus
    # -----------------------------
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{PROMETHEUS_URL}/-/healthy")

        if response.status_code == 200:
            health_status["services"]["prometheus"] = "reachable"
        else:
            health_status["services"]["prometheus"] = "unreachable"
            health_status["status"] = "degraded"

    except Exception:
        health_status["services"]["prometheus"] = "offline"
        health_status["status"] = "degraded"

    # -----------------------------
    # Loki
    # -----------------------------
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{LOKI_URL}/ready")

        if response.status_code == 200:
            health_status["services"]["loki"] = "reachable"
        else:
            health_status["services"]["loki"] = "unreachable"
            health_status["status"] = "degraded"

    except Exception:
        health_status["services"]["loki"] = "offline"
        health_status["status"] = "degraded"

    return health_status

# ==================================================
# Prometheus Client
# ==================================================

async def query_prometheus(query: str) -> Dict[str, Any]:

    url = f"{PROMETHEUS_URL}/api/v1/query"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            url,
            params={"query": query},
        )

        response.raise_for_status()

        return response.json()

# ==================================================
# Loki Client
# ==================================================

async def query_loki(query: str) -> Dict[str, Any]:

    url = f"{LOKI_URL}/loki/api/v1/query"

    async with httpx.AsyncClient(timeout=10) as client:

        response = await client.get(
            url,
            params={"query": query},
        )

        response.raise_for_status()

        return response.json()

# ==================================================
# Database Helpers
# ==================================================

def save_incident(incident: Incident) -> None:
    """Save an incident to SQLite."""

    cursor.execute(
        """
        INSERT INTO incidents (
            service,
            severity,
            message,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            incident.service,
            incident.severity,
            incident.message,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()


def fetch_incidents(limit: int = 20):

    cursor.execute(
        """
        SELECT
            id,
            service,
            severity,
            message,
            created_at
        FROM incidents
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "service": row[1],
            "severity": row[2],
            "message": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]

# ==================================================
# Monitoring
# ==================================================

async def collect_monitoring_data() -> Dict[str, Any]:
    """
    Collect metrics from Prometheus and logs from Loki.
    """

    metrics = {}

    # -----------------------------
    # Prometheus Metrics
    # -----------------------------
    try:
        metrics["cpu"] = await query_prometheus(
            '100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
        )

        metrics["memory"] = await query_prometheus(
            '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100'
        )

        metrics["pods"] = await query_prometheus("up")

    except Exception as exc:
        logger.error(f"Prometheus Error: {exc}")
        metrics["prometheus_error"] = str(exc)

    # -----------------------------
    # Loki Logs
    # -----------------------------
    try:
        metrics["logs"] = await query_loki('{job="varlogs"}')

    except Exception as exc:
        logger.error(f"Loki Error: {exc}")
        metrics["loki_error"] = str(exc)

    return metrics

# ==================================================
# Gemini AI
# ==================================================

async def generate_ai_analysis(
    incident: Incident,
    monitoring_data: Dict[str, Any],
) -> AIResponse:

    prompt = f"""
You are an expert Kubernetes SRE.

Analyze this production incident.

Service:
{incident.service}

Severity:
{incident.severity}

Message:
{incident.message}

Monitoring Data:
{monitoring_data}

Provide:

1. Executive Summary

2. Root Cause

3. Final Severity

4. Five remediation recommendations.

Keep the response concise.
"""

    try:

        response = gemini_model.generate_content(prompt)

        text = response.text

        recommendations = []

        for line in text.splitlines():

            line = line.strip()

            if (
                line.startswith("-")
                or line.startswith("*")
                or line[:2].isdigit()
            ):
                recommendations.append(
                    line.lstrip("-*0123456789. ").strip()
                )

        if not recommendations:

            recommendations = [
                "Inspect Kubernetes events.",
                "Review Prometheus alerts.",
                "Review Loki logs.",
                "Verify latest deployment.",
                "Restart unhealthy pods if required.",
            ]

        return AIResponse(
            summary=text,
            root_cause="Generated by Gemini AI",
            severity=incident.severity.upper(),
            recommendations=recommendations[:5],
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Gemini Error: {exc}",
        )


# ==================================================
# Trend Analysis
# ==================================================

def get_trend_analysis():

    cursor.execute(
        """
        SELECT
            severity,
            COUNT(*)
        FROM incidents
        GROUP BY severity
        """
    )

    rows = cursor.fetchall()

    total = sum(row[1] for row in rows)

    return {
        "total_incidents": total,
        "severity_distribution": {
            row[0]: row[1]
            for row in rows
        },
    } 
# ==================================================
# API Endpoints
# ==================================================

@app.get(
    "/metrics",
    tags=["Monitoring"],
    summary="Get monitoring metrics",
    description="Collect metrics from Prometheus and logs from Loki.",
)
async def metrics():
    """Return current monitoring data."""
    return await collect_monitoring_data()


@app.post(
    "/analyze",
    response_model=AIResponse,
    tags=["AI"],
    summary="Analyze production incident",
    description="Analyze production incidents using Gemini AI, Prometheus metrics and Loki logs.",
)
async def analyze(incident: Incident):
    """Analyze an incident using Gemini AI."""

    # Save incident
    save_incident(incident)

    logger.info(
        f"New incident received | Service={incident.service} | Severity={incident.severity}"
    )

    # Collect monitoring data
    monitoring_data = await collect_monitoring_data()

    # Generate AI response
    return await generate_ai_analysis(
        incident,
        monitoring_data,
    )


@app.get(
    "/incidents",
    tags=["Incidents"],
    summary="Get recent incidents",
    description="Return recently analyzed incidents stored in SQLite.",
)
def incidents():
    """Return recent incidents."""
    return fetch_incidents()


@app.get(
    "/trend-analysis",
    tags=["Incidents"],
    summary="Incident trend analysis",
    description="Return severity distribution and incident statistics.",
)
def trend_analysis():
    """Return incident statistics."""
    return get_trend_analysis()


@app.get(
    "/summary",
    tags=["AI"],
    summary="Generate executive summary",
    description="Generate an executive health summary using Gemini AI.",
)
async def summary():

    monitoring_data = await collect_monitoring_data()

    prompt = f"""
Summarize the current health of this Kubernetes platform.

Monitoring Data:

{monitoring_data}

Write a concise executive summary.
"""

    response = gemini_model.generate_content(prompt)

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "summary": response.text,
    }


@app.get(
    "/root-cause",
    tags=["AI"],
    summary="Root cause analysis",
    description="Identify the most probable root cause using Gemini AI.",
)
async def root_cause():

    monitoring_data = await collect_monitoring_data()

    prompt = f"""
Based on the following monitoring information,
identify the most probable root cause.

Monitoring Data:

{monitoring_data}

Return:

Root Cause
Impact
Confidence
"""

    response = gemini_model.generate_content(prompt)

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "analysis": response.text,
    }


@app.post(
    "/remediate",
    response_model=RemediationResponse,
    tags=["Automation"],
    summary="Recommend remediation",
    description="Generate AI-powered remediation recommendations for incidents.",
)
async def remediate(incident: Incident):

    prompt = f"""
You are an expert Kubernetes SRE.

Incident

Service:
{incident.service}

Severity:
{incident.severity}

Description:
{incident.message}

Recommend ONE remediation.
"""

    response = gemini_model.generate_content(prompt)

    return RemediationResponse(
        incident=incident.message,
        recommended_action=response.text.strip(),
        automation_possible=True,
        commands=[
            f"kubectl rollout restart deployment/{incident.service}",
            f"kubectl describe deployment {incident.service}",
            f"kubectl get pods -l app={incident.service}",
        ],
        risk_level="MEDIUM",
    )


@app.get(
    "/automation-status",
    tags=["Automation"],
    summary="Automation status",
    description="Show available automation capabilities.",
)
def automation_status():

    return {
        "mode": "Simulation",
        "auto_execute": False,
        "supported_actions": [
            "Restart Deployment",
            "Scale Deployment",
            "Restart Pod",
            "Describe Deployment",
            "View Logs",
        ],
    }


@app.get(
    "/ai-status",
    tags=["Health"],
    summary="AI integration status",
    description="Verify Gemini AI, Prometheus, Loki and database configuration.",
)
def ai_status():

    return {
        "gemini": bool(GEMINI_API_KEY),
        "database": str(DB_PATH),
        "prometheus": PROMETHEUS_URL,
        "loki": LOKI_URL,
        "version": "4.0.0",
    }