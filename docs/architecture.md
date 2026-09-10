# Architecture

## Purpose

This project is a control-plane for planning authorized red-team and adversary-emulation exercises. It intentionally separates engagement governance from any offensive execution tooling.

## Components

1. `src/models.py` — immutable domain objects for engagements, scope, ATT&CK techniques and safety controls.
2. `src/io.py` — fail-closed JSON ingestion and schema-level validation.
3. `src/planner.py` — readiness findings, deterministic IDs, scoring and the execution gate.
4. `src/reporting.py` — human-readable Markdown reporting for security and business stakeholders.
5. `src/cli.py` — offline command-line entry point suitable for CI and local review.
6. `data/` — synthetic engagement records only.
7. `tests/` — unit coverage for authorization, safety, validation and reporting behavior.

## Data Flow

`engagement JSON -> validation -> readiness assessment -> execution gate -> Markdown report`

The execution gate is deliberately conservative. An engagement is blocked when:

- status is not `approved` or `in_progress`;
- an unapproved asset remains in scope;
- any critical readiness finding remains open; or
- readiness score is below 80.

## Trust Boundaries

The repository does not perform network access, exploitation, credential collection, payload generation, persistence, evasion or command-and-control. All input is local JSON and all output is local Markdown.

## Determinism

Finding identifiers are derived from engagement ID, category and title using SHA-256 truncation. This makes repeated assessments comparable without introducing external state.

## Extension Points

Future safe extensions can add:

- JSON Schema validation;
- structured exception records with expiry;
- evidence references and approval signatures;
- ATT&CK Navigator export;
- detection-control ownership mapping;
- signed readiness snapshots;
- CI policy gates for engagement-plan pull requests.
