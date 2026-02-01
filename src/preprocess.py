"""
Data Preprocessing: COVID-19 Mobility Panel Dataset
----------------------------------------------------
This script transforms Google's COVID-19 Community Mobility Reports into a clean
panel dataset suitable for difference-in-differences analysis.

Input:  Raw Google mobility data (state-level, daily observations)
Output: Preprocessed panel with columns needed for Callaway-Sant'Anna estimator

Treatment definition:
- Treated: States that implemented stay-at-home orders on March 15, 2020
  (New York, California, New Jersey, Washington)
- Control: States that did not implement orders at that time
  (Texas, Florida, Georgia, South Dakota)

Outcome: Workplace mobility (% change from pre-COVID baseline)
"""
# 
from pathlib import Path
import pandas as pd

# ---- paths ----
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "data/raw/covid_mobility/2020_US_Region_Mobility_Report.csv"
OUT_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

# ---- settings ----
Y_COL = "workplaces_percent_change_from_baseline"

TREATED_STATES = ["New York", "California", "New Jersey", "Washington"]
CONTROL_STATES = ["Texas", "Florida", "Georgia", "South Dakota"]

# State-specific adoption dates (EDIT THESE to the correct policy start dates you want)
POLICY_DATES = {
    "New York": pd.Timestamp("2020-03-22"),
    "California": pd.Timestamp("2020-03-19"),
    "New Jersey": pd.Timestamp("2020-03-21"),
    "Washington": pd.Timestamp("2020-03-23"),
}


def main() -> None:
    """
    Preprocess Google mobility data into panel format for staggered DiD (Callaway-Sant'Anna / Sun-Abraham).

    Key outputs:
    - unit: State name
    - date: Calendar date
    - outcome: Workplace mobility (% change from baseline)
    - treated: time-varying treatment indicator (1 if date >= that state's policy date, else 0; always 0 for controls)
    - post: alias for treated (kept for readability)
    - time: Integer days since first date in dataset (0, 1, 2, ...)
    - first_treat: first treated time period per unit (0 for never-treated controls; >=1 for treated states)
    """
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing file: {CSV_PATH.resolve()}")

    df = pd.read_csv(CSV_PATH)

    # US state-level only
    df = df[
        (df["country_region_code"] == "US")
        & (df["sub_region_1"].notna())
        & (df["sub_region_2"].isna())
    ].copy()

    df["date"] = pd.to_datetime(df["date"])

    keep_states = set(TREATED_STATES + CONTROL_STATES)
    df = df[df["sub_region_1"].isin(keep_states)].copy()

    # Build minimal panel
    df = df[["sub_region_1", "date", Y_COL]].rename(
        columns={"sub_region_1": "unit", "date": "date", Y_COL: "outcome"}
    )

    # Integer time index (days since start)
    t0 = df["date"].min()
    df["time"] = (df["date"] - t0).dt.days

    # Map each unit to its policy date (controls get NaT)
    df["policy_date"] = df["unit"].map(POLICY_DATES)

    # first_treat: 0 for never-treated controls, else days-from-t0 of that state's policy date
    df["first_treat"] = (df["policy_date"] - t0).dt.days
    df["first_treat"] = df["first_treat"].fillna(0).astype(int)

    # Ever-treated flag (useful for debugging / summaries)
    df["ever_treated"] = df["unit"].isin(TREATED_STATES).astype(int)

    # Time-varying treatment indicator (needed for some placebo helpers)
    df["treated"] = 0
    is_treated_state = df["unit"].isin(POLICY_DATES.keys())
    df.loc[is_treated_state, "treated"] = (
        df.loc[is_treated_state, "date"] >= df.loc[is_treated_state, "policy_date"]
    ).astype(int)

    # Keep 'post' as a readability alias (state-specific)
    df["post"] = df["treated"]

    df = df.sort_values(["unit", "time"]).reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    # Quick diagnostics
    print(f"Saved: {OUT_PATH}")
    print(f"Rows: {len(df):,} | Units: {df['unit'].nunique()} | t0={t0.date()}")
    print("\nFirst treatment times by unit (days since t0):")
    print(df.groupby("unit")["first_treat"].first().sort_values())


if __name__ == "__main__":
    main()