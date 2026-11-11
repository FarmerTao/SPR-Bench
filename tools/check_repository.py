"""Structural, schema and generated-copy checks; does not execute submissions."""

import hashlib, json, tomllib
from pathlib import Path
from harbor.models.task.config import TaskConfig
from ingest import ROOT


def main():
    catalog = json.loads((ROOT / "task_catalog.json").read_text())
    assert len(catalog) == 10
    assert {p.name for p in (ROOT / "tasks").iterdir()} == {t["id"] for t in catalog}
    for t in catalog:
        p = ROOT / "tasks" / t["id"]
        TaskConfig.model_validate(tomllib.loads((p / "task.toml").read_text()))
        cfg = json.loads((p / "tests/scoring.json").read_text())
        assert abs(sum(cfg["weights"].values()) - 1) < 1e-12
        for source, dest in [
            ("tools/reference.py", "solution/run.py"),
            ("tools/verifier.py", "tests/verifier.py"),
            ("CONTRACT.md", "environment/spec/CONTRACT.md"),
            ("SCORING.md", "environment/spec/SCORING.md"),
        ]:
            assert (ROOT / source).read_bytes() == (p / dest).read_bytes(), (
                t["id"],
                dest,
            )
        assert {x.name for x in (p / "environment").iterdir()} == {
            "Dockerfile",
            "data",
            "spec",
        }
        assert {x.name for x in (p / "environment/data").iterdir()} == {
            "measurements.csv",
            "config.json",
        }
        assert {x.name for x in (p / "tests/cases").iterdir()} == {"observed", "subset"}
        for case in (p / "tests/cases").iterdir():
            expected = json.loads((case / "expected.json").read_text())
            assert expected["records"]
            assert expected["input_sha256"] == {
                x.name: hashlib.sha256(x.read_bytes()).hexdigest()
                for x in sorted((case / "data").iterdir())
            }
        for f in ["config.json", "measurements.csv"]:
            assert (p / "environment/data" / f).read_bytes() == (
                p / "tests/cases/observed/data" / f
            ).read_bytes()
        assert "synthetic" not in (p / "task.toml").read_text()
    for source in json.loads((ROOT / "sources/manifest.json").read_text()):
        assert (
            hashlib.sha256((ROOT / "sources" / source["file"]).read_bytes()).hexdigest()
            == source["sha256"]
        )
    print(
        "PASS: ten Harbor 0.25.0 configurations, generated code, input isolation layout, manifests and scoring weights"
    )


if __name__ == "__main__":
    main()
