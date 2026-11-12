# Rubrics

Fields and weights per task. Coverage and response fields are listed in the executable contract; provenance and scope are weighted checks.

## stat3-binding

STAT3: compare measured response and scoped negative evidence

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 15% | n, concentration_M, start_s, end_s |
| Response | 50% | initial_median_RU, initial_sd_RU, p95_delta_RU, tail_delta_RU, auc_RU_s |
| Binding evidence | 20% | binding_assessments |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## tbxt-binding

TBXT: operational binding triage from corrected report points

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 15% | n, n_corrected_late, n_concentrations, max_concentration_M |
| Response | 50% | max_corrected_RU, min_corrected_RU, mean_corrected_RU, max_reference_RU, dose_slope_RU_per_uM, max_reference_subtraction_error_RU |
| Binding evidence | 20% | binding_assessments |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## lrrk2-traces

LRRK2: analyze protein binder concentration series

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 20% | n, concentration_M, start_s, end_s |
| Response | 65% | initial_median_RU, initial_sd_RU, p95_delta_RU, tail_delta_RU, auc_RU_s |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## lrrk2-affinity

LRRK2: refit E11 affinity with a free offset

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 15% | n, max_concentration_M |
| Response | 70% | KD_M, Rmax_RU, offset_RU, rmse_RU, max_concentration_over_KD |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## macrocycle-traces

Designed macrocycles: analyze SPR sensorgrams

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 20% | n, concentration_M, start_s, end_s |
| Response | 65% | initial_median_RU, initial_sd_RU, p95_delta_RU, tail_delta_RU, auc_RU_s |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## isg65-c3b-traces

ISG65 C3b binding: analyze SPR sensorgrams

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 20% | n, concentration_M, start_s, end_s |
| Response | 65% | initial_median_RU, initial_sd_RU, p95_delta_RU, tail_delta_RU, auc_RU_s |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## isg65-c3d-traces

ISG65 C3d binding: analyze SPR sensorgrams

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 20% | n, concentration_M, start_s, end_s |
| Response | 65% | initial_median_RU, initial_sd_RU, p95_delta_RU, tail_delta_RU, auc_RU_s |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## isg65-affinity

ISG65: apparent steady-state affinity

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 15% | n, max_concentration_M |
| Response | 70% | KD_M, Rmax_RU, offset_RU, rmse_RU, max_concentration_over_KD |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## dbox-d20-affinity

D-box D20: fit apparent steady-state affinity

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 15% | n, max_concentration_M |
| Response | 70% | KD_M, Rmax_RU, offset_RU, rmse_RU, max_concentration_over_KD |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |

## dbox-d21-affinity

D-box D21: fit apparent steady-state affinity

| Category | Weight | Fields |
|---|---:|---|
| Coverage | 15% | n, max_concentration_M |
| Response | 70% | KD_M, Rmax_RU, offset_RU, rmse_RU, max_concentration_over_KD |
| Provenance | 10% | input_sha256 |
| Scope | 5% | disclosed claims |
