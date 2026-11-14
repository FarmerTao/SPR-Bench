# Contributing

Use English for code, instructions and documentation, and Python 3.12 with
`requirements-dev.txt`.

## Task layout

Tasks follow the Terminal-Bench-Science format under
`tasks/life-sciences/biology/<slug>/`. Generated boilerplate (task.toml,
Dockerfiles, test.sh, solve.sh, README header and calibration table, vendored
`authoring/sprsim.py`) comes from `tools/catalog.json` via
`python tools/scaffold.py`; never edit it by hand. Authored files are
`instruction.md`, the README sections, `tests/test_outputs.py`,
`solution/solve.py` and `authoring/{generate.py,independent.py,variants.json}`.
Every task file carries the harbor canary on its first lines.

## Changing a task

1. Edit the generator, regenerate data and ground truth.
2. Make the reference solution pass; keep `diagnostics()` in the test module.
3. Calibrate: `python tools/calibrate.py <slug> --seeds 1-12 --write`. Correct
   analyses (reference, independent solver, accepted variants) must pass every
   seed; essential ablations must fail every seed. Report comparators that pass
   as passing (`non-essential` or `partial-ablation`) rather than tuning them
   away. Never edit ground truth or tolerances to make a solver pass.
4. `python tools/scaffold.py && python tools/check_tasks.py && harbor lint tasks/life-sciences/biology/*`.

Instruction text must be written by the task author (TB-Science screens it
for AI-generated text). Do not commit credentials or private evaluation data.
