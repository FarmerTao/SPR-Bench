# SPR Research Workflow Tasks

All ten tasks are integrated synthetic campaign analyses. The former component exercises have been replaced.


---

# Adjudicate an SPR Screening Campaign

Deliver an evidence-supported hit assessment for a screening campaign assembled from several acquisition batches. Reconcile the sample records, determine which experiments can support a conclusion, and distinguish interpretable binding from apparent hits that do not survive the campaign controls. Produce a defensible follow-up shortlist.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Recover Binding Evidence from Solvent-Affected Runs

The screening team reports strong responses that change between solvent conditions. Determine which compounds retain credible binding evidence after defensible calibration and correction. Quantify the recovered responses and identify cases that should not be advanced.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Audit the Reportability of Binding Kinetics

Audit the kinetic characterization campaign. Decide which compounds support numerical rate constants, which show binding but do not support the proposed kinetic interpretation, and which require a repeat. Supply condition-specific fits and explain the limits of the reportable estimates.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Assess Flow-Dependent Binding Evidence

Evaluate whether the characterization results are stable across flow conditions. Determine which compounds admit a common intrinsic-rate interpretation and which should be held for a condition-dependence investigation. Do not infer a unique transport mechanism from disagreement alone.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Resolve Model Inadequacy in a Binding Campaign

A previous campaign report presented every response as a single-site kinetic interaction. Reassess whether that description is supported across concentration and replicate series. Identify compounds for which a simple model is an adequate reporting model and those requiring a more cautious interpretation.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Recover a Campaign with Changing Surface Activity

Recover the campaign interpretation across changing surface activity and invalid acquisitions. Use the supplied control measurements to determine whether normalization is supported. Distinguish declining assay performance from genuine differences between compounds, and report which conclusions remain usable.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Reconcile Conflicting Replicate Measurements

Resolve disagreement between independent replicate series. Distinguish stable evidence from compounds whose apparent affinity cannot be responsibly summarized by a single estimate. Preserve every measurement in the audit trail and do not discard disagreeing repeats merely to improve a fit.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Reconstruct and Analyze an Acquisition Archive

Reconstruct the compound identities and concentrations in the acquisition archive, then complete a scientific hit assessment. The archive contains repeated exports, unsorted observations, mixed declared concentration units, and indirect sample identifiers. Demonstrate that the recovered mapping supports the reported conclusions.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Repair a Faulty SPR Analysis Pipeline

Repair or replace the supplied legacy analysis pipeline so that it produces scientifically defensible results for this campaign and new campaigns using the documented file contract. The current output is not a reference answer. Diagnose the scientific and software defects, deliver a corrected implementation, and include a regression-test explanation in the report.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.

The legacy implementation is under `/app/legacy/`; its outputs are not ground truth. Your submission may repair it or replace it with a justified implementation.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.


---

# Prioritize Orthogonal Validation from Campaign Evidence

Choose a shortlist for the next orthogonal-validation round under the project budget. Decisions must follow from the supplied raw measurements, run validity, replicate consistency, and reportable binding parameters. Make the scientific exclusions auditable; an attractive fitted affinity alone is insufficient.

The campaign inputs are in `/app/data/`. Acquisition conventions and experimental context are documented in `/app/data/RUN_NOTES.md`; project-specific reporting and advancement criteria are in `/app/data/project.json` and the authoritative output contract `/app/spec/CONTRACT.md`. You have Bash, Python, NumPy, SciPy, pandas, and matplotlib. Inspect the files, implement and test the analysis, and deliver `/app/submission/run.py` with any helpers under `/app/submission`. It must accept `--input-dir` and `--output-dir` and produce the artifacts specified by the contract. The evaluator reruns it on new campaigns with the same contract. No particular optimizer or programming style is required.

You may include a short scientific report for your own audit; it has no effect on scoring. Do not treat a good fit as proof of a biological mechanism or advancement as proof of druglikeness. All supplied data are explicitly synthetic; the task evaluates a coupled analysis workflow, not validated real-world performance.
Scoring uses the fully automatic 0-1 rubric in `/app/spec/SCORING.md`. Reports are optional and never graded.
