"""
Callaway-Sant'Anna Difference-in-Differences Event Study Analysis
-----------------------------------------------------------------
This script estimates the causal effect of stay-at-home orders on mobility
using the Callaway-Sant'Anna (2021) estimator, which is robust to:
- Heterogeneous treatment effects across units and time
- Staggered treatment adoption
- Dynamic treatment effects

The estimator uses "never-treated" states as the control group and employs
doubly-robust estimation with bootstrap standard errors clustered at the state level.
"""
from pathlib import Path
import pandas as pd
import io
import contextlib

from diff_diff import CallawaySantAnna, SunAbraham

DATA_PATH = Path("data/processed/panel_mobility.csv")

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ROBUSTNESS_TXT = OUTPUT_DIR / "robustness_results.txt"


def main() -> None:
    """
    Run a robustness check comparing two modern Difference-in-Differences estimators:
    Callaway–Sant’Anna (CS) and Sun–Abraham (SA).

    This function:
    1. Loads the preprocessed panel dataset
    2. Estimates the overall Average Treatment Effect on the Treated (ATT)
       using the Callaway–Sant’Anna staggered DiD estimator
    3. Re-estimates the same ATT using the Sun–Abraham estimator
    4. Prints a side-by-side comparison of point estimates and standard errors
    5. Saves the formatted comparison table to a text file for reproducibility

    Purpose:
    - Assess robustness of the estimated treatment effect to the choice of
      DiD estimator
    - Verify that conclusions are not driven by estimator-specific assumptions

    Output:
    - A text file containing a comparison table of CS vs. Sun–Abraham estimates
      (overall ATT and standard errors)

    Raises:
        FileNotFoundError: If the preprocessed panel data file does not exist
    """
    df = pd.read_csv(DATA_PATH)

    # Callaway–Sant'Anna (CS)
    cs = CallawaySantAnna(control_group="not_yet_treated", estimation_method="dr",anticipation=7)
    results_cs = cs.fit(
        df,
        outcome="outcome",
        unit="unit",
        time="time",
        first_treat="first_treat",
    )

    # Sun–Abraham (SA)
    sa = SunAbraham(control_group="not_yet_treated")
    results_sa = sa.fit(
        df,
        outcome="outcome",
        unit="unit",
        time="time",
        first_treat="first_treat",
    )

    # Capture printed output
    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        cs_name = "Callaway-Sant'Anna"
        sa_name = "Sun-Abraham"

        print("\nRobustness Check: CS vs Sun-Abraham")
        print("=" * 60)
        print(f"{'Estimator':<25} {'Overall ATT':>15} {'SE':>10}")
        print("-" * 60)
        print(f"{cs_name:<25} {results_cs.overall_att:>15.4f} {results_cs.overall_se:>10.4f}")
        print(f"{sa_name:<25} {results_sa.overall_att:>15.4f} {results_sa.overall_se:>10.4f}")

    ROBUSTNESS_TXT.write_text(buffer.getvalue(), encoding="utf-8")

    print(f"✅ Robustness results saved to: {ROBUSTNESS_TXT.resolve()}")

if __name__ == "__main__":
    main()
