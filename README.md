# SPR-Bench

Agentic analysis of surface plasmon resonance data: from raw measurements to binding evidence, reportable kinetics and follow-up decisions.

[![Validate benchmark](https://github.com/FarmerTao/SPR-Bench/actions/workflows/validate.yml/badge.svg)](https://github.com/FarmerTao/SPR-Bench/actions/workflows/validate.yml)

**Research preview · synthetic data · 10 tasks · fully automatic scoring**

Version 0.5.0 — November 11, 2026. All task materials are in English.

This release **replaces the ten former component exercises** with ten integrated campaign-analysis tasks. No former basic task directories are included. Each task requires a reusable analysis program that reads multiple related experimental files, performs coupled calibration and quality assessment, estimates reportable parameters, and produces an auditable scientific decision.

All data are **synthetic**, with independently stored generating truth. These are research-workflow pilots, not expert-certified experimental tasks or a validated Terminal-Bench Science submission. Task difficulty has not been calibrated with blind LLM trials.

## Quick start: trusted local validation

```bash
git clone https://github.com/FarmerTao/SPR-Bench.git
cd SPR-Bench
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python tools/check_repository.py
python tools/test_scoring.py
python tools/validate.py
python tools/robustness.py
```

These commands validate trusted bundled programs on the host; they do not run an
LLM agent or provide a sandbox for unknown submissions. See **Running** below for
Harbor trials and [evaluation guidance](docs/EVALUATION.md) for reporting results.

## Repository map

| Path | Purpose |
|---|---|
| `tasks/` | Ten self-contained Harbor tasks, visible inputs, reference solutions and public test fixtures |
| `tools/` | Canonical generator, reference analysis, verifier, scoring and validation tools |
| `rubrics/` | Per-task Markdown and machine-readable scoring criteria |
| `SCORING.md`, `RUBRICS.md` | Shared scoring specification and task rubric index |
| `QUESTIONS.md`, `task_catalog.json` | Human-readable prompts and machine-readable task catalog |
| `data_manifest.json` | SHA-256 checksums of agent-visible data files |
| `docs/EVALUATION.md` | Contamination, reproducibility and interpretation guidance |
| `validation.json`, `robustness.json`, `scoring_validation.json` | Recorded host validation results |

## Tasks

| Task | Compounds per campaign | Main research objective |
|---|---:|---|
| Adjudicate an SPR Screening Campaign | 15 | Integrate mapping, calibration, controls, repeats, kinetics and follow-up decisions |
| Recover Binding Evidence from Solvent-Affected Runs | 15 | Separate recoverable binding from solvent and reference-surface responses |
| Audit the Reportability of Binding Kinetics | 16 | Distinguish supported rate estimates, unresolved dissociation, model inadequacy and conflicting repeats |
| Assess Flow-Dependent Binding Evidence | 16 | Compare three flow conditions and identify nonportable apparent kinetics |
| Resolve Model Inadequacy in a Binding Campaign | 16 | Audit a single-site reporting model against heterogeneous and unresolved responses |
| Recover a Campaign with Changing Surface Activity | 15 | Combine independently measured controls with normalization and batch-validity decisions |
| Reconcile Conflicting Replicate Measurements | 16 | Preserve and adjudicate conflicting repeats without cherry-picking |
| Reconstruct and Analyze an Acquisition Archive | 15 | Reconstruct indirect identifiers and mixed units from duplicated, unsorted exports, then complete scientific analysis |
| Repair a Faulty SPR Analysis Pipeline | 18 | Audit and repair a substantial legacy implementation with interacting scientific/software defects |
| Prioritize Orthogonal Validation from Campaign Evidence | 24 | Select a budget-limited shortlist from raw evidence with explicit exclusion reasons |

Each task has three campaign fixtures with different IDs, parameters, noise and acquisition values. The original campaign is agent-visible; two additional campaigns are verifier-only during a properly isolated trial. All campaigns use five concentrations and two independent replicate series. The condition-consistency task has three flows for every compound; flow-sensitive cases elsewhere also include three conditions. A common reporting contract lets the same scientific software serve several campaign objectives; the tasks are not ten independent scientific modalities.

[QUESTIONS.md](QUESTIONS.md) contains all English prompts. The authoritative detailed contract is in each task's environment/spec/CONTRACT.md.

## Inputs and tools

The sandbox provides Bash, Python, NumPy, SciPy, pandas and matplotlib. There is no prebuilt SPR solver, except for the intentionally faulty legacy code supplied in the repair task.

Each campaign includes:

- measurements.csv: raw active/reference time series.
- acquisition.csv: trace IDs, indirect sample keys, batch, concentration values and units, replicate, flow, injection end, and solvent offset.
- vials.csv and compounds.csv: two-stage sample identity mapping.
- blanks.csv: batch/time-matched blank measurements.
- solvent_calibration.csv: independent instrument solvent-calibration observations.
- controls.csv: independent positive-control activity measurements.
- RUN_NOTES.md: measurement conventions, instrument assumptions and acquisition context.
- project.json: explicit project-specific acceptance criteria and follow-up budget.

The integrated challenge is to propagate these records correctly through analysis. Missing a correction may still produce a smooth curve and a plausible fitted number. The research objective and scientific reporting conventions are supplied; individual compound diagnoses, generating parameters and private cases are not.

## Agent deliverables

Implement `/app/submission/run.py`, with optional helpers in the same directory:

```bash
python /app/submission/run.py --input-dir /app/data --output-dir /app/output
```

The program must accept fresh paths, create its output directory, and produce:

1. results.json: per-compound evidence calls, kinetic reportability, justified issues, reportable parameters or nulls, batch calibration/QC, and the shortlist.
2. trace_evidence.csv: an auditable trace-to-compound mapping, normalized corrected endpoints, reference-surface evidence, concentration and batch validity.
3. condition_fits.csv: condition-specific fits and residual errors for compounds reaching model assessment.
4. provenance.json: hashes of the actual input files.
5. report.md (optional, unscored): scientific method, findings and limitations for the author’s own audit.

Do not hardcode sample identities or outcomes. The verifier reruns the submitted code on three campaigns in fresh output directories. The code has 180 seconds per invocation, 2 CPUs, 4 GB RAM, one BLAS thread and no network. The agent has 3600 seconds to develop and test it.

## Task-specific rubric tables

See [RUBRICS.md](RUBRICS.md) for ten independent weight tables and atomic subcriteria, supplied in English Markdown and JSON. These administrator-facing files are not copied into the agent image. They expand the implemented scoring contract without changing previous scores.

## Fully automatic scoring

Each task receives a final score from **0 to 1**, and the benchmark score is the mean of the ten task scores (10% per task). All scoring is deterministic and automatic. **There is no report-review component or LLM judge. Reports are optional and never affect the score.**

See [SCORING.md](SCORING.md) for the complete executable specification: all ten weight rows, every submetric and denominator, parameter partial-credit formulas, numerical tolerances, missing-output rules, critical-error caps, worked examples and output schemas. [scoring_weights.json](scoring_weights.json) provides machine-readable weights. The nine automatic components are mapping, correction, QC, binding, reportability, quantification, fit consistency, decisions, and execution/provenance; their task-specific weights sum to 100%.

The verifier writes the same fractional score to reward.txt and scorecard.json. Category achievements and contributions are included in the scorecard. metrics.json and ctrf.json provide detailed diagnostics; all_checks_passed is supplementary and does not replace the graded score. No human assessment is required to finish a run. Harbor consumers that display only binary success should consume scorecard.json for fractional results; this is a custom scoring track, not a claim of compliance with Terminal-Bench Science's binary-reward submission policy.

```bash
python tools/summarize_scores.py --scorecards-root PATH_TO_TASK_LOG_DIRECTORIES --output benchmark_score.json
```

Input layout is `<root>/<task-slug>/scorecard.json`. Missing tasks are recorded and count as zero, without reweighting the remaining tasks. Historical manual assessments are not used in v0.5. Changing the scale and weights does not make the experimental cases more difficult.

## Ground truth and scientific limits

`tools/build.py` writes private truth from the generating parameters and case construction **before** the solver runs. The reference program consumes the public measurements; it does not generate its own expected kinetic values or labels. Trace truth is independently computed during measurement generation.

The verifier reconstructs model residuals directly from stored raw observations, blank measurements and private generating calibration/activity values. The implementation differs from the reference preprocessing code, but both are authored in this package; no independent scientist has reviewed either.

Synthetic challenges include differential solvent effects, reference adsorption, activity variation, invalid controls, replicate disagreement, unresolved slow dissociation, flow-dependent apparent rates and heterogeneous responses. They are not a comprehensive mechanistic simulation of a commercial instrument. In particular, flow dependence is represented by different apparent rate constants, not a transport PDE. The tasks assess consistency and reportability, not proof of aggregation, binding-site count or a unique transport mechanism.

Advancement means eligibility for orthogonal follow-up under the stated project rules. It does not establish functional efficacy, druglikeness or clinical utility. Real-data performance must be measured separately.

## Environment and verifier isolation

Each task uses the Harbor layout:

```text
instruction.md
task.toml
environment/
  Dockerfile
  requirements.txt
  data/
  spec/CONTRACT.md
  legacy/analyze.py          # Repair task only
solution/
  solve.sh
  run.py
tests/
  Dockerfile
  test.sh
  verifier.py
  cases/0..2/
    data/
    truth.json
    trace_truth.csv
```

The configuration uses schema 1.4 with `environment_mode="separate"` and exports only `/app/submission`. The agent image copies only environment data/specifications and the intentionally faulty code where applicable. The verifier image contains pristine test inputs and truth, with no network. Within that image, submitted programs run under uid/gid 65534 with a writable temporary output directory and restricted access to test materials. This is an isolation design, **not a completed container integration or security audit**.

Only trusted reference, alternative and deliberately defective programs were run locally. Do not use the local harness to execute untrusted submissions on the host. Before public evaluation, test artifact transfer, image construction, privilege dropping and the entire Harbor trial in Docker. The authoring machine does not have Docker.

Public release of the package exposes its test fixtures to anyone downloading it. For genuine blind evaluation, generate and keep private additional campaigns and rotate them under a versioned evaluation protocol. Do not mount the repository, generators, solutions or tests into the agent sandbox.

## Running

Install Docker and start its daemon. Commands below assume this directory is the working directory:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt

# Containerized reference trial; not yet exercised by the package author:
.venv/bin/harbor run -p tasks -a oracle

# No-operation baseline:
.venv/bin/harbor run -p tasks -a nop

# Replace placeholders with a supported terminal-capable agent and model:
.venv/bin/harbor run -p tasks -a <agent-name> -m <provider/model-name>
```

The image uses Python 3.12.10 and pinned NumPy 2.2.6, SciPy 1.15.3, pandas 2.2.3 and matplotlib 3.10.3. Image tags are not digest-pinned. Build-time dependency downloads require internet; task execution does not.

## Rebuilding and validation

```bash
.venv/bin/python tools/rebuild.py
```

This regenerates synthetic campaigns, checks the reference workflow against all generating-truth fixtures, tests defective analyses and a legitimate optimizer alternative, and refreshes the catalog, questions and checksum manifest.

Local validation uses Python 3.13.5, Harbor 0.25.0, NumPy 2.2.6 and SciPy 1.15.3. See validation.json and robustness.json for measured results. The alternate optimizer shares preprocessing with the reference and is not an independently authored full scientific analysis.

Not completed: Docker execution, privilege-isolation testing, actual LLM trials, expert review, real-data integration, or calibration of research difficulty. The package is ready for those next validation steps, not evidence that those steps succeeded.

## Design references

The design draws on [Terminal-Bench Science's proposal rubric](https://github.com/harbor-framework/terminal-bench-science/blob/main/rubrics/task-proposal.md), [implementation rubric](https://github.com/harbor-framework/terminal-bench-science/blob/main/rubrics/task-implementation.toml), and its [navigation calibration](https://github.com/harbor-framework/terminal-bench-science/blob/main/tasks/engineering-sciences/electrical-engineering/navigation-sensor-calibration/instruction.md) and [nanoindentation](https://github.com/harbor-framework/terminal-bench-science/blob/main/tasks/physical-sciences/materials-science/nanoindentation-property-extraction/instruction.md) tasks. No third-party benchmark data or task answers are copied into these campaigns.

## Contributing, license and citation

See [CONTRIBUTING.md](CONTRIBUTING.md) for source/generated-file conventions and
required checks, [SECURITY.md](SECURITY.md) for execution boundaries, and
[CHANGELOG.md](CHANGELOG.md) for version history. Open issues for reproducible
scientific or scoring defects; pull requests are welcome.

Original code, documentation and generated synthetic fixtures are distributed
under the [MIT License](LICENSE). Third-party dependencies retain their own
licenses. No external experimental dataset is bundled. Use [CITATION.cff](CITATION.cff)
and include the exact commit when citing an evaluation. There is no associated
peer-reviewed paper or independently validated leaderboard at this stage.
