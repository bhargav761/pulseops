from incident_service import (
    get_all_incidents,
    get_incident_count,
    get_recent_incidents,
    get_severity_distribution,
)

# ==========================================================
# Incident Timeline
# ==========================================================

def get_incident_timeline():
    """
    Return all incidents ordered by timestamp.
    """

    return get_all_incidents()


# ==========================================================
# Recent Incidents
# ==========================================================

def get_recent_history(limit: int = 10):
    """
    Return recent incidents.
    """

    return get_recent_incidents(limit)


# ==========================================================
# Dashboard Summary
# ==========================================================

def get_dashboard_summary():
    """
    Return incident statistics.
    """

    return {
        "total_incidents": get_incident_count(),
        "severity_distribution": get_severity_distribution(),
    }


# ==========================================================
# Search Incidents
# ==========================================================

def search_incidents(keyword: str):
    """
    Search incidents by service, title or description.
    """

    keyword = keyword.lower()

    results = []

    for incident in get_all_incidents():

        service = (incident["service"] or "").lower()
        title = (incident["title"] or "").lower()
        description = (incident["description"] or "").lower()

        if (
            keyword in service
            or keyword in title
            or keyword in description
        ):
            results.append(incident)

    return results


# ==========================================================
# Filter by Severity
# ==========================================================

def filter_by_severity(severity: str):

    severity = severity.lower()

    return [
        incident
        for incident in get_all_incidents()
        if incident["severity"].lower() == severity
    ]


# ==========================================================
# Filter by Service
# ==========================================================

def filter_by_service(service: str):

    service = service.lower()

    return [
        incident
        for incident in get_all_incidents()
        if incident["service"].lower() == service
    ]