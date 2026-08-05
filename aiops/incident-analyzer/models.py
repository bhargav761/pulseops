from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

# ==========================================================
# Incident Request
# ==========================================================

class IncidentRequest(BaseModel):
    service: str = Field(..., example="backend")
    severity: str = Field(..., example="critical")
    message: str = Field(..., example="CrashLoopBackOff detected")


# ==========================================================
# Incident Record
# ==========================================================

class Incident(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    service: str
    severity: str
    title: str
    description: str
    root_cause: str
    recommendation: str
    status: str = "OPEN"


# ==========================================================
# AI Recommendation
# ==========================================================

class Recommendation(BaseModel):
    recommendation: str
    priority: str


# ==========================================================
# AI Analysis Response
# ==========================================================

class AIResponse(BaseModel):
    summary: str
    severity: str
    root_cause: str
    recommendations: List[str]


# ==========================================================
# Health Response
# ==========================================================

class HealthResponse(BaseModel):
    status: str
    services: dict


# ==========================================================
# Incident History
# ==========================================================

class IncidentHistory(BaseModel):
    total_incidents: int
    severity_distribution: dict
    incidents: List[Incident]