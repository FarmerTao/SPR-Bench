# Source catalogue and extraction notes

Six studies; seven bundled source files. Accessed 2026-11-12. These are measured experimental data, with source preprocessing retained.

## STAT3 — stat3.xlsx

Mtwebana and Prinsloo, 2020. [Primary source](https://doi.org/10.1186/s13104-020-05189-w); [original download](https://static-content.springer.com/esm/art%3A10.1186%2Fs13104-020-05189-w/MediaObjects/13104_2020_5189_MOESM1_ESM.xlsx).

License: CC0-1.0 (data); article CC-BY-4.0. Bytes: 145,294. SHA-256: `a8078400650985e5de25b44d4ae8e642c4fcc0dff31df9418c44ad294a81d58d`.

## TBXT — tbxt.xlsx

Davis-Gilbert, Drewry, Hossain et al., 2022. [Primary source](https://doi.org/10.5281/zenodo.6394811); [original download](https://zenodo.org/api/records/6394811/files/20201028%20LMW%20binding%20affinity%20screen%20for%20136%20UNC%20and%20Piramal%20compounds.xlsx/content).

License: CC-BY-2.0. Bytes: 9,108,722. SHA-256: `f010cca202fb4174dadd987425d45e2d3a75d7eea2a85a5cb454d5df70e08e53`.

## LRRK2 — lrrk2.zip

Dederer et al., 2024. [Primary source](https://doi.org/10.5281/zenodo.10471514); [original download](https://zenodo.org/api/records/10471514/files/Figure%201B_SPR%20datasets.zip/content).

License: CC-BY-4.0. Bytes: 2,316,436. SHA-256: `484b7e7782ebc66ff69ca734592d3ec9d0681d86c8d1ddca6b070ec738b68997`.

## Macrocycle — macrocycle-fig2.xlsx

Rettie et al., 2025. [Primary source](https://doi.org/10.1038/s41589-025-01929-w); [original download](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-025-01929-w/MediaObjects/41589_2025_1929_MOESM4_ESM.xlsx).

License: CC-BY-4.0. Bytes: 389,575. SHA-256: `36e1c96e9603fbcf0c9eacac9f3c72aa479ab30dd8f757a0ee28fa686d274f50`.

## Macrocycle — macrocycle-fig4.xlsx

Rettie et al., 2025. [Primary source](https://doi.org/10.1038/s41589-025-01929-w); [original download](https://static-content.springer.com/esm/art%3A10.1038%2Fs41589-025-01929-w/MediaObjects/41589_2025_1929_MOESM6_ESM.xlsx).

License: CC-BY-4.0. Bytes: 184,250. SHA-256: `aec410468f8730c6306eaf50154985b24c65c11612308349d1ddc3d510f11321`.

## ISG65 — isg65-fig2-data1.xlsx

Cook, Carrington, Higgins, 2024. [Primary source](https://doi.org/10.7554/eLife.88960); [original download](https://cdn.elifesciences.org/articles/88960/elife-88960-fig2-data1-v1.xlsx).

License: CC-BY-4.0. Bytes: 217,765. SHA-256: `82f9885508388e446ebd013cc9952bf86a544df36d81a69d3b1612e9c711e5a0`.

## D-box — dbox-fig4-data1.xlsx

Eapen et al., 2026. [Primary source](https://doi.org/10.7554/eLife.104238); [original download](https://cdn.elifesciences.org/articles/104238/elife-104238-fig4-data1-v1.xlsx).

License: CC-BY-4.0. Bytes: 363,946. SHA-256: `3d4a19398f04fb6f3dd0bc919a819535aea607f389b4a5e467126cda69b351cc`.

## Exact selection and evidence boundaries

- STAT3: three nonempty sheets in Additional file 1; numerical TIME and three
  flow-rate response columns. Blank cells are omitted per trace. Article methods
  specify double referencing. S3I-201 interaction and DPP lack of measurable
  response are author-reported conclusions restricted to mouse STAT3beta core
  residues 127–722 and tested conditions. They are not universal binding labels.
- TBXT: `Report point table`, rows with Step purpose=Analysis, preserving original
  compound names and replicate/series suffixes. Relative responses, windows,
  concentrations, reference types and source row indices are retained. Selected
  workbook is `20201028 LMW binding affinity screen for 136 UNC and Piramal
  compounds.xlsx`. It supplies numeric report points and embedded sensorgram
  images, not a usable numeric full-time-series export. Source-fitted kinetic/
  affinity tables are excluded from input. The binding labels are a disclosed
  operational 10 RU threshold on the maximum corrected binding-late response,
  not an independently validated 140-compound binder/nonbinder ground truth.
- LRRK2: ZIP members `Sensorgrams_E11.txt` and first two columns of
  `Steady state_E11.txt`. Seven concentration series, 7.8125–500 nM. Source-fitted
  parameters and curve columns are retained only in the original archive, never
  provided to agents. Original authors report apparent KD 70.3 nM; this is a
  comparison, not a gold-standard truth label. The specified unweighted
  free-offset refit is not forced to that value. Do not infer catalytic inhibition
  from SPR alone.
- Macrocycle: `macrocycle-fig2.xlsx` Sheet1 columns A/B (MCB_D2) and E/F
  (MDB_D8), plus `macrocycle-fig4.xlsx` Sheet1 columns A/B (RBB_D10). Header rows
  1–2; measured cells only; source-fitted columns C/G excluded. These are
  single-concentration traces (20, 50 and 20 µM; 30 µL/min), not KD
  measurements. The source reports global-fit KD values of 2 µM (MCB_D2),
  1.9 µM (MDB_D8) and 9.4 nM (RBB_D10); these traces do not reproduce those
  global fits.
- ISG65: Figure 2—source data 1, six sheets (C3b/C3d × WT/ΔL2/L2N188A). Column A
  is time; measured cycle columns are B,D,F,H,J,L (`Cycle ... _Y`); interleaved
  source-fitted columns C,E,G,I,K are excluded. Six cycles per sheet, twofold
  dilutions from 10 µM, 30 µL/min. The affinity task uses the measured response
  cell nearest 120 s (end of the 120 s association phase) for each trace; this is
  a derived endpoint, not a source-reported equilibrium fit. Source-fitted curves
  and reported affinities are not scoring targets.
- D-box: `dbox-fig4-data1.xlsx` sheets `Figure 4C -D20 Fc4-1 isotherm` and
  `Figure 4D -D21 Fc4-1 isotherm`, data from row 2 (0.15625–10 µM). The paired
  sensorgrams remain in the source file but are not task inputs. No fitted curve
  is selected. D20/D21 are Fc-fused D-box peptides binding Cdc20; the tasks
  summarize observed endpoints, not a kinetic mechanism.

CSV conversion, selected sheets/columns, unit conversion, omitted empty cells,
row ordering and robustness-case ID aliases are the only changes. No smoothing,
interpolation, digitized images, simulated negatives, fabricated concentrations,
synthetic replicates or source-fitted curves enter measurements.csv.

No pathogen targets, nucleic-acid hybridization or aptamer cases are included.
Original data licenses apply to originals and extracted subsets. Preserve author,
source and license attribution when redistributing. License links are in
THIRD_PARTY_NOTICES.md. All inclusion decisions and limitations are public; the
source catalogue is not a blinded label set.
