import json
import tempfile
import unittest
from pathlib import Path

from src.io import load_engagement
from src.models import Engagement, SafetyControl, ScopeItem, Technique
from src.planner import assess_engagement, execution_gate
from src.reporting import render_markdown


class PlannerTests(unittest.TestCase):
    def healthy_engagement(self) -> Engagement:
        return Engagement(
            engagement_id="RT-TEST-001",
            name="Synthetic Exercise",
            business_owner="Business Owner",
            security_owner="Security Engineering",
            start_date="2026-10-01",
            end_date="2026-10-02",
            status="approved",
            risk_level="medium",
            scope=[ScopeItem("lab-01", "isolated-lab", "Platform", True)],
            techniques=[Technique("T1078", "Valid Accounts", "Initial Access", "Validate identity telemetry", "Correlate synthetic sign-in telemetry", True)],
            safety_controls=[SafetyControl("Named authorization", "Written approval", True, True)],
            objectives=["Validate detection coverage"],
            exclusions=["Production systems"],
        )

    def test_healthy_plan_passes_gate(self):
        engagement = self.healthy_engagement()
        assessment = assess_engagement(engagement)
        allowed, reasons = execution_gate(engagement, assessment)
        self.assertTrue(allowed)
        self.assertEqual([], reasons)
        self.assertEqual(100, assessment.readiness_score)

    def test_unapproved_asset_blocks_execution(self):
        base = self.healthy_engagement()
        engagement = Engagement(**{**base.__dict__, "scope": [ScopeItem("lab-01", "lab", "Platform", False)]})
        assessment = assess_engagement(engagement)
        allowed, reasons = execution_gate(engagement, assessment)
        self.assertFalse(allowed)
        self.assertIn("unapproved assets remain in scope", reasons)

    def test_missing_mandatory_control_is_critical(self):
        base = self.healthy_engagement()
        engagement = Engagement(**{**base.__dict__, "safety_controls": [SafetyControl("Stop authority", "Immediate stop", True, False)]})
        assessment = assess_engagement(engagement)
        self.assertTrue(any(f.severity == "critical" for f in assessment.findings))

    def test_no_controls_is_critical(self):
        base = self.healthy_engagement()
        engagement = Engagement(**{**base.__dict__, "safety_controls": []})
        assessment = assess_engagement(engagement)
        self.assertTrue(any(f.title == "No safety controls defined" for f in assessment.findings))

    def test_disallowed_technique_is_counted(self):
        base = self.healthy_engagement()
        techniques = list(base.techniques) + [Technique("T1562.001", "Impair Defenses", "Defense Evasion", "Tabletop only", "Review tamper telemetry", False)]
        assessment = assess_engagement(Engagement(**{**base.__dict__, "techniques": techniques}))
        self.assertEqual(1, assessment.blocked_techniques)

    def test_planned_status_blocks_gate(self):
        base = self.healthy_engagement()
        engagement = Engagement(**{**base.__dict__, "status": "planned"})
        assessment = assess_engagement(engagement)
        allowed, reasons = execution_gate(engagement, assessment)
        self.assertFalse(allowed)
        self.assertIn("engagement status is not approved for execution", reasons)

    def test_finding_ids_are_deterministic(self):
        base = self.healthy_engagement()
        engagement = Engagement(**{**base.__dict__, "exclusions": []})
        first = assess_engagement(engagement).findings[0].finding_id
        second = assess_engagement(engagement).findings[0].finding_id
        self.assertEqual(first, second)

    def test_invalid_technique_id_fails_validation(self):
        base = self.healthy_engagement()
        engagement = Engagement(**{**base.__dict__, "techniques": [Technique("BAD", "Test", "Test", "Goal", "Detection", True)]})
        with self.assertRaises(ValueError):
            assess_engagement(engagement)

    def test_loader_rejects_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"engagement_id": "x"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_engagement(path)

    def test_report_contains_gate_and_attack_plan(self):
        engagement = self.healthy_engagement()
        assessment = assess_engagement(engagement)
        report = render_markdown(engagement, assessment)
        self.assertIn("**Execution gate:** PASS", report)
        self.assertIn("T1078", report)
        self.assertIn("ATT&CK Validation Plan", report)


if __name__ == "__main__":
    unittest.main()
