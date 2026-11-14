# SPR-Bench

**Ten expert-level surface plasmon resonance (SPR) analysis tasks for AI agents,
in the [Terminal-Bench-Science](https://github.com/harbor-framework/terminal-bench-science)
task format.**

Each task hands an agent the raw export of a realistic biosensor experiment
(absolute responses from reference and active flow cells, run method, surface
description) and asks for the scientific result an SPR specialist would
report: interaction classes, intrinsic rate constants, affinities, mechanisms,
thermodynamics, epitope bins or active concentrations. Every task hides
failure modes that a generic curve fit does not survive, and every task is
graded with a binary, outcome-only verifier against exact latent truth.

**Status:** all ten tasks pass local oracle/empty-submission checks and
TB-Science static checks; tolerances are calibrated over simulation seeds with
reference, independent and ablated analyses (see each task's
`authoring/calibration.md`). Harbor + Docker end-to-end runs and real-agent
baselines have not been run yet, and author metadata in `task.toml` still has
`TODO` fields.

## Tasks

| Task | Workflow | What has to be got right |
|---|---|---|
| [spr-kinetic-triage](tasks/life-sciences/biology/spr-kinetic-triage/instruction.md) | multi-cycle kinetics campaign | DMSO solvent correction, double referencing, mass transport, unresolvable fast kinetics, aggregators, air-bubble cycles |
| [single-cycle-kinetics](tasks/life-sciences/biology/single-cycle-kinetics/instruction.md) | single-cycle kinetics on a capture surface | capture decay that removes bound complex, capture-scaled blanks, local capacities |
| [avidity-model-select](tasks/life-sciences/biology/avidity-model-select/instruction.md) | antibody format panel | bivalent avidity vs heterogeneous ligand vs 1:1, intrinsic site affinity |
| [solution-competition](tasks/life-sciences/biology/solution-competition/instruction.md) | inhibition in solution | ligand depletion, unknown active fraction, transport-limited readout calibration |
| [fragment-clean-screen](tasks/life-sciences/biology/fragment-clean-screen/instruction.md) | single-concentration fragment screen | solvent correction on two protein surfaces, occupancy from MW and control-tracked activity, promiscuity |
| [surface-decay-correct](tasks/life-sciences/biology/surface-decay-correct/instruction.md) | randomized long run | activity decay and a regeneration step tracked by positive controls; steady-state scaling |
| [induced-fit-linkage](tasks/life-sciences/biology/induced-fit-linkage/instruction.md) | mechanism study | linked-reaction (contact-time) test separating two-state from heterogeneous binding |
| [thermo-vant-hoff](tasks/life-sciences/biology/thermo-vant-hoff/instruction.md) | multi-temperature kinetics | temperature-dependent transport, re-equilibration, nonlinear van't Hoff with dCp, Arrhenius |
| [epitope-binning](tasks/life-sciences/biology/epitope-binning/instruction.md) | tandem epitope binning | exchange with fast-off antibodies, slow-on antibodies, capture normalization, orientation logic |
| [cfca-concentration](tasks/life-sciences/biology/cfca-concentration/instruction.md) | calibration-free concentration analysis | Leveque transport from geometry, unit conversion, transport-limitation QC |

All tasks live under `tasks/life-sciences/biology/<task>/` with the
TB-Science layout: `instruction.md`, `task.toml`, `README.md`,
`environment/`, `solution/`, `tests/` (separate no-network verifier,
pytest + CTRF, binary reward) and `authoring/` (generator, independent solver,
variants and calibration; never mounted into a container).

## Data

Task data are simulated from a shared physical biosensor model
([`tools/sprsim.py`](tools/sprsim.py)): two flow cells in series with transit
lag and injection dispersion, 1:1, bivalent, two-state and heterogeneous
binding, two-compartment transport from flow-cell geometry and diffusion,
DMSO bulk response with excluded volume, regeneration drift, capture decay,
and white plus correlated noise. Simulation gives exact latent truth, which
measured public datasets cannot. Noise levels, sampling rates and affinity
ranges are anchored on the measured SPR exports bundled in [`sources/`](sources/README.md)
(LRRK2/DARPin E11, designed macrocycles, ISG65/C3, D-box peptides, STAT3,
TBXT); those files are retained with their licenses for provenance only.

The previous measured-data task set (v0.8 core tier) is preserved at git tag
`v0.8-core`. The extracted CSVs in `data/` and `tools/ingest.py` are retained
only to regenerate `sources/anchors.json`; they are not task inputs and are not
used by the simulated tasks.

## Running

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
python tools/scaffold.py --check          # generated boilerplate is current
python tools/check_tasks.py               # oracle passes, empty submission fails, per task
harbor lint tasks/life-sciences/biology/*

# With Docker:
harbor run -p tasks/life-sciences/biology/<task> -a oracle    # expect reward 1
harbor run -p tasks/life-sciences/biology/<task> -a nop       # expect reward 0
harbor run -p tasks/life-sciences/biology/<task> -a claude-code -m <provider/model> -k 5
```

Report pass rates per task over all trials (pass@1 = mean binary reward); see
[docs/EVALUATION.md](docs/EVALUATION.md). To regenerate a task's data or
recalibrate it:

```bash
python tasks/life-sciences/biology/<task>/authoring/generate.py
python tools/calibrate.py <task> --seeds 1-12 --write
python tools/scaffold.py                  # refresh boilerplate and README tables
```

## Contamination

Ground truth (`tests/ground_truth.json`) and the generators with their default
seeds are in this repository. TB-Science agents have internet access, so
publishing this repository before a benchmark freeze exposes the answers; keep
it private until submission, or regenerate data with new seeds.

## License and citation

Code and documentation: MIT ([LICENSE](LICENSE)). Bundled third-party source
data keep their own licenses ([THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)).
See [CITATION.cff](CITATION.cff).
