# Prioritize Orthogonal Validation from Campaign Evidence

Choose a shortlist for the next orthogonal-validation round under the project budget. Decisions must follow from the supplied raw measurements, run validity, replicate consistency, and reportable binding parameters. Make the scientific exclusions auditable; an attractive fitted affinity alone is insufficient.

## Data

24 compounds per campaign, three independently generated campaign fixtures. Generating truth is private under tests/cases; no oracle-generated labels are used. All data are synthetic.

## Difficulty

Correct interpretation depends on reconstructing acquisitions, applying calibrated corrections, handling invalid controls and repeat conflicts, and reporting parameters only under the declared project criteria. The mix of experimental conditions varies by task. Difficulty has not been calibrated with blind agent trials.

## Reference solution

solution/run.py implements calibration, correction, QC, bounded global fitting and policy-based selection. It reads only the supplied campaign data.

## Verification

A separate verifier reruns the program on three cases, compares results against generating truth, checks keyed evidence and reproduces condition-fit residuals. Reward is the fully automatic 0-1 task score; see environment/spec/SCORING.md. See the package README and validation reports for limitations and tested baselines. Container integration remains untested.
