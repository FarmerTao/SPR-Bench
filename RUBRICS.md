# Task-specific automatic rubrics

Every task is scored from 0 to 1. No report points are awarded.

## stat3-binding

Compare DPP and S3I-201 against mouse STAT3beta core 127-722. Distinguish a lack of measured response in this construct from a universal non-binder claim.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 15% | Exact record-ID coverage; `n`, `concentration_M`, `start_s`, `end_s` |
| response | 50% | `initial_median_RU`, `initial_sd_RU`, `p95_delta_RU`, `tail_delta_RU`, `auc_RU_s` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |
| binding_evidence | 20% | Exact compound coverage and scoped binding calls compared with Mtwebana and Prinsloo (2020), DOI 10.1186/s13104-020-05189-w. Author-reported interpretation; not independent adjudication. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## stat3-flow

Compare the three flow rates for S3I-201. Quantify differences without treating flow conditions as biological replicates or estimating a concentration-series KD.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 20% | Exact record-ID coverage; `n`, `concentration_M`, `start_s`, `end_s` |
| response | 65% | `initial_median_RU`, `initial_sd_RU`, `p95_delta_RU`, `tail_delta_RU`, `auc_RU_s` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## cyp3a4-sparse

Recover the eight fluconazole traces from sparse measured cells. Preserve each trace time grid and quantify its response without using the source fitted curves.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 20% | Exact record-ID coverage; `n`, `concentration_M`, `start_s`, `end_s` |
| response | 65% | `initial_median_RU`, `initial_sd_RU`, `p95_delta_RU`, `tail_delta_RU`, `auc_RU_s` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## cyp3a4-affinity

Fit the observed fluconazole concentration-response points, quantify residuals and concentration coverage. Do not interpret an apparent KD as target selectivity or a kinetic rate.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 15% | Exact record-ID coverage; `n`, `max_concentration_M` |
| response | 70% | `KD_M`, `Rmax_RU`, `offset_RU`, `rmse_RU`, `max_concentration_over_KD` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## lrrk2-traces

Analyze the seven DARPin E11 sensorgrams. Separate measured binding response from evidence of catalytic inhibition or therapeutic readiness.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 20% | Exact record-ID coverage; `n`, `concentration_M`, `start_s`, `end_s` |
| response | 65% | `initial_median_RU`, `initial_sd_RU`, `p95_delta_RU`, `tail_delta_RU`, `auc_RU_s` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## lrrk2-affinity

Refit seven observed E11 equilibrium responses with a free offset. Report residuals and coverage; author-fitted parameters are a comparison, not ground truth.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 15% | Exact record-ID coverage; `n`, `max_concentration_M` |
| response | 70% | `KD_M`, `Rmax_RU`, `offset_RU`, `rmse_RU`, `max_concentration_over_KD` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## klhdc2-hits

Compare measured sensorgrams for compounds 1 and 2. Avoid treating the neighboring fluorescence-polarization sheets as SPR data or treating representative traces as replicates.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 20% | Exact record-ID coverage; `n`, `concentration_M`, `start_s`, `end_s` |
| response | 65% | `initial_median_RU`, `initial_sd_RU`, `p95_delta_RU`, `tail_delta_RU`, `auc_RU_s` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## klhdc2-analogs

Analyze measured sensorgrams for compounds 5 and 6. Compare concentration-normalized evidence without inventing unreported controls or kinetic ground truth.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 20% | Exact record-ID coverage; `n`, `concentration_M`, `start_s`, `end_s` |
| response | 65% | `initial_median_RU`, `initial_sd_RU`, `p95_delta_RU`, `tail_delta_RU`, `auc_RU_s` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## tbxt-reference

Join active, reference and reference-subtracted late-binding report points by run/cycle/channel/window. Audit correction arithmetic and retain compound/series identities.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 25% | Exact record-ID coverage; `n`, `n_corrected_late`, `n_concentrations`, `max_concentration_M` |
| response | 60% | `max_corrected_RU`, `min_corrected_RU`, `mean_corrected_RU`, `max_reference_RU`, `dose_slope_RU_per_uM`, `max_reference_subtraction_error_RU` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.

## tbxt-triage

Summarize corrected late-binding responses, reference binding and dose trends. These are screening-evidence metrics; a large response alone does not establish specific binding or justify a drug-development decision.

| Component | Weight | Automatic criterion |
|---|---:|---|
| coverage | 20% | Exact record-ID coverage; `n`, `n_corrected_late`, `n_concentrations`, `max_concentration_M` |
| response | 65% | `max_corrected_RU`, `min_corrected_RU`, `mean_corrected_RU`, `max_reference_RU`, `dose_slope_RU_per_uM`, `max_reference_subtraction_error_RU` |
| provenance | 10% | Exact SHA-256 map of every supplied input file. |
| scope | 5% | Exact disclosed scope constraints in config.json; these are contract checks, not inferred biological ground truth. |

All checks within each component receive equal shares of that component. Missing expected records fail their field checks; unknown IDs fail the exact-coverage check. Two case scores are averaged. See SCORING.md for the formula and CONTRACT.md for numerical conventions/tolerances.
