from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from datetime import datetime

from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = FastAPI(
    title="PulseOps Auth Service",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Prometheus Metrics
# -----------------------------
REQUEST_COUNT = Counter(
    "pulseops_requests_total",
    "Total API Requests"
)

CPU_USAGE = Gauge(
    "pulseops_cpu_usage_percent",
    "CPU Usage"
)

MEMORY_USAGE = Gauge(
    "pulseops_memory_usage_percent",
    "Memory Usage"
)

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    REQUEST_COUNT.inc()

    CPU_USAGE.set(32)
    MEMORY_USAGE.set(48)

    return {
        "service": "PulseOps Auth Service",
        "status": "running",
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

    CPU_USAGE.set(32)
    MEMORY_USAGE.set(48)

    return {
        "cpu_usage": 32,
        "memory_usage": 48,
        "requests": REQUEST_COUNT._value.get()
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from datetime import datetime
import requests

from prometheus_client import (
    Counter,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = FastAPI(
    title="PulseOps Auth Service",
    version="1.0.0"
)

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Prometheus Metrics
# ---------------------------------------------------

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

# ---------------------------------------------------
# Helper Function
# ---------------------------------------------------

PROMETHEUS_URL = "http://prometheus:9090/api/v1/query"


def query_prometheus(metric_name: str):

    try:

        response = requests.get(
            PROMETHEUS_URL,
            params={
                "query": metric_name
            },
            timeout=5,
        )

        result = response.json()

        if result["status"] == "success":

            data = result["data"]["result"]

            if len(data) > 0:
                return float(data[0]["value"][1])

    except Exception:
        pass

    return 0


# ---------------------------------------------------
# API Routes
# ---------------------------------------------------

@app.get("/")
def root():

    REQUEST_COUNT.inc()

    CPU_USAGE.set(32)
    MEMORY_USAGE.set(48)

    return {
        "service": "PulseOps Auth Service",
        "status": "running",
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
        media_type=CONTENT_TYPE_LATEST
    )