# Methods & verification log — Week 3 condition prevalence

## Counting rules (from the week-3 brief)

1. Cycles: 2013-2014, 2015-2016, 2017-March 2020 only (RXDRSC codes don't exist before 2013).
2. A person "has" a condition if ANY of their drugs has a reason code in ANY of RXDRSC1/2/3 whose first 3 characters match the condition's category (E10 yes; E10.2 too specific; E too broad).
3. Count unique SEQN, not rows.
4. Codes ending in `P` are NHANES prevention codes ("taken to prevent X") and are counted in a separate column, matched the same way on the first 3 characters.
5. Weight = WTINT2YR (2013-14, 2015-16) or WTINTPRP (2017-Mar 2020). Share = Σ weights of matching people ÷ Σ weights of all 35,706 people in the period = 950.0 million (311.2 + 316.5 + 322.3).

## Verification performed (2026-10-15)

- Total weight = 950.0M, matching the expected ~950M. No missing weights; weight is constant within each SEQN.
- E10 and I48 recomputed with an independent row-by-row loop: 41 / 201 people, identical shares.
- Every 3-character count (treat and prevent) matches Daniel's `condition_list_icd10cm_2013_2020.csv` exactly (e.g. I48 201, E10 41, I21 57 / P 498, C50 56 / P 30, T86 P 36, F11 29).
- Final script `scripts/condition_prevalence.py` reproduces the delivered TSV byte-for-byte.

## Judgment calls (also in the Notes column)

- **T78 excluded from anaphylaxis.** All 508 T78 people are T78.40 "Allergy, unspecified" (antihistamine users). Row uses Z91 only (3 people). Literal 3-char result would be T78+Z91 = 510, 1.477%.
- **B18 excluded from hepatitis B.** All 3 B18 people are B18.2 hepatitis C. Row uses B19 (11 people). Literal result B18+B19 = 14, 0.027%.
- **Z95** at 3 characters merges valves, stents, bypass grafts and pacemakers (39); only Z95.2 = 7 is a prosthetic valve. Kept as one implant row.
- **Transplant** lives almost entirely in the P code T86.9P (36 vs 1 under Z94). **Breast cancer** P-code people (C50.P, 30) are likely survivors on adjuvant therapy. For these two rows "P" does not mean "doesn't have the condition".
- **D75.9P "Prevent blood clots"** (456 people, 1.4%) is where most warfarin/DOAC users land. It has no single 3-char condition, so it is in no row; needs a group decision.
- Pooling three cycles without rescaling weights gives an average prevalence over the period (as the brief specifies). A formal pooled NHANES estimate would divide each weight by 3; shares would be unchanged since numerator and denominator scale together, but the "Americans represented" counts would be ÷3.

## Not findable by reason code (2013+)

C92 chronic myeloid leukemia, G70 myasthenia gravis, E84 cystic fibrosis. Their drugs appear (5 TKI users, 5 pyridostigmine, 23 pancrelipase/ivacaftor) but are coded to other/unknown reasons.
