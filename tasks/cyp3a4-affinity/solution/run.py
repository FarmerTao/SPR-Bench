"""Reproducible numerical reference, not an assertion of biological ground truth."""

import argparse, csv, hashlib, json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar


def analyze(data):
    data = Path(data)
    cfg = json.loads((data / "config.json").read_text())
    rows = list(csv.DictReader((data / "measurements.csv").open()))
    kind = cfg["kind"]
    groups = {}
    for r in rows:
        key = (
            r["trace_id"]
            if kind == "trace"
            else (
                r["compound"]
                if kind == "affinity"
                else r["compound"] + "|" + r["channel"]
            )
        )
        groups.setdefault(key, []).append(r)
    records = []
    for key, g in sorted(groups.items()):
        rec = {"id": key}
        if kind == "trace":
            g = sorted(g, key=lambda r: float(r["time_s"]))
            t = np.array([float(r["time_s"]) for r in g])
            y = np.array([float(r["response_RU"]) for r in g])
            initial = y[t < t[0] + 20]
            base = float(np.median(initial))
            tail = y[t > t[-1] - 20]
            rec.update(
                n=len(g),
                concentration_M=float(g[0]["concentration_M"]),
                start_s=float(t[0]),
                end_s=float(t[-1]),
                initial_median_RU=base,
                initial_sd_RU=float(np.std(initial, ddof=1)),
                p95_delta_RU=float(np.percentile(y, 95) - base),
                tail_delta_RU=float(np.mean(tail) - base),
                auc_RU_s=float(np.trapezoid(y - base, t)),
            )
        elif kind == "affinity":
            g = sorted(g, key=lambda r: float(r["concentration_M"]))
            x = np.array([float(r["concentration_M"]) * 1e6 for r in g])
            y = np.array([float(r["response_RU"]) for r in g])

            def fit(logkd):
                a = np.column_stack([x / (10**logkd + x), np.ones(len(x))])
                p = np.linalg.lstsq(a, y, rcond=None)[0]
                if p[0] < 0:
                    p = np.array([0, np.mean(y)])
                return float(np.sum((a @ p - y) ** 2)), p

            # Coarse global scan then bounded refinement avoids dependence on initial guess.
            grid = np.linspace(-6, 6, 241)
            i = int(np.argmin([fit(v)[0] for v in grid]))
            lo = grid[max(i - 1, 0)]
            hi = grid[min(i + 1, len(grid) - 1)]
            opt = minimize_scalar(
                lambda v: fit(v)[0],
                bounds=(lo, hi),
                method="bounded",
                options={"xatol": 1e-12},
            )
            sse, p = fit(opt.x)
            rec.update(
                n=len(g),
                KD_M=float(10**opt.x * 1e-6),
                Rmax_RU=float(p[0]),
                offset_RU=float(p[1]),
                rmse_RU=float(np.sqrt(sse / len(x))),
                max_concentration_M=float(x.max() * 1e-6),
                max_concentration_over_KD=float(x.max() / 10**opt.x),
            )
        else:
            late = [r for r in g if "binding late" in r["window"].lower()]
            corrected = [r for r in late if r["sensorgram_type"] == "Corrected"]
            reference = [r for r in late if r["sensorgram_type"] == "Reference"]
            if not corrected:
                continue
            x = np.array([float(r["concentration_M"]) * 1e6 for r in corrected])
            y = np.array([float(r["response_RU"]) for r in corrected])
            order = np.argsort(x)
            rec.update(
                n=len(g),
                n_corrected_late=len(corrected),
                n_concentrations=len(set(x)),
                max_concentration_M=float(x.max() * 1e-6),
                max_corrected_RU=float(y.max()),
                min_corrected_RU=float(y.min()),
                mean_corrected_RU=float(y.mean()),
                max_reference_RU=max(float(r["response_RU"]) for r in reference),
                dose_slope_RU_per_uM=(
                    float(np.polyfit(x, y, 1)[0]) if len(set(x)) > 1 else 0.0
                ),
            )
            pairs = {}
            for r in late:
                pairs.setdefault((r["run"], r["cycle"], r["channel"], r["window"]), {})[
                    r["sensorgram_type"]
                ] = float(r["response_RU"])
            errors = [
                abs(v["Active"] - v["Reference"] - v["Reference subtracted"])
                for v in pairs.values()
                if {"Active", "Reference", "Reference subtracted"} <= v.keys()
            ]
            rec["max_reference_subtraction_error_RU"] = max(errors) if errors else None
        records.append(rec)
    assessments = {}
    if cfg["task"] == "stat3-binding":
        # Study-specific baseline heuristic, checked against published scoped conclusions.
        # It is not a general SPR binding classifier.
        slopes = {}
        for g in groups.values():
            window = [r for r in g if 10 <= float(r["time_s"]) <= 55]
            slope = float(
                np.polyfit(
                    [float(r["time_s"]) for r in window],
                    [float(r["response_RU"]) for r in window],
                    1,
                )[0]
            )
            slopes.setdefault(g[0]["compound"], []).append(slope)
        assessments = {
            k: (
                "interaction_supported"
                if float(np.median(v)) > 0.1
                else "no_measurable_binding_under_tested_conditions"
            )
            for k, v in slopes.items()
        }
    return {
        "records": records,
        "binding_assessments": assessments,
        "claims": cfg["required_claims"],
        "input_sha256": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(data.iterdir())
            if p.is_file()
        },
    }


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--input-dir", required=True)
    a.add_argument("--output-dir", required=True)
    a = a.parse_args()
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(
        json.dumps(analyze(a.input_dir), indent=2, allow_nan=False) + "\n"
    )


if __name__ == "__main__":
    main()
