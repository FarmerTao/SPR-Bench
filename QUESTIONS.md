# Task questions

All tasks use measured experimental data. See [CONTRACT.md](CONTRACT.md) for required program outputs.

## stat3-binding: STAT3: compare measured response and scoped negative evidence

Compare DPP and S3I-201 against mouse STAT3beta core 127-722. Distinguish a lack of measured response in this construct from a universal non-binder claim.

Source study: STAT3; input: `stat3.csv`; 7,262 selected rows.

## tbxt-binding: TBXT: operational binding triage from corrected report points

Compute corrected late-binding report points and classify each compound with the disclosed 10 RU operational threshold. This is a triage rule, not author-reported binding truth.

Source study: TBXT; input: `tbxt.csv`; 23,040 selected rows.

## lrrk2-traces: LRRK2: analyze protein binder concentration series

Analyze the seven DARPin E11 sensorgrams. Separate measured binding response from evidence of catalytic inhibition or therapeutic readiness.

Source study: LRRK2; input: `lrrk2-traces.csv`; 48,314 selected rows.

## lrrk2-affinity: LRRK2: refit E11 affinity with a free offset

Refit seven observed E11 equilibrium responses with a free offset. Report residuals and coverage; author-fitted parameters are a comparison, not ground truth.

Source study: LRRK2; input: `lrrk2-affinity.csv`; 7 selected rows.

## macrocycle-traces: Designed macrocycles: analyze SPR sensorgrams

Analyze measured SPR sensorgrams for three designed macrocyclic binders (MCB_D2/MCL1, MDB_D8/MDM2 and RBB_D10/RbtA). Report the benchmark trace summaries; do not use the source-fitted curves or treat a single-concentration trace as a KD measurement.

Source study: Macrocycle; input: `macrocycle-traces.csv`; 7,669 selected rows.

## isg65-c3b-traces: ISG65 C3b binding: analyze SPR sensorgrams

Analyze measured C3b-binding SPR sensorgrams for ISG65 WT, ISG65ΔL2 and ISG65 L2N188A. Report the benchmark trace summaries; do not use the source-fitted columns or infer kinetic rates.

Source study: ISG65; input: `isg65-traces.csv`; 5,425 selected rows.

## isg65-c3d-traces: ISG65 C3d binding: analyze SPR sensorgrams

Analyze measured C3d-binding SPR sensorgrams for ISG65 WT, ISG65ΔL2 and ISG65 L2N188A. Report the benchmark trace summaries; do not use the source-fitted columns or infer kinetic rates.

Source study: ISG65; input: `isg65-traces.csv`; 5,425 selected rows.

## isg65-affinity: ISG65: apparent steady-state affinity

Fit the six observed ISG65 concentration-response series (C3b/C3d × WT/ΔL2/L2N188A) using the measured end-of-association responses. Report residuals and coverage; do not treat the fit as a kinetic mechanism.

Source study: ISG65; input: `isg65-affinity.csv`; 36 selected rows.

## dbox-d20-affinity: D-box D20: fit apparent steady-state affinity

Fit the observed D20 concentration-response endpoints. Report residuals and coverage; an apparent KD does not establish a mechanism.

Source study: D-box; input: `dbox-affinity.csv`; 7 selected rows.

## dbox-d21-affinity: D-box D21: fit apparent steady-state affinity

Fit the observed D21 concentration-response endpoints. Report residuals and coverage; an apparent KD does not establish a mechanism.

Source study: D-box; input: `dbox-affinity.csv`; 7 selected rows.
