from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --- settings (kept minimal, inside script) ---
CSV_PATH = Path("data/raw/covid_mobility/2020_US_Region_Mobility_Report.csv")
Y_COL = "workplaces_percent_change_from_baseline"

TREATED_STATES = ["New York", "California", "New Jersey", "Washington"]
CONTROL_STATES = ["Texas", "Florida", "Georgia", "South Dakota"]

POLICY_DATE = pd.Timestamp("2020-03-15")
PRE_DAYS = 180


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

    # keep only selected states
    keep_states = set(TREATED_STATES + CONTROL_STATES)
    df = df[df["sub_region_1"].isin(keep_states)].copy()

    # treated indicator
    df["treated"] = df["sub_region_1"].isin(TREATED_STATES).astype(int)

    # daily mean trend by treated vs control
    trend = df.groupby(["date", "treated"], as_index=False)[Y_COL].mean()

    # pre-period filter (parallel trends check)
    pre_start = POLICY_DATE - pd.Timedelta(days=PRE_DAYS)
    trend_pre = trend[(trend["date"] >= pre_start) & (trend["date"] < POLICY_DATE)].copy()

    # pivot + plot
    pivot = (
        trend_pre.pivot(index="date", columns="treated", values=Y_COL)
        .rename(columns={0: "Control", 1: "Treated"})
        .sort_index()
    )

    ax = pivot.plot(figsize=(10, 5))
    ax.set_title("Parallel Trends Check (Pre-Treatment Only)")
    ax.set_ylabel("Workplaces % Change from Baseline")
    ax.set_xlabel("Date")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()