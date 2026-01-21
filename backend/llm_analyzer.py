# Deterministic fallback AI analyzer to guarantee schema-safe output
from dotenv import load_dotenv
from backend.models import IssueAnalysis

load_dotenv()

def analyze_issue(issue_data: dict):
    """
    MOCK AI ANALYZER (Deterministic & Reliable)
    Guarantees correct JSON output even without LLM access.
    """

    title = issue_data.get("title", "").lower()
    body = issue_data.get("body", "").lower()
# Heuristic-based detection of runtime errors and failures

    error_keywords = [
        "error", "exception", "cannot", "failed",
        "failure", "crash", "traceback", "runtime"
    ]

    if any(word in title for word in error_keywords) or any(word in body for word in error_keywords):
        issue_type = "bug"
        priority = 4
        labels = ["bug", "runtime-error"]
        impact = "May block execution or cause failures during runtime."
    else:
        issue_type = "feature_request"
        priority = 3
        labels = ["enhancement", "discussion"]
        impact = "Improves developer experience but does not block users."

    return IssueAnalysis(
        summary=issue_data.get("title", "GitHub issue analysis"),
        type=issue_type,
        priority_score=priority,
        suggested_labels=labels[:3],
        potential_impact=impact
    )
