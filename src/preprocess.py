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

POLICY_DATE = pd.Timestamp("2020-03-15")


def main() -> None:
    """
    Preprocess Google mobility data into panel format for DiD analysis.
    
    Processing steps:
    1. Load raw Google mobility data
    2. Filter to US state-level observations only
    3. Keep only treated and control states
    4. Create treatment indicators (treated, post, first_treat)
    5. Convert dates to integer time periods
    6. Save cleaned panel dataset
    
    Output columns:
    - unit: State name
    - date: Calendar date
    - outcome: Workplace mobility (% change from baseline)
    - treated: 1 if state received treatment, 0 otherwise
    - post: 1 if date is on/after March 15, 0 otherwise
    - time: Integer days since first date in dataset (0, 1, 2, ...)
    - first_treat: Time period when treatment starts (policy_time for treated, 0 for control)
    
    Raises:
        FileNotFoundError: If raw Google mobility data doesn't exist
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

    df["treated"] = df["unit"].isin(TREATED_STATES).astype(int)
    df["post"] = (df["date"] >= POLICY_DATE).astype(int)

    # Integer time index (days since start)
    t0 = df["date"].min()
    df["time"] = (df["date"] - t0).dt.days

    policy_time = int((POLICY_DATE - t0).days)

    # diff-diff expects first_treat: 0 for never-treated, else first treated period
    df["first_treat"] = df["treated"].apply(lambda x: policy_time if x == 1 else 0)

    df = df.sort_values(["unit", "time"]).reset_index(drop=True)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Saved: {OUT_PATH}")
    print(f"Rows: {len(df):,} | Units: {df['unit'].nunique()} | policy_time={policy_time}")


if __name__ == "__main__":
    main()
