# Deliverable contract

Implement `/app/submission/run.py` with `--input-dir DIRECTORY --output-dir DIRECTORY`. Keep helpers under /app/submission. Read only the supplied campaign directory for task data. Create the output directory, write all persistent outputs there, and support repeated invocations with fresh paths. No network or precomputed results are available in evaluation. Each invocation has 180 seconds, 2 CPUs, 4 GB RAM, and one BLAS thread.

## results.json
Top-level keys: compounds (one record per compound), selected (ordered compound IDs), batches (one record per acquired batch).
Each compound record contains compound_id, binding_call (supported / not_detected / artifact_suspected / inconclusive), kinetics_status (supported / not_applicable / unresolved / condition_dependent / model_inadequate), issues (list from invalid_control, reference_binding, repeat_disagreement, flow_dependence, model_mismatch, unresolved_dissociation), KD_M, kon_M_inv_s_inv, koff_s_inv, and decision (advance / reserve / hold). Unsupported numeric estimates must be JSON null.
Batch records contain batch_id, solvent_slope (RU per DMSO percentage point), activity_fraction, and valid (boolean).

## Campaign policy
Apply the documented controls before making negative or positive claims. A compound with any invalid acquired batch is inconclusive with invalid_control. Otherwise compare the highest-concentration endpoints across repeats and conditions. An endpoint reference response above reference_signal_limit_RU and reference/(abs(corrected)+reference)>0.8 indicates reference_binding. Corrected response below detection_limit_RU is not_detected under the tested conditions. Excessive endpoint population CV indicates repeat_disagreement. These unresolved/invalid/artifact cases do not admit rate estimates.

For the remaining compounds, compare fitted conditions: kon ratio above maximum_kon_ratio gives condition_dependent; otherwise any condition RMSE above maximum_model_rmse_RU gives model_inadequate. If neither applies, assess the mean highest-concentration dissociation drop from the first three post-switch observations to the last three observations. A drop below minimum_resolved_drop_RU is unresolved. Only compounds passing all gates receive globally fitted numerical rate constants and KD. This ordering defines the project's adjudication convention where issues coexist. These rules determine reportability, not molecular mechanism.

Only binding_call=supported and kinetics_status=supported are eligible. Rank eligible compounds by ascending KD, using compound_id to break exact ties; advance up to validation_budget, reserve other eligible compounds, and hold the rest. Advancement means justified follow-up under this project's policy, not established druglikeness.

## trace_evidence.csv
Columns: trace_id,compound_id,concentration_M,peak_corrected_RU,reference_peak_RU,batch_valid. Include each distinct acquired trace once. Corrected peaks are activity-normalized endpoint means after solvent, matched blank, reference, and baseline correction. Reference peaks remove common solvent response and pre-injection baseline, without activity normalization. Row order is arbitrary; IDs define alignment.

## condition_fits.csv
Columns: compound_id,flow_uL_min,kon,koff,KD,Rmax,rmse. Include a fit for each compound/flow combination reaching model assessment. Records are numerical evidence for the adequacy and condition-consistency decisions; they must not be represented as intrinsic kinetic estimates for failed cases.

## provenance.json and report.md
provenance.json is {"inputs": {"relative/path": "sha256hex", ...}} for all files under input-dir. report.md is optional and is never scored, including its presence or absence. No human or LLM judge participates in scoring.

## Evaluation
The submitted program is rerun on three campaign fixtures. Each task receives a fully automatic score from 0 to 1, using the task-specific weights, submetrics, tolerances and critical-error caps in `/app/spec/SCORING.md`. The same value is written to Harbor reward.txt and scorecard.json. The benchmark score is the arithmetic mean of the ten task scores; each task contributes 10%. Numeric reference values come from independent generating truth. Nonidentifiable parameters must be null. Correct alternative implementations are allowed. Selection permits a 10% generating-affinity equivalence band. Returned files are inspected in a separate verifier.
