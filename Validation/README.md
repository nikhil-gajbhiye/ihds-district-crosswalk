# Validation results

`validate.py` (repo root) merges the crosswalk against the real IHDS-I and
IHDS-II household files on `(STATEID, DIST01)`. Rerunnable, not a claim.

## Results (after the Tamil Nadu / Maharashtra fix — see CHANGELOG_fix.md)

| Wave | Households | Matched | Unmatched | Match rate |
|---|---|---|---|---|
| IHDS-I (2005) | 41,554 | 40,239 | 1,315 | 96.84% |
| IHDS-II (2012) | 42,152 | 40,906 | 1,246 | 97.04% |

Not 100%, and this file isn't going to pretend otherwise. All remaining
unmatched households belong to states/UTs that IHDS itself only ever coded
at the state level (`DIST01=0` for every household) -- this is a real
limitation of the source data, not a crosswalk error. See
`state_level_only_states.csv` for the full breakdown: it's actually
**11 states/UTs**, not the 5 + Daman & Diu that METHODOLOGY.md currently
says (Chandigarh, Sikkim, Arunachal Pradesh, Nagaland, Manipur, Mizoram,
Tripura, Meghalaya, Daman & Diu, Dadra & Nagar Haveli, Puducherry) -- all of
IHDS's original "extension sample" states. Worth updating METHODOLOGY.md
to reflect the full list.

## How to interpret this if you're merging your own data
If your analysis excludes those 11 states/UTs, or you're comfortable
dropping the ~3% of the sample concentrated there, the crosswalk's
resolvable ~97% match rate is reliable everywhere else.

## Before your next tagged release
- [x] Tamil Nadu (Tiruvannamalai) and Maharashtra (Mumbai Suburban) gaps
      fixed -- see CHANGELOG_fix.md
- [ ] Update METHODOLOGY.md's "state-level-only" section to list all 11
      states/UTs, not 6
- [ ] Only then cut a Zenodo-archived release, so the permanent citable
      snapshot reflects this corrected version
