"""
Parallel Trends Visualization (Pre-Treatment Period)
----------------------------------------------------
This script creates a visual test of the parallel trends assumption by plotting
average mobility trends for treated vs. control states BEFORE treatment.

Parallel trends assumption:
- In the absence of treatment, treated and control groups would have followed
  the same trend over time
- Critical assumption for causal inference in difference-in-differences designs
- Visual test: Lines should move together (parallel) in pre-treatment period

What to look for:
✅ GOOD: Lines move together, similar slopes, no systematic divergence
❌ BAD: Lines diverge, different slopes, one group trending up while other trends down

If parallel trends are violated, the treatment effect estimates may be biased.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"
PLOT_PATH = OUTPUT_DIR / "parallel_trends.png"

PRE_DAYS = 180


def main() -> None:
    """
    Generate parallel trends plot comparing treated vs. control states before treatment.
    
    Steps:
    1. Load panel data
    2. Identify treatment timing (when treated states received orders)
    3. Filter to pre-treatment period only
    4. Calculate average mobility for treated vs. control groups each day
    5. Plot time series to visually assess parallel trends
    
    Raises:
        FileNotFoundError: If preprocessed data doesn't exist
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first.")

    df = pd.read_csv(DATA_PATH)

    # policy_time is constant for treated rows; grab it once
    policy_time = int(df.loc[df["first_treat"] > 0, "first_treat"].iloc[0])
    pre_start = policy_time - PRE_DAYS

    trend = df.groupby(["time", "ever_treated"], as_index=False)["outcome"].mean()
    trend_pre = trend[(trend["time"] >= pre_start) & (trend["time"] < policy_time)].copy()

    pivot = (
        trend_pre.pivot(index="time", columns="ever_treated", values="outcome")
        .rename(columns={0: "Control", 1: "Treated"})
        .sort_index()
    )

    ax = pivot.plot(figsize=(10, 5))
    ax.set_title("Parallel Trends Check (Pre-Treatment Only)")
    ax.set_ylabel("Workplaces % Change from Baseline")
    ax.set_xlabel("Days since start")

    plt.tight_layout()

    # ---- Save plot as image ----
    plt.savefig(PLOT_PATH, dpi=300)

    print(f"✅ Parallel trends plot saved to: {PLOT_PATH.resolve()}")

    plt.show()


if __name__ == "__main__":
    main()
