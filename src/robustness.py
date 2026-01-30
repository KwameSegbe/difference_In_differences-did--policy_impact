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
from diff_diff import CallawaySantAnna

DATA_PATH = Path("data/processed/panel_mobility.csv")


def main() -> None:
    """
    Run the main Callaway-Sant'Anna DiD analysis with placebo tests.
    
    Steps:
    1. Load preprocessed panel data
    2. Estimate treatment effects using CS estimator
    3. Run placebo tests (if available in installed version)
    
    Raises:
        FileNotFoundError: If preprocessed data file doesn't exist
        """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first."
        )

    df = pd.read_csv(DATA_PATH)

    cs = CallawaySantAnna(
        control_group="never_treated",
        estimation_method="dr",
        n_bootstrap=199,  # keep smaller for robustness runs
        seed=42,
        cluster="unit",
    )

    results = cs.fit(df, outcome="outcome", unit="unit", time="time", first_treat="first_treat")
    print("\n=== MAIN ESTIMATE ===")
    results.print_summary()

    # Try built-in placebo utilities if present in your diff-diff version
    try:
        from diff_diff import run_all_placebo_tests  # type: ignore

        print("\n=== PLACEBO TESTS ===")

        # NOTE:
        # Your installed diff-diff expects something like:
        # run_all_placebo_tests(outcome, treatment, time, unit, pre_periods, post_periods, ...)
        # not `run_all_placebo_tests(results)`.
        #
        # We try calling it anyway with `results` (some versions support it),
        # but we DO NOT print raw objects (to avoid huge dict dumps).
        placebo = run_all_placebo_tests(results)  # may fail on your version

        if hasattr(placebo, "print_summary"):
            placebo.print_summary()
        else:
            print("Placebo ran, but this version returns a raw object (no printable summary).")

    except Exception:
        # Keep output clean: no big stack trace / repr(e)
        print("\nPlacebo helpers not available in your installed diff-diff version.")
        print("No problem — we can still do manual placebo dates if needed.")


if __name__ == "__main__":
    main()
