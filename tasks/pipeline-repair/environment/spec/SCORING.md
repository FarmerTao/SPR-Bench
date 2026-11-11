# Fully Automatic Scoring Specification — v0.5

All task scores and the benchmark score lie in [0, 1]. There is no reviewer score, no narrative judgment, no LLM judge, and no pending manual assessment. `report.md` is optional; adding, removing or changing it does not affect any score. The former automatic weights are normalized by their sum (80); the former report component is removed, not awarded by default.

## Weights by task

Every row sums to 100%. These are fractions of the final uncapped task score.

| Task | Mapping | Correction | QC | Binding | Reportability | Parameters | Fit consistency | Decisions | Execution/provenance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| campaign-adjudication | 7.5% | 12.5% | 12.5% | 17.5% | 12.5% | 7.5% | 7.5% | 17.5% | 5% |
| solvent-reference-recovery | 5% | 30% | 10% | 17.5% | 7.5% | 10% | 7.5% | 7.5% | 5% |
| kinetic-evidence-audit | 5% | 10% | 10% | 10% | 25% | 20% | 10% | 5% | 5% |
| condition-consistency | 5% | 10% | 10% | 10% | 25% | 10% | 20% | 5% | 5% |
| model-adequacy | 5% | 10% | 10% | 10% | 25% | 10% | 20% | 5% | 5% |
| surface-activity-drift | 5% | 20% | 27.5% | 12.5% | 10% | 10% | 5% | 5% | 5% |
| replicate-adjudication | 5% | 10% | 22.5% | 15% | 22.5% | 10% | 5% | 5% | 5% |
| campaign-reconstruction | 27.5% | 17.5% | 12.5% | 10% | 10% | 7.5% | 5% | 5% | 5% |
| pipeline-repair | 7.5% | 12.5% | 12.5% | 12.5% | 12.5% | 12.5% | 12.5% | 12.5% | 5% |
| budgeted-validation | 5% | 10% | 10% | 12.5% | 12.5% | 10% | 7.5% | 27.5% | 5% |

## Aggregation equations

For task i, category j and case c, let a[i,c,j] be the category achievement in [0,1], and w[i,j] the weight in the table divided by 100. The three supplied evaluation cases have equal weight.

    category_achievement[i,j] = (a[i,0,j] + a[i,1,j] + a[i,2,j]) / 3
    uncapped_score[i] = sum_j(w[i,j] * category_achievement[i,j])
    task_score[i] = min(uncapped_score[i], critical_error_cap[i])
    benchmark_score = sum_i(task_score[i]) / 10

Example: a category weighted 12.5% with case achievements 1, 0.5 and 0 contributes 0.125 * 0.5 = 0.0625. All other category contributions are added before applying the cap. Example benchmark scores: nine tasks at 0.92 and one at 0.88 yield 0.916.

Every elementary boolean check earns 1 when correct and 0 otherwise. A mean over an empty expected group is 0; a missing subcategory never disappears from its denominator. The current fixtures contain reportable parameters and fits in every task. Categories must be redefined explicitly if future fixtures contain no applicable instances.

## Category definitions and denominators

### 1. Mapping

Equal mean of five subcategories: exact compound-ID coverage; exact batch-ID coverage; exact trace-ID coverage; per-trace compound mapping accuracy; per-trace concentration accuracy. Coverage checks are binary. Per-trace accuracy averages over all expected trace IDs. Concentration tolerance: abs(error) <= 1e-15 M + 1e-8*abs(reference). Trace row order is irrelevant. Missing IDs fail coverage and their corresponding expected records. Duplicate IDs are an invalid output contract.

### 2. Correction

Equal mean of three subcategories: mean batch solvent-calibration correctness; mean corrected-endpoint correctness over traces; mean reference-endpoint correctness over traces.

- Solvent slope tolerance: 0.01 RU/percentage point + 0.002*abs(reference).
- Corrected and reference endpoints: 0.1 RU + 0.01*abs(reference).

Endpoints must follow the acquisition notes: matched reference/blank/solvent correction, baseline treatment, and target-response activity normalization. A large number of trace rows cannot outweigh the separate calibration subcategory.

### 3. Quality control

Equal mean of four subcategories: per-compound exact issue-set correctness; mean batch activity correctness; mean batch validity correctness; mean trace batch-validity correctness. Issue order is irrelevant but duplicates are rejected. Batch validity is a JSON boolean. Activity tolerance: 0.0001 + 0.002*abs(reference). Numerical tolerances are fixed synthetic-pilot settings, not universal instrument accuracy claims.

### 4. Binding evidence

Compute classification accuracy separately for each ground-truth binding-call class present in the case, then average those class accuracies equally. Classes are supported, not_detected, artifact_suspected and inconclusive. Missing records count as incorrect. This is macro-average class recall, not precision or an overall majority-class accuracy. Coverage and other categories separately penalize extraneous records.

