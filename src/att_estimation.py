"""
Overall Average Treatment Effect (ATT) Estimation
--------------------------------------------------
This script estimates a SINGLE overall average treatment effect of stay-at-home
orders on mobility, aggregating across all treated units and post-treatment periods.

Key difference from event study:
- aggregate="overall" collapses all period-specific effects into ONE number
- Answers: "What was the average effect of stay-at-home orders on mobility?"
- Simpler interpretation but loses information about dynamics (when effect appears,
  how it evolves, whether it fades over time)

Use this when you want a single summary statistic rather than period-by-period effects.
"""
from pathlib import Path
import io
import contextlib
import pandas as pd
from diff_diff import CallawaySantAnna


PROJECT_ROOT = Path(__file__).resolve().parents[1]  # did2/
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "panel_mobility.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"
SUMMARY_TXT = OUTPUT_DIR / "att_summary.txt"


def main() -> None:
    """
    Estimate the overall average treatment effect on the treated (ATT).

    The overall ATT is a weighted average of all group-time ATT(g,t) estimates.
    Output is saved as a TXT file for reproducibility and reporting.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first."
        )

    df = pd.read_csv(DATA_PATH)

    cs = CallawaySantAnna(
        control_group="never_treated",
        estimation_method="dr",
        n_bootstrap=499,
        seed=42,
        cluster="unit",
    )

    results = cs.fit(
        df,
        outcome="outcome",
        unit="unit",
        time="time",
        first_treat="first_treat",
        aggregate="overall",
    )

    # Capture printed summary into TXT
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        results.print_summary()

        # Some versions expose overall ATT separately
        if hasattr(results, "overall_att"):
            print("\nOverall ATT:", results.overall_att)

    SUMMARY_TXT.write_text(buffer.getvalue(), encoding="utf-8")

    print(f"✅ ATT summary saved to: {SUMMARY_TXT.resolve()}")


if __name__ == "__main__":
    main()