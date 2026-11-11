# Assess Flow-Dependent Binding Evidence

Evaluate whether the characterization results are stable across flow conditions. Determine which compounds admit a common intrinsic-rate interpretation and which should be held for a condition-dependence investigation. Do not infer a unique transport mechanism from disagreement alone.

## Data

16 compounds per campaign, three independently generated campaign fixtures. Generating truth is private under tests/cases; no oracle-generated labels are used. All data are synthetic.

## Difficulty

Correct interpretation depends on reconstructing acquisitions, applying calibrated corrections, handling invalid controls and repeat conflicts, and reporting parameters only under the declared project criteria. The mix of experimental conditions varies by task. Difficulty has not been calibrated with blind agent trials.

## Reference solution

solution/run.py implements calibration, correction, QC, bounded global fitting and policy-based selection. It reads only the supplied campaign data.

## Verification

A separate verifier reruns the program on three cases, compares results against generating truth, checks keyed evidence and reproduces condition-fit residuals. Reward is the fully automatic 0-1 task score; see environment/spec/SCORING.md. See the package README and validation reports for limitations and tested baselines. Container integration remains untested.
