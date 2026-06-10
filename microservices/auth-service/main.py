from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title="PulseOps Auth Service",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "service": "PulseOps Auth Service",
        "status": "running",
        "timestamp": str(datetime.utcnow())
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }