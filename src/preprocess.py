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
