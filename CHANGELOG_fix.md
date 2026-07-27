# Crosswalk fix — sourced from the official IHDS-I codebook

## What changed
Two rows added to `data/ihds_district_crosswalk.csv` (379 → 381 rows), one
existing row's note updated. Both changes are sourced from primary
documents, not inferred:

1. **Tamil Nadu, dist01=6, Tiruvannamalai — added, status CONFIRMED.**
   This was a genuine omission, not a structural limitation. Confirmed
   present in the IHDS-I codebook's own official District Codes table
   (`Docrelinfo.pdf`), and in real household data: 45 households in
   IHDS-I, 41 in IHDS-II.

2. **Maharashtra, dist01=22, Mumbai Suburban — added, status CONFIRMED.**
   This one your own crosswalk had already flagged as an open question —
   the existing dist01=23 (Mumbai) row's note read *"verify whether this
   DISTID captures Mumbai City only or also Mumbai Suburban... Mumbai
   Suburban does not appear as its own DISTID in this state's sampled
   list."* Resolved: confirmed via IHDS-II's own `DISTRICT` variable value
   label (code 2722 = "Mumbai (suburban)" in the .dta metadata itself —
   a primary source). It has 0 households in IHDS-I and 319 in IHDS-II,
   confirming Mumbai Suburban only became its own trackable code starting
   with IHDS-II. The Mumbai (23) row's note now states it should be read
   as covering both Mumbai City and Suburban for IHDS-I-only analyses.

## What did NOT need fixing
The other 6 Maharashtra codes I'd flagged as a "gap" in the last patch
(4, 12, 19, 24, 28, 33) turned out **not to be a gap at all** — I
cross-checked them against the official IHDS-I codebook's own District
Codes table and confirmed these exact same 7 codes are simply absent from
IHDS's own documented sampling frame (0 households in either wave). The
crosswalk's original 27-row Maharashtra coverage was already complete and
correct relative to what IHDS actually sampled. That earlier "gap" claim
was wrong — retracted here with the source that corrects it.

## New result after the fix
| Wave | Match rate before | Match rate after |
|---|---|---|
| IHDS-I (2005) | 96.73% | 96.84% |
| IHDS-II (2012) | 96.19% | 97.04% |

## One more thing worth a documentation update (not fixed here — flagging only)
Checking the remaining unmatched households after the fix shows the
"state-level-only, DIST01=0" limitation is **broader than what
METHODOLOGY.md currently documents**. The current doc names 5 states +
Daman & Diu. The real full list, confirmed directly from both household
files, is **11 states/UTs**: Chandigarh, Sikkim, Arunachal Pradesh,
Nagaland, Manipur, Mizoram, Tripura, Meghalaya, Daman & Diu, Dadra & Nagar
Haveli, and Puducherry — all of them IHDS's original "extension sample"
states (sampled at state level only, per the IHDS-I codebook's own
sampling methodology section). This doesn't change any data, just means
the methodology write-up undersells the true scope of this known,
structural limitation. Worth a one-line update next time you touch
METHODOLOGY.md.
