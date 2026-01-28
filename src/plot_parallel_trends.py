from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"
PRE_DAYS = 180

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first.")

    df = pd.read_csv(DATA_PATH)

    # policy_time is constant for treated rows; grab it once
    policy_time = int(df.loc[df["first_treat"] > 0, "first_treat"].iloc[0])
    pre_start = policy_time - PRE_DAYS

    trend = df.groupby(["time", "treated"], as_index=False)["outcome"].mean()
    trend_pre = trend[(trend["time"] >= pre_start) & (trend["time"] < policy_time)].copy()

    pivot = (
        trend_pre.pivot(index="time", columns="treated", values="outcome")
        .rename(columns={0: "Control", 1: "Treated"})
        .sort_index()
    )

    ax = pivot.plot(figsize=(10, 5))
    ax.set_title("Parallel Trends Check (Pre-Treatment Only)")
    ax.set_ylabel("Workplaces % Change from Baseline")
    ax.set_xlabel("Days since start")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()