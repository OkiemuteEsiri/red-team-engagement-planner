from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable, List

from .models import Engagement, SafetyControl, ScopeItem, Technique


@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    category: str
    title: str
    detail: str
    remediation: str


@dataclass(frozen=True)
class Assessment:
    engagement_id: str
    readiness_score: int
    findings: List[Finding]
    approved_assets: int
    blocked_assets: int
    allowed_techniques: int
    blocked_techniques: int


def _finding_id(engagement_id: str, category: str, title: str) -> str:
    digest = sha256(f"{engagement_id}|{category}|{title}".encode()).hexdigest()[:10]
    return f"RT-{digest.upper()}"


def _finding(engagement: Engagement, severity: str, category: str, title: str, detail: str, remediation: str) -> Finding:
    return Finding(_finding_id(engagement.engagement_id, category, title), severity, category, title, detail, remediation)


def assess_engagement(engagement: Engagement) -> Assessment:
    engagement.validate()
    findings: List[Finding] = []

    approved_assets = sum(1 for item in engagement.scope if item.approved)
    blocked_assets = len(engagement.scope) - approved_assets
    allowed_techniques = sum(1 for technique in engagement.techniques if technique.allowed)
    blocked_techniques = len(engagement.techniques) - allowed_techniques

    if not engagement.scope:
        findings.append(_finding(engagement, "critical", "scope", "No authorized scope", "No assets are present in the engagement scope.", "Define named assets, owners, environments and approval state before execution."))

    if blocked_assets:
        findings.append(_finding(engagement, "high", "scope", "Unapproved assets present", f"{blocked_assets} scope item(s) are not approved.", "Keep unapproved assets technically blocked and obtain explicit authorization before use."))

    prod_critical = [item.asset for item in engagement.scope if item.production and item.critical_service]
    if prod_critical:
        findings.append(_finding(engagement, "high", "safety", "Critical production services in scope", f"Critical production assets require heightened controls: {', '.join(prod_critical)}.", "Require executive risk acceptance, narrowed techniques, monitoring, rollback and immediate stop authority."))

    missing_controls = [control.name for control in engagement.safety_controls if control.mandatory and not control.implemented]
    if missing_controls:
        findings.append(_finding(engagement, "critical", "safety", "Mandatory safety controls missing", f"Not implemented: {', '.join(missing_controls)}.", "Implement every mandatory safety control before changing status to approved or in_progress."))

    if not engagement.safety_controls:
        findings.append(_finding(engagement, "critical", "safety", "No safety controls defined", "The engagement has no explicit safety-control record.", "Define deconfliction, monitoring, stop conditions, communications and evidence handling controls."))

    if blocked_techniques:
        findings.append(_finding(engagement, "medium", "technique", "Disallowed techniques retained in plan", f"{blocked_techniques} technique(s) are explicitly disallowed.", "Keep disallowed techniques excluded from execution artifacts and document the rationale."))

    if not engagement.techniques:
        findings.append(_finding(engagement, "high", "technique", "No ATT&CK-aligned techniques defined", "No technique-level validation goals are recorded.", "Map approved test objectives to ATT&CK techniques and a defensive detection or validation goal."))

    missing_detection_goals = [t.technique_id for t in engagement.techniques if t.allowed and not t.detection_goal.strip()]
    if missing_detection_goals:
        findings.append(_finding(engagement, "medium", "detection", "Detection goals missing", f"Missing for: {', '.join(missing_detection_goals)}.", "Define expected telemetry, detection ownership and validation criteria for each allowed technique."))

    if not engagement.exclusions:
        findings.append(_finding(engagement, "medium", "governance", "No explicit exclusions", "The rules of engagement do not record exclusions.", "Document prohibited systems, actions, data classes and business processes."))

    weights = {"critical": 25, "high": 15, "medium": 8, "low": 3}
    penalty = sum(weights[f.severity] for f in findings)
    readiness = max(0, 100 - penalty)

    return Assessment(
        engagement_id=engagement.engagement_id,
        readiness_score=readiness,
        findings=findings,
        approved_assets=approved_assets,
        blocked_assets=blocked_assets,
        allowed_techniques=allowed_techniques,
        blocked_techniques=blocked_techniques,
    )


def execution_gate(engagement: Engagement, assessment: Assessment) -> tuple[bool, List[str]]:
    reasons: List[str] = []
    if engagement.status not in {"approved", "in_progress"}:
        reasons.append("engagement status is not approved for execution")
    if assessment.blocked_assets:
        reasons.append("unapproved assets remain in scope")
    if any(f.severity == "critical" for f in assessment.findings):
        reasons.append("critical readiness findings remain open")
    if assessment.readiness_score < 80:
        reasons.append("readiness score is below 80")
    return (not reasons, reasons)
