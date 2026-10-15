# CLAUDE.md — context for Claude Code

Read this first. It is the handoff from the Cowork session that built this repo (2026-10-15).

## What this project is

CREL x HSPH group research project (Justin Li, Harvard; teammates Michael, Mahin, Aarush, Daniel; supervisor Jesse) on **medication access/adherence and mortality**. The approach is parametrized: estimate the proportion of the US population in each category (has condition X → takes life-saving drug Y → ...) from NHANES and the literature, then multiply the proportions. We deliberately do NOT compare people who take their medication vs those who don't, because of confounding (lifestyle, SES, habits).

The current task (Week 3) is to find conditions that satisfy all of:
1. there is a life-saving drug for it,
2. nobody would take that drug without having the condition,
3. someone with the condition who stops the drug is in serious trouble.

Jesse's suggested starting points: anticoagulants, oral cancer drugs, immunosuppressants.

## Data (NOT committed — put in `data/`, from the team's shared Google Drive folder "CREL x HSPH")

- `nhanes_2003_2020_rx_demo_drug.csv` (65 MB): NHANES RXQ_RX prescription file merged with DEMO, cycles 2003–Mar 2020. One row per drug per person; people reporting no drugs have one row with RXDDRUG blank. 169,334 rows.
- `condition_list_icd10cm_2013_2020.csv`: Daniel's table of every 3-character reason code (people_treat, people_prevent, top_drugs). Our counts match it exactly — use it as a cross-check.
- `DATA_DICTIONARY.xlsx`.
- `Week 3 Results` Google Sheet: tabs Michael, Mahin (top-50 drugs), Aarush, Justin (conditions). Only the **Justin** tab is ours. Columns: Condition | ICD-10-CM code(s) | Life-saving drug(s) | Found in data? | Raw # people (without P) | Share of US population (%) (without P) | Raw # people with P code | Source(s) | Notes. We don't edit the sheet from code; we produce a TSV (`outputs/justin_conditions.tsv`) that Justin pastes in.

## Counting rules that must not change silently

See `docs/METHODS.md`. In short: 2013+ cycles only; match the first 3 characters of RXDRSC1–3; count unique SEQN; `P`-suffixed codes counted separately; weights WTINT2YR (2013-16) / WTINTPRP (2017-Mar 2020); denominator = Σ weights of everyone in 2013–Mar 2020 = 950.0 million.

Two documented deviations from the 3-character rule (T78 excluded from anaphylaxis, B18 excluded from hepatitis B) — keep them unless the team decides otherwise.

## Reproduce / verify

```bash
pip install -r requirements.txt
python scripts/condition_prevalence.py data/nhanes_2003_2020_rx_demo_drug.csv --out outputs/justin_conditions.tsv
git diff --stat outputs/   # should be empty
```

Verification already done is logged in `docs/METHODS.md`. Keep that log updated: every time a number in `outputs/` changes, say why there.

## Working conventions

- Python 3 + pandas. Keep everything in `scripts/`; one script per deliverable, runnable from the repo root with the data path as an argument. No notebooks unless the team asks.
- Outputs that go into the shared sheet are TSVs in `outputs/`, header in the sheet's column order, so they can be pasted into A1.
- Commit outputs alongside the code that made them. Never commit `data/`.
- Justin's preference: fix substantive problems, keep his wording; be picky and honest about errors.

## Open questions for the team (raise before building on them)

1. The generic anticoagulant prevention code **D75.9P "Prevent blood clots"** (456 people, 1.4% of US) holds most warfarin/DOAC users but maps to no single condition (AF / VTE / valves). How do we allocate it?
2. For **transplant** (T86.9P, 36 people) and **breast cancer** (C50.P, 30), the "P" code clearly describes people who HAVE the condition. Treat those P counts as "has condition"?
3. Drop list: CML, myasthenia gravis, cystic fibrosis, anaphylaxis (0–3 people by code). Swap-in candidates: hypothyroidism/levothyroxine (large but rarely fatal), sickle cell/hydroxyurea, treatment-resistant schizophrenia/clozapine.
4. Pooled weights: the brief says divide by the summed weight (~950M). A formal pooled estimate divides each weight by 3. Shares are the same either way; "Americans represented" counts are not.

## Likely next steps (instructions "will come later" — don't start these without them)

- Narrow the 20 candidates to a final set with the team.
- For each final condition: among people with the code, what fraction take the specific life-saving drug (the second proportion in the chain)? `scripts/explore_codes.py drug-users` already lists who takes a drug and why.
- Literature review per condition: mortality with vs without the drug (sources column has starting citations).
- Possibly use RXDDAYS (days on drug) and RXQSEEN (container seen) as adherence/quality signals — see `docs/nhanes-rxq-rx-change-audit.md` for how these variables changed across cycles.
