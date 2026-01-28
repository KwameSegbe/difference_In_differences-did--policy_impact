# from pathlib import Path
# import pandas as pd
# from diff_diff import CallawaySantAnna

# PROJECT_ROOT = Path(__file__).resolve().parents[1]  # did2/
# DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

# def main() -> None:
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
#         aggregate="event_study",
#     )

#     # Print event-study summary table
#     res.print_summary()


# if __name__ == "__main__":
#     main()

from pathlib import Path
import pandas as pd
from diff_diff import CallawaySantAnna

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # did2/
DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

def main() -> None:
    print("Loading data from:", DATA_PATH.resolve())

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first.")

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
        aggregate="event_study",  # ← This gives you period-by-period effects
    )

    # Print event-study summary table
    res.print_summary()


if __name__ == "__main__":
    main()