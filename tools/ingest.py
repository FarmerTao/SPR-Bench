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


def traces(file, names, source, target, scale=1e-9):
    out = []
    for name, compound in names:
        r = sheet(file, name)
        for col, header in enumerate(r[0][1:], 1):
            concentration = float(re.search(r"[\d.]+", str(header))[0]) * scale
            for rownum, row in enumerate(r[1:], 2):
                if isinstance(row[0], (int, float)) and isinstance(
                    row[col], (int, float)
                ):
                    out.append(
                        dict(
                            trace_id=f"{compound}-{col}",
                            compound=compound,
                            target=target,
                            concentration_M=concentration,
                            flow_uL_min="",
                            time_s=row[0],
                            response_RU=row[col],
                            source=source,
                            source_sheet=name,
                            source_row=rownum,
                            source_column=col + 1,
                        )
                    )
    return out


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
            "lrrk2.zip",
            "LRRK2",
            "https://doi.org/10.5281/zenodo.10471514",
            "https://zenodo.org/api/records/10471514/files/Figure%201B_SPR%20datasets.zip/content",
            "CC-BY-4.0",
            "Dederer et al., 2024",
        ),
        (
            "cyp3a4.xlsx",
            "CYP3A4",
            "https://doi.org/10.5281/zenodo.14721783",
            "https://zenodo.org/api/records/14721783/files/Figure%20S6%20Fluconazole%20SPR%20titrations.xlsx/content",
            "CC-BY-4.0",
            "Knetsch et al., 2025",
        ),
        (
            "klhdc2-hits.xlsx",
            "KLHDC2",
            "https://doi.org/10.7554/eLife.106844",
            "https://cdn.elifesciences.org/articles/106844/elife-106844-fig2-data1-v1.xlsx",
            "CC-BY-4.0",
            "Zhou, Zhou et al., 2025",
        ),
        (
            "klhdc2-analogs.xlsx",
            "KLHDC2",
            "https://doi.org/10.7554/eLife.106844",
            "https://cdn.elifesciences.org/articles/106844/elife-106844-fig3-data1-v1.xlsx",
            "CC-BY-4.0",
            "Zhou, Zhou et al., 2025",
        ),
        (
            "tbxt.xlsx",
            "TBXT",
            "https://doi.org/10.5281/zenodo.6394811",
            "https://zenodo.org/api/records/6394811/files/20201028%20LMW%20binding%20affinity%20screen%20for%20136%20UNC%20and%20Piramal%20compounds.xlsx/content",
            "CC-BY-2.0",
            "Davis-Gilbert, Drewry, Hossain et al., 2022",
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
    names = [("Figure 2E", "compound-1"), ("Figure 2F", "compound-2")]
    write(d / "klhdc2-hits.csv", traces("klhdc2-hits.xlsx", names, "KLHDC2", "KLHDC2"))
    write(
        d / "klhdc2-analogs.csv",
        traces(
            "klhdc2-analogs.xlsx",
            [("Figure 3F", "compound-5"), ("Figure 3G", "compound-6")],
            "KLHDC2",
            "KLHDC2",
        ),
    )
    # Explicitly select observed columns 2..9, never the paired fitted columns.
    r = sheet("cyp3a4.xlsx", "SPR titration sheet 1")
    rows = []
    for col in range(1, 9):
        c = float(re.search(r"[\d.]+", r[0][col])[0]) * 1e-6
        for n, row in enumerate(r[1:], 2):
            if isinstance(row[0], (int, float)) and isinstance(row[col], (int, float)):
                rows.append(
                    dict(
                        trace_id=f"fluconazole-{col}",
                        compound="fluconazole",
                        target="CYP3A4 nanodisc",
                        concentration_M=c,
                        flow_uL_min="",
                        time_s=row[0],
                        response_RU=row[col],
                        source="CYP3A4",
                        source_sheet="SPR titration sheet 1",
                        source_row=n,
                        source_column=col + 1,
                    )
                )
    write(d / "cyp3a4-traces.csv", rows)
    points = []
    for n, row in enumerate(sheet("cyp3a4.xlsx", "SPR titration sheet 2")[1:], 2):
        for col in range(1, 9):
            if isinstance(row[col], (int, float)):
                points.append(
                    dict(
                        point_id=f"fluconazole-{col}",
                        compound="fluconazole",
                        concentration_M=row[0] * 1e-6,
                        response_RU=row[col],
                        source="CYP3A4",
                        source_sheet="SPR titration sheet 2",
                        source_row=n,
                        source_column=col + 1,
                    )
                )
    write(d / "cyp3a4-affinity.csv", points)
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
