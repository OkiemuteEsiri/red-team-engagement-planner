# Engagement Methodology

## 1. Define the Business Objective

Start with the defensive question the exercise is meant to answer. Examples include validating telemetry coverage, analyst triage quality, identity monitoring, or remediation effectiveness. Technique selection follows the objective; it does not replace it.

## 2. Establish Rules of Engagement

Record:

- named business and security owners;
- start and end dates;
- explicit scope and environment;
- prohibited systems and actions;
- stop authority and escalation contacts;
- evidence-handling expectations;
- synthetic-data requirements;
- rollback and recovery expectations where relevant.

Unapproved assets remain blocked by design.

## 3. Map Defensive Validation to MITRE ATT&CK

Each allowed technique must include an objective and detection goal. ATT&CK is used as a common taxonomy for coverage communication, not as an instruction set for exploitation.

Example mappings in the synthetic exercise:

| Technique | Defensive purpose |
| --- | --- |
| T1078 Valid Accounts | Validate abnormal synthetic authentication detection |
| T1059.001 PowerShell | Validate process, command-line and script telemetry |
| T1021.001 RDP | Validate authorized remote-session monitoring |
| T1562.001 Impair Defenses | Explicitly excluded; retained for tabletop control discussion |

## 4. Evaluate Readiness

The planner evaluates authorization, safety controls, technique disposition and exclusions. Critical findings block execution. The score is a governance signal and must not replace human authorization.

## 5. Execute Only Through Separately Approved Test Procedures

This repository intentionally contains no offensive execution procedures. Any real exercise requires separately reviewed procedures, isolated or approved environments, named operators and live deconfliction.

## 6. Validate Detections

For every allowed technique, record whether expected telemetry was present, whether a detection fired, whether the alert contained sufficient context, and whether an analyst could reach the intended conclusion.

## 7. Remediate and Retest

A finding is not considered closed simply because a rule or control changed. The preferred lifecycle is:

`observe -> identify gap -> assign owner -> remediate -> repeat approved validation -> capture evidence -> close`

## 8. Report Outcomes

Report both technical and governance results: coverage achieved, blocked scenarios, unresolved safety issues, detection gaps, ownership, retest state and residual risk. Avoid presenting simulated activity as evidence of real-world compromise or professional experience.
