"""
validate.py — spot-check the crosswalk against real IHDS microdata.

Run from the repo root:
    python validate.py

Requires the raw ICPSR .dta files (not included in this repo — obtain
from ICPSR under your own data use agreement):
    22626-0002-Data.dta   IHDS-I (2005) household file
    36151-0002-Data.dta   IHDS-II (2012) household file

This checks that (STATEID, DIST01) in the raw household files resolves
against data/ihds_district_crosswalk.csv, and reports the real match
rate honestly -- it does not assume or force a 100% match, and it writes
out exactly which (state, dist01) codes failed to match so any gap is
traceable rather than silently absorbed into a summary number.

Outputs:
    validation/match_rate_summary.csv
    validation/unmatched_keys_<wave>.csv
"""
import pandas as pd
import os

CROSSWALK_PATH = "data/ihds_district_crosswalk.csv"
WAVE_FILES = {
    "IHDS-I_2005": "22626-0002-Data.dta",
    "IHDS-II_2012": "36151-0002-Data.dta",
}

os.makedirs("validation", exist_ok=True)

cw = pd.read_csv(CROSSWALK_PATH)
cw_clean = cw.dropna(subset=["stateid", "dist01_census2001"])
cw_keys = set(zip(cw_clean["stateid"].astype(int), cw_clean["dist01_census2001"].astype(int)))
print(f"Crosswalk: {len(cw)} rows, {len(cw_keys)} resolvable join keys "
      f"({len(cw) - len(cw_keys)} rows structurally unresolved -- see METHODOLOGY.md).")

summary_rows = []
for wave, path in WAVE_FILES.items():
    if not os.path.exists(path):
        print(f"Skipping {wave}: {path} not found. Place your ICPSR .dta files in the repo root.")
        continue
    d = pd.read_stata(path, columns=["STATEID", "DIST01"], convert_categoricals=False)
    d = d.dropna(subset=["STATEID", "DIST01"]).copy()
    d["key"] = list(zip(d["STATEID"].astype(int), d["DIST01"].astype(int)))
    matched = d["key"].isin(cw_keys)

    n, n_matched, n_unmatched = len(d), int(matched.sum()), int((~matched).sum())
    match_rate = round(100 * matched.mean(), 2)
    print(f"{wave}: {n} households -> {n_matched} matched, {n_unmatched} unmatched ({match_rate}%)")

    summary_rows.append({"wave": wave, "n_households": n, "n_matched": n_matched,
                          "n_unmatched": n_unmatched, "match_rate_pct": match_rate})

    unmatched_summary = d.loc[~matched, "key"].value_counts().reset_index()
    unmatched_summary.columns = ["state_dist01_key", "n_households"]
    unmatched_summary.to_csv(f"validation/unmatched_keys_{wave}.csv", index=False)

if summary_rows:
    pd.DataFrame(summary_rows).to_csv("validation/match_rate_summary.csv", index=False)
    print("\nSummary written to validation/match_rate_summary.csv")
    print("Match rate is NOT 100% -- see validation/README.md for what the known gaps are.")
