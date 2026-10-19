# weekly findings log

## Week 2 — year-over-year audit of RXQ_RX

Source pages: RXQ_RX_F (2009-10), RXQ_RX_G (2011-12), RXQ_RX_H (2013-14), RXQ_RX_I (2015-16), P_RXQ_RX (2017-Mar 2020), RXQ_RX_L (Aug 2021-Aug 2023). Audited 2026-10-12. Full cell-by-cell text lives in the project doc `claude/nhanes-rxq-rx-change-audit.md` (Claude project "CREL x HSPH") and the Week 2 results sheet.

- Eligible sample never changes in meaning: all survey participants, all ages, every cycle.
- 2013-14 adds RXDRSC1/2/3 (ICD-10-CM reason-for-use codes, up to 3 per drug; self-reported reason coded by NCHS with 2016 ICD-10-CM, NOT a physician diagnosis) and RXDRSD1/2/3 (descriptions). Prevention gets a "P" suffix (A49.9P = prevent bacterial infection); 55555/77777/99999 = unknown/refused/don't know. RXQSEEN gains code 3 ("Only pharmacy print out seen").
- ICD appendix granularity drops: 489 distinct codes (2013-14) -> 244 (2015-16) -> 251 (2017-Mar 2020); only 184 shared between 2013-14 and 2015-16. 2013-14 used fine codes like Z95.5; 2015+ lists bare Z95. => Pool RXDRSC at the 3-character category.
- 2017-Mar 2020 (P_) is a 3.2-year combined pre-pandemic file with its own weights (WTINTPRP); never stack with the separate 2017-18 file.
- Aug 2021-Aug 2023 keeps only SEQN, RXQ033 (any Rx past 30 d), RXQ050 (count 1-5+); one row per person. No drug names, codes, duration, container-seen, or reasons. Drug/indication-specific analysis ends at March 2020.
- Rows per file: 20,905 / 18,704 / 20,194 / 19,647 / 32,962 / 11,933. Multum Lexicon: Dec 2010 / Dec 2012 / Dec 2014 / Dec 2016 / Dec 2019 / none.

## Week 3 — candidate "life-saving drug" conditions and their prevalence

Data: `nhanes_2003_2020_rx_demo_drug.csv` (aggregated RXQ_RX + DEMO), filtered to 2013-14, 2015-16, 2017-Mar 2020. Code: `scripts/condition_prevalence.py` (reproduces `outputs/justin_conditions.tsv` byte-for-byte). Deliverable: "Justin" tab of the Week 3 Results sheet. Analysis date 2026-10-15.

### Selection criteria

A condition qualifies if (1) there is a life-saving drug for it, (2) nobody would take that drug without the condition, and (3) a person with the condition who stops the drug is in serious trouble. Jesse's starting points: anticoagulants, oral cancer drugs, immunosuppressants. 20 candidates were drawn up from the literature, then checked against the reason-for-use codes.

### Counting rules

- Person-level: unique SEQN, counted once if any of RXDRSC1/2/3 on any of their drugs matches.
- Match on the first 3 characters of the ICD-10-CM code (E10 yes; E10.2 too specific; E too broad), because 2015+ coding is coarser than 2013-14.
- Codes ending in "P" (NHANES "taken to prevent") counted in a separate column.
- Weight = WTINT2YR (2013-14, 2015-16) or WTINTPRP (2017-Mar 2020). Share of US population = summed weight of matching people / summed weight of all 35,706 people in the period = 950.0 million (311.2 + 316.5 + 322.3).

### Results (raw people; % of US population; P-code people)

