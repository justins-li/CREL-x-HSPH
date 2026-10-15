#!/usr/bin/env python3
"""
Exploration helpers used to build the Week 3 candidate list (not needed to
reproduce the final table, but kept for provenance).

  list-codes   every distinct RXDRSC code + RXDRSD description, with row counts
  drug-users   number of unique people (2013+) taking drugs matching a regex,
               and the reason codes they report

Usage:
    python scripts/explore_codes.py list-codes data/nhanes_2003_2020_rx_demo_drug.csv
    python scripts/explore_codes.py drug-users data/nhanes_2003_2020_rx_demo_drug.csv "WARFARIN|APIXABAN"
"""
import sys

import pandas as pd

CYCLES_2013_PLUS = ["2013-2014", "2015-2016", "2017-March 2020 pre-pandemic"]


def load(path):
    cols = ["SEQN", "cycle", "RXDDRUG"] + [f"RXDRS{k}{i}" for k in "CD" for i in (1, 2, 3)]
    df = pd.read_csv(path, low_memory=False, usecols=cols)
    return df[df.cycle.isin(CYCLES_2013_PLUS)]


def long_codes(df):
    parts = [df[["SEQN", "RXDDRUG"]].assign(c=df[f"RXDRSC{i}"], d=df[f"RXDRSD{i}"]) for i in (1, 2, 3)]
    return pd.concat(parts).dropna(subset=["c"])


def main():
    cmd, path = sys.argv[1], sys.argv[2]
    df = load(path)
    long = long_codes(df)
    if cmd == "list-codes":
        vc = long.groupby(["c", "d"]).size().reset_index(name="rows").sort_values("c")
        vc.to_csv(sys.stdout, index=False)
    elif cmd == "drug-users":
        pat = sys.argv[3]
        users = df[df.RXDDRUG.str.contains(pat, na=False)]
        print(f"unique people taking /{pat}/ (2013+): {users.SEQN.nunique()}")
        print(users.RXDDRUG.value_counts().head(15).to_string())
        print("\nreasons they report:")
        print(long[long.RXDDRUG.str.contains(pat, na=False)].c.value_counts().head(15).to_string())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
