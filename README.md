# SPR-Bench

**An experimental-data pilot for executable SPR analysis in drug discovery.**

SPR-Bench v0.6 replaces the previous synthetic pilot with publicly released,
measured SPR data for small molecules or protein binders against protein targets.
It contains ten Harbor tasks drawn from five studies: STAT3, CYP3A4, LRRK2,
KLHDC2 and TBXT. There are **49 measured sensorgrams, 15 observed affinity
report points, and 23,040 TBXT report-point rows** in the canonical selected data.
No responses, concentrations, negative examples or replicates are simulated.

**Status:** public experimental-data pilot; local numerical and provenance checks
have passed. Harbor + Docker end-to-end evaluation, independent SPR expert
adjudication and actual agent baselines have not been completed. Do not treat this
as a validated drug-discovery benchmark or a difficulty-calibrated leaderboard.

## What the agent does

The agent reads measured CSV data and experimental scope, writes Python, and
submits a reusable analysis program. A separate verifier reruns it on two cases:
the visible data and a reordered/renamed subset of the same measured observations.
It checks numerical evidence, descriptive affinity fitting where appropriate,
input hashes and explicit scope constraints. Each task receives a score in [0,1].
No narrative report or LLM judge contributes to the score.

The current automatic score primarily measures reproducible data analysis.
**It does not independently validate binding/nonbinding ground truth, target
selectivity, clinical utility, or which molecule should enter development.**
The STAT3 paper supplies a scoped reported negative result; TBXT screening responses
and source-fitted affinity values are not independently adjudicated binder labels.
The STAT3 binding task includes a 20% structured call component scored against
the paper's scoped conclusions; those labels are not given in the agent input.
They remain public, author-reported interpretations, not independently reviewed
ground truth. Its reference program uses a study-specific association-slope
heuristic, not a validated general binding classifier. The 5% scope component
checks disclosed evidence limits, not hidden biological reasoning. More complete binding/advancement scoring requires expert-reviewed
labels and orthogonal evidence; this release does not manufacture those labels.

## Tasks

| Task | Study | Input | Rows |
|---|---|---|---:|
| [stat3-binding](tasks/stat3-binding/instruction.md) | STAT3 | trace | 7,262 |
| [stat3-flow](tasks/stat3-flow/instruction.md) | STAT3 | trace | 2,419 |
| [cyp3a4-sparse](tasks/cyp3a4-sparse/instruction.md) | CYP3A4 | trace | 12,770 |
| [cyp3a4-affinity](tasks/cyp3a4-affinity/instruction.md) | CYP3A4 | affinity | 8 |
| [lrrk2-traces](tasks/lrrk2-traces/instruction.md) | LRRK2 | trace | 48,314 |
| [lrrk2-affinity](tasks/lrrk2-affinity/instruction.md) | LRRK2 | affinity | 7 |
| [klhdc2-hits](tasks/klhdc2-hits/instruction.md) | KLHDC2 | trace | 54,626 |
| [klhdc2-analogs](tasks/klhdc2-analogs/instruction.md) | KLHDC2 | trace | 50,190 |
| [tbxt-reference](tasks/tbxt-reference/instruction.md) | TBXT | report | 23,040 |
| [tbxt-triage](tasks/tbxt-triage/instruction.md) | TBXT | report | 23,040 |

Tasks sharing a study are related views of the same experiments, not independent
studies. In particular STAT3 and TBXT task pairs overlap, and affinity endpoints
are not independent from the corresponding sensorgrams. Report per-task results
and a study-balanced aggregate; never inflate sample size by counting these as
independent experiments. See [evaluation protocol](docs/EVALUATION.md).

## Data provenance and rights

See [source catalogue](sources/README.md), [machine-readable source manifest](sources/manifest.json)
and [data manifest](data_manifest.json). Original source files are retained outside
agent images. Every extracted row records its original sheet/text member and row,
plus a measurement-column index where applicable. SHA-256 hashes protect both
originals and derived CSVs. The extraction code selects observed cells and converts
concentration units to M; it never smooths, interpolates or generates responses.

