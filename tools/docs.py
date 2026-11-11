import json
from pathlib import Path
from ingest import ROOT


def main():
    catalog = json.loads((ROOT / "task_catalog.json").read_text())
    manifest = json.loads((ROOT / "sources/manifest.json").read_text())
    data = json.loads((ROOT / "data_manifest.json").read_text())
    table = "| Task | Study | Input | Rows |\n|---|---|---|---:|\n" + "\n".join(
        f"| [{x['id']}](tasks/{x['id']}/instruction.md) | {x['study']} | {x['kind']} | {x['rows']:,} |"
        for x in catalog
    )
    (ROOT / "README.md").write_text(
        """# SPR-Bench

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

"""
        + table
        + """

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
"""
    )
    questions = "# Task questions\n\nAll tasks use measured experimental data. See [contract](CONTRACT.md) for required program outputs.\n\n"
    rubrics = "# Task-specific automatic rubrics\n\nEvery task is scored from 0 to 1. No report points are awarded.\n\n"
    for x in catalog:
        questions += f"## {x['id']}: {x['title']}\n\n{x['question']}\n\nSource study: {x['study']}; input: `{x['source_file']}`; {x['rows']:,} selected rows.\n\n"
        cfg = json.loads((ROOT / "tasks" / x["id"] / "tests/scoring.json").read_text())
        rubrics += f"## {x['id']}\n\n{x['question']}\n\n| Component | Weight | Automatic criterion |\n|---|---:|---|\n"
        for cat, w in cfg["weights"].items():
            desc = ", ".join("`" + f + "`" for f in cfg["fields"].get(cat, []))
            if cat == "coverage":
                desc = "Exact record-ID coverage; " + desc
            if cat == "provenance":
                desc = "Exact SHA-256 map of every supplied input file."
            if cat == "binding_evidence":
                desc = "Exact compound coverage and scoped binding calls compared with Mtwebana and Prinsloo (2020), DOI 10.1186/s13104-020-05189-w. Author-reported interpretation; not independent adjudication."
            if cat == "scope":
                desc = "Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth."
            rubrics += f"| {cat} | {w:.0%} | {desc} |\n"
        rubrics += "\nAll checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.\n\n"
    (ROOT / "QUESTIONS.md").write_text(questions.rstrip() + "\n")
    (ROOT / "RUBRICS.md").write_text(rubrics.rstrip() + "\n")
    (ROOT / "SCORING.md").write_text(
        """# Automatic scoring v0.6

Every task has its own score in [0,1]. Both cases contain real observations.
For case c, category k, let m(c,k) be passed checks / expected checks, or zero if
there are no checks. The case score is sum_k w(k)*m(c,k). The task score is the
arithmetic mean of its two case scores. Every task has weights summing to 1.

| Task type | Coverage | Response / fit | Provenance | Disclosed scope | Binding evidence |
|---|---:|---:|---:|---:|---:|
| Trace (except STAT3 binding) and TBXT triage | 20% | 65% | 10% | 5% | 0% |
| STAT3 binding | 15% | 50% | 10% | 5% | 20% |
| Affinity | 15% | 70% | 10% | 5% | 0% |
| TBXT reference audit | 25% | 60% | 10% | 5% | 0% |

For N expected records and F coverage fields, coverage contains 1 + N*F checks:
one exact ID-set check and one check per expected record/field. Response contains
N*R checks for R response fields. Provenance has one check. Scope has one check
per disclosed claim. STAT3 binding evidence has one exact compound-coverage
check plus one check for each source-supported scoped call. These labels are
withheld from the agent image, but public in the repository and source article.
No weighting depends on the amount of optional prose.
See RUBRICS.md for exact fields and weights for each of ten tasks.

Missing output, invalid JSON, duplicate JSON keys/record IDs, nonfinite JSON,
program failure or timeout gives that case zero. Missing fields/records fail
corresponding checks. An entirely empty record list can earn only provenance and
scope credit (at most 0.15); STAT3 binding can additionally earn up to 0.20
for source-consistent calls even if numerical evidence is absent. This partial
credit does not constitute successful numerical analysis. Unexpected record
IDs fail exact coverage. Null matches only a documented null reference value.
Counts must match exactly. All numerical tolerances are in CONTRACT.md.

The reference numbers are recomputed from selected measurements, not synthesized
kinetic truth. Measured source fit curves are excluded. Apparent KD fits use a
specified least-squares model; the score does not claim this is the true biological
mechanism. The disclosed scope component is intentionally easy and should be
reported separately when comparing scientific analysis ability.

Report all ten task scores and study means. The recommended overall score is the
mean of five study means (each study has two tasks in this release, so this equals
the ten-task mean). A missing task counts as zero. Do not treat ten tasks or the
two robustness cases as independent biological replicates. Do not pool scores
with the archived synthetic version or with later scoring versions.

The STAT3 call rubric uses author-reported scoped conclusions for the tested
compounds, construct and conditions (DOI
10.1186/s13104-020-05189-w). It does not assert universal nonbinding, selectivity,
or suitability for development. No independent expert adjudication is claimed.

All fixtures, reference outputs and source papers are public. This is a public
fixture evaluation; it is not a blind assessment. Local oracle scores and scoring
regression tests measure implementation consistency, not model capability or
scientific label validity. No manually graded report or model-as-judge is used.
"""
    )
    lines = "# Source catalogue and extraction notes\n\nFive studies; six bundled source files. Accessed 2026-11-11. These are measured experimental data, with source preprocessing retained.\n\n"
    for s in manifest:
        lines += f"## {s['source']} — {Path(s['file']).name}\n\n{s['authors']}. [Primary source]({s['doi']}); [original download]({s['download_url']}).\n\nLicense: {s['license']}. Bytes: {s['bytes']:,}. SHA-256: `{s['sha256']}`.\n\n"
    lines += """## Exact selection and evidence boundaries

- STAT3: the three nonempty sheets in Additional file 1; numerical TIME and three
  flow-rate response columns. Blank cells are omitted per trace. Article methods
  specify double referencing. S3I-201 interaction and DPP lack of measurable
  response are author-reported conclusions restricted to mouse STAT3beta core
  residues 127–722 and tested conditions. They are not universal binding labels.
- CYP3A4: `SPR titration sheet 1`, columns 1–9 (time and eight observations); and
  observed cells in columns 2–9 of `SPR titration sheet 2`. Exclude `_Fit` and
  `FittedCurve`. Trace concentration headers are rounded (e.g. 0.78 µM), whereas
  endpoint concentrations retain their exported precision. Do not equate these
  two representations without allowing for the source rounding.
- LRRK2: ZIP members `Sensorgrams_E11.txt` and first two columns of
  `Steady state_E11.txt`. Seven concentration series, 7.8125–500 nM. Source-fitted
  parameters and curve columns are retained only in the original archive, never
  provided to agents. Original authors report apparent KD 70.3 nM; this is a
  comparison, not a gold-standard truth label. This release's specified unweighted
  free-offset refit yields about 104 nM rather than 70.3 nM; the exported source
  parameter is not used as the scoring target. Do not infer catalytic inhibition
  from the SPR data alone.
- KLHDC2: Figure 2E/2F and Figure 3F/3G only, corresponding to compounds 1/2 and
  5/6. These are representative SPR traces; other worksheets contain orthogonal
  fluorescence-polarization data and are excluded. Do not invent sensorgrams for
  the compounds for which the article reports no robust SPR signal.
- TBXT: `Report point table`, rows with Step purpose=Analysis, preserving original
  compound names and replicate/series suffixes. Relative responses, windows,
  concentrations, reference types and source row indices are retained. Selected
  workbook is `20201028 LMW binding affinity screen for 136 UNC and Piramal
  compounds.xlsx`. It supplies numeric report points and embedded sensorgram
  images, not a usable numeric full-time-series export. Source-fitted kinetic/
  affinity tables are excluded from input. Response values do not supply an
  independently validated 136-compound binder/nonbinder ground truth.

CSV conversion, selected sheets/columns, unit conversion, omitted empty cells,
row ordering and robustness-case ID aliases are the only changes. No smoothing,
interpolation, digitized images, simulated negatives, fabricated concentrations,
synthetic replicates or source-fitted curves enter measurements.csv.

No pathogen targets, nucleic-acid hybridization or aptamer cases are included.
Original data licenses apply to originals and extracted subsets. Preserve author,
source and license attribution when redistributing. License links are in
THIRD_PARTY_NOTICES.md. All inclusion decisions and limitations are public; the
source catalogue is not a blinded label set.
"""
    (ROOT / "sources/README.md").write_text(lines)
    (ROOT / "THIRD_PARTY_NOTICES.md").write_text(
        """# Third-party data notices

The repository MIT license applies to code and benchmark-authored documentation,
not to third-party experimental data. Original and extracted data retain their
source terms. Attribution and exact source URLs are in sources/README.md and
sources/manifest.json.

| Data | Attribution | Terms |
|---|---|---|
| STAT3 | S. S. Mtwebana and E. Prinsloo (2020) | [CC0 data waiver](https://creativecommons.org/publicdomain/zero/1.0/); article [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| CYP3A4/nanodiscs | T. G. J. Knetsch, M. Ubbink, H. van Son, M. Kobayashi and contributors (2025) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| LRRK2/E11 | V. Dederer, M. Sanz Murillo, E. P. Karasmanis, S. Mathea, A. E. Leschziner, S. L. Reck-Peterson, S. Knapp (2024) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| KLHDC2 | H. Zhou, T. Zhou et al. (2025) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| TBXT | Z. Davis-Gilbert, D. Drewry, M. A. Hossain et al. (2022) | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) |

Changes: selected measured sheets/cells, CSV conversion, concentration conversion
to M, added source coordinates, and row/ID transformations for robustness tests.
Original downloaded files are unmodified. No endorsement by the original authors
is implied. Cite the original studies/datasets when using these measurements.
"""
    )
    (ROOT / "docs/EVALUATION.md").write_text(
        """# Evaluation protocol

This is a public experimental-data pilot. Ten task scores are computed
individually, with an aggregate mean over five study means. Each study has two
related tasks; curves, derived endpoints and subset cases are not independent
replicates. No confidence interval based on ten independent studies is justified.

All inputs, expected outputs, reference programs and sources are public. Agent
images exclude reference/test material, but this cannot undo prior exposure.
Renaming IDs and taking measured subsets tests program reuse, not blind scientific
generalization. A blind release requires held-out studies and independent reviewed
labels, versioned acquisition metadata, a freeze date and an exposure policy.

For any run record: repository commit, data/scoring version, Harbor version,
model/provider, agent configuration, prompts, tools, resource limits, retries,
randomness settings and costs. Report every trial, not only the best retry.
Keep per-task metrics and logs with credentials removed. A missing task counts
as zero. Do not pool results across synthetic v0.5 and experimental v0.6.

Local tests check source cell provenance, numerical consistency, defective outputs
and an alternative optimizer. They do not establish independent scientific
adjudication or secure Harbor runtime integration. No real-agent baseline has yet
been measured. Harbor + Docker end-to-end testing remains outstanding.

Do not interpret the score as validated binding classification, drug candidacy,
clinical utility, or proof of wet-lab reliability. The present score primarily
measures reproducible numerical analysis under an explicit contract. Expanded
biological decision scoring requires expert-reviewed evidence and orthogonal
validation; these have not been fabricated to fill gaps in public datasets.
"""
    )
    (ROOT / "CONTRIBUTING.md").write_text(
        """# Contributing

Use English for code, task prompts and benchmark documentation. Use Python 3.12
and install requirements-dev.txt. Edit canonical files in tools/, then rebuild
with tools/ingest.py, tools/build.py and tools/docs.py. Generated copies must match.
Run tools/check_repository.py and tools/validate.py before submitting.
Local validation executes trusted code only; never run an unknown submission on
your host. Use isolated disposable containers for untrusted agents.

Every new dataset needs an experimentally verified origin, clear redistribution
rights, source/derived hashes, exact extraction coordinates and documented assay
scope. Simulated curves, fitted predictions, image reconstructions and fabricated
negative labels are not eligible for this experimental task set. Any separate
simulation track must be explicitly named and excluded from real-data scores.

Scoring changes need documented behavior, regression checks, version changes and
honest scientific limitations. Never hand-edit expected results to make a solver
pass. Add independent expert review before claiming biological decision validity.
Preserve original source licenses and attribution. Code contributions are MIT
licensed; third-party data retain their own licenses.

Pull requests should explain the problem, resulting behavior and validation.
Do not commit credentials, private evaluation data or unrelated run logs.
"""
    )
    (ROOT / "CHANGELOG.md").write_text(
        """# Changelog

## 0.6.0 — 2026-11-11

- Replace the active synthetic task set with ten experimental-data tasks from
  five protein-target drug-discovery studies.
- Bundle six attributable original files, exact source-cell mappings, hashes,
  licenses and reproducible extraction of 49 sensorgrams and report-point data.
- Exclude fitted predictions, non-SPR assays, nucleic-acid and aptamer examples.
- Score numerical workflows, apparent equilibrium fits, reference audits and
  explicit scope constraints automatically on a 0–1 scale; no report score.
- Add measured-subset reruns, source-cell audits and scoring regression tests.
- Limit claims explicitly: no expert-adjudicated binding/advancement ground truth,
  no agent baseline, and Harbor + Docker end-to-end validation still outstanding.
- Preserve the synthetic predecessor at tag v0.5.0-synthetic. Scores are incompatible.
"""
    )
    for x in catalog:
        p = ROOT / "tasks" / x["id"] / "environment/spec/SCORING.md"
        p.write_text((ROOT / "SCORING.md").read_text())


if __name__ == "__main__":
    main()
