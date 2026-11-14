"""Measure sampling interval and noise in the bundled measured SPR traces.

The simulation parameters in tools/sprsim.py and the task generators are
anchored on these statistics. Writes sources/anchors.json.
"""

import csv, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TRACE_FILES = ["lrrk2-traces.csv", "macrocycle-traces.csv", "isg65-traces.csv", "stat3.csv"]


def main():
    out = {}
    for name in TRACE_FILES:
        groups = {}
        for r in csv.DictReader((ROOT / "data" / name).open()):
            groups.setdefault(r["trace_id"], []).append((float(r["time_s"]), float(r["response_RU"])))
        dts, noise = [], []
        for pts in groups.values():
            t, y = np.array(sorted(pts)).T
            dts.append(np.median(np.diff(t)))
            # White-noise estimate from first differences of the pre-injection baseline.
            base = y[t < 0] if (t < 0).sum() > 20 else y[: max(len(y) // 20, 20)]
            noise.append(np.std(np.diff(base)) / np.sqrt(2))
        out[name] = dict(traces=len(groups), sample_interval_s=round(float(np.median(dts)), 3),
                         baseline_noise_RU_median=round(float(np.median(noise)), 4))
    (ROOT / "sources/anchors.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
