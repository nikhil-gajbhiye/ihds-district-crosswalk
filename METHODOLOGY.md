# A District Crosswalk for IHDS: Methodology Note

## What this is

A crosswalk linking district identifiers in the India Human Development
Survey (IHDS-I, 2004-05 and IHDS-II, 2011-12) to current (2026)
administrative districts. It exists because IHDS's own geography is
anchored to 2001 Census district boundaries, and India has since split,
renamed, and reorganized dozens of districts — a mismatch that affects
anyone trying to link IHDS to present-day administrative, electoral, or
programmatic data.

## The core finding: don't join on `DISTID`

IHDS's household files carry a field called `DISTID` that looks, at
first glance, like the natural join key — it is small, sequential, and
consistently present. **It is the wrong field to use.**

`DISTID` is an internal survey-administration code. In at least six
states (Madhya Pradesh, Karnataka, Gujarat, Tamil Nadu, Rajasthan, and
Delhi) it does not map one-to-one onto real districts: a single
`DISTID` value can span two genuinely different districts, or two
different `DISTID` values can both refer to the same real district. For
example, in both IHDS-I and IHDS-II, `DISTID=27` in Madhya Pradesh
contains households from both West Nimar (Khargone) *and* Barwani —
two different, adjacent, real districts collapsed into one internal
code.

The correct field is `DIST01`, documented in the IHDS-II codebook
(ICPSR 36151) as *"District ID corrected Census 2001."* Cross-checking
`DIST01` against every `DISTID` collision found in this project
resolved all of them, identically, in both IHDS-I and IHDS-II —
independent confirmation that this is a real, general property of the
IHDS data model, not a one-off data-entry error. IHDS-II additionally
provides a `DISTRICT` variable that combines state and `DIST01` into a
single pre-labeled field, which is the simplest key to use for any
IHDS-II-based work going forward.

**Practical takeaway for anyone using IHDS district geography:**
join and aggregate on `DIST01` (or IHDS-II's `DISTRICT`), never on
`DISTID`. This project's crosswalk is keyed on `DIST01` throughout;
the original `DISTID` is retained in the output only as a legacy
reference column, explicitly labeled not to be used as a join key.

## What the crosswalk covers

The crosswalk maps each 2001-Census district sampled by IHDS-I
(now 377 state-district combinations across 33 states/UTs, after the
Tamil Nadu and Maharashtra additions below) to its current (2026)
successor district(s), drawing on real administrative-history sourcing
(state government notifications, Wikipedia district lists cross-checked
against contemporaneous news coverage, the official IHDS-I codebook's
District Codes table, and — for the cases it resolved — cross-wave
codebook lookups) rather than assumption.

Status breakdown (381 rows delivered; 3 rows dropped as confirmed
duplicates once `DIST01` resolved them to a single real district):

- **330 CONFIRMED** — multiply-sourced, or directly resolved via
  `DIST01`/`DISTRICT`. A dedicated verification pass upgraded Bihar
  (17 rows — confirmed no new district since Arwal in 2001), Himachal
  Pradesh (9 rows — confirmed stable since 1972), Rajasthan (21 rows —
  cross-checked against three independent news sources on the exact
  2023/2024 district list), and several individual Uttar Pradesh and
  Chhattisgarh rows from PROVISIONAL to CONFIRMED. Also includes two
  rows added in a later pass — Tamil Nadu's Tiruvannamalai and
  Maharashtra's Mumbai Suburban — see below.
- **40 PROVISIONAL** — either not individually re-verified against a
  dedicated source, or a genuine multi-parent split that can't be
  fully resolved at the district level alone. Delhi's real revenue
  districts are now structurally resolved (see below) but several
  remain provisional pending confirmation of a December 2025/January
  2026 reorganization that expanded Delhi from 11 to 13 districts —
  too recent to have settled, reliable secondary coverage yet.
- **14 UNRESOLVED** — see below.
- **3 WEAK** — thin sourcing, flagged for a follow-up check.

## Delhi: a second structural finding, resolved via the IHDS-I codebook

Delhi's `DISTID` list looked, on inspection, like it mixed real
districts with something else entirely — and the official IHDS-I
codebook (22626-0002-Codebook.pdf) confirmed exactly that. Of the
codes present, seven are genuine revenue districts (North West, North,
North East, East, West, South West, South) — but two more,
**"Delhi Municipal Corp" and "New Delhi Municipal Corp,"** are not
districts at all. They are local governance bodies (the Municipal
Corporation of Delhi and the New Delhi Municipal Council), included in
IHDS's sampling frame alongside real districts but not translatable
into the same district-crosswalk framework. Households coded under
those two values cannot be placed onto a district map without a
different, non-district geography — they are marked UNRESOLVED here
for that reason, not because the code itself is unclear.

Separately, Delhi's real revenue districts have been reorganized twice
since IHDS-I's 2001-Census vintage: expanded from 9 to 11 in 2012, and
then from 11 to 13 in a December 2025/January 2026 restructuring that
dissolved Shahdara and realigned district boundaries to match
Municipal Corporation of Delhi zones. That second change is recent
enough that several of Delhi's rows are marked PROVISIONAL pending
clearer confirmation of exactly which old district each new one
succeeded.

## Tamil Nadu and Maharashtra: two gaps found and fixed via primary sourcing

A later validation pass (see `validation/`) cross-checked this
crosswalk directly against real IHDS microdata and found two genuine
gaps, both now fixed:

- **Tamil Nadu, Tiruvannamalai (`DIST01=6`)** was simply missing — a
  plain omission, not a structural limitation. Confirmed present in
  the IHDS-I codebook's own official District Codes table, and in real
  household data (45 households in IHDS-I, 41 in IHDS-II). Added as
  CONFIRMED.
- **Maharashtra, Mumbai Suburban (`DIST01=22`)** resolves a question
  this crosswalk had already flagged in its own notes on the Mumbai
  (23) row. Confirmed via IHDS-II's own `DISTRICT` variable value
  label ("Mumbai (suburban)," embedded directly in the .dta metadata)
  — a primary source, not an inference. It has 0 households in IHDS-I
  and 319 in IHDS-II, meaning Mumbai Suburban only became separately
  trackable starting with IHDS-II; IHDS-I-only analyses should treat
  the Mumbai (23) row as covering both Mumbai City and Mumbai Suburban
  jointly.

A third apparent gap — six other Maharashtra `DIST01` codes (4, 12, 19,
24, 28, 33) initially flagged as missing — turned out not to be a gap
at all on closer check: the official IHDS-I codebook's District Codes
table confirms these exact codes were never part of IHDS's sampling
frame (0 households in either wave). Maharashtra's original 27-row
coverage was already complete relative to what IHDS actually sampled;
only the Mumbai Suburban case above was real.

## What's still genuinely unresolved, and why

Twelve rows, across five states/UTs — Nagaland, Manipur, Tripura,
Meghalaya, and Daman & Diu — cannot be resolved from IHDS data at all.
In both IHDS-I and IHDS-II, every sampled household in these states
carries `DISTID=0` **and** `DIST01=0`: IHDS itself only geocodes these
states down to the state level, not the district level, in either
wave. This is very likely a deliberate design choice tied to small
sample sizes in these states rather than an oversight, but either way
it is a hard limit of the source data, not something a better lookup
can fix. Any work needing district-level detail in these five
states/UTs will need a different data source entirely.

**This same limitation is broader than the five states/UTs above.**
Direct inspection of the raw household files (both waves) shows the
identical `DISTID=0`/`DIST01=0` pattern in six more states/UTs:
Chandigarh, Sikkim, Arunachal Pradesh, Mizoram, Dadra & Nagar Haveli,
and Puducherry — real household counts for all eleven are in
`validation/state_level_only_states.csv`. These six aren't necessarily
marked UNRESOLVED in this crosswalk's row-level status column (some
may carry CONFIRMED or PROVISIONAL name-level reference rows, similar
in spirit to Nagaland/Manipur/Tripura/Meghalaya), but the underlying
constraint is identical: **none of these eleven states/UTs can be
joined back to individual IHDS households at the district level, full
stop**, regardless of what this crosswalk's status column says for
them. Treat the crosswalk's coverage for these eleven as name-level
reference only, not as a working join key, until each is individually
re-audited against this same standard.