- STAT3: double-referenced measured curves for S3I-201 and 5,15-DPP; three flow rates
  are distinct conditions, not replicate experiments.
- CYP3A4: fluconazole curves and measured equilibrium points. Source `_Fit` and
  `FittedCurve` columns are excluded; sparse observed time grids are preserved.
- LRRK2: DARPin E11 curves and observed equilibrium points. Fitted curve and parameter
  columns are excluded from agent inputs.
- KLHDC2: only the SPR sheets for compounds 1, 2, 5 and 6. Neighboring fluorescence
  polarization assays are not mislabelled as SPR.
- TBXT: numerical report-point tables, not densely sampled sensorgrams. No kinetic
  rate fitting is requested from these data.

Code and benchmark-authored documentation are MIT licensed. Source data retain
their original CC BY / CC0 terms; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
Nucleic-acid hybridization and aptamer studies are outside this release's scope.
The old synthetic pilot is retained in Git history/tag `v0.5.0-synthetic`, not in
the active task set. Scores across these releases are not comparable.

## Quick start: trusted local checks

Use Python 3.12 (also tested locally with Python 3.13):

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python tools/check_repository.py
python tools/validate.py
```

`validate.py` executes only committed trusted reference programs. It checks every
selected measurement against its original source cell, runs ten tasks on both
cases, tests malformed/wrong submissions, and verifies two independent SciPy
curve-fit implementations against the affinity rubric. It is not a sandbox for
untrusted programs. Reports: [validation.json](validation.json) and
[scoring_validation.json](scoring_validation.json).

To reproduce the release from bundled originals:

```bash
python tools/ingest.py
python tools/build.py
python tools/docs.py
python tools/check_repository.py
python tools/validate.py
```

No download is needed to reproduce the selected data. Download URLs in the source
manifest are retained for attribution and independent retrieval. Changing source
bytes requires a new data version and hash review.

## Harbor evaluation

Tasks use Harbor **0.25.0** and schema 1.4. Each directory contains `instruction.md`,
`task.toml`, `environment/Dockerfile`, `solution/solve.sh` and `tests/test.sh`.
Agent containers receive data and the public contract only. Original workbooks,
reference solutions, expected outputs and scoring code are not in their build
contexts. Separate verifier containers receive the submitted `/app/submission`
artifact and rerun `run.py` without networking. Submission processes run as an
unprivileged user; trusted tests/logs are protected from that user.

With Docker running, the intended commands are:

```bash
harbor run --path tasks --agent oracle --n-concurrent 1
harbor run --path tasks --agent codex --model <provider/model> --n-concurrent 1
```

These commands/configurations have been schema checked, **not run end to end** in
this release. Verify artifact transfer and isolation before evaluating untrusted
submissions. A host validation score of 1 is not a model result.

## Scoring and limitations

[CONTRACT.md](CONTRACT.md) defines all output fields and tolerances.
[SCORING.md](SCORING.md) defines exact score formulas.
[RUBRICS.md](RUBRICS.md) gives each task's weights, subcriteria and evidence boundaries.
[QUESTIONS.md](QUESTIONS.md) provides the task questions in one place.
All fixtures and answers are public. Subsets test code reuse, not generalization
to a new laboratory, patient, instrument or chemical series.

Real response data alone do not establish label quality. Representative curves,
limited controls, unknown processing steps in some sources, rounded concentration
headers and unavailable independent repeats limit inference. Initial-window
summaries are explicitly defined numerical conventions, not confirmed association
phase annotation. Affinity fits are apparent descriptive estimates, not true
kinetic constants. No binary development-ready labels are supplied.

Contributions: [CONTRIBUTING.md](CONTRIBUTING.md).
Security: [SECURITY.md](SECURITY.md). Citation: [CITATION.cff](CITATION.cff).
