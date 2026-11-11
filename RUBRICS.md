# Task-Specific Rubrics

These ten English rubrics expand the implemented v0.5 scoring rules into atomic criteria. Each task totals 1.0; all scoring is automatic. They share verifier primitives but have independent weights and campaign-specific scientific emphasis. They do not introduce unimplemented tests or new deductions.

The administrator-facing rubric files live outside environment/ and are not copied into the agent image. Public task specifications still disclose the required outputs, measurement conventions, execution limits, graded metrics and project decision policies. Generating truth, case labels and private fixtures remain verifier-only during a correctly configured run. Do not hide information necessary for an unambiguous scientific decision.

| Task | Main scientific emphasis | Rubric |
|---|---|---|
| campaign-adjudication | Assess supported binding and follow-up eligibility across an entire campaign; a smooth or high-response trace alone is insufficient. | [campaign-adjudication](rubrics/campaign-adjudication.md) |
| solvent-reference-recovery | Recover solvent- and reference-corrected evidence; distinguish apparent responses that disappear after justified correction. | [solvent-reference-recovery](rubrics/solvent-reference-recovery.md) |
| kinetic-evidence-audit | Distinguish binding evidence from permission to report precise kinetic parameters; preserve unresolved and model-inadequate outcomes. | [kinetic-evidence-audit](rubrics/kinetic-evidence-audit.md) |
| condition-consistency | Preserve flow-condition identities, reproduce condition-specific fits, and reject unsupported pooling of apparent rates. | [condition-consistency](rubrics/condition-consistency.md) |
| model-adequacy | Identify when the campaign single-site reporting model is inadequate; better numerical fitting is not proof of a biological mechanism. | [model-adequacy](rubrics/model-adequacy.md) |
| surface-activity-drift | Recover control activity and normalized response across batches without rescuing invalid batches by numerical division. | [surface-activity-drift](rubrics/surface-activity-drift.md) |
| replicate-adjudication | Retain conflicting repeats and correctly withhold unsupported numerical estimates instead of selecting convenient measurements. | [replicate-adjudication](rubrics/replicate-adjudication.md) |
| campaign-reconstruction | Recover unique traces, indirect compound mappings and declared concentration units before scientific interpretation. | [campaign-reconstruction](rubrics/campaign-reconstruction.md) |
| pipeline-repair | Correct the behavior of the supplied faulty pipeline across new cases; equivalent replacement code is acceptable. | [pipeline-repair](rubrics/pipeline-repair.md) |
| budgeted-validation | Prioritize only scientifically eligible candidates under the fixed budget, with consistent advance/reserve/hold dispositions. | [budgeted-validation](rubrics/budgeted-validation.md) |
