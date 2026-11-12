import json
from pathlib import Path
from ingest import ROOT

FIELDS = {
    "trace": {
        "coverage": ["n", "concentration_M", "start_s", "end_s"],
        "response": [
            "initial_median_RU",
            "initial_sd_RU",
            "p95_delta_RU",
            "tail_delta_RU",
            "auc_RU_s",
        ],
    },
    "affinity": {
        "coverage": ["n", "max_concentration_M"],
        "response": [
            "KD_M",
            "Rmax_RU",
            "offset_RU",
            "rmse_RU",
            "max_concentration_over_KD",
        ],
    },
    "report": {
        "coverage": [
            "n",
            "n_corrected_late",
            "n_concentrations",
            "max_concentration_M",
        ],
        "response": [
            "max_corrected_RU",
            "min_corrected_RU",
            "mean_corrected_RU",
            "max_reference_RU",
            "dose_slope_RU_per_uM",
            "max_reference_subtraction_error_RU",
        ],
    },
}


def main():
    catalog = json.loads((ROOT / "task_catalog.json").read_text())
    manifest = json.loads((ROOT / "sources/manifest.json").read_text())
    data = json.loads((ROOT / "data_manifest.json").read_text())
    table = "| Task | Study | Input | Rows |\n|---|---|---|---:|\n" + "\n".join(
        f"| [{x['id']}](tasks/{x['id']}/instruction.md) | {x['study']} | {x['kind']} | {x['rows']:,} |"
        for x in catalog
    )
    (ROOT / "README.md").write_text(
        f"""# SPR-Bench

**An experimental-data pilot for executable protein/antibody SPR analysis.**

SPR-Bench v0.7 is a protein/antibody SPR benchmark with two binding-assessment
tasks. It contains ten Harbor tasks drawn from six studies: LRRK2/DARPin,
designed macrocycles, ISG65/C3, D-box peptides, STAT3, and TBXT. There are **55
measured sensorgrams, 57 observed affinity endpoints, 23,040 TBXT report-point
rows, and two binding/non-binding tasks** in the canonical selected data. No responses,
concentrations, negative examples or replicates are simulated.

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

## Tasks

{table}

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

## Source attribution

See [sources/README.md](sources/README.md) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Original files are unmodified;
CSV conversion, selected measured cells, unit conversion, opaque identifiers and
robustness subsets are the only changes.

## Citation

Cite the original studies and this repository. Third-party data retain their
source licenses; no endorsement by the original authors is implied.
"""
    )
    (ROOT / "QUESTIONS.md").write_text(
        "# Task questions\n\nAll tasks use measured experimental data. See [CONTRACT.md](CONTRACT.md) for required program outputs.\n\n"
        + "\n".join(
            f"## {x['id']}: {x['title']}\n\n{x['question']}\n\nSource study: {x['study']}; input: `{x['source_file']}`; {x['rows']:,} selected rows.\n"
            for x in catalog
        )
    )
    (ROOT / "SCORING.md").write_text(
        """# Scoring

Each task is scored in [0,1] by a rule-based verifier. The score combines
coverage, numerical response fields, provenance and disclosed scope claims.

| Task family | Coverage | Response | Binding evidence | Provenance | Scope |
|---|---:|---:|---:|---:|---:|
| Trace | 20% | 65% | 0% | 10% | 5% |
| Affinity | 15% | 70% | 0% | 10% | 5% |
| STAT3 binding | 15% | 50% | 20% | 10% | 5% |
| TBXT operational binding | 15% | 50% | 20% | 10% | 5% |

Coverage checks exact record IDs plus the listed coverage fields. Response checks
the listed numerical fields against the reference computed from the supplied
measurements. Provenance checks the SHA-256 manifest of the input files. Scope
checks the disclosed claims exactly.

For N expected records and F coverage fields, coverage contains 1 + N*F checks:
one exact ID-set check and one check per expected record/field. Response contains
N*R checks for R response fields. Provenance has one check. Scope has one check
per disclosed claim.

Missing output, invalid JSON, duplicate JSON keys/record IDs, nonfinite JSON,
program failure or timeout gives that case zero. Missing fields/records fail
corresponding checks. An entirely empty record list can earn only provenance and
scope credit (at most 0.15). A record list that passes coverage/provenance/scope
but no response checks still earns those weights under the official score; its
analysis_reward is zero. Unexpected record IDs fail exact coverage. Null matches
only a documented null reference value. Counts must match exactly. All numerical
tolerances are in CONTRACT.md.

The reference numbers are recomputed from selected measurements, not synthesized
kinetic truth. Source-fitted curves are excluded. Apparent KD fits use a specified
least-squares model; the score does not claim this is the true biological
mechanism. The disclosed scope component is intentionally easy and should be
reported separately when comparing scientific analysis ability.

Report all ten task scores and study means. The recommended overall score is
the mean of the ten task scores. Macrocycle, STAT3 and TBXT each contribute one
task; LRRK2, ISG65 and D-box contribute multiple related tasks, so study means are
descriptive rather than equally weighted. A missing task counts as zero. Do not treat ten tasks or
the two robustness cases as independent biological replicates. Do not pool scores
with the archived synthetic version or with later scoring versions.

All fixtures, reference outputs and source papers are public. This is a public
fixture evaluation; it is not a blind assessment. Local oracle scores and scoring
regression tests measure implementation consistency, not model capability or
scientific label validity. No manually graded report or model-as-judge is used.
"""
    )
    rub = "# Rubrics\n\nFields and weights per task. Coverage and response fields are listed in the executable contract; provenance and scope are weighted checks.\n\n"
    for x in catalog:
        f = FIELDS[x["kind"]]
        rub += f"## {x['id']}\n\n{x['title']}\n\n| Category | Weight | Fields |\n|---|---:|---|\n"
        rub += f"| Coverage | {x['weights']['coverage']:.0%} | {', '.join(f['coverage'])} |\n"
        rub += f"| Response | {x['weights']['response']:.0%} | {', '.join(f['response'])} |\n"
        if "binding_evidence" in x["weights"]:
            rub += f"| Binding evidence | {x['weights']['binding_evidence']:.0%} | binding_assessments |\n"
        rub += f"| Provenance | {x['weights']['provenance']:.0%} | input_sha256 |\n"
        rub += f"| Scope | {x['weights']['scope']:.0%} | disclosed claims |\n\n"
    (ROOT / "RUBRICS.md").write_text(rub.rstrip() + "\n")
    (ROOT / "docs/EVALUATION.md").write_text(
        """# Evaluation protocol

This is a public protein/antibody SPR pilot. Ten task scores are computed
individually, with an aggregate mean over the ten tasks. Macrocycle, STAT3 and
TBXT contribute one task each; LRRK2, ISG65 and D-box contain related tasks and
are not independent replicates. No confidence interval based on ten
independent studies is justified.

All inputs, expected outputs, reference programs and sources are public. Agent
images exclude reference/test material, but this cannot undo prior exposure.
Renaming IDs and taking measured subsets tests program reuse, not blind scientific
generalization. A blind release requires held-out studies and independently
reviewed labels, versioned acquisition metadata, a freeze date and an exposure
policy.

For any run record: repository commit, data/scoring version, Harbor version,
model/provider, agent configuration, prompts, tools, resource limits, retries,
randomness settings and costs. Report every trial, not only the best retry.
Keep per-task metrics and logs with credentials removed. A missing task counts
as zero. Report both the official reward and analysis_reward; the latter excludes
coverage, provenance and scope. Do not pool results across synthetic v0.5 and
experimental v0.6/v0.7.

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
    lines = "# Source catalogue and extraction notes\n\nSix studies; seven bundled source files. Accessed 2026-11-12. These are measured experimental data, with source preprocessing retained.\n\n"
    for s in manifest:
        lines += f"## {s['source']} — {Path(s['file']).name}\n\n{s['authors']}. [Primary source]({s['doi']}); [original download]({s['download_url']}).\n\nLicense: {s['license']}. Bytes: {s['bytes']:,}. SHA-256: `{s['sha256']}`.\n\n"
    lines += """## Exact selection and evidence boundaries

- STAT3: three nonempty sheets in Additional file 1; numerical TIME and three
  flow-rate response columns. Blank cells are omitted per trace. Article methods
  specify double referencing. S3I-201 interaction and DPP lack of measurable
  response are author-reported conclusions restricted to mouse STAT3beta core
  residues 127–722 and tested conditions. They are not universal binding labels.
- TBXT: `Report point table`, rows with Step purpose=Analysis, preserving original
  compound names and replicate/series suffixes. Relative responses, windows,
  concentrations, reference types and source row indices are retained. Selected
  workbook is `20201028 LMW binding affinity screen for 136 UNC and Piramal
  compounds.xlsx`. It supplies numeric report points and embedded sensorgram
  images, not a usable numeric full-time-series export. Source-fitted kinetic/
  affinity tables are excluded from input. The binding labels are a disclosed
  operational 10 RU threshold on the maximum corrected binding-late response,
  not an independently validated 140-compound binder/nonbinder ground truth.
- LRRK2: ZIP members `Sensorgrams_E11.txt` and first two columns of
  `Steady state_E11.txt`. Seven concentration series, 7.8125–500 nM. Source-fitted
  parameters and curve columns are retained only in the original archive, never
  provided to agents. Original authors report apparent KD 70.3 nM; this is a
  comparison, not a gold-standard truth label. The specified unweighted
  free-offset refit is not forced to that value. Do not infer catalytic inhibition
  from SPR alone.
- Macrocycle: `macrocycle-fig2.xlsx` Sheet1 columns A/B (MCB_D2) and E/F
  (MDB_D8), plus `macrocycle-fig4.xlsx` Sheet1 columns A/B (RBB_D10). Header rows
  1–2; measured cells only; source-fitted columns C/G excluded. These are
  single-concentration traces (20, 50 and 20 µM; 30 µL/min), not KD
  measurements. The source reports global-fit KD values of 2 µM (MCB_D2),
  1.9 µM (MDB_D8) and 9.4 nM (RBB_D10); these traces do not reproduce those
  global fits.
- ISG65: Figure 2—source data 1, six sheets (C3b/C3d × WT/ΔL2/L2N188A). Column A
  is time; measured cycle columns are B,D,F,H,J,L (`Cycle ... _Y`); interleaved
  source-fitted columns C,E,G,I,K are excluded. Six cycles per sheet, twofold
  dilutions from 10 µM, 30 µL/min. The affinity task uses the measured response
  cell nearest 120 s (end of the 120 s association phase) for each trace; this is
  a derived endpoint, not a source-reported equilibrium fit. Source-fitted curves
  and reported affinities are not scoring targets.
- D-box: `dbox-fig4-data1.xlsx` sheets `Figure 4C -D20 Fc4-1 isotherm` and
  `Figure 4D -D21 Fc4-1 isotherm`, data from row 2 (0.15625–10 µM). The paired
  sensorgrams remain in the source file but are not task inputs. No fitted curve
  is selected. D20/D21 are Fc-fused D-box peptides binding Cdc20; the tasks
  summarize observed endpoints, not a kinetic mechanism.

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
| TBXT | Z. Davis-Gilbert, D. Drewry, M. A. Hossain et al. (2022) | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) |
| LRRK2/DARPin E11 | V. Dederer, M. Sanz Murillo, E. P. Karasmanis, S. Mathea, A. E. Leschziner, S. L. Reck-Peterson, S. Knapp (2024) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Designed macrocycles | S. A. Rettie et al. (2025) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| ISG65/C3b-C3d | A. D. Cook, M. Carrington, M. K. Higgins (2024) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| D-box peptides | R. Eapen et al. (2026) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

