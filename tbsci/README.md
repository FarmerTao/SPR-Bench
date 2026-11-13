# TB-Science track

Tasks staged for submission to
[Terminal-Bench-Science](https://github.com/harbor-framework/terminal-bench-science).
The directory mirrors that repository's layout (`tasks/<domain>/<field>/<task>/`),
so a task folder can be copied into a fork unchanged.

This is a separately named **simulation track**. Its data are generated from a
physical model with known latent truth (see each task's `authoring/`), and its
scores are never pooled with the measured-data core tier in `tasks/`.

| Task | Domain / field | Agent budget | Expert estimate |
|---|---|---|---|
| [spr-kinetic-triage](tasks/life-sciences/biology/spr-kinetic-triage/instruction.md) | life sciences / biology | 8 h | 6 h |

## Before opening a TB-Science PR

1. Get the task proposal approved first (TB-Science `rubrics/task-proposal.md`,
   Discord `#tb-science-task-proposals`); the PR must link it.
2. Replace every `TODO` in `task.toml` (organization, profile, relevant
   experience, conflicts of interest), then regenerate the README header with
   TB-Science's `tools/task-readme/generate.py --force <task>`.
3. Rewrite `instruction.md` in your own words. TB-Science requires
   author-written instructions and screens them with AI-text detection; the
   current text is a draft that fixes the required content (inputs, output
   schema, class definitions, graded metrics, time-limit suffix).
4. Run their checks from a fork: `ci_checks/check-*.sh <task>`,
   `harbor check -r rubrics/task-implementation.toml <task>`,
   `harbor run -p <task> -a oracle` (expect 1.0), `-a nop` (expect 0), then real
   agent trials and `harbor analyze -r rubrics/trial-analysis.toml -m <model>`.
5. Mind exposure. TB-Science agents have internet access, and
   `tests/ground_truth.json` plus `authoring/generate.py` with its default seed
   reproduce the answers. Pushing `tbsci/` to a public repository before the
   benchmark freeze makes them searchable; keep it on a private branch until
   submission.

Locally, `python tools/check_tbsci.py` verifies that the oracle passes and an
empty submission fails each staged task's own pytest verifier.
