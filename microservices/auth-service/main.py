from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from datetime import datetime
import os
import requests

from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------

app = FastAPI(
    title="PulseOps Auth Service",
    version="1.0.0"
)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Prometheus Metrics
# ----------------------------------------------------

REQUEST_COUNT = Counter(
    "pulseops_requests_total",
    "Total API Requests"
)

CPU_USAGE = Gauge(
    "pulseops_cpu_usage_percent",
    "CPU Usage Percentage"
)

MEMORY_USAGE = Gauge(
    "pulseops_memory_usage_percent",
    "Memory Usage Percentage"
)

# ----------------------------------------------------
# Environment Variables
# ----------------------------------------------------

PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://prometheus:9090/api/v1/query"
)

# ----------------------------------------------------
# Helper Function
# ----------------------------------------------------

def query_prometheus(query: str):
    try:
        response = requests.get(
            PROMETHEUS_URL,
            params={"query": query},
            timeout=5
        )

        result = response.json()

        if result["status"] == "success":
            data = result["data"]["result"]

            if data:
                return float(data[0]["value"][1])

    except Exception as e:
        print("Prometheus Error:", e)

    return 0

# ----------------------------------------------------
# Routes
# ----------------------------------------------------

@app.get("/")
def root():

    REQUEST_COUNT.inc()

    return {
        "service": "PulseOps Auth Service",
        "status": "running",
        "version": "1.0.0",
        "timestamp": str(datetime.utcnow())
    }


@app.get("/health")
def health():

    REQUEST_COUNT.inc()

    return {
        "status": "healthy"
    }


@app.get("/dashboard-metrics")
def dashboard_metrics():

    REQUEST_COUNT.inc()

    cpu = query_prometheus(
        '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
    )

    memory = query_prometheus(
        '100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))'
    )

    requests_count = query_prometheus(
        "pulseops_requests_total"
    )

    return {
        "cpu_usage": round(cpu, 2),
        "memory_usage": round(memory, 2),
        "requests": int(requests_count)
    }


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )