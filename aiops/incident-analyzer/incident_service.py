
from database import execute_query, fetch_all, fetch_one
from models import Incident

# ==========================================================
# Create Incident
# ==========================================================

def create_incident(incident: Incident) -> int:
    """Insert a new incident into the database."""

    query = """
    INSERT INTO incidents (
        timestamp,
        service,
        severity,
        title,
        description,
        root_cause,
        recommendation,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    return execute_query(
        query,
        (
            incident.timestamp.isoformat(),
            incident.service,
            incident.severity,
            incident.title,
            incident.description,
            incident.root_cause,
            incident.recommendation,
            incident.status,
        ),
    )


# ==========================================================
# Get Incident By ID
# ==========================================================

def get_incident(incident_id: int):
    """Return a single incident."""

    query = """
    SELECT *
    FROM incidents
    WHERE id = ?
    """

    return fetch_one(query, (incident_id,))


# ==========================================================
# Get All Incidents
# ==========================================================

def get_all_incidents():
    """Return all incidents."""

    query = """
    SELECT *
    FROM incidents
    ORDER BY timestamp DESC
    """

    return fetch_all(query)


# ==========================================================
# Update Incident Status
# ==========================================================

def update_status(incident_id: int, status: str):
    """Update incident status."""

    query = """
    UPDATE incidents
    SET status = ?
    WHERE id = ?
    """

    execute_query(query, (status, incident_id))


# ==========================================================
# Delete Incident
# ==========================================================

def delete_incident(incident_id: int):
    """Delete an incident."""

    query = """
    DELETE FROM incidents
    WHERE id = ?
    """

    execute_query(query, (incident_id,))


# ==========================================================
# Recent Incidents
# ==========================================================

def get_recent_incidents(limit: int = 10):
    """Return the most recent incidents."""

    query = """
    SELECT *
    FROM incidents
    ORDER BY timestamp DESC
    LIMIT ?
    """

    return fetch_all(query, (limit,))


# ==========================================================
# Incident Count
# ==========================================================

def get_incident_count():
    """Return total number of incidents."""

    query = """
    SELECT COUNT(*) AS total
    FROM incidents
    """

    row = fetch_one(query)

    return row["total"] if row else 0


# ==========================================================
# Severity Distribution
# ==========================================================

def get_severity_distribution():
    """Return incident counts grouped by severity."""

    query = """
    SELECT severity, COUNT(*) AS total
    FROM incidents
    GROUP BY severity
    """

    rows = fetch_all(query)

    return {row["severity"]: row["total"] for row in rows}