"""Build ten Harbor tasks using only extracted experimental measurements."""

import csv, json, hashlib, shutil, sys
from pathlib import Path
from ingest import ROOT, dump, write
from reference import analyze

TASKS = [
    (
        "stat3-binding",
        "STAT3: compare measured response and scoped negative evidence",
        "stat3.csv",
        "trace",
        "STAT3",
        {},
        "Compare DPP and S3I-201 against mouse STAT3beta core 127-722. Distinguish a lack of measured response in this construct from a universal non-binder claim.",
    ),
    (
        "tbxt-binding",
        "TBXT: operational binding triage from corrected report points",
        "tbxt.csv",
        "report",
        "TBXT",
        {
            "operational_threshold_RU": 10.0,
            "labels_are_benchmark_rule_not_author_truth": True,
        },
        "Compute corrected late-binding report points and classify each compound with the disclosed 10 RU operational threshold. This is a triage rule, not author-reported binding truth.",
    ),
    (
        "lrrk2-traces",
        "LRRK2: analyze protein binder concentration series",
        "lrrk2-traces.csv",
        "trace",
        "LRRK2",
        {
            "analyte_class": "protein_DARPin",
            "catalytic_inhibition_established_by_SPR": False,
        },
        "Analyze the seven DARPin E11 sensorgrams. Separate measured binding response from evidence of catalytic inhibition or therapeutic readiness.",
    ),
    (
        "lrrk2-affinity",
        "LRRK2: refit E11 affinity with a free offset",
        "lrrk2-affinity.csv",
        "affinity",
        "LRRK2",
        {"affinity_type": "apparent_steady_state", "source_fit_is_ground_truth": False},
        "Refit seven observed E11 equilibrium responses with a free offset. Report residuals and coverage; author-fitted parameters are a comparison, not ground truth.",
    ),
    (
        "macrocycle-traces",
        "Designed macrocycles: analyze SPR sensorgrams",
        "macrocycle-traces.csv",
        "trace",
        "Macrocycle",
        {
            "source_fit_columns_used": False,
            "single_concentration_traces_do_not_establish_KD": True,
        },
        "Analyze measured SPR sensorgrams for three designed macrocyclic binders (MCB_D2/MCL1, MDB_D8/MDM2 and RBB_D10/RbtA). Report the benchmark trace summaries; do not use the source-fitted curves or treat a single-concentration trace as a KD measurement.",
    ),
    (
        "isg65-c3b-traces",
        "ISG65 C3b binding: analyze SPR sensorgrams",
        "isg65-traces.csv",
        "trace",
        "ISG65",
        {
            "source_fit_columns_used": False,
            "kinetic_rates_identifiable": False,
        },
        "Analyze measured C3b-binding SPR sensorgrams for ISG65 WT, ISG65ΔL2 and ISG65 L2N188A. Report the benchmark trace summaries; do not use the source-fitted columns or infer kinetic rates.",
    ),
    (
        "isg65-c3d-traces",
        "ISG65 C3d binding: analyze SPR sensorgrams",
        "isg65-traces.csv",
        "trace",
        "ISG65",
        {
            "source_fit_columns_used": False,
            "kinetic_rates_identifiable": False,
        },
        "Analyze measured C3d-binding SPR sensorgrams for ISG65 WT, ISG65ΔL2 and ISG65 L2N188A. Report the benchmark trace summaries; do not use the source-fitted columns or infer kinetic rates.",
    ),
    (
        "isg65-affinity",
        "ISG65: apparent steady-state affinity",
        "isg65-affinity.csv",
        "affinity",
        "ISG65",
        {
            "affinity_type": "apparent_steady_state",
            "source_fit_is_ground_truth": False,
        },
        "Fit the six observed ISG65 concentration-response series (C3b/C3d × WT/ΔL2/L2N188A) using the measured end-of-association responses. Report residuals and coverage; do not treat the fit as a kinetic mechanism.",
    ),
    (
        "dbox-d20-affinity",
        "D-box D20: fit apparent steady-state affinity",
        "dbox-affinity.csv",
        "affinity",
        "D-box",
        {
            "affinity_type": "apparent_steady_state",
            "source_fit_is_ground_truth": False,
        },
        "Fit the observed D20 concentration-response endpoints. Report residuals and coverage; an apparent KD does not establish a mechanism.",
    ),
    (
        "dbox-d21-affinity",
        "D-box D21: fit apparent steady-state affinity",
        "dbox-affinity.csv",
        "affinity",
        "D-box",
        {
            "affinity_type": "apparent_steady_state",
            "source_fit_is_ground_truth": False,
        },
        "Fit the observed D21 concentration-response endpoints. Report residuals and coverage; an apparent KD does not establish a mechanism.",
    ),
]
CLAIMS = {
    "drug_readiness": "not_established",
    "biological_ground_truth_available": False,
}
FIELDS = {
    "trace": {
        "coverage": ["n", "concentration_M", "start_s", "end_s"],
        "response": [
            "initial_median_RU",
            "initial_sd_RU",
            "p95_delta_RU",
            "tail_delta_RU",
            "auc_RU_s",
        ],
    },
    "affinity": {
        "coverage": ["n", "max_concentration_M"],
        "response": [
            "KD_M",
            "Rmax_RU",
            "offset_RU",
            "rmse_RU",
            "max_concentration_over_KD",
        ],
    },
    "report": {
        "coverage": [
            "n",
            "n_corrected_late",
            "n_concentrations",
            "max_concentration_M",
        ],
        "response": [
            "max_corrected_RU",
            "min_corrected_RU",
            "mean_corrected_RU",
            "max_reference_RU",
            "dose_slope_RU_per_uM",
            "max_reference_subtraction_error_RU",
        ],
    },
}
WEIGHTS = {"coverage": 0.20, "response": 0.65, "provenance": 0.10, "scope": 0.05}
CONTRACT = """# Executable output contract
Create `/app/submission/run.py`, runnable as:
`python run.py --input-dir INPUT --output-dir OUTPUT`.
It must read the supplied directory and write `OUTPUT/results.json`. Use Python, NumPy, SciPy, pandas or standard libraries. No network is available. The verifier reruns your program on the visible input and a deterministic subset with renamed IDs and reordered rows. Compound names and source-sheet metadata may also be aliased in the subset. All response values remain real measured values; these are robustness cases, not independent experiments. Do not hardcode record IDs or results.

JSON schema: `{"records":[{"id":"...", ...numeric fields...}], "claims":{...}, "input_sha256":{"config.json":"...","measurements.csv":"..."}}`. Include exactly the required records, no duplicate IDs. Hash every input file. `claims` must retain the explicitly supplied evidence-scope constraints in config.json; these are disclosed guardrails, not a hidden biological reasoning test. The 5% scope score is a contract check. No prose report is scored.

For stat3-binding only, also output `binding_assessments`: a mapping from each compound present to one of `interaction_supported`, `no_measurable_binding_under_tested_conditions`, or `inconclusive`. Interpret the measured curves across flow/concentration conditions and respect the supplied construct. Response sign alone is insufficient. These calls are scored against the original paper's scoped interpretation, not independently adjudicated universal binding truth. Other tasks may omit this field or use an empty object.

For trace tasks group by trace_id; sort by time_s. Output n, concentration_M, start_s, end_s. Initial window: t < min(t)+20 seconds; initial_median_RU is its median, initial_sd_RU its sample SD (ddof=1). p95_delta_RU is linear-interpolated 95th percentile of all responses minus initial median. tail_delta_RU is mean of samples t > max(t)-20 minus initial median. auc_RU_s is trapezoidal integral of response minus initial median over the whole observed time grid. This initial window is a benchmark summary convention, not an experimentally confirmed pre-injection baseline. Do not fill missing values, smooth, average concentrations, or manufacture points. Multiple flow rates are conditions, not replicates.

For affinity tasks group by compound. Fit unweighted least squares R = Rmax*C/(KD+C)+offset to the provided observed endpoints. Use Rmax >= 0, free offset and KD in [1e-12,1] M. Report n, KD_M, Rmax_RU, offset_RU, rmse_RU (sqrt(SSE/n)), max_concentration_M, max_concentration_over_KD. Fitting this descriptive model does not validate its mechanism. These two small datasets do not establish kon/koff, selectivity, independent uncertainty, or drug readiness.

For tbxt-binding, classify each compound by the maximum Corrected response among binding-late rows: at least 10 RU means `interaction_supported`; otherwise `no_measurable_binding_under_operational_threshold`. This is a disclosed operational triage rule, not author-reported binding truth.

For report tasks group by compound + "|" + channel, keeping the original compound identifiers (including suffixes). Use rows whose window contains "binding late" case-insensitively. Retain only groups containing Corrected rows. Output n (all input rows in group), n_corrected_late, n_concentrations (unique corrected-late concentrations), max_concentration_M, max_corrected_RU, min_corrected_RU, mean_corrected_RU, max_reference_RU (Reference late rows), dose_slope_RU_per_uM (ordinary linear regression with intercept over corrected-late responses; 0 if one concentration). For max_reference_subtraction_error_RU, among rows whose window contains "binding late", match run/cycle/channel/window and take max(abs(Active - Reference - Reference subtracted)); use null if no complete triplet. This checks provided relative report-point arithmetic, not unavailable raw sensorgrams. Do not assume solvent-corrected values equal reference subtraction.

Numerical scoring tolerances: counts exact; concentration/time values rtol=1e-6 with atol=1e-15 for concentration and 1e-6 seconds for time; trace/report response summaries rtol=1e-4, atol=1e-4; affinity parameter/reconstruction summaries rtol=0.02, atol=1e-5 RU (KD atol=1e-12 M). Nonfinite values and duplicate JSON keys are invalid. See SCORING.md for weights and limits.
"""


