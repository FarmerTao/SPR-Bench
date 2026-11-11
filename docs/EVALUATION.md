# Evaluation protocol

## What a score means

SPR-Bench v0.5 measures executable analysis of synthetic SPR campaigns under
explicit project rules. Each of ten tasks receives a deterministic score in
[0, 1]; their unweighted mean is the benchmark score. A missing task counts as
zero. Reports are optional and unscored. See [SCORING.md](../SCORING.md) and
[RUBRICS.md](../RUBRICS.md) for formulas, caps and task-specific criteria.

A reference score of 1 verifies implementation consistency on these fixtures; it
is not an independently measured LLM result, proof of real-world generalization,
or evidence of clinical or drug-development utility. Tasks share code, contracts
and scientific motifs; they are not ten independent scientific modalities.

## Public versus blind evaluation

The repository publishes all three fixtures per task, generating code, truth and
reference solutions for reproducibility. Agent images include only the visible
campaign and public contract. Separate verifier images contain the other cases.
This protects a properly isolated trial from direct filesystem access, but cannot
undo prior model exposure to the repository.

Call results on this release **public-fixture evaluation**. A blind evaluation
requires separately held, versioned cases and reviewed labels, an explicit freeze
date, restricted access and a documented contamination policy. Merely changing
IDs or random seeds does not establish distributional generalization. The current
rebuild command recreates public fixtures; it is not a private-set service.

## Report a run

Record the repository commit, scoring version, task set, Harbor version, model
identifier and provider, agent version/configuration, date, prompts, tool access,
resource limits, retries, sampling settings and token/cost usage where available.
Disclose any access to reference solutions, rubric details or test fixtures.
Separate development attempts from evaluation attempts; do not report only the
best retry. Retain per-task scorecards, failures and logs with credentials removed.
For repeated trials, report every trial and the aggregation/uncertainty method.

Use `tools/summarize_scores.py` on `<root>/<task-slug>/scorecard.json`.
Keep run outputs outside version control. Docker/Harbor commands are documented
in the root README but remain unvalidated end to end in this release.

## Validation status

The checked-in validation files record trusted host runs: reference solutions,
score semantics, defective analyses and an optimizer alternative. The alternative
shares preprocessing with the reference. CI repeats these checks on Linux/Python
3.12. A green host CI does not establish container isolation or scientific validity.

Still required: container end-to-end trials, adversarial isolation review,
independent SPR expert review, blind agent baselines, real-data validation and
empirical difficulty calibration. No leaderboard or model superiority claims are
made by this release.
