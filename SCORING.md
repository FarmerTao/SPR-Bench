# Scoring

Each task's official reward is binary. A rule-based verifier reruns the
submission on every case and pytest asserts that every coverage, response,
binding-evidence, provenance and scope check passes; test.sh writes 1 only if
all pass, else 0. The weighted partial score below is a diagnostic written to
`metrics.json` as `partial_reward`.

| Task family | Coverage | Response | Binding evidence | Provenance | Scope |
|---|---:|---:|---:|---:|---:|
| Trace | 20% | 65% | 0% | 10% | 5% |
| Affinity | 15% | 70% | 0% | 10% | 5% |
| STAT3 binding | 15% | 50% | 20% | 10% | 5% |
| TBXT operational binding | 15% | 50% | 20% | 10% | 5% |

Coverage checks exact record IDs plus the listed coverage fields. Response checks
the listed numerical fields against the reference computed from the supplied
measurements. Provenance checks the SHA-256 manifest of the input files. Scope
checks the disclosed claims exactly.

For N expected records and F coverage fields, coverage contains 1 + N*F checks:
one exact ID-set check and one check per expected record/field. Response contains
N*R checks for R response fields. Provenance has one check. Scope has one check
per disclosed claim.

Missing output, invalid JSON, duplicate JSON keys/record IDs, nonfinite JSON,
program failure or timeout gives that case zero. A bookkeeping-only submission
(IDs, counts, hashes, copied claims and a constant binding call, no analysis)
earns partial_reward of 0.24-0.43 but binary reward 0; tools/validate.py enforces this. Missing fields/records fail
corresponding checks. An entirely empty record list can earn only provenance and
scope credit (at most 0.15). A record list that passes coverage/provenance/scope
but no response checks still earns those weights under the official score; its
analysis_reward is zero. Unexpected record IDs fail exact coverage. Null matches
only a documented null reference value. Counts must match exactly. All numerical
tolerances are in CONTRACT.md.

The reference numbers are recomputed from selected measurements, not synthesized
kinetic truth. Source-fitted curves are excluded. Apparent KD fits use a specified
least-squares model; the score does not claim this is the true biological
mechanism. The disclosed scope component is intentionally easy and should be
reported separately when comparing scientific analysis ability.

Report all ten task pass rates and study means. The recommended overall score is
the mean binary reward over the ten tasks. Macrocycle, STAT3 and TBXT each contribute one
task; LRRK2, ISG65 and D-box contribute multiple related tasks, so study means are
descriptive rather than equally weighted. A missing task counts as zero. Do not treat ten tasks or
the two robustness cases as independent biological replicates. Do not pool scores
with the archived synthetic version or with later scoring versions.

All fixtures, reference outputs and source papers are public. This is a public
fixture evaluation; it is not a blind assessment. Local oracle scores and scoring
regression tests measure implementation consistency, not model capability or
scientific label validity. No manually graded report or model-as-judge is used.
