"""Bookkeeping-only submission used as a regression floor: no SPR analysis at all.

It reports IDs, counts, concentrations, time ranges, input hashes and the
disclosed claims, and must never earn the binary reward.
"""

import argparse, hashlib, json
from pathlib import Path
import pandas as pd


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--input-dir", required=True)
    a.add_argument("--output-dir", required=True)
    a = a.parse_args()
    data, out = Path(a.input_dir), Path(a.output_dir)
    cfg = json.loads((data / "config.json").read_text())
    df = pd.read_csv(data / "measurements.csv")
    records, assessments = [], {}
    if cfg["kind"] == "trace":
        for key, g in df.groupby("trace_id"):
            records.append(
                dict(
                    id=key,
                    n=len(g),
                    concentration_M=float(g.concentration_M.iloc[0]),
                    start_s=float(g.time_s.min()),
                    end_s=float(g.time_s.max()),
                )
            )
    elif cfg["kind"] == "affinity":
        for key, g in df.groupby("compound"):
            records.append(
                dict(id=key, n=len(g), max_concentration_M=float(g.concentration_M.max()))
            )
    if "binding_assessment_contract" in cfg:
        assessments = {c: cfg["binding_assessment_contract"]["allowed"][0] for c in df.compound.unique()}
    (out / "results.json").write_text(
        json.dumps(
            dict(
                records=records,
                claims=cfg["required_claims"],
                binding_assessments=assessments,
                input_sha256={
                    p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(data.iterdir())
                },
            )
        )
    )


if __name__ == "__main__":
    main()
