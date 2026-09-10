from dataclasses import dataclass, field
from typing import List

ALLOWED_RISK_LEVELS = {"low", "medium", "high", "critical"}
ALLOWED_STATUSES = {"planned", "approved", "in_progress", "paused", "completed", "cancelled"}


@dataclass(frozen=True)
class Technique:
    technique_id: str
    name: str
    tactic: str
    objective: str
    detection_goal: str
    allowed: bool = True

    def validate(self) -> None:
        if not self.technique_id.startswith("T"):
            raise ValueError("technique_id must be a MITRE ATT&CK technique identifier")
        if not self.name.strip() or not self.tactic.strip():
            raise ValueError("technique name and tactic are required")
        if not self.objective.strip() or not self.detection_goal.strip():
            raise ValueError("objective and detection_goal are required")


@dataclass(frozen=True)
class ScopeItem:
    asset: str
    environment: str
    owner: str
    approved: bool
    production: bool = False
    critical_service: bool = False

    def validate(self) -> None:
        if not self.asset.strip() or not self.environment.strip() or not self.owner.strip():
            raise ValueError("asset, environment, and owner are required")


@dataclass(frozen=True)
class SafetyControl:
    name: str
    description: str
    mandatory: bool = True
    implemented: bool = False


@dataclass(frozen=True)
class Engagement:
    engagement_id: str
    name: str
    business_owner: str
    security_owner: str
    start_date: str
    end_date: str
    status: str
    risk_level: str
    scope: List[ScopeItem] = field(default_factory=list)
    techniques: List[Technique] = field(default_factory=list)
    safety_controls: List[SafetyControl] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    exclusions: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.engagement_id.strip() or not self.name.strip():
            raise ValueError("engagement_id and name are required")
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f"unsupported status: {self.status}")
        if self.risk_level not in ALLOWED_RISK_LEVELS:
            raise ValueError(f"unsupported risk level: {self.risk_level}")
        if not self.business_owner.strip() or not self.security_owner.strip():
            raise ValueError("business_owner and security_owner are required")
        if not self.objectives:
            raise ValueError("at least one objective is required")
        for item in self.scope:
            item.validate()
        for technique in self.techniques:
            technique.validate()