One additional case worth flagging even though it's now resolved:
Rajasthan went through a 33-to-50-district reorganization in 2023,
followed by a partial reversal of 9 of those 17 new districts in
December 2024 after sustained local protest (Neem Ka Thana being the
most visible case). The current 41-district structure is reflected
here, but Rajasthan's district map has been unusually unstable and is
worth re-checking against a primary source if this crosswalk is used
much beyond mid-2026.

## Validation

Run `validate.py` from the repo root (requires your own copy of the raw
ICPSR `.dta` files) to check the crosswalk against real IHDS microdata,
not just against itself. Full results and known gaps are in
`validation/README.md`. Current headline numbers: **96.84% match rate
against IHDS-I, 97.04% against IHDS-II** — not 100%, and the validation
folder documents exactly why, including the eleven-state structural
limitation described above.

## Known open items for a future pass

- ~90 rows marked PROVISIONAL were not individually re-verified with a
  dedicated search this round (mostly Bihar, Himachal Pradesh, and
  several "no change identified" rows elsewhere) — treat as
  reasonable defaults, not confirmed facts.
- A handful of multi-parent splits (e.g. Sambhal in Uttar Pradesh,
  drawn from both Moradabad and Budaun; Amethi, drawn from Sultanpur
  and Rae Bareli) are flagged but not resolved at sub-district level —
  doing so would require tehsil-level detail this crosswalk doesn't
  have.
- West Bengal's June 2026 district announcements (Jangipur, Basirhat,
  Arambagh, Sundarban, and a Kolkata reorganization) are included as
  provisional; their notification/implementation status should be
  re-checked before relying on them.
- The six additional state-level-only states/UTs identified above
  (Chandigarh, Sikkim, Arunachal Pradesh, Mizoram, Dadra & Nagar
  Haveli, Puducherry) should each be individually re-audited and, if
  needed, relabeled consistently with Nagaland/Manipur/Tripura/
  Meghalaya/Daman & Diu.

## Data sources

- IHDS-I household file (ICPSR 22626, DS2) and village file (DS7)
- IHDS-I official household and individual linking files
  (IHDS-I ↔ IHDS-II panel linkage)
- IHDS-I official documentation (Docrelinfo.pdf), including its
  District Codes table — used to verify Maharashtra and Tamil Nadu
  coverage against IHDS's own original sampling frame
- IHDS-II household file (ICPSR 36151, DS2) and codebook
- Public sourcing for administrative-history claims: state government
  notifications, Wikipedia district lists, contemporaneous news
  coverage — cited inline in the `reorg_events`/`notes` columns of the
  crosswalk itself, not reproduced here
