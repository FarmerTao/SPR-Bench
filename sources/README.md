# Source catalogue and extraction notes

Five studies; six bundled source files. Accessed 2026-11-11. These are measured experimental data, with source preprocessing retained.

## STAT3 — stat3.xlsx

Mtwebana and Prinsloo, 2020. [Primary source](https://doi.org/10.1186/s13104-020-05189-w); [original download](https://static-content.springer.com/esm/art%3A10.1186%2Fs13104-020-05189-w/MediaObjects/13104_2020_5189_MOESM1_ESM.xlsx).

License: CC0-1.0 (data); article CC-BY-4.0. Bytes: 145,294. SHA-256: `a8078400650985e5de25b44d4ae8e642c4fcc0dff31df9418c44ad294a81d58d`.

## LRRK2 — lrrk2.zip

Dederer et al., 2024. [Primary source](https://doi.org/10.5281/zenodo.10471514); [original download](https://zenodo.org/api/records/10471514/files/Figure%201B_SPR%20datasets.zip/content).

License: CC-BY-4.0. Bytes: 2,316,436. SHA-256: `484b7e7782ebc66ff69ca734592d3ec9d0681d86c8d1ddca6b070ec738b68997`.

## CYP3A4 — cyp3a4.xlsx

Knetsch et al., 2025. [Primary source](https://doi.org/10.5281/zenodo.14721783); [original download](https://zenodo.org/api/records/14721783/files/Figure%20S6%20Fluconazole%20SPR%20titrations.xlsx/content).

License: CC-BY-4.0. Bytes: 1,706,313. SHA-256: `89f69d55df6ebd3a06cad2ecf01c3f5f4286347387b45f98fbc611f44eb93f29`.

## KLHDC2 — klhdc2-hits.xlsx

Zhou, Zhou et al., 2025. [Primary source](https://doi.org/10.7554/eLife.106844); [original download](https://cdn.elifesciences.org/articles/106844/elife-106844-fig2-data1-v1.xlsx).

License: CC-BY-4.0. Bytes: 553,634. SHA-256: `bc1b7ff69f55c5c7febb7ca0a05ff39f88496eef9694f5a45f14f5329b5c245c`.

## KLHDC2 — klhdc2-analogs.xlsx

Zhou, Zhou et al., 2025. [Primary source](https://doi.org/10.7554/eLife.106844); [original download](https://cdn.elifesciences.org/articles/106844/elife-106844-fig3-data1-v1.xlsx).

License: CC-BY-4.0. Bytes: 442,591. SHA-256: `4af37ee7723dde7f21e5f4bcf7bcd4ecfc9a187d323e28b29df2273c9ef42fc5`.

## TBXT — tbxt.xlsx

Davis-Gilbert, Drewry, Hossain et al., 2022. [Primary source](https://doi.org/10.5281/zenodo.6394811); [original download](https://zenodo.org/api/records/6394811/files/20201028%20LMW%20binding%20affinity%20screen%20for%20136%20UNC%20and%20Piramal%20compounds.xlsx/content).

License: CC-BY-2.0. Bytes: 9,108,722. SHA-256: `f010cca202fb4174dadd987425d45e2d3a75d7eea2a85a5cb454d5df70e08e53`.

## Exact selection and evidence boundaries

- STAT3: the three nonempty sheets in Additional file 1; numerical TIME and three
  flow-rate response columns. Blank cells are omitted per trace. Article methods
  specify double referencing. S3I-201 interaction and DPP lack of measurable
  response are author-reported conclusions restricted to mouse STAT3beta core
  residues 127–722 and tested conditions. They are not universal binding labels.
- CYP3A4: `SPR titration sheet 1`, columns 1–9 (time and eight observations); and
  observed cells in columns 2–9 of `SPR titration sheet 2`. Exclude `_Fit` and
  `FittedCurve`. Trace concentration headers are rounded (e.g. 0.78 µM), whereas
  endpoint concentrations retain their exported precision. Do not equate these
  two representations without allowing for the source rounding.
- LRRK2: ZIP members `Sensorgrams_E11.txt` and first two columns of
  `Steady state_E11.txt`. Seven concentration series, 7.8125–500 nM. Source-fitted
  parameters and curve columns are retained only in the original archive, never
  provided to agents. Original authors report apparent KD 70.3 nM; this is a
  comparison, not a gold-standard truth label. This release's specified unweighted
  free-offset refit yields about 104 nM rather than 70.3 nM; the exported source
  parameter is not used as the scoring target. Do not infer catalytic inhibition
  from the SPR data alone.
- KLHDC2: Figure 2E/2F and Figure 3F/3G only, corresponding to compounds 1/2 and
  5/6. These are representative SPR traces; other worksheets contain orthogonal
  fluorescence-polarization data and are excluded. Do not invent sensorgrams for
  the compounds for which the article reports no robust SPR signal.
- TBXT: `Report point table`, rows with Step purpose=Analysis, preserving original
  compound names and replicate/series suffixes. Relative responses, windows,
  concentrations, reference types and source row indices are retained. Selected
  workbook is `20201028 LMW binding affinity screen for 136 UNC and Piramal
  compounds.xlsx`. It supplies numeric report points and embedded sensorgram
  images, not a usable numeric full-time-series export. Source-fitted kinetic/
  affinity tables are excluded from input. Response values do not supply an
  independently validated 136-compound binder/nonbinder ground truth.

CSV conversion, selected sheets/columns, unit conversion, omitted empty cells,
row ordering and robustness-case ID aliases are the only changes. No smoothing,
interpolation, digitized images, simulated negatives, fabricated concentrations,
synthetic replicates or source-fitted curves enter measurements.csv.

No pathogen targets, nucleic-acid hybridization or aptamer cases are included.
Original data licenses apply to originals and extracted subsets. Preserve author,
source and license attribution when redistributing. License links are in
THIRD_PARTY_NOTICES.md. All inclusion decisions and limitations are public; the
source catalogue is not a blinded label set.
