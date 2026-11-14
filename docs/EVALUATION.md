# Evaluation protocol

SPR-Bench v0.9 has ten independent tasks. Each trial earns a binary reward: 1
only if every pytest check of that task's verifier passes, else 0. Partial
credit is not defined.

## Running

Use Harbor with Docker. Validate every task first: `-a oracle` must give
reward 1 and `-a nop` reward 0. Then run each agent configuration for k >= 5
trials per task (`-k 5`).

## Reporting

- Per task: number of passing trials out of k.
- Overall: pass@1 = mean binary reward over all trials of all ten tasks, with
  the per-task breakdown. Tasks are weighted equally.
- Record repository commit, Harbor version, model/provider, agent and its
  configuration, prompts, tools, resource limits, retries, randomness settings
  and cost. Report every trial, not only the best.
- Run `harbor analyze` on failing trials and keep the trajectories; for each
  failure, note which scientific step went wrong (the task READMEs and
  `authoring/variants.json` list the known failure modes).

## Interpretation

The tasks measure whether an agent can carry raw SPR data through expert
processing to correct scientific conclusions. The data are simulated from a
physical model with exact latent truth; noise, sampling and affinity ranges
are anchored on measured exports (`sources/anchors.json`). Passing does not
validate wet-lab practice, and failing a task does not identify which step
failed unless the trajectory is analyzed.

## Exposure

Ground truth, generators and default seeds are in this repository. Agents
with internet access could find them once it is public. For a blind
evaluation, regenerate each task with a private seed
(`authoring/generate.py --seed N`) and keep the result out of public view.
