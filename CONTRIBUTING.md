# Contributing

Use English for task prompts, contracts, code comments and benchmark documentation.
Discuss new scientific tasks or changes to scoring in an issue before implementation.
Bug fixes and documentation improvements are welcome as pull requests.

## Development

Use Python 3.12 and install `requirements-dev.txt` in a virtual environment.
Run `python tools/check_repository.py`, `python tools/test_scoring.py`,
`python tools/validate.py`, and `python tools/robustness.py` before submitting.
The host-side validators execute only trusted project programs; never substitute
an unknown submission on your host.

Edit canonical code in `tools/`. `python tools/rebuild.py` regenerates campaigns,
copies implementations into tasks, updates documentation, and validates results.
It overwrites generated task files. Review the resulting diff and run
`python tools/check_repository.py` again. Do not hand-edit generated truth to
make a solver pass.

Every scoring change must include an example of the affected behavior, regression
coverage, updated scoring documentation and a version/changelog entry. Scores
from different scoring versions must not be silently combined. Data changes must
update checksums and identify whether previous evaluations remain comparable.

New scientific tasks need a stated evidence boundary, provenance, a generating
truth or independently adjudicated reference, a working reference solution,
plausible failing solutions and at least one reasonable alternative method.
Do not claim expert validation, realistic difficulty or agent performance without
measured evidence. Real experimental data require documented redistribution
rights, de-identification where applicable and independent review.

PRs should state the problem, resulting behavior and exact validation commands.
Do not commit model credentials, private evaluation datasets, run logs or answers
from unrelated evaluations. Contributions are licensed under the repository's
MIT license. Be respectful and focus reviews on evidence and reproducibility.
