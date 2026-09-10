import json
from pathlib import Path

from .models import Engagement, SafetyControl, ScopeItem, Technique


def load_engagement(path: str | Path) -> Engagement:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"engagement_id", "name", "business_owner", "security_owner", "start_date", "end_date", "status", "risk_level", "objectives", "scope", "techniques", "safety_controls", "exclusions"}
    missing = sorted(required - payload.keys())
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    scope = [ScopeItem(**item) for item in payload["scope"]]
    techniques = [Technique(**item) for item in payload["techniques"]]
    controls = [SafetyControl(**item) for item in payload["safety_controls"]]

    engagement = Engagement(
        engagement_id=payload["engagement_id"],
        name=payload["name"],
        business_owner=payload["business_owner"],
        security_owner=payload["security_owner"],
        start_date=payload["start_date"],
        end_date=payload["end_date"],
        status=payload["status"],
        risk_level=payload["risk_level"],
        scope=scope,
        techniques=techniques,
        safety_controls=controls,
        objectives=payload["objectives"],
        exclusions=payload["exclusions"],
    )
    engagement.validate()
    return engagement
