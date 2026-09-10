from .models import Engagement
from .planner import Assessment, execution_gate


def render_markdown(engagement: Engagement, assessment: Assessment) -> str:
    allowed, reasons = execution_gate(engagement, assessment)
    lines = [
        f"# Red Team Engagement Readiness Report — {engagement.name}",
        "",
        f"**Engagement ID:** {engagement.engagement_id}",
        f"**Status:** {engagement.status}",
        f"**Risk level:** {engagement.risk_level}",
        f"**Readiness score:** {assessment.readiness_score}/100",
        f"**Execution gate:** {'PASS' if allowed else 'BLOCKED'}",
        "",
        "## Objectives",
    ]
    lines.extend(f"- {objective}" for objective in engagement.objectives)
    lines.extend(["", "## Scope Summary", f"- Approved assets: {assessment.approved_assets}", f"- Unapproved assets: {assessment.blocked_assets}", f"- Allowed techniques: {assessment.allowed_techniques}", f"- Disallowed techniques: {assessment.blocked_techniques}"])
    if reasons:
        lines.extend(["", "## Execution Gate Reasons"])
        lines.extend(f"- {reason}" for reason in reasons)
    lines.extend(["", "## Findings"])
    if not assessment.findings:
        lines.append("No readiness findings identified.")
    for finding in assessment.findings:
        lines.extend([
            f"### {finding.finding_id} — {finding.title}",
            f"- Severity: **{finding.severity.upper()}**",
            f"- Category: {finding.category}",
            f"- Detail: {finding.detail}",
            f"- Remediation: {finding.remediation}",
            "",
        ])
    lines.extend(["## ATT&CK Validation Plan"])
    for technique in engagement.techniques:
        lines.append(f"- **{technique.technique_id} — {technique.name}** ({technique.tactic}): {technique.detection_goal} | {'Allowed' if technique.allowed else 'Excluded'}")
    lines.extend(["", "## Exclusions"])
    lines.extend(f"- {item}" for item in engagement.exclusions)
    lines.extend(["", "## Safety Statement", "This project plans authorized defensive validation only. It contains no exploit payloads, credential theft, persistence mechanisms, evasion tooling, production targeting, or command-and-control infrastructure."])
    return "\n".join(lines) + "\n"
