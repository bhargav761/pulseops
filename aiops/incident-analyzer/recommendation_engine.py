"""
PulseOps Recommendation Engine

Generates rule-based recommendations for common infrastructure
and Kubernetes incidents.
"""

from typing import List


def generate_recommendations(
    service: str,
    severity: str,
    message: str,
) -> List[str]:
    """
    Return remediation recommendations based on
    severity and incident message.
    """

    recommendations = []

    message = message.lower()
    severity = severity.lower()

    # =====================================================
    # Kubernetes
    # =====================================================

    if "crashloopbackoff" in message:
        recommendations.extend(
            [
                "Restart the affected deployment.",
                "Check application logs for startup failures.",
                "Verify ConfigMaps and Secrets.",
                "Inspect recent deployment changes.",
            ]
        )

    if "imagepullbackoff" in message:
        recommendations.extend(
            [
                "Verify container image name.",
                "Check image registry credentials.",
                "Confirm image exists in registry.",
            ]
        )

    if "pending" in message:
        recommendations.extend(
            [
                "Check node resource availability.",
                "Verify scheduler events.",
                "Inspect taints and tolerations.",
            ]
        )

    # =====================================================
    # Infrastructure
    # =====================================================

    if "cpu" in message:
        recommendations.extend(
            [
                "Scale application replicas.",
                "Investigate high CPU processes.",
                "Review recent deployments.",
            ]
        )

    if "memory" in message:
        recommendations.extend(
            [
                "Increase memory limits.",
                "Investigate memory leaks.",
                "Restart affected workload.",
            ]
        )

    if "disk" in message:
        recommendations.extend(
            [
                "Clean unnecessary logs.",
                "Remove unused Docker images.",
                "Increase storage capacity.",
            ]
        )

    if "network" in message:
        recommendations.extend(
            [
                "Verify network connectivity.",
                "Check firewall rules.",
                "Inspect Kubernetes Services and Ingress.",
            ]
        )

    # =====================================================
    # Severity
    # =====================================================

    if severity == "critical":
        recommendations.insert(
            0,
            "Escalate immediately to the SRE/DevOps team.",
        )

    elif severity == "high":
        recommendations.insert(
            0,
            "Investigate the incident as soon as possible.",
        )

    elif severity == "medium":
        recommendations.insert(
            0,
            "Monitor the service closely.",
        )

    else:
        recommendations.insert(
            0,
            "Continue monitoring the service.",
        )

    # =====================================================
    # Default Recommendation
    # =====================================================

    if not recommendations:
        recommendations.append(
            "No predefined recommendation available."
        )

    return recommendations