"""Trusted local checks for the TB-Science track (tbsci/); executes only committed code.

For each staged task: the oracle solution must pass the task's own pytest
verifier, an empty submission must fail it, and the ground truth must cover
exactly the analytes in the agent-visible run method.
"""

import csv, json, shutil, subprocess, sys, tempfile
from pathlib import Path
from ingest import ROOT

TASKS = sorted(p.parent for p in (ROOT / "tbsci/tasks").rglob("task.toml"))


def pytest_passes(task, results):
    with tempfile.TemporaryDirectory(prefix="tbsci-") as tmp:
        tests = Path(tmp) / "tests"
        shutil.copytree(task / "tests", tests)
        test = tests / "test_outputs.py"
        test.write_text(
            test.read_text().replace('Path("/app/output/results.csv")', f'Path("{results}")')
        )
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(test)],
            cwd=tests,
            capture_output=True,
            text=True,
        )
        return r.returncode == 0, r.stdout.strip().splitlines()[-1:]


def main():
    assert TASKS, "no tbsci tasks found"
    for task in TASKS:
        truth = json.loads((task / "tests/ground_truth.json").read_text())["analytes"]
        cycles = csv.DictReader((task / "environment/data/cycles.csv").open())
        assert set(truth) == {r["analyte_id"] for r in cycles if r["analyte_id"]}
        with tempfile.TemporaryDirectory(prefix="tbsci-out-") as out:
            subprocess.run(
                [
                    sys.executable,
                    str(task / "solution/solve.py"),
                    "--data-dir",
                    str(task / "environment/data"),
                    "--output-dir",
                    out,
                ],
                check=True,
            )
            ok, tail = pytest_passes(task, Path(out) / "results.csv")
            assert ok, (task.name, "oracle failed", tail)
            ok, tail = pytest_passes(task, Path(out) / "missing.csv")
            assert not ok, (task.name, "empty submission passed")
        print(f"PASS: {task.relative_to(ROOT)} oracle passes, empty submission fails")


if __name__ == "__main__":
    main()
