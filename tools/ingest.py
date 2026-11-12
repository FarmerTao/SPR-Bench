"""Lossless selection of measured cells; no response synthesis or interpolation."""

import csv, hashlib, io, json, re, zipfile
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[1]


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def sheet(file, name):
    return list(
        openpyxl.load_workbook(
            ROOT / "sources/originals" / file, read_only=True, data_only=True
        )[name].values
    )


def main():
    d = ROOT / "data"
    sources = []
    info = [
        (
            "stat3.xlsx",
            "STAT3",
            "https://doi.org/10.1186/s13104-020-05189-w",
            "https://static-content.springer.com/esm/art%3A10.1186%2Fs13104-020-05189-w/MediaObjects/13104_2020_5189_MOESM1_ESM.xlsx",
            "CC0-1.0 (data); article CC-BY-4.0",
            "Mtwebana and Prinsloo, 2020",
        ),
        (
            "tbxt.xlsx",
            "TBXT",
            "https://doi.org/10.5281/zenodo.6394811",
            "https://zenodo.org/api/records/6394811/files/20201028%20LMW%20binding%20affinity%20screen%20for%20136%20UNC%20and%20Piramal%20compounds.xlsx/content",
            "CC-BY-2.0",
            "Davis-Gilbert, Drewry, Hossain et al., 2022",
        ),
        (
            "lrrk2.zip",
            "LRRK2",
            "https://doi.org/10.5281/zenodo.10471514",
            "https://zenodo.org/api/records/10471514/files/Figure%201B_SPR%20datasets.zip/content",
            "CC-BY-4.0",
            "Dederer et al., 2024",
        ),
        (
            "macrocycle-fig2.xlsx",
            "Macrocycle",
            "https://doi.org/10.1038/s41589-025-01929-w",
            "https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-025-01929-w/MediaObjects/41589_2025_1929_MOESM4_ESM.xlsx",
            "CC-BY-4.0",
            "Rettie et al., 2025",
        ),
        (
            "macrocycle-fig4.xlsx",
            "Macrocycle",
            "https://doi.org/10.1038/s41589-025-01929-w",
            "https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-025-01929-w/MediaObjects/41589_2025_1929_MOESM6_ESM.xlsx",
            "CC-BY-4.0",
            "Rettie et al., 2025",
        ),
        (
            "isg65-fig2-data1.xlsx",
            "ISG65",
            "https://doi.org/10.7554/eLife.88960",
            "https://cdn.elifesciences.org/articles/88960/elife-88960-fig2-data1-v1.xlsx",
            "CC-BY-4.0",
            "Cook, Carrington, Higgins, 2024",
        ),
        (
            "dbox-fig4-data1.xlsx",
            "D-box",
            "https://doi.org/10.7554/eLife.104238",
            "https://cdn.elifesciences.org/articles/104238/elife-104238-fig4-data1-v1.xlsx",
            "CC-BY-4.0",
            "Eapen et al., 2026",
        ),
    ]
    for file, source, doi, url, license, authors in info:
        p = ROOT / "sources/originals" / file
        sources.append(
            dict(
                file="originals/" + file,
                source=source,
                doi=doi,
                download_url=url,
                license=license,
                authors=authors,
                sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                bytes=p.stat().st_size,
            )
        )
    dump(ROOT / "sources/manifest.json", sources)

    # STAT3: three nonempty sheets; numerical TIME and three flow-rate responses.
    rows = []
    for name, compound, conc in [
        ("80Um 30 60 100uLper min 5dpp", "DPP", 80),
        ("80Um 30 60 100uLper min s3i201", "S3I-201", 80),
        ("100uM 30uL 60 100 5 15 DPP", "DPP", 100),
    ]:
        for n, row in enumerate(sheet("stat3.xlsx", name)[1:], 2):
            for col, flow in enumerate([30, 60, 100], 1):
                if isinstance(row[0], (int, float)) and isinstance(
                    row[col], (int, float)
                ):
                    rows.append(
                        dict(
                            trace_id=f"{compound}-{conc}-{flow}",
                            compound=compound,
                            target="mouse STAT3beta core 127-722",
                            concentration_M=conc * 1e-6,
                            flow_uL_min=flow,
                            time_s=row[0],
                            response_RU=row[col],
                            source="STAT3",
                            source_sheet=name,
                            source_row=n,
                            source_column=col + 1,
                        )
                    )
    write(d / "stat3.csv", rows)

    # TBXT: corrected late-binding report points; no fitted curves.
    r = sheet("tbxt.xlsx", "Report point table")
    rows = []
    for n, row in enumerate(r[3:], 4):
        if row[15] != "Analysis":
            continue
        rows.append(
            dict(
                record_id=f"row-{n}",
                run=row[0],
                cycle=row[1],
                channel=row[2],
                sensorgram_type=row[4],
                window=row[5],
                time_s=row[6],
                window_s=row[7],
                response_RU=row[9],
                sd_RU=row[10],
                slope_RU_s=row[11],
                compound=row[17],
                concentration_M=(
                    row[18] * 1e-6 if isinstance(row[18], (float, int)) else ""
                ),
                flow_uL_min=row[20],
                contact_s=row[21],
                source="TBXT",
                source_sheet="Report point table",
                source_row=n,
            )
        )
    write(d / "tbxt.csv", rows)

    # LRRK2 DARPin E11: seven concentration series plus seven equilibrium endpoints.
    with zipfile.ZipFile(ROOT / "sources/originals/lrrk2.zip") as z:
        r = list(
            csv.reader(
                io.StringIO(z.read("Sensorgrams_E11.txt").decode("cp1252")),
                delimiter="\t",
            )
        )
        rows = []
        for col in range(0, 14, 2):
            c = float(re.search(r"([\d.]+) µM", r[0][col])[1]) * 1e-6
            for n, row in enumerate(r[1:], 2):
                if len(row) > col + 1 and row[col] and row[col + 1]:
                    rows.append(
                        dict(
                            trace_id=f"E11-{col//2+1}",
                            compound="E11",
                            target="LRRK2",
                            concentration_M=c,
                            flow_uL_min="",
                            time_s=float(row[col]),
                            response_RU=float(row[col + 1]),
                            source="LRRK2",
                            source_sheet="Sensorgrams_E11.txt",
                            source_row=n,
                            source_column=col + 2,
                        )
                    )
        write(d / "lrrk2-traces.csv", rows)
        r = list(
            csv.reader(
                io.StringIO(z.read("Steady state_E11.txt").decode("cp1252")),
                delimiter="\t",
            )
        )
        points = []
        for n, row in enumerate(r[1:], 2):
            if row[0] and row[1]:
                points.append(
                    dict(
                        point_id=f"E11-{n-1}",
                        compound="E11",
                        concentration_M=float(row[0]),
                        response_RU=float(row[1]),
                        source="LRRK2",
                        source_sheet="Steady state_E11.txt",
                        source_row=n,
                        source_column=2,
                    )
                )
        write(d / "lrrk2-affinity.csv", points)

    # Designed macrocycles: measured sensorgrams only; fitted columns are not selected.
    macro_specs = [
        ("macrocycle-fig2.xlsx", "MCB_D2", "MCL1", 20e-6, 1, 2, "Macrocycle-Fig2"),
        ("macrocycle-fig2.xlsx", "MDB_D8", "MDM2", 50e-6, 5, 6, "Macrocycle-Fig2"),
        ("macrocycle-fig4.xlsx", "RBB_D10", "RbtA", 20e-6, 1, 2, "Macrocycle-Fig4"),
    ]
    rows = []
    for file, compound, target, conc, tcol, ycol, source in macro_specs:
        r = sheet(file, "Sheet1")
        for n, row in enumerate(r[2:], 3):
            if isinstance(row[tcol - 1], (int, float)) and isinstance(
                row[ycol - 1], (int, float)
            ):
                rows.append(
                    dict(
                        trace_id=compound,
                        compound=compound,
                        target=target,
                        concentration_M=conc,
                        flow_uL_min=30,
                        time_s=row[tcol - 1],
                        response_RU=row[ycol - 1],
                        source=source,
                        source_sheet="Sheet1",
                        source_row=n,
                        source_column=ycol,
                    )
                )
    write(d / "macrocycle-traces.csv", rows)

    # ISG65 SPR: six sheets, six measured cycles each; fitted columns are skipped.
    isg65 = [
        ("biotin-C3b ISG65", "C3b", "ISG65-WT"),
        ("biotin-C3d ISG65", "C3d", "ISG65-WT"),
        ("biotin-C3b ISG65ΔL2", "C3b", "ISG65-dL2"),
        ("biotin-C3d ISG65ΔL2", "C3d", "ISG65-dL2"),
        ("biotin-C3b ISG65L2N188A etc.", "C3b", "ISG65-L2N188A"),
        ("biotin-C3d ISG65L2N188A etc.", "C3d", "ISG65-L2N188A"),
    ]
    rows = []
    for sheet_name, target, compound in isg65:
        r = sheet("isg65-fig2-data1.xlsx", sheet_name)
        for col, header in enumerate(r[0]):
            if (
                not isinstance(header, str)
                or header.startswith("Fitted")
                or not header.startswith("Cycle:")
                or not header.endswith("_Y")
            ):
                continue
            m = re.search(r"([\d.]+)\s*nM", header)
            c = re.search(r"Cycle: (\d+)", header)
            if not m or not c:
                continue
            concentration = float(m.group(1)) * 1e-9
            cycle = int(c.group(1))
            for n, row in enumerate(r[1:], 2):
                if isinstance(row[0], (int, float)) and isinstance(
                    row[col], (int, float)
                ):
                    rows.append(
                        dict(
                            trace_id=f"{compound}-{target}-c{cycle}",
                            compound=compound,
                            target=target,
                            concentration_M=concentration,
                            flow_uL_min=30,
                            time_s=row[0],
                            response_RU=row[col],
                            source="ISG65",
                            source_sheet=sheet_name,
                            source_row=n,
                            source_column=col + 1,
                        )
                    )
    write(d / "isg65-traces.csv", rows)
    # Apparent steady-state endpoints: the measured response at the end of the
    # 120 s association phase (closest observed time to 120 s), one cell per trace.
    by_trace = {}
    for r in rows:
        by_trace.setdefault(r["trace_id"], []).append(r)
    points = []
    for trace_id, g in sorted(by_trace.items()):
        p = min(g, key=lambda r: abs(float(r["time_s"]) - 120.0))
        points.append(
            dict(
                point_id=trace_id,
                compound=p["compound"] + "-" + p["target"],
                concentration_M=p["concentration_M"],
                response_RU=p["response_RU"],
                source=p["source"],
                source_sheet=p["source_sheet"],
                source_row=p["source_row"],
                source_column=p["source_column"],
            )
        )
    write(d / "isg65-affinity.csv", points)

    # D-box peptides D20/D21: eight measured concentrations in each sensorgram
    # and the paired observed isotherms; no fitted values are selected.
    dbox_specs = [
        ("Figure 4C -D20 Fc4-1 sensorgram", "Figure 4C -D20 Fc4-1 isotherm", "D20"),
        ("Figure 4D -D21 Fc4-1 sensorgram", "Figure 4D -D21 Fc4-1 isotherm", "D21"),
    ]
    points = []
    for _sensorgram_sheet, isotherm_sheet, compound in dbox_specs:
        r = sheet("dbox-fig4-data1.xlsx", isotherm_sheet)
        for n, row in enumerate(r[1:], 2):
            if isinstance(row[0], (int, float)) and isinstance(row[1], (int, float)):
                points.append(
                    dict(
                        point_id=f"{compound}-p{n-1}",
                        compound=compound,
                        target="Cdc20",
                        concentration_M=row[0] * 1e-6,
                        response_RU=row[1],
                        source="D-box",
                        source_sheet=isotherm_sheet,
                        source_row=n,
                        source_column=2,
                    )
                )
    write(d / "dbox-affinity.csv", points)

    dump(
        ROOT / "data_manifest.json",
        [
            dict(
                file=p.name,
                rows=sum(1 for _ in csv.DictReader(p.open())),
                sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            )
            for p in sorted(d.glob("*.csv"))
        ],
    )


if __name__ == "__main__":
    main()
