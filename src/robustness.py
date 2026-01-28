from pathlib import Path
import pandas as pd
from diff_diff import CallawaySantAnna

DATA_PATH = Path("data/processed/panel_mobility.csv")

def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing processed file: {DATA_PATH.resolve()}. Run preprocess.py first.")

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
        from diff_diff import run_all_placebo_tests
        print("\n=== PLACEBO TESTS ===")
        placebo = run_all_placebo_tests(results)
        placebo.print_summary() if hasattr(placebo, "print_summary") else print(placebo)
    except Exception as e:
        print("\nPlacebo helpers not available in your installed diff-diff version.")
        print("Error:", repr(e))
        print("No problem — we can still do manual placebo dates if needed.")

if __name__ == "__main__":
    main()