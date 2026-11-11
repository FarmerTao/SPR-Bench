# Task questions

All tasks use measured experimental data. See [contract](CONTRACT.md) for required program outputs.

## stat3-binding: STAT3: compare measured response and scoped negative evidence

Compare DPP and S3I-201 against mouse STAT3beta core 127-722. Distinguish a lack of measured response in this construct from a universal non-binder claim.

Source study: STAT3; input: `stat3.csv`; 7,262 selected rows.

## stat3-flow: STAT3: audit flow-dependent responses

Compare the three flow rates for S3I-201. Quantify differences without treating flow conditions as biological replicates or estimating a concentration-series KD.

Source study: STAT3; input: `stat3.csv`; 2,419 selected rows.

## cyp3a4-sparse: CYP3A4: reconstruct sparse observed sensorgrams

Recover the eight fluconazole traces from sparse measured cells. Preserve each trace time grid and quantify its response without using the source fitted curves.

Source study: CYP3A4; input: `cyp3a4-traces.csv`; 12,770 selected rows.

## cyp3a4-affinity: CYP3A4: audit apparent steady-state affinity

Fit the observed fluconazole concentration-response points, quantify residuals and concentration coverage. Do not interpret an apparent KD as target selectivity or a kinetic rate.

Source study: CYP3A4; input: `cyp3a4-affinity.csv`; 8 selected rows.

## lrrk2-traces: LRRK2: analyze protein binder concentration series

Analyze the seven DARPin E11 sensorgrams. Separate measured binding response from evidence of catalytic inhibition or therapeutic readiness.

Source study: LRRK2; input: `lrrk2-traces.csv`; 48,314 selected rows.

## lrrk2-affinity: LRRK2: refit E11 affinity with a free offset

Refit seven observed E11 equilibrium responses with a free offset. Report residuals and coverage; author-fitted parameters are a comparison, not ground truth.

Source study: LRRK2; input: `lrrk2-affinity.csv`; 7 selected rows.

## klhdc2-hits: KLHDC2: compare initial small-molecule hits

Compare measured sensorgrams for compounds 1 and 2. Avoid treating the neighboring fluorescence-polarization sheets as SPR data or treating representative traces as replicates.

Source study: KLHDC2; input: `klhdc2-hits.csv`; 54,626 selected rows.

## klhdc2-analogs: KLHDC2: compare follow-up small molecules

Analyze measured sensorgrams for compounds 5 and 6. Compare concentration-normalized evidence without inventing unreported controls or kinetic ground truth.

Source study: KLHDC2; input: `klhdc2-analogs.csv`; 50,190 selected rows.

## tbxt-reference: TBXT: audit experimental reference correction

Join active, reference and reference-subtracted late-binding report points by run/cycle/channel/window. Audit correction arithmetic and retain compound/series identities.

Source study: TBXT; input: `tbxt.csv`; 23,040 selected rows.

## tbxt-triage: TBXT: quantify corrected dose-response evidence

Summarize corrected late-binding responses, reference binding and dose trends. These are screening-evidence metrics; a large response alone does not establish specific binding or justify a drug-development decision.

Source study: TBXT; input: `tbxt.csv`; 23,040 selected rows.
