# NHANES RXQ_RX year-over-year audit (Week 2) — key findings

Source pages: RXQ_RX_F (2009-10), RXQ_RX_G (2011-12), RXQ_RX_H (2013-14), RXQ_RX_I (2015-16), P_RXQ_RX (2017-Mar 2020), RXQ_RX_L (Aug 2021-Aug 2023). Audited 2026-10-12. Full cell-by-cell text lives in the project doc `claude/nhanes-rxq-rx-change-audit.md` (Claude project "CREL x HSPH") and the Week 2 results sheet.

- Eligible sample never changes in meaning: all survey participants, all ages, every cycle.
- 2013-14 adds RXDRSC1/2/3 (ICD-10-CM reason-for-use codes, up to 3 per drug; self-reported reason coded by NCHS with 2016 ICD-10-CM, NOT a physician diagnosis) and RXDRSD1/2/3 (descriptions). Prevention gets a "P" suffix (A49.9P = prevent bacterial infection); 55555/77777/99999 = unknown/refused/don't know. RXQSEEN gains code 3 ("Only pharmacy print out seen").
- ICD appendix granularity drops: 489 distinct codes (2013-14) -> 244 (2015-16) -> 251 (2017-Mar 2020); only 184 shared between 2013-14 and 2015-16. 2013-14 used fine codes like Z95.5; 2015+ lists bare Z95. => Pool RXDRSC at the 3-character category.
- 2017-Mar 2020 (P_) is a 3.2-year combined pre-pandemic file with its own weights (WTINTPRP); never stack with the separate 2017-18 file.
- Aug 2021-Aug 2023 keeps only SEQN, RXQ033 (any Rx past 30 d), RXQ050 (count 1-5+); one row per person. No drug names, codes, duration, container-seen, or reasons. Drug/indication-specific analysis ends at March 2020.
- Rows per file: 20,905 / 18,704 / 20,194 / 19,647 / 32,962 / 11,933. Multum Lexicon: Dec 2010 / Dec 2012 / Dec 2014 / Dec 2016 / Dec 2019 / none.
