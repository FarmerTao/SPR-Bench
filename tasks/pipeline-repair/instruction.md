# Repair a Faulty SPR Analysis Pipeline

Repair or replace the supplied legacy analysis pipeline so that it produces scientifically defensible results for this campaign and new campaigns using the documented file contract. The current output is not a reference answer. Diagnose the scientific and software defects, deliver a corrected implementation, and include a regression-test explanation in the report.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.

The legacy implementation is under `/app/legacy/`; its outputs are not ground truth. Your submission may repair it or replace it with a justified implementation.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.
