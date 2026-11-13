# Changelog

## 0.8.0 — 2026-11-13

- Adopt the Terminal-Bench-Science task format for the core tier: canary
  strings, author metadata, task-voice instructions with the time-limit suffix,
  three-section task READMEs, pytest + CTRF verifier with pinned tooling, and a
  binary reward (all checks on all cases). Partial scores move to metrics.json.
- Stop shipping SCORING.md inside agent environments.
- Alias STAT3/TBXT robustness-case compounds in hash order so aliases no longer
  reveal the alphabetical order of real compound names.
- Add a bookkeeping-only floor submission to validate.py; it must earn reward 0.
- Add the separately named TB-Science track `tbsci/` with
  `spr-kinetic-triage`: raw dual-flow-cell multi-cycle kinetics on simulated
  data with latent truth, a reference and an independent solver, and
  seed-calibrated tolerances.

## 0.7.0 — 2026-11-12

- Build ten SPR tasks from six studies: LRRK2/DARPin, designed macrocycles,
  ISG65/C3, D-box peptides, STAT3, and TBXT.
- Bundle seven attributable original files with exact source-cell mappings,
  hashes, licenses and reproducible extraction of 55 sensorgrams, 57 affinity
  endpoints and 23,040 TBXT report-point rows.
- Add ISG65 C3b/C3d trace tasks and an ISG65 apparent-affinity task (measured
  end-of-association endpoints), plus D20/D21 trace and affinity tasks.
- Add a STAT3 binding/non-binding task with author-scoped DPP/S3I-201 calls,
  and a TBXT operational binding-triage task with a disclosed 10 RU threshold,
  input hashes and a binding-evidence scoring category.
- Keep source-fitted curves out of every task input; scope claims disclose
  single-concentration and derived-endpoint limits.
- Remove the STAT3, CYP3A4, KLHDC2 and TBXT small-molecule tasks from the active
  set. The archived v0.6 release remains in git history.
- Limit claims explicitly: no expert-adjudicated binding/advancement ground
  truth, no agent baseline, and Harbor + Docker end-to-end validation still
  outstanding.

## 0.6.0 — 2026-11-11

- Experimental-data pilot with ten mixed small-molecule/protein SPR tasks.
