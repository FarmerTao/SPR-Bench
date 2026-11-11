# Changelog

## Open-source packaging — 2026-11-11

- Publish SPR-Bench with tasks at the repository root.
- Add MIT licensing, software citation, contribution and evaluation guidance.
- Add pinned development dependencies and Linux/Python 3.12 CI.
- Add read-only dataset, rubric and implementation integrity checks.
- Make scoring-document generation idempotent, removing duplicated prompt footers.
- Preserve v0.5 data and scientific scoring behavior.

## 0.5.0 — 2026-11-11

- Score every task automatically on a 0–1 scale; the benchmark score is the mean of ten task scores.
- Remove report-review points. Reports are optional and do not affect scores.
- Provide ten separate rubrics in Markdown and JSON, with task-specific weights, atomic criteria, denominators and partial-credit rules.
- Share the verifier and scoring primitives across tasks while retaining each task's scientific emphasis.
- Document numerical tolerances, missing-output handling and critical-error caps in SCORING.md.
- Include regression checks for report independence, partial credit, invalid outputs and benchmark aggregation.

The tasks use synthetic data. Docker end-to-end execution, independent expert review and blind LLM trials remain pending.
