# CREL x HSPH — Medication access & mortality: NHANES condition prevalence

Code and outputs for the "life-saving drug" condition work (Week 3 onward).
Project approach: estimate the proportion of the US population in each
category (has condition → takes the drug → ...) from NHANES and the
literature, then multiply proportions; we deliberately avoid directly
comparing adherent vs non-adherent people because of confounding.

## Layout

```
scripts/condition_prevalence.py   # Week 3: candidate conditions → counts + weighted US share (reproduces outputs/justin_conditions.tsv)
scripts/explore_codes.py          # helpers: list every RXDRSC code; who takes a given drug and why
outputs/justin_conditions.tsv     # the "Justin" sheet of "Week 3 Results" (copy-paste into Sheets)
docs/METHODS.md                   # counting rules, verification log, judgment calls
docs/nhanes-rxq-rx-change-audit.md# Week 2: year-over-year audit of RXQ_RX variables (2009–2023)
data/                             # NOT committed. Put nhanes_2003_2020_rx_demo_drug.csv here (from the shared Drive)
```

## Reproduce

```bash
pip install pandas numpy
python scripts/condition_prevalence.py data/nhanes_2003_2020_rx_demo_drug.csv --out outputs/justin_conditions.tsv
```

Expected stderr: `people: 35,706  total weight: 950.0 million`, and the TSV
should be identical to the committed one (`git diff` is empty).

## Inputs (shared Drive, not in repo)

- `nhanes_2003_2020_rx_demo_drug.csv` — aggregated NHANES RXQ_RX + DEMO, 2003–Mar 2020, one row per drug per person (169,334 rows; people with no drugs have one row). 65 MB.
- `condition_list_icd10cm_2013_2020.csv` — Daniel's list of every 3-character reason code with people_treat / people_prevent counts. Used only as an independent check (all counts match).
- `DATA_DICTIONARY.xlsx` — variable definitions.

## Key variables

| Variable | Meaning |
|---|---|
| `SEQN` | person ID (repeats across drug rows) |
| `cycle` | survey cycle; reason codes exist only from 2013-2014 on |
| `RXDDRUG` | generic drug name (Multum) |
| `RXDRSC1..3` / `RXDRSD1..3` | up to 3 ICD-10-CM reason-for-use codes / descriptions per drug. Suffix `P` = NHANES "taken to prevent" |
| `WTINT2YR` | interview weight, 2-year cycles (2013-14, 2015-16) |
| `WTINTPRP` | interview weight, 2017–Mar 2020 pre-pandemic file |
