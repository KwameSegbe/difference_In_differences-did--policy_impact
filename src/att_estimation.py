from pathlib import Path
import pandas as pd

from diff_diff import CallawaySantAnna

PROJECT_ROOT = Path(__file__).resolve().parents[1]  # did2/
DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first.")

    df = pd.read_csv(DATA_PATH)

    cs = CallawaySantAnna(
        control_group="never_treated",
        estimation_method="dr",   # doubly robust
        n_bootstrap=499,          # increase to 999 later
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

    results.print_summary()

    # Some versions expose overall ATT differently; keep both prints safe:
    if hasattr(results, "overall_att"):
        print("\nOverall ATT:", results.overall_att)

if __name__ == "__main__":
    main()

