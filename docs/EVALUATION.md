# Evaluation protocol

This is a public protein/antibody SPR pilot. Ten task scores are computed
individually, with an aggregate mean over the ten tasks. Macrocycle, STAT3 and
TBXT contribute one task each; LRRK2, ISG65 and D-box contain related tasks and
are not independent replicates. No confidence interval based on ten
independent studies is justified.

All inputs, expected outputs, reference programs and sources are public. Agent
images exclude reference/test material, but this cannot undo prior exposure.
Renaming IDs and taking measured subsets tests program reuse, not blind scientific
generalization. A blind release requires held-out studies and independently
reviewed labels, versioned acquisition metadata, a freeze date and an exposure
policy.

For any run record: repository commit, data/scoring version, Harbor version,
model/provider, agent configuration, prompts, tools, resource limits, retries,
randomness settings and costs. Report every trial, not only the best retry.
Keep per-task metrics and logs with credentials removed. A missing task counts
as zero. Report the binary reward (pass rate over all trials); analysis_reward
and partial_reward are diagnostics. Do not pool results across synthetic v0.5,
experimental v0.6-v0.8 core tasks, or the simulated TB-Science track.

Local tests check source cell provenance, numerical consistency, defective outputs
and an alternative optimizer. They do not establish independent scientific
adjudication or secure Harbor runtime integration. No real-agent baseline has yet
been measured. Harbor + Docker end-to-end testing remains outstanding.

Do not interpret the score as validated binding classification, drug candidacy,
clinical utility, or proof of wet-lab reliability. The present score primarily
measures reproducible numerical analysis under an explicit contract. Expanded
biological decision scoring requires expert-reviewed evidence and orthogonal
validation; these have not been fabricated to fill gaps in public datasets.