Changes: selected measured sheets/cells, CSV conversion, concentration conversion
to M, added source coordinates, and row/ID transformations for robustness tests.
Original downloaded files are unmodified. No endorsement by the original authors
is implied. Cite the original studies/datasets when using these measurements.
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

## 0.7.0 — 2026-11-12

- Build ten SPR tasks from six studies: LRRK2/DARPin, designed macrocycles,
  ISG65/C3, D-box peptides, STAT3, and TBXT.
- Bundle seven attributable original files with exact source-cell mappings,
  hashes, licenses and reproducible extraction of 55 sensorgrams, 57 affinity
  endpoints and 23,040 TBXT report-point rows.
- Add ISG65 C3b/C3d trace tasks and an ISG65 apparent-affinity task (measured
  end-of-association endpoints), plus D20/D21 trace and affinity tasks.
- Add a STAT3 binding/non-binding task with author-scoped DPP/S3I-201 calls,
  and a TBXT operational binding-triage task with a disclosed 10 RU threshold,
  input hashes and a binding-evidence scoring category.
- Keep source-fitted curves out of every task input; scope claims disclose
  single-concentration and derived-endpoint limits.
- Remove the STAT3, CYP3A4, KLHDC2 and TBXT small-molecule tasks from the active
  set. The archived v0.6 release remains in git history.
- Limit claims explicitly: no expert-adjudicated binding/advancement ground
  truth, no agent baseline, and Harbor + Docker end-to-end validation still
  outstanding.

## 0.6.0 — 2026-11-11

- Experimental-data pilot with ten mixed small-molecule/protein SPR tasks.
"""
    )
    for x in catalog:
        (ROOT / "tasks" / x["id"] / "environment/spec/SCORING.md").write_text(
            (ROOT / "SCORING.md").read_text()
        )



if __name__ == "__main__":
    main()
