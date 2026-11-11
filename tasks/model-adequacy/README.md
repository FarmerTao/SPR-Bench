# Resolve Model Inadequacy in a Binding Campaign

A previous campaign report presented every response as a single-site kinetic interaction. Reassess whether that description is supported across concentration and replicate series. Identify compounds for which a simple model is an adequate reporting model and those requiring a more cautious interpretation.

## Data

16 compounds per campaign, three independently generated campaign fixtures. Generating truth is private under tests/cases; no oracle-generated labels are used. All data are synthetic.

## Difficulty

Correct interpretation depends on reconstructing acquisitions, applying calibrated corrections, handling invalid controls and repeat conflicts, and reporting parameters only under the declared project criteria. The mix of experimental conditions varies by task. Difficulty has not been calibrated with blind agent trials.

## Reference solution

solution/run.py implements calibration, correction, QC, bounded global fitting and policy-based selection. It reads only the supplied campaign data.

## Verification

A separate verifier reruns the program on three cases, compares results against generating truth, checks keyed evidence and reproduces condition-fit residuals. Reward is the fully automatic 0-1 task score; see environment/spec/SCORING.md. See the package README and validation reports for limitations and tested baselines. Container integration remains untested.
