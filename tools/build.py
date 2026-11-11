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
        {
            "DPP": "no_measurable_binding_under_tested_conditions",
            "S3I-201": "source_supports_interaction_not_selectivity",
        },
        "Compare DPP and S3I-201 against mouse STAT3beta core 127-722. Distinguish a lack of measured response in this construct from a universal non-binder claim.",
    ),
    (
        "stat3-flow",
        "STAT3: audit flow-dependent responses",
        "stat3.csv",
        "trace",
        "STAT3",
        {
            "flow_rates_are_independent_replicates": False,
            "flow_effects_can_confound_kinetics": True,
        },
        "Compare the three flow rates for S3I-201. Quantify differences without treating flow conditions as biological replicates or estimating a concentration-series KD.",
    ),
    (
        "cyp3a4-sparse",
        "CYP3A4: reconstruct sparse observed sensorgrams",
        "cyp3a4-traces.csv",
        "trace",
        "CYP3A4",
        {"interpolated_missing_values": False, "source_fit_columns_used": False},
        "Recover the eight fluconazole traces from sparse measured cells. Preserve each trace time grid and quantify its response without using the source fitted curves.",
    ),
    (
        "cyp3a4-affinity",
        "CYP3A4: audit apparent steady-state affinity",
        "cyp3a4-affinity.csv",
        "affinity",
        "CYP3A4",
        {"affinity_type": "apparent_steady_state", "kinetic_rates_identifiable": False},
        "Fit the observed fluconazole concentration-response points, quantify residuals and concentration coverage. Do not interpret an apparent KD as target selectivity or a kinetic rate.",
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
        "klhdc2-hits",
        "KLHDC2: compare initial small-molecule hits",
        "klhdc2-hits.csv",
        "trace",
        "KLHDC2",
        {"compound_set": "1_and_2", "SPR_sheets_only": True},
        "Compare measured sensorgrams for compounds 1 and 2. Avoid treating the neighboring fluorescence-polarization sheets as SPR data or treating representative traces as replicates.",
    ),
    (
        "klhdc2-analogs",
        "KLHDC2: compare follow-up small molecules",
        "klhdc2-analogs.csv",
        "trace",
        "KLHDC2",
        {"compound_set": "5_and_6", "SPR_sheets_only": True},
        "Analyze measured sensorgrams for compounds 5 and 6. Compare concentration-normalized evidence without inventing unreported controls or kinetic ground truth.",
    ),
    (
        "tbxt-reference",
        "TBXT: audit experimental reference correction",
        "tbxt.csv",
        "report",
        "TBXT",
        {"data_type": "report_points", "kinetic_rates_identifiable": False},
        "Join active, reference and reference-subtracted late-binding report points by run/cycle/channel/window. Audit correction arithmetic and retain compound/series identities.",
    ),
    (
        "tbxt-triage",
        "TBXT: quantify corrected dose-response evidence",
        "tbxt.csv",
        "report",
        "TBXT",
        {"data_type": "report_points", "drug_readiness": "not_established"},
        "Summarize corrected late-binding responses, reference binding and dose trends. These are screening-evidence metrics; a large response alone does not establish specific binding or justify a drug-development decision.",
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
It must read the supplied directory and write `OUTPUT/results.json`. Use Python, NumPy, SciPy, pandas or standard libraries. No network is available. The verifier reruns your program on the visible input and a deterministic subset with renamed IDs and reordered rows. All response values remain real measured values; these are robustness cases, not independent experiments. Do not hardcode record IDs or results.

JSON schema: `{"records":[{"id":"...", ...numeric fields...}], "claims":{...}, "input_sha256":{"config.json":"...","measurements.csv":"..."}}`. Include exactly the required records, no duplicate IDs. Hash every input file. `claims` must retain the explicitly supplied evidence-scope constraints in config.json; these are disclosed guardrails, not a hidden biological reasoning test. The 5% scope score is a contract check. No prose report is scored.

For stat3-binding only, also output `binding_assessments`: a mapping from each compound present to one of `interaction_supported`, `no_measurable_binding_under_tested_conditions`, or `inconclusive`. Interpret the measured curves across flow/concentration conditions and respect the supplied construct. Response sign alone is insufficient. These calls are scored against the original paper's scoped interpretation, not independently adjudicated universal binding truth. Other tasks may omit this field or use an empty object.

For trace tasks group by trace_id; sort by time_s. Output n, concentration_M, start_s, end_s. Initial window: t < min(t)+20 seconds; initial_median_RU is its median, initial_sd_RU its sample SD (ddof=1). p95_delta_RU is linear-interpolated 95th percentile of all responses minus initial median. tail_delta_RU is mean of samples t > max(t)-20 minus initial median. auc_RU_s is trapezoidal integral of response minus initial median over the whole observed time grid. This initial window is a benchmark summary convention, not an experimentally confirmed pre-injection baseline. Do not fill missing values, smooth, average concentrations, or manufacture points. Multiple flow rates are conditions, not replicates.

For affinity tasks group by compound. Fit unweighted least squares R = Rmax*C/(KD+C)+offset to the provided observed endpoints. Use Rmax >= 0, free offset and KD in [1e-12,1] M. Report n, KD_M, Rmax_RU, offset_RU, rmse_RU (sqrt(SSE/n)), max_concentration_M, max_concentration_over_KD. Fitting this descriptive model does not validate its mechanism. These two small datasets do not establish kon/koff, selectivity, independent uncertainty, or drug readiness.

For report tasks group by compound + "|" + channel, keeping the original compound identifiers (including suffixes). Use rows whose window contains "binding late" case-insensitively. Retain only groups containing Corrected rows. Output n (all input rows in group), n_corrected_late, n_concentrations (unique corrected-late concentrations), max_concentration_M, max_corrected_RU, min_corrected_RU, mean_corrected_RU, max_reference_RU (Reference late rows), dose_slope_RU_per_uM (ordinary linear regression with intercept over corrected-late responses; 0 if one concentration). For max_reference_subtraction_error_RU match run/cycle/channel/window and take max(abs(Active - Reference - Reference subtracted)); use null if no complete triplet. This checks provided relative report-point arithmetic, not unavailable raw sensorgrams. Do not assume solvent-corrected values equal reference subtraction.

Numerical scoring tolerances: counts exact; concentration/time values rtol=1e-6 with atol=1e-15 for concentration and 1e-6 seconds for time; trace/report response summaries rtol=1e-4, atol=1e-4; affinity parameter/reconstruction summaries rtol=0.02, atol=1e-5 RU (KD atol=1e-12 M). Nonfinite values and duplicate JSON keys are invalid. See SCORING.md for weights and limits.
"""


def main():
    catalog = []
    for ix, (name, title, file, kind, study, claims, question) in enumerate(TASKS):
        root = ROOT / "tasks" / name
        env = root / "environment"
        test = root / "tests"
        sol = root / "solution"
        for p in [env / "data", env / "spec", test / "cases", sol]:
            p.mkdir(parents=True, exist_ok=True)
        rows = list(csv.DictReader((ROOT / "data" / file).open()))
        if name == "stat3-flow":
            rows = [r for r in rows if r["compound"] == "S3I-201"]
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
            write(d / "measurements.csv", r)
            dump(d / "config.json", config)
            expected = analyze(d)
            if name == "stat3-binding":
                expected["binding_assessments"] = {
                    k: (
                        "interaction_supported"
                        if k == "S3I-201"
                        else "no_measurable_binding_under_tested_conditions"
                    )
                    for k in sorted({x["compound"] for x in r})
                }
            dump(casepath / "expected.json", expected)
        weights = dict(WEIGHTS)
        if "affinity" in name:
            weights.update(coverage=0.15, response=0.70)
        if name == "stat3-binding":
            weights.update(coverage=0.15, response=0.50, binding_evidence=0.20)
        if name == "tbxt-reference":
            weights.update(coverage=0.25, response=0.60)
        dump(
            test / "scoring.json", dict(fields=FIELDS[kind], weights=weights, kind=kind)
        )
        (env / "spec/CONTRACT.md").write_text(CONTRACT)
        (root / "instruction.md").write_text(
            f"# {title}\n\n{question}\n\nMeasured data are in `/app/data`. Read `/app/spec/CONTRACT.md` and implement the reproducible analysis program. No narrative report is graded. Input responses are experimental; no simulated curves are included.\n"
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
