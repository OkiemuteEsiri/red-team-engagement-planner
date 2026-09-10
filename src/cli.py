import argparse
from pathlib import Path

from .io import load_engagement
from .planner import assess_engagement, execution_gate
from .reporting import render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess an authorized red-team engagement plan")
    parser.add_argument("engagement", help="Path to engagement JSON")
    parser.add_argument("--report", default="reports/readiness-report.md", help="Markdown output path")
    args = parser.parse_args()

    engagement = load_engagement(args.engagement)
    assessment = assess_engagement(engagement)
    output = Path(args.report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(engagement, assessment), encoding="utf-8")
    allowed, reasons = execution_gate(engagement, assessment)
    print(f"readiness_score={assessment.readiness_score}")
    print(f"execution_gate={'PASS' if allowed else 'BLOCKED'}")
    if reasons:
        print("reasons=" + "; ".join(reasons))
    return 0 if allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