### 5. Parameter reportability

One boolean for each compound's kinetics_status, plus one boolean for each of its three required null parameters when generating truth marks those parameters unreportable. Average all of these booleans. Thus the denominator is N + 3U, where N is the number of compounds and U the number with unreportable kinetics. A missing field is not equivalent to null. Unsupported non-null estimates can also activate a critical-error cap.

### 6. Quantitative parameters

Only generating-truth-identifiable kon, koff and KD contribute here. Average over all three parameters of all reportable compounds. For relative error e=abs(estimate-truth)/abs(truth):

    credit(e) = 1                         if e <= 0.01
                (0.25-e)/0.24            if 0.01 < e < 0.25
                0                         if e >= 0.25

Missing, null, boolean, nonpositive or nonfinite estimates receive 0. Unreportable null parameters do not earn extra points in this category. Examples: errors of 0.5%, 13% and 25% earn 1, 0.5 and 0, respectively.

### 7. Fit consistency

Equal mean of three subcategories: exact required compound/flow fit coverage; absence of duplicate condition-fit records; average per-condition fit-reproduction correctness. A condition passes the latter only when all of the following hold:

- The independently reconstructed observation RMSE is <=0.3 RU for ordinary assessed conditions, or <=5 RU for a generating-truth model-inadequate case.
- Reported RMSE agrees with the independently computed RMSE within 0.02 RU + 0.01*abs(reference).
- Reported KD agrees with koff/kon to relative tolerance 0.001.

Forward-model parameters must be finite and positive. Coverage follows the truth-defined compounds that reach model assessment, not the submitter's self-selected subset. Fits are evaluated numerically, not by inspecting source-code keywords.

### 8. Candidate decisions

    achievement = 0.50 * mean(per-compound disposition correctness)
                + 0.25 * shortlist correctness
                + 0.25 * ordering correctness

Advance/reserve/hold consistency is checked against eligibility and the submitted selected list. Shortlist correctness requires the exact permitted count, unique IDs and eligible members within the affinity-equivalence band. Ordering is checked against generating affinities with a 10% adjacent equivalence allowance. The current fixtures have a budget of three; the validator's selected-count rule matches that fixed fixture policy. Changing budgets requires updating the validator and tests rather than assuming arbitrary budgets are supported.

### 9. Execution and provenance

Equal mean of: exact recursive input-file SHA-256 manifest; nonempty structured compound results from a successful fresh execution. Each execution uses a new input/output directory, with a 180-second time limit and the declared environment. A missing executable, timeout or nonzero exit produces zero for every category in that case. The score does not reward tool-call count, report length or verbosity.

## Invalid outputs and critical-error caps

- Missing required files, invalid JSON, duplicate record IDs, parsing exceptions or another output-contract exception zero every category in that case and cap the task at 0. This strict schema gate prevents partial credit from malformed output. Execution failures alone zero the affected case; they do not automatically zero other completed cases.
- If any case advances an unknown compound or one whose truth-defined kinetics do not support advancement, cap the task at 0.49.
- Otherwise, if any case reports a non-null precise KD, kon or koff for an unsupported compound, cap the task at 0.69.
- Otherwise the cap is 1. Apply the minimum cap across cases. Caps can only reduce a score.
- A malformed fixture/configuration is an evaluation infrastructure issue to investigate, not a scientific conclusion.

These caps and tolerances are declared evaluation policies. They have not been independently calibrated by an expert panel and should not be interpreted as clinical risk estimates.

## Machine-readable results

Each task writes the same final 0-1 value to `/logs/verifier/reward.txt` and `scorecard.json` (`score`). scorecard.json records `uncapped_score`, `score_cap`, category weights, achievements, contributions, case weights and critical errors. `metrics.json` contains case diagnostics and `all_checks_passed`, a supplementary strict boolean rather than the graded reward. `ctrf.json` records named checks. There are no reviewer fields and no provisional totals.

Aggregate a full run with:

```bash
python tools/summarize_scores.py --scorecards-root PATH_TO_TASK_LOG_DIRECTORIES --output benchmark_score.json
```

Expected layout: PATH_TO_TASK_LOG_DIRECTORIES/<task-slug>/scorecard.json. Each of the ten expected tasks has weight 10%. Missing tasks count as zero and are listed; incomplete runs are not silently reweighted. Incompatible versions or invalid scores are rejected.

## Scope and versioning

This v0.5 rubric replaces v0.4's report component. Historical v0.3/v0.4 assessments remain historical, not current scoring rules. No subjective report deduction carries over. A mathematically correct existing answer can therefore receive 1.0 on every task. Normalizing weights does not increase difficulty; real difficulty requires better independent cases, not arbitrary penalties. Data remain synthetic. Docker execution and real unseen-data performance remain unverified.
