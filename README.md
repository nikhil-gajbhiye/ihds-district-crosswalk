# IHDS District Crosswalk

A crosswalk linking district identifiers in the India Human
Development Survey (IHDS-I, 2004-05 and IHDS-II, 2011-12) to current
(2026) administrative districts.

IHDS's own geography is anchored to 2001 Census district boundaries.
India has since split, renamed, and reorganized dozens of districts —
this project maps the old codes to today's districts, so IHDS data can
be linked to any present-day administrative, electoral, or programmatic
dataset.

**Read [METHODOLOGY.md](METHODOLOGY.md) first.** It explains the most
important finding here: IHDS's `DISTID` field looks like the right key
to join on and isn't — use `DIST01`/`DISTRICT` instead, as documented
inside.

## What's in this repo

- `data/ihds_district_crosswalk.csv` — the crosswalk itself. One row
  per 2001-Census district sampled by IHDS-I, with its current (2026)
  successor district(s), a `status` column (CONFIRMED / PROVISIONAL /
  UNRESOLVED / WEAK), and a `notes` column explaining the sourcing or
  the open question.
- `METHODOLOGY.md` — the write-up: what `DIST01` is and why it matters,
  what's still open, and what's a hard limit of the source data rather
  than something more research can fix.
- `lookup.py` — a small helper function for pulling a district's
  current name(s) out of the crosswalk in your own analysis code.

## Quick use

```python
import pandas as pd

crosswalk = pd.read_csv("data/ihds_district_crosswalk.csv")

# look up a district by its IHDS DIST01 code and state
row = crosswalk[
    (crosswalk["state_2001"] == "Madhya Pradesh") &
    (crosswalk["dist01_census2001"] == 27)
]
print(row["current_districts_2026"].values[0])
```

Or use the helper in `lookup.py`:

```python
from lookup import get_current_district
get_current_district("Madhya Pradesh", 27)
```

## Status of the crosswalk

As of this release: 330 CONFIRMED, 33 PROVISIONAL, 14 UNRESOLVED, 2 WEAK
(379 rows total). See METHODOLOGY.md for what each status means and
what's still open.

## Contributing

If you can verify a PROVISIONAL or WEAK row against a primary source
(a state gazette notification, a Census District Handbook, or similar),
please open an issue or pull request with the source. UNRESOLVED rows
are unresolved for a stated structural reason (see METHODOLOGY.md) —
if you believe one is actually resolvable, please explain why in the
issue.

## Citation

If this is useful in your own research, please cite this repository
(see `CITATION.cff`) and, where relevant, the original IHDS data
(Desai, Sonalde and Reeve Vanneman. *India Human Development Survey*,
ICPSR 22626 and 36151).

## License

Code (`lookup.py`) is released under the MIT License — see `LICENSE`.
The crosswalk data (`data/ihds_district_crosswalk.csv`) is released
under CC-BY 4.0 — see `LICENSE-DATA`.
