# SPR-Bench

**An experimental-data pilot for executable protein/antibody SPR analysis.**

SPR-Bench v0.8 has two tiers, both in the
[Terminal-Bench-Science](https://github.com/harbor-framework/terminal-bench-science)
task format (Harbor, separate no-network verifier, binary reward, canary strings):

- **Core tier** (`tasks/`): ten measured-data tasks with fully specified
  analysis contracts, for internal evaluation and RL rollouts.
- **TB-Science track** (`tbsci/`): `spr-kinetic-triage`, an expert-level raw
  multi-cycle kinetics task on simulated data with exact latent truth, staged
  for submission to Terminal-Bench-Science. It is a separately named simulation
  track and is never pooled with core-tier scores.

The core tier is a protein/antibody SPR set with two binding-assessment
tasks. It contains ten Harbor tasks drawn from six studies: LRRK2/DARPin,
designed macrocycles, ISG65/C3, D-box peptides, STAT3, and TBXT. There are **55
measured sensorgrams, 57 observed affinity endpoints, 23,040 TBXT report-point
rows, and two binding/non-binding tasks** in the canonical selected data. No core-tier
responses, concentrations, negative examples or replicates are simulated.

**Status:** public experimental-data pilot; local numerical and provenance checks
have passed. Harbor + Docker end-to-end evaluation, independent SPR expert
adjudication and actual agent baselines have not been completed. Do not treat this
as a validated drug-discovery benchmark or a difficulty-calibrated leaderboard.

## What the agent does

The agent reads measured CSV data and experimental scope, writes Python, and
submits a reusable analysis program. A separate verifier reruns it on two cases:
the visible data and a reordered/renamed subset of the same measured observations.
It checks numerical evidence, descriptive affinity fitting where appropriate,
input hashes and explicit scope constraints. The reward is binary: 1 only if
every pytest check passes on both cases. Per-category partial scores are kept in
`metrics.json` (`partial_reward`, `analysis_reward`) for diagnostics and reward
shaping, never as the headline score. No narrative report or LLM judge
contributes to the score.

The core tier primarily measures reproducible data analysis under an explicit
contract; it is not calibrated to Terminal-Bench-Science difficulty.

## Running agents

```bash
pip install harbor==0.25.0
harbor run -p tasks -a oracle            # expect reward 1 on every task
harbor run -p tasks -a nop               # expect reward 0 on every task
harbor run -p tasks -a claude-code -m <provider/model> -k 5 -n 4
harbor run -p tbsci/tasks/life-sciences/biology/spr-kinetic-triage -a oracle
```

Report pass@1 as the mean binary reward over all k trials per task, plus
per-task pass counts. For RL rollouts, the binary reward is the
default signal; `analysis_reward` from `metrics.json` may be used for shaping
but must not be reported as a benchmark score.

## Tasks

| Task | Study | Input | Rows |
|---|---|---|---:|
| [stat3-binding](tasks/stat3-binding/instruction.md) | STAT3 | trace | 7,262 |
| [tbxt-binding](tasks/tbxt-binding/instruction.md) | TBXT | report | 23,040 |
| [lrrk2-traces](tasks/lrrk2-traces/instruction.md) | LRRK2 | trace | 48,314 |
| [lrrk2-affinity](tasks/lrrk2-affinity/instruction.md) | LRRK2 | affinity | 7 |
| [macrocycle-traces](tasks/macrocycle-traces/instruction.md) | Macrocycle | trace | 7,669 |
| [isg65-c3b-traces](tasks/isg65-c3b-traces/instruction.md) | ISG65 | trace | 5,425 |
| [isg65-c3d-traces](tasks/isg65-c3d-traces/instruction.md) | ISG65 | trace | 5,425 |
| [isg65-affinity](tasks/isg65-affinity/instruction.md) | ISG65 | affinity | 36 |
| [dbox-d20-affinity](tasks/dbox-d20-affinity/instruction.md) | D-box | affinity | 7 |
| [dbox-d21-affinity](tasks/dbox-d21-affinity/instruction.md) | D-box | affinity | 7 |

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
```

## Design and evidence boundaries

The six studies provide measured protein/peptide/antibody SPR data:

- **STAT3 binding**: DPP and S3I-201 across three flow conditions; the task also
  requires a per-compound binding assessment. The author-scoped calls are
  S3I-201 interaction-supported and DPP no-measurable-response in this construct;
  they are not universal binder labels. **TBXT operational binding**: corrected
  late-binding report points are classified with a disclosed 10 RU threshold;
  the labels are a triage rule, not author binding truth.
- **LRRK2/DARPin E11**: seven concentration series and seven equilibrium
  endpoints. The protein binder is a DARPin; catalytic inhibition is not
  established by SPR.
- **Designed macrocycles**: three single-concentration sensorgrams for designed
  macrocyclic binders. The source-fitted curves are excluded; a single trace does
  not establish a KD.
- **ISG65/C3**: six sheets of measured cycles for WT, ΔL2 and L2N188A ISG65
  binding C3b and C3d. The ISG65 affinity task uses the measured response at the
  end of the 120 s association phase from each trace; this derived endpoint is
  documented in sources/README.md.
- **D-box peptides**: D20 and D21 observed isotherms across the reported
  concentration series. Source-fitted curves are excluded; the paired
  sensorgrams remain in the source file but are not task inputs.

All response values are experimental. Source-fitted curves, simulated negatives,
digitized images and fabricated concentrations are not included. The task
contract distinguishes measured response summaries from fitted affinity
parameters; neither establishes a biological mechanism, selectivity or drug
readiness.

## Limitations

- **Two binding tasks, different label authority.** STAT3 uses author-scoped
  calls restricted to the tested construct/conditions. TBXT uses a disclosed
  operational 10 RU threshold on corrected report points; it is a triage rule,
  not author-reported binding truth. The other eight tasks are protein/peptide
  trace or affinity analyses.
- **Uneven study coverage.** LRRK2 contributes two tasks, ISG65 three, D-box
  two, and Macrocycle/STAT3/TBXT one each. The recommended overall score is the
  mean of the ten task scores, and study means are descriptive.
- **Single-concentration traces.** The Macrocycle task cannot establish KD; its
  disclosed claims say so.
- **Derived ISG65 endpoints.** The ISG65 affinity endpoints are measured cells at
  a fixed time, not source-reported equilibrium fits. See sources/README.md.
- **No cluster-disjoint split, expert adjudication, agent baseline or
  Docker/Harbor end-to-end run yet.**
- **Core-tier answers are public.** Expected outputs live in this repository, so
  core-tier agents run without network access, unlike Terminal-Bench-Science.

## Source attribution

See [sources/README.md](sources/README.md) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Original files are unmodified;
CSV conversion, selected measured cells, unit conversion, opaque identifiers and
robustness subsets are the only changes.

## Citation

Cite the original studies and this repository. Third-party data retain their
source licenses; no endorsement by the original authors is implied.
