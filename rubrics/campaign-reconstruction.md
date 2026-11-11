# campaign-reconstruction — Official Automatic Rubric

Recover unique traces, indirect compound mappings and declared concentration units before scientific interpretation.

**Maximum score: 1.0. No report, human judgment, or LLM judge is scored.**

| Criterion | Max | Weight | Requirements and subcredit |
|---|---:|---:|---|
| 1. Identity and units | 0.275 | 27.5% | **0.055 (5.5%)**: Exact compound-ID set; missing or extra IDs fail.; **0.055 (5.5%)**: Exact acquired-batch set.; **0.055 (5.5%)**: Exact distinct acquired-trace set.; **0.055 (5.5%)**: Correct trace-to-compound joins, averaged over expected traces.; **0.055 (5.5%)**: Correct molar concentration per trace; tolerance 1e-15 M + 1e-8 relative. |
| 2. Signal correction | 0.175 | 17.5% | **0.0583333 (5.83333%)**: Batch solvent slopes match generating calibration; tolerance 0.01 + 0.002 relative.; **0.0583333 (5.83333%)**: Corrected, baseline-adjusted and activity-normalized endpoint means; tolerance 0.1 RU + 0.01 relative.; **0.0583333 (5.83333%)**: Reference endpoints remove common solvent/baseline without target-activity normalization; tolerance 0.1 RU + 0.01 relative. |
| 3. Quality control | 0.125 | 12.5% | **0.03125 (3.125%)**: Exact issue sets per compound; no duplicate reasons.; **0.03125 (3.125%)**: Control activity recovery per batch; tolerance 0.0001 + 0.002 relative.; **0.03125 (3.125%)**: Correct boolean validity for every acquired batch.; **0.03125 (3.125%)**: Every trace carries its batch validity correctly. |
| 4. Binding evidence classification | 0.1 | 10% | Split 0.1 equally among the K truth classes present. Each class earns its share times correct predictions / expected members. All-negative output cannot earn the supported-binder share. Missing compounds count as incorrect. |
| 5. Parameter reportability | 0.1 | 10% | Each of N correct kinetic-status labels and 3U correctly withheld parameters earns 0.1/(N+3U). N is compound count; U is unreportable-compound count. A missing field is not null. A precise unsupported value loses credit and can activate the cap. |
| 6. Parameter accuracy | 0.075 | 7.5% | Split 0.075 over 3P identifiable parameters, where P is the reportable-compound count. Multiply each share by credit(e): 1 for relative error <=1%; (0.25-e)/0.24 for 1%-25%; 0 at >=25% or for invalid values. Unreportable nulls earn no points here. |
| 7. Condition-fit consistency | 0.05 | 5% | **0.0166667 (1.66667%)**: Exactly the required compound/flow fit pairs, including inadequate-model cases that reach assessment.; **0.0166667 (1.66667%)**: No duplicate compound/flow fit records.; **0.0166667 (1.66667%)**: Each fit reproduces the corrected observations, reports consistent RMSE, and satisfies KD=koff/kon. All three must hold for that condition. |
| 8. Follow-up decisions | 0.05 | 5% | **0.025 (2.5%)**: Correct advance/reserve/hold assignment per expected compound, averaged across compounds.; **0.0125 (1.25%)**: Correct shortlist size, unique eligible members and the declared 10% affinity-equivalence allowance.; **0.0125 (1.25%)**: Correct order under the declared adjacent 10% affinity-equivalence allowance. |
| 9. Executable output and provenance | 0.05 | 5% | **0.025 (2.5%)**: Exact SHA-256 manifest of actual inputs, from a successful fresh invocation.; **0.025 (2.5%)**: Nonempty structured compound results, produced by the submitted program. |

## Application rules

Evaluate each category on all three campaign fixtures; average the three category achievements equally, multiply by this task's category weight, and sum. Missing expected subcategories receive zero without denominator reweighting. Row order is ignored where IDs establish correspondence. Each expected trace or compound, not arbitrary lines of narrative, is the unit of checking.

A nonzero process exit, missing executable or timeout earns zero for that execution. A required-output contract exception activates the documented zero cap. Unsupported advancement caps the entire task at 0.49; unsupported precise parameters cap it at 0.69; otherwise the cap is 1.0. Keep uncapped submetrics for diagnosis. Reports have no effect, even if absent or misleading.

Fit reproduction uses independently reconstructed observed RMSE <=0.3 RU for ordinary assessed conditions or <=5 RU for model-inadequate cases. Reported RMSE must agree within 0.02 RU + 1% relative, and reported KD must agree with koff/kon within 0.1% relative. These are project-specific synthetic-pilot settings.

See ../SCORING.md for the complete shared numerical contract and tools/scoring.py plus tools/verifier.py for the executable implementation. Expected labels, references and private cases are not defined by text matching. Merely mentioning a correction, uncertainty or diagnosis earns no credit.

## Scope of this rubric

This is a task-specific weighting and atomic expansion of the current shared computational checks, not a claim that ten independent scientific test engines have been implemented. In particular, model adequacy is assessed through the declared reporting model and its evidence; a separate unseen-concentration prediction challenge is not currently scored. Pipeline repair is judged by corrected behavior, not edit count, diagnosis prose, or a newly invented regression-test submission requirement.