def main():
    (ROOT / "CONTRACT.md").write_text(CONTRACT)
    catalog = []
    for ix, (name, title, file, kind, study, claims, question) in enumerate(TASKS):
        root = ROOT / "tasks" / name
        env = root / "environment"
        test = root / "tests"
        sol = root / "solution"
        for p in [env / "data", env / "spec", test / "cases", sol]:
            p.mkdir(parents=True, exist_ok=True)
        rows = list(csv.DictReader((ROOT / "data" / file).open()))
        if name == "isg65-c3b-traces":
            rows = [r for r in rows if r["target"] == "C3b"]
        if name == "isg65-c3d-traces":
            rows = [r for r in rows if r["target"] == "C3d"]
        if name.startswith("dbox-d20"):
            rows = [r for r in rows if r["compound"] == "D20"]
        if name.startswith("dbox-d21"):
            rows = [r for r in rows if r["compound"] == "D21"]
        if name == "stat3-binding":
            claims = {}
        config = dict(
            task=name, kind=kind, study=study, required_claims=CLAIMS | claims
        )
        if name == "stat3-binding":
            config["binding_assessment_contract"] = {
                "keys": "each distinct compound present in measurements.csv",
                "allowed": [
                    "interaction_supported",
                    "no_measurable_binding_under_tested_conditions",
                    "inconclusive",
                ],
                "construct": "mouse STAT3beta core 127-722",
                "methods": "Double referenced; association 60 seconds, dissociation 600 seconds. Three flow rates are conditions, not replicates. Evaluate specific interaction patterns, not response sign alone.",
            }
        if name == "tbxt-binding":
            config["binding_assessment_contract"] = {
                "keys": "each distinct compound present in measurements.csv",
                "allowed": [
                    "interaction_supported",
                    "no_measurable_binding_under_operational_threshold",
                ],
                "threshold_RU": 10.0,
                "rule": "classify each compound by the maximum Corrected response among binding-late rows; >= 10 RU => interaction_supported, otherwise no_measurable_binding_under_operational_threshold",
                "methods": "This is a disclosed operational triage rule, not author-reported binding truth.",
            }
        write(env / "data/measurements.csv", rows)
        dump(env / "data/config.json", config)
        for case in ["observed", "subset"]:
            casepath = test / "cases" / case
            d = casepath / "data"
            d.mkdir(parents=True, exist_ok=True)
            r = [dict(x) for x in rows]
            if case == "subset":
                key = "trace_id" if kind == "trace" else "compound"
                ids = sorted(set(x[key] for x in r))
                keep = set(ids[::2]) if kind != "affinity" else set(ids)
                r = [x for x in r if x[key] in keep]
                if kind == "affinity":
                    r = [
                        x for i, x in enumerate(r) if i != 1
                    ]  # remove one measured endpoint only
                mapping = {
                    old: f"sample-{i+1:03d}" for i, old in enumerate(sorted(keep))
                }
                for x in r:
                    x[key] = mapping[x[key]]
                r.reverse()
            compound_map = {}
            binding_labels = {}
            if name in ("stat3-binding", "tbxt-binding"):
                if name == "stat3-binding":
                    binding_labels = {
                        c: (
                            "interaction_supported"
                            if c == "S3I-201"
                            else "no_measurable_binding_under_tested_conditions"
                        )
                        for c in sorted({x["compound"] for x in r})
                    }
                else:
                    by_compound = {}
                    for x in r:
                        if (
                            "binding late" in x["window"].lower()
                            and x["sensorgram_type"] == "Corrected"
                        ):
                            c = x["compound"]
                            by_compound[c] = max(
                                by_compound.get(c, float("-inf")),
                                float(x["response_RU"]),
                            )
                    binding_labels = {
                        c: (
                            "interaction_supported"
                            if by_compound.get(c, float("-inf")) >= 10.0
                            else "no_measurable_binding_under_operational_threshold"
                        )
                        for c in sorted({x["compound"] for x in r})
                    }
                if case == "subset":
                    compound_map = {
                        c: f"sample-C{i+1:03d}"
                        for i, c in enumerate(sorted(binding_labels))
                    }
                    for x in r:
                        x["compound"] = compound_map[x["compound"]]
                        # Do not leave the original compound recoverable from
                        # subset metadata; the binding call must come from curves.
                        x["source_sheet"] = "anonymized"
                        x["source_row"] = "0"
                        x["source_column"] = "0"
            write(d / "measurements.csv", r)
            dump(d / "config.json", config)
            expected = analyze(d)
            if name in ("stat3-binding", "tbxt-binding"):
                expected["binding_assessments"] = {
                    (compound_map[c] if case == "subset" else c): label
                    for c, label in binding_labels.items()
                }
            dump(casepath / "expected.json", expected)
        weights = dict(WEIGHTS)
        if "affinity" in name:
            weights.update(coverage=0.15, response=0.70)
        if name in ("stat3-binding", "tbxt-binding"):
            weights.update(coverage=0.15, response=0.50, binding_evidence=0.20)
        dump(
            test / "scoring.json", dict(fields=FIELDS[kind], weights=weights, kind=kind)
        )
        (env / "spec/CONTRACT.md").write_text(CONTRACT)
        (root / "instruction.md").write_text(
            f"# {title}\n\n{question}\n\nMeasured data are in `/app/data`. Read `/app/spec/CONTRACT.md` and implement the reproducible analysis program. No narrative report is graded. Input responses are experimental; no simulated curves are included. Identifiers may be aliased in the robustness subset; do not key analysis off names.\n"
        )
        (env / "Dockerfile").write_text(
            'FROM python:3.12.10-slim\nWORKDIR /app\nRUN pip install --no-cache-dir numpy==2.2.6 scipy==1.15.3 pandas==2.2.3 matplotlib==3.10.3\nCOPY data /app/data\nCOPY spec /app/spec\nRUN mkdir -p /app/submission /app/output\nCMD ["bash"]\n'
        )
        (test / "Dockerfile").write_text(
            'FROM python:3.12.10-slim\nRUN pip install --no-cache-dir numpy==2.2.6 scipy==1.15.3 pandas==2.2.3 matplotlib==3.10.3\nCOPY . /tests\nWORKDIR /app\nRUN mkdir -p /logs/verifier\nCMD ["bash"]\n'
        )
        shutil.copyfile(ROOT / "tools/reference.py", sol / "run.py")
        shutil.copyfile(ROOT / "tools/verifier.py", test / "verifier.py")
        (sol / "solve.sh").write_text(
            "#!/bin/bash\nset -eu\nmkdir -p /app/submission\ncp /solution/run.py /app/submission/run.py\npython3 /app/submission/run.py --input-dir /app/data --output-dir /app/output\n"
        )
        (test / "test.sh").write_text(
            '#!/bin/bash\nset -eu\nmkdir -p /logs/verifier\nprintf "0\\n" > /logs/verifier/reward.txt\npython3 /tests/verifier.py\n'
        )
        (sol / "solve.sh").chmod(0o755)
        (test / "test.sh").chmod(0o755)
        (root / "task.toml").write_text(
            f"""schema_version = "1.4"
artifacts = ["/app/submission"]
[task]
name = "spr-real/{name}"
description = "{title}"
[metadata]
author_name = "SPR-Bench contributors"
difficulty = "hard"
category = "scientific-data-analysis"
tags = ["spr", "experimental", "{study.lower()}"]
[agent]
timeout_sec = 3600.0
[verifier]
timeout_sec = 600.0
environment_mode = "separate"
[verifier.environment]
network_mode = "no-network"
cpus = 2
memory_mb = 4096
storage_mb = 10240
[environment]
network_mode = "no-network"
cpus = 2
memory_mb = 4096
storage_mb = 10240
build_timeout_sec = 600.0
"""
        )
        catalog.append(
            dict(
                id=name,
                title=title,
                study=study,
                kind=kind,
                source_file=file,
                rows=len(rows),
                weights=weights,
                question=question,
            )
        )
    dump(ROOT / "task_catalog.json", catalog)
    (ROOT / "CONTRACT.md").write_text(CONTRACT)


if __name__ == "__main__":
    main()