| Condition | 3-char code(s) | n | % | P n (%) |
|---|---|---|---|---|
| Heart failure | I50 | 312 | 0.844 | 0 |
| Atrial fibrillation | I48 | 201 | 0.757 | 0 |
| Bipolar disorder | F31 | 195 | 0.755 | 0 |
| Epilepsy | G40 + R56 | 248 | 0.733 | 1 |
| Venous thromboembolism (DVT/PE) | I26 + I80 | 90 | 0.285 | 0 |
| Breast cancer | C50 | 56 | 0.235 | 30 (0.112) |
| Heart attack / ischemic heart disease | I21 + I25 | 64 | 0.231 | 498 (1.411) |
| Type 1 diabetes | E10 | 41 | 0.178 | 0 |
| Cardiac/vascular implant (valve, stent, CABG, pacemaker) | Z95 | 39 | 0.153 | 0 |
| HIV | B20 | 41 | 0.145 | 0 |
| Opioid use disorder | F11 | 29 | 0.143 | 0 |
| Prostate cancer | C61 | 24 | 0.059 | 1 |
| Adrenal insufficiency | E27 | 11 | 0.032 | 0 |
| Pulmonary hypertension | I27 | 9 | 0.022 | 0 |
| Hepatitis B | B19 | 11 | 0.017 | 0 |
| Severe allergy / anaphylaxis risk | Z91 | 3 | 0.006 | 0 |
| Solid organ transplant | Z94 / T86 | 1 | 0.002 | 36 (0.093) |
| CML, myasthenia gravis, cystic fibrosis | C92, G70, E84 | 0 | 0 | 0 |

### Verification

- Total weight = 950.0M as expected; no missing weights; weight constant within each SEQN.
- E10 and I48 recomputed with an independent row-by-row loop: identical counts and shares.
- Every 3-character count (treat and prevent) matches Daniel's `condition_list_icd10cm_2013_2020.csv` exactly.

### Judgment calls

- **T78 excluded from anaphylaxis.** All 508 T78 people are T78.40 "Allergy, unspecified" (antihistamine users). Row uses Z91 only. Literal 3-char result would be 510 / 1.477%.
- **B18 excluded from hepatitis B.** All 3 B18 people are B18.2 = hepatitis C. Row uses B19 only. Literal result would be 14 / 0.027%.
- **Z95** at 3 characters lumps valves, stents, bypass and pacemakers; only Z95.2 (7 people, all on warfarin) is the mechanical-valve case.
- **Transplant** lives almost entirely in the P code T86.9P (36 vs 1 under Z94); **breast cancer** P-code people (30) are likely survivors on adjuvant therapy. For these two rows "P" does not mean "doesn't have the condition".
- **D75.9P "Prevent blood clots"** (456 people, 1.4% of US) is where most warfarin/DOAC users land, but it maps to no single condition (AF / VTE / valves), so it is in no row. Needs a group decision.
- Pooling three cycles without rescaling weights gives an average prevalence over the period, as the brief specifies. Shares are unchanged under a formal pooled estimate (weights ÷ 3); "Americans represented" counts would be ÷ 3.

### Fit assessment

- Strong fits (condition visible, drug specific, stopping is dangerous): HIV, transplant, type 1 diabetes, atrial fibrillation, VTE, mechanical valve, stent/MI, breast cancer, epilepsy, adrenal insufficiency, opioid use disorder.
- Borderline: heart failure (only sacubitril/valsartan is HF-specific; 8 of 312 take it), bipolar (20 of 195 on lithium), pulmonary hypertension and hepatitis B (tiny n, vague codes).
- Likely drops: CML, myasthenia gravis, cystic fibrosis, anaphylaxis (0-3 people by code even though their drugs appear). Swap-in candidates if needed: hypothyroidism/levothyroxine, sickle cell/hydroxyurea, clozapine/schizophrenia.

### Open questions for the team

1. How to allocate D75.9P "Prevent blood clots" across AF / VTE / valves.
2. Whether transplant and breast-cancer P codes count as "has the condition".
3. Confirm the drop list and whether to swap in replacements.
4. Pooled-weight convention (÷ 3 or not) for reporting counts of Americans.

### Next step

For each condition kept, estimate the second proportion in the chain: among people with the code, the fraction on the specific life-saving drug (already noted in the sheet where checked, e.g. AF 90/201 on an anticoagulant, epilepsy 220/248 on an antiseizure drug, T1D 40/41 on insulin). `scripts/explore_codes.py drug-users` lists who takes a drug and why.