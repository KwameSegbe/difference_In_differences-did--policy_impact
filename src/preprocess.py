"""
Data Preprocessing: COVID-19 Mobility Panel Dataset
---------------------------------------------------
This script transforms Google's COVID-19 Community Mobility Reports into a clean
panel dataset suitable for staggered difference-in-differences analysis.

Input:  Raw Google mobility data (state-level, daily observations)
Output: Preprocessed panel with columns needed for Callaway-Sant'Anna estimator

Treatment definition (stay-at-home order start dates):
- Early-treated: New York, California, New Jersey, Washington (Mar 19–23, 2020)
- Late-treated: Texas, Florida, Georgia (Apr 2–3, 2020)
- Never-treated: South Dakota (no statewide stay-at-home order)

Outcome: Workplace mobility (% change from pre-COVID baseline)

Notes for Callaway & Sant'Anna:
- The estimator primarily uses `first_treat` (group/cohort timing) + `time`.
- `treated` and `post` are included for readability/diagnostics but are not required
  by the CS estimator itself.
"""

from pathlib import Path
import pandas as pd

# ---- paths ----
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data/raw/covid_mobility/2020_US_Region_Mobility_Report.csv"
OUT_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

# ---- settings ----
Y_COL = "workplaces_percent_change_from_baseline"

# Keep a small demo set (you can expand later for more stable estimates)
EARLY_TREATED_STATES = ["New York", "California", "New Jersey", "Washington"]
LATE_TREATED_STATES = ["Texas", "Florida", "Georgia"]
NEVER_TREATED_STATES = ["South Dakota"]

KEEP_STATES = set(EARLY_TREATED_STATES + LATE_TREATED_STATES + NEVER_TREATED_STATES)

# State-specific adoption dates (edit if you want a different policy definition)
POLICY_DATES = {
    # Early-treated
    "New York": pd.Timestamp("2020-03-22"),
    "California": pd.Timestamp("2020-03-19"),
    "New Jersey": pd.Timestamp("2020-03-21"),
    "Washington": pd.Timestamp("2020-03-23"),
    # Late-treated
    "Texas": pd.Timestamp("2020-04-02"),
    "Florida": pd.Timestamp("2020-04-03"),
    "Georgia": pd.Timestamp("2020-04-03"),
    # Never-treated (intentionally omitted): South Dakota
}


def main() -> None:
    """
    Preprocess Google mobility data into panel format for staggered DiD.

    Key outputs:
    - unit: State name
    - date: Calendar date
    - outcome: Workplace mobility (% change from baseline)
    - time: Integer days since first date in dataset (0, 1, 2, ...)
    - policy_date: Mapped adoption date per unit (NaT for never-treated)
    - first_treat: First treated time period per unit (0 for never-treated; >0 otherwise)
    - ever_treated: 1 if policy_date exists, else 0
    - treated: time-varying treatment indicator (1 if date >= policy_date else 0; 0 for never-treated)
    - post: alias for treated (kept for readability)
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing file: {CSV_PATH.resolve()}")

    df = pd.read_csv(CSV_PATH)

    # US state-level only: country US, state present, county missing
    df = df[
        (df["country_region_code"] == "US")
        & (df["sub_region_1"].notna())
        & (df["sub_region_2"].isna())
    ].copy()

    df["date"] = pd.to_datetime(df["date"])

    # Restrict to the chosen states
    df = df[df["sub_region_1"].isin(KEEP_STATES)].copy()

    # Build minimal panel
    df = df[["sub_region_1", "date", Y_COL]].rename(
        columns={"sub_region_1": "unit", Y_COL: "outcome"}
    )

    # Integer time index (days since start)
    t0 = df["date"].min()
    df["time"] = (df["date"] - t0).dt.days

    # Map each unit to its policy date (never-treated -> NaT)
    df["policy_date"] = df["unit"].map(POLICY_DATES)

    # first_treat: 0 for never-treated, else days-from-t0 of that state's policy date
    df["first_treat"] = (df["policy_date"] - t0).dt.days
    df["first_treat"] = df["first_treat"].fillna(0).astype(int)

    # ever_treated: derived from policy_date (not from a hard-coded list)
    df["ever_treated"] = df["policy_date"].notna().astype(int)

    # time-varying treatment indicator (diagnostics/readability)
    df["treated"] = (df["date"] >= df["policy_date"]).astype(int)
    df.loc[df["policy_date"].isna(), "treated"] = 0  # never-treated stays 0

    # alias
    df["post"] = df["treated"]

    df = df.sort_values(["unit", "time"]).reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    # Quick diagnostics
    print(f"Saved: {OUT_PATH}")
    print(f"Rows: {len(df):,} | Units: {df['unit'].nunique()} | t0={t0.date()}")
    print("\nPolicy dates by unit:")
    print(df.groupby("unit")["policy_date"].first().sort_values())
    print("\nFirst treatment times by unit (days since t0):")
    print(df.groupby("unit")["first_treat"].first().sort_values())
    print("\nEver treated by unit:")
    print(df.groupby("unit")["ever_treated"].first().sort_values())


if __name__ == "__main__":
    main()
