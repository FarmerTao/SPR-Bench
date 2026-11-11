# Reconstruct and Analyze an Acquisition Archive

Reconstruct the compound identities and concentrations in the acquisition archive, then complete a scientific hit assessment. The archive contains repeated exports, unsorted observations, mixed declared concentration units, and indirect sample identifiers. Demonstrate that the recovered mapping supports the reported conclusions.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.
