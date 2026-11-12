"""Trusted local verification. Never execute unknown submissions on the host."""

import csv, hashlib, io, json, tempfile, zipfile
from pathlib import Path
import numpy as np
import openpyxl
from scipy.optimize import curve_fit
from ingest import ROOT, dump
from verifier import evaluate, prepare_submission, score


def audit_submission_hardening():
    with tempfile.TemporaryDirectory(prefix="spr-submission-") as tmp:
        root = Path(tmp) / "submission"
        root.mkdir()
        (root / "run.py").write_text("print('ok')\n")
        assert prepare_submission(root / "run.py") == (root / "run.py").resolve()
        (root / "escape").symlink_to("/")
        try:
            prepare_submission(root / "run.py")
        except ValueError:
            pass
        else:
            raise AssertionError("symlinked submission accepted")


def audit_sources():
    for item in json.loads((ROOT / "sources/manifest.json").read_text()):
        assert (
            hashlib.sha256((ROOT / "sources" / item["file"]).read_bytes()).hexdigest()
            == item["sha256"]
        )
    books = {
        k: openpyxl.load_workbook(
            ROOT / "sources/originals" / v, read_only=True, data_only=True
        )
        for k, v in [
            ("STAT3", "stat3.xlsx"),
            ("TBXT", "tbxt.xlsx"),
            ("Macrocycle-Fig2", "macrocycle-fig2.xlsx"),
            ("Macrocycle-Fig4", "macrocycle-fig4.xlsx"),
            ("ISG65", "isg65-fig2-data1.xlsx"),
            ("D-box", "dbox-fig4-data1.xlsx"),
        ]
    }
    sheets = {}
    count = 0
    with zipfile.ZipFile(ROOT / "sources/originals/lrrk2.zip") as z:
        for name in ["Sensorgrams_E11.txt", "Steady state_E11.txt"]:
            sheets["LRRK2", name] = list(
                csv.reader(io.StringIO(z.read(name).decode("cp1252")), delimiter="\t")
            )
    for item in json.loads((ROOT / "data_manifest.json").read_text()):
        p = ROOT / "data" / item["file"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item["sha256"]
        rows = list(csv.DictReader(p.open()))
        assert len(rows) == item["rows"]
        for row in rows:
            source = row["source"]
            name = row["source_sheet"]
            k = source
            if (k, name) not in sheets:
                sheets[k, name] = list(books[k][name].values)
            original = sheets[k, name][int(row["source_row"]) - 1]
            col = int(row.get("source_column", 10)) - 1
            assert float(original[col]) == float(row["response_RU"]), (p, row)
            if "time_s" in row:
                tc = (
                    6
                    if source == "TBXT"
                    else col - 1
                    if source == "LRRK2" or source.startswith("Macrocycle")
                    else 0
                )
                assert float(original[tc]) == float(row["time_s"])
            count += 1
    return count


def main():
    audit_submission_hardening()
    n = audit_sources()
    results = {}
    semantics = {}
    with tempfile.TemporaryDirectory(prefix="spr-validation-") as tmp:
        tmp = Path(tmp)
        for task in sorted((ROOT / "tasks").iterdir()):
            report = evaluate(
                task / "solution/run.py", task / "tests", tmp / task.name, isolate=False
            )
            assert abs(report["reward"] - 1) < 1e-12, (task.name, report["reward"])
            assert abs(report["analysis_reward"] - 1) < 1e-12, (
                task.name,
                report["analysis_reward"],
            )
            results[task.name] = {
                "reward": report["reward"],
                "analysis_reward": report.get("analysis_reward"),
                "cases": len(report["cases"]),
            }
            case = task / "tests/cases/observed"
            cfg = json.loads((task / "tests/scoring.json").read_text())
            expected = case / "expected.json"
            value = json.loads(expected.read_text())
            bad = tmp / "bad.json"
            bad.write_text("{}")
            assert score(bad, expected, cfg)["score"] == 0
            duplicate = dict(value)
            duplicate["records"] = value["records"] + [value["records"][0]]
            bad.write_text(json.dumps(duplicate))
            assert score(bad, expected, cfg)["score"] == 0
            missing = dict(value)
            missing["records"] = []
            bad.write_text(json.dumps(missing))
            assert (
                score(bad, expected, cfg)["score"]
                <= 0.15 + cfg["weights"].get("binding_evidence", 0) + 1e-12
            )
            bad.write_text('{"records":1e999}')
            assert score(bad, expected, cfg)["score"] == 0
            bad.write_text('{"records":NaN}')
            assert score(bad, expected, cfg)["score"] == 0
            assert (
                score(expected, task / "tests/cases/subset/expected.json", cfg)["score"]
                < 0.8
            ), "fixed output escaped subset check"
            wrong = json.loads(expected.read_text())
            for r in wrong["records"]:
                for f in cfg["fields"]["response"]:
                    r[f] = 1e90
            bad.write_text(json.dumps(wrong))
            assert (
                score(bad, expected, cfg)["score"]
                <= 1 - cfg["weights"]["response"] + 1e-12
            )
            semantics[task.name] = (
                "empty, duplicate, nonfinite, missing records, fixed output, wrong response checks passed"
            )
        alternatives = {}
        for name in ["dbox-d20-affinity", "lrrk2-affinity"]:
            p = ROOT / "tasks" / name / "environment/data"
            rows = list(csv.DictReader((p / "measurements.csv").open()))
            x = np.array([float(r["concentration_M"]) * 1e6 for r in rows])
            y = np.array([float(r["response_RU"]) for r in rows])
            f = lambda c, rm, k, b: rm * c / (k + c) + b
            fit, _ = curve_fit(
                f,
                x,
                y,
                p0=[max(y), np.median(x), min(y)],
                bounds=([0, 1e-6, -np.inf], [np.inf, 1e6, np.inf]),
                maxfev=100000,
                ftol=1e-12,
                xtol=1e-12,
                gtol=1e-12,
            )
            expected = json.loads(
                (
                    ROOT / "tasks" / name / "tests/cases/observed/expected.json"
                ).read_text()
            )
            r = expected["records"][0]
            r.update(
                Rmax_RU=float(fit[0]),
                KD_M=float(fit[1] * 1e-6),
                offset_RU=float(fit[2]),
                rmse_RU=float(np.sqrt(np.mean((f(x, *fit) - y) ** 2))),
                max_concentration_over_KD=float(x.max() / fit[1]),
            )
            p = tmp / "alternative.json"
            p.write_text(json.dumps(expected))
            cfg = json.loads((ROOT / "tasks" / name / "tests/scoring.json").read_text())
            s = score(
                p, ROOT / "tasks" / name / "tests/cases/observed/expected.json", cfg
            )["score"]
            assert abs(s - 1) < 1e-12
            alternatives[name] = {"score": s, "KD_M": r["KD_M"]}
    dump(
        ROOT / "validation.json",
        {
            "source_measurements_checked_cell_by_cell": n,
            "tasks": results,
            "alternative_optimizer": alternatives,
            "host_only": True,
            "harbor_docker_end_to_end": "not_run",
            "expert_adjudication": "not_completed",
            "agent_baseline": "not_run",
        },
    )
    dump(ROOT / "scoring_validation.json", semantics)
    print(
        f"PASS: {n} source measurement cells, 10 tasks x 2 cases, scoring regressions, "
        "submission symlink hardening, 2 alternative fits"
    )


if __name__ == "__main__":
    main()
