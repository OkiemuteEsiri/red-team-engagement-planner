# Red Team Engagement Planner

A defensive control-plane for planning **authorized red-team and adversary-emulation exercises**. The project demonstrates how engagement scope, ATT&CK coverage, safety controls, execution gates, remediation, and retesting can be modeled as code without embedding offensive payloads or live exploitation logic.

## Problem Statement

Red-team exercises fail operationally when authorization, scope, deconfliction, safety controls, detection objectives, or stop conditions are ambiguous. This project turns those governance requirements into deterministic, reviewable artifacts that can be assessed locally and in CI.

## What This Repository Demonstrates

- Security engineering for red-team governance and rules of engagement
- MITRE ATT&CK-aligned defensive validation planning
- Explicit asset authorization and scope controls
- Safety-control enforcement and fail-closed execution gating
- Deterministic readiness findings and repeatable scoring
- Detection-goal mapping for approved techniques
- Remediation and retest workflow design
- Synthetic-data handling and evidence minimization
- Unit-tested Python security logic
- Least-privilege GitHub Actions CI

## Architecture

```text
Synthetic/approved engagement JSON
            |
            v
      Validation layer
       src/io.py
            |
            v
  Engagement domain model
      src/models.py
            |
            v
 Readiness assessment engine
     src/planner.py
      /           \
     v             v
Execution gate   Findings + score
     |             |
     +------v------+
            |
            v
   Markdown reporting
   src/reporting.py
            |
            v
 reports/readiness-report.md
```

See [`docs/architecture.md`](docs/architecture.md) for trust boundaries and extension points.

## Repository Structure

```text
.
├── .github/workflows/ci.yml
├── data/
│   └── synthetic-engagement.json
├── docs/
│   ├── architecture.md
│   └── methodology.md
├── reports/
│   └── example-readiness-report.md
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── io.py
│   ├── models.py
│   ├── planner.py
│   └── reporting.py
└── tests/
    └── test_planner.py
```

## Readiness Controls

The assessment engine evaluates whether an engagement is ready to proceed. Key checks include:

| Control | Risk when absent | Gate behavior |
| --- | --- | --- |
| Named approved scope | Unauthorized activity | Blocks when unapproved assets remain |
| Mandatory safety controls | Operational / business impact | Critical finding and block |
| Approved engagement status | Governance failure | Blocks |
| Explicit exclusions | Ambiguous operator boundaries | Medium finding |
| ATT&CK-aligned techniques | Poor validation traceability | High finding when absent |
| Detection goals | Weak blue-team validation value | Finding |
| Critical production-service exposure | Elevated business impact | High finding requiring heightened controls |

The execution gate requires all of the following:

1. status is `approved` or `in_progress`;
2. no unapproved assets remain;
3. no critical readiness findings remain; and
4. readiness score is at least 80.

A passing gate is **not** a substitute for human authorization.

## MITRE ATT&CK Mapping

The included synthetic engagement maps approved defensive validation goals to:

- **T1078 — Valid Accounts**: abnormal synthetic authentication monitoring
- **T1059.001 — PowerShell**: benign process, command-line, and script telemetry validation
- **T1021.001 — Remote Desktop Protocol**: authorized remote-session telemetry validation
- **T1562.001 — Impair Defenses**: explicitly excluded from execution and retained only for tabletop control discussion

ATT&CK is used as a taxonomy for coverage and detection communication, not as an exploitation guide.

## Usage

Requires Python 3.11+ and no third-party packages.

```bash
python -m unittest discover -s tests -v
python -m src.cli data/synthetic-engagement.json --report reports/readiness-report.md
```

The CLI returns exit code `0` when the policy gate passes and `2` when the plan is blocked, making it suitable for CI policy enforcement.

## Example Outcome

The supplied synthetic engagement includes two approved lab assets, three allowed validation techniques, one explicitly excluded technique, named owners, deconfliction, stop authority, synthetic identities/data, and evidence-handling controls. It produces a high readiness score while preserving the excluded technique as a documented governance item.

See [`reports/example-readiness-report.md`](reports/example-readiness-report.md).

## Methodology

The engagement lifecycle is:

```text
Business objective
      -> Rules of engagement
      -> Scope authorization
      -> ATT&CK + detection goals
      -> Safety/readiness assessment
      -> Human approval
      -> Separately approved validation procedure
      -> Detection review
      -> Remediation
      -> Retest
      -> Closure with evidence
```

See [`docs/methodology.md`](docs/methodology.md) for the full workflow.

## Risk Classification

Readiness findings use four severity levels:

- **Critical** — conditions that make execution unsafe or unauthorized
- **High** — material scope or production-safety concerns
- **Medium** — governance, exclusion, or technique-disposition gaps
- **Low** — minor hygiene issues

The score is intentionally transparent and deterministic. It is a planning aid, not a quantitative measure of enterprise breach likelihood.

## Remediation and Validation Workflow

Findings are designed to be closed through control correction and reassessment, not narrative acceptance alone. Examples:

- unapproved asset -> remove from scope or obtain explicit authorization -> reassess;
- missing stop authority -> establish named stop authority -> reassess;
- undefined detection goal -> map expected telemetry and owner -> reassess;
- prohibited technique -> retain as excluded or remove from the execution plan.

The preferred closure lifecycle is:

`observe -> assign -> remediate -> reassess -> capture evidence -> close`

## CI/CD Security Checks

The GitHub Actions workflow uses read-only repository permissions and performs:

- Python bytecode compilation;
- unit-test discovery and execution;
- validation of the synthetic engagement through the same CLI used locally.

CI configuration is intentionally dependency-light to reduce supply-chain exposure.

## Limitations

- This repository does not perform exploitation or adversary execution.
- It does not replace legal review, executive authorization, change management, or operational deconfliction.
- The readiness score is policy-oriented, not an empirical probability of compromise.
- Date strings are recorded but not yet validated against a calendar library.
- Approval signatures and evidence integrity are modeled conceptually rather than cryptographically.
- ATT&CK technique coverage is illustrative and synthetic.

## Safety Boundaries

This project contains no:

- credential theft or password cracking;
- phishing infrastructure;
- persistence mechanisms;
- defense-evasion payloads;
- command-and-control infrastructure;
- destructive actions;
- denial-of-service logic;
- production targeting;
- real credentials, confidential employer data, or client data.

## Skills Demonstrated

**Red Teaming:** engagement design, scope control, ATT&CK mapping, rules of engagement, deconfliction, stop conditions  
**Security Engineering:** policy-as-code, deterministic controls, safe failure modes, validation gates  
**Detection Engineering:** technique-to-detection-goal mapping, telemetry validation planning  
**Incident Response:** escalation, stop authority, evidence minimization, operational coordination  
**DevSecOps:** testable security controls, CI policy gates, least-privilege workflows  
**Python:** dataclasses, validation, deterministic identifiers, CLI design, reporting, unit testing

## Roadmap

- JSON Schema enforcement
- structured exception and expiry handling
- ATT&CK Navigator layer export
- evidence-reference model with integrity metadata
- detection-owner and telemetry-source mapping
- approval/signature workflow
- richer remediation status tracking
- machine-readable SARIF or JSON findings export
- policy profiles for lab, staging, and production-adjacent exercises

## Portfolio Positioning

This repository is intended as a recruiter-facing example of how red-team programs can be engineered with strong authorization, safety, detection validation, and remediation discipline. All scenarios and data are synthetic and should not be interpreted as evidence of activity against real organizations.
