"""
Small helper for looking up current (2026) districts from the
IHDS district crosswalk.

Usage:
    from lookup import get_current_district, load_crosswalk

    get_current_district("Madhya Pradesh", 27)
    # -> "Khargone"

    df = load_crosswalk()
    # -> full crosswalk as a pandas DataFrame, for anything more custom
"""

import pandas as pd
from pathlib import Path

_CSV_PATH = Path(__file__).parent / "data" / "ihds_district_crosswalk.csv"


def load_crosswalk() -> pd.DataFrame:
    """Load the full crosswalk as a DataFrame."""
    return pd.read_csv(_CSV_PATH)


def get_current_district(state_2001: str, dist01_census2001: int, quiet: bool = False):
    """
    Look up the current (2026) district(s) for a given 2001-Census
    state name and DIST01 code.

    Parameters
    ----------
    state_2001 : str
        State name as of the 2001 Census (e.g. "Madhya Pradesh").
    dist01_census2001 : int
        The DIST01 code from the IHDS household file -- NOT the
        internal DISTID field. See METHODOLOGY.md for why this
        distinction matters.
    quiet : bool
        If False (default), prints a warning when the matched row's
        status is PROVISIONAL, UNRESOLVED, or WEAK.

    Returns
    -------
    str or None
        The current district name(s), or None if no match is found.
    """
    df = load_crosswalk()
    match = df[
        (df["state_2001"] == state_2001)
        & (df["dist01_census2001"] == dist01_census2001)
    ]

    if match.empty:
        if not quiet:
            print(f"No match found for {state_2001}, DIST01={dist01_census2001}")
        return None

    row = match.iloc[0]
    if not quiet and row["status"] != "CONFIRMED":
        print(
            f"Note: this row's status is {row['status']}. "
            f"See notes: {row['notes']}"
        )

    return row["current_districts_2026"]


if __name__ == "__main__":
    # quick self-test
    print(get_current_district("Madhya Pradesh", 27))
    print(get_current_district("Karnataka", 24))
