# """
# Event Study Analysis: Period-by-Period Treatment Effects
# ---------------------------------------------------------
# This script runs a Callaway-Sant'Anna event study to estimate the dynamic
# treatment effects of stay-at-home orders on mobility at EACH time period
# relative to treatment (e.g., -28, -27, ..., -1, 0, 1, 2, ...).

# Key difference from standard CS estimator:
# - aggregate="event_study" produces coefficients for each relative time period
# - Allows us to visualize pre-treatment trends (parallel trends test) and
#   post-treatment dynamics (how effects evolve over time)

# Output: A table with estimates for periods -28 to +291 showing:
# - Pre-treatment coefficients (should be ~0 and insignificant if parallel trends hold)
# - Post-treatment coefficients (the actual treatment effect at each time)
# """
# from pathlib import Path
# import pandas as pd
# from diff_diff import CallawaySantAnna

# PROJECT_ROOT = Path(__file__).resolve().parents[1]  # did2/
# DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

# def main() -> None:
#     """
#     Run event study analysis to estimate treatment effects at each relative time period.
    
#     Event study specification:
#     - Estimates separate coefficients for each period relative to treatment
#     - Pre-treatment periods (-28 to -1): test parallel trends assumption
#     - Treatment period (0): day orders were implemented  
#     - Post-treatment periods (1 to 291): dynamic treatment effects
    
#     Raises:
#         FileNotFoundError: If preprocessed data doesn't exist
#     """
#     print("Loading data from:", DATA_PATH.resolve())

#     if not DATA_PATH.exists():
#         raise FileNotFoundError(f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first.")

#     df = pd.read_csv(DATA_PATH)

#     cs = CallawaySantAnna(
#         control_group="never_treated",
#         estimation_method="dr",
#         seed=42,
#         cluster="unit",
#     )

#     res = cs.fit(
#         df,
#         outcome="outcome",
#         unit="unit",
#         time="time",
#         first_treat="first_treat",
#         aggregate="event_study",  # ← This gives you period-by-period effects
#     )

#     # Print event-study summary table
#     res.print_summary()


# if __name__ == "__main__":
#     main()


"""
Event Study Analysis: Period-by-Period Treatment Effects
---------------------------------------------------------
Runs a Callaway-Sant'Anna event study and saves the printed summary
as a TXT file in the output/ folder.
"""

from pathlib import Path
import io
import contextlib
import pandas as pd
from diff_diff import CallawaySantAnna


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "panel_mobility.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"
SUMMARY_TXT = OUTPUT_DIR / "event_study_summary.txt"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data from:", DATA_PATH.resolve())

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first."
        )

    df = pd.read_csv(DATA_PATH)

    cs = CallawaySantAnna(
        control_group="never_treated",
        estimation_method="dr",
        seed=42,
        cluster="unit",
    )

    res = cs.fit(
        df,
        outcome="outcome",
        unit="unit",
        time="time",
        first_treat="first_treat",
        aggregate="event_study",
    )

    # Capture printed summary into TXT
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        res.print_summary()

    SUMMARY_TXT.write_text(buffer.getvalue(), encoding="utf-8")

    print(f"✅ Event study summary saved to: {SUMMARY_TXT.resolve()}")


if __name__ == "__main__":
    main()

