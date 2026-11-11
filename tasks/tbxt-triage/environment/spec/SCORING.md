# Automatic scoring v0.6

Every task has its own score in [0,1]. Both cases contain real observations.
For case c, category k, let m(c,k) be passed checks / expected checks, or zero if
there are no checks. The case score is sum_k w(k)*m(c,k). The task score is the
arithmetic mean of its two case scores. Every task has weights summing to 1.

| Task type | Coverage | Response / fit | Provenance | Disclosed scope | Binding evidence |
|---|---:|---:|---:|---:|---:|
| Trace (except STAT3 binding) and TBXT triage | 20% | 65% | 10% | 5% | 0% |
| STAT3 binding | 15% | 50% | 10% | 5% | 20% |
| Affinity | 15% | 70% | 10% | 5% | 0% |
| TBXT reference audit | 25% | 60% | 10% | 5% | 0% |

For N expected records and F coverage fields, coverage contains 1 + N*F checks:
one exact ID-set check and one check per expected record/field. Response contains
N*R checks for R response fields. Provenance has one check. Scope has one check
per disclosed claim. STAT3 binding evidence has one exact compound-coverage
check plus one check for each source-supported scoped call. These labels are
withheld from the agent image, but public in the repository and source article.
No weighting depends on the amount of optional prose.
See RUBRICS.md for exact fields and weights for each of ten tasks.

Missing output, invalid JSON, duplicate JSON keys/record IDs, nonfinite JSON,
program failure or timeout gives that case zero. Missing fields/records fail
corresponding checks. An entirely empty record list can earn only provenance and
scope credit (at most 0.15); STAT3 binding can additionally earn up to 0.20
for source-consistent calls even if numerical evidence is absent. This partial
credit does not constitute successful numerical analysis. Unexpected record
IDs fail exact coverage. Null matches only a documented null reference value.
Counts must match exactly. All numerical tolerances are in CONTRACT.md.

The reference numbers are recomputed from selected measurements, not synthesized
kinetic truth. Measured source fit curves are excluded. Apparent KD fits use a
specified least-squares model; the score does not claim this is the true biological
mechanism. The disclosed scope component is intentionally easy and should be
reported separately when comparing scientific analysis ability.

Report all ten task scores and study means. The recommended overall score is the
mean of five study means (each study has two tasks in this release, so this equals
the ten-task mean). A missing task counts as zero. Do not treat ten tasks or the
two robustness cases as independent biological replicates. Do not pool scores
with the archived synthetic version or with later scoring versions.

The STAT3 call rubric uses author-reported scoped conclusions for the tested
compounds, construct and conditions (DOI
10.1186/s13104-020-05189-w). It does not assert universal nonbinding, selectivity,
or suitability for development. No independent expert adjudication is claimed.

All fixtures, reference outputs and source papers are public. This is a public
fixture evaluation; it is not a blind assessment. Local oracle scores and scoring
regression tests measure implementation consistency, not model capability or
scientific label validity. No manually graded report or model-as-judge is used.
