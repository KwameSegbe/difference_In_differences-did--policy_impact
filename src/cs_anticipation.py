"""
Callaway–Sant'Anna Robustness: Anticipation Only
------------------------------------------------
Runs Callaway–Sant'Anna (mans/diff_diff) with multiple anticipation windows
and saves each result to output/anticipation/.

- Uses NOT-YET-TREATED controls (staggered adoption)
- Does NOT modify the diff_diff library
- Anchors paths to PROJECT_ROOT (did2/)
"""

from pathlib import Path
import pandas as pd
import io
import contextlib

from diff_diff import CallawaySantAnna


# ---- project paths (KEEP THIS PATTERN) ----
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # did2/
DATA_PATH = PROJECT_ROOT / "data/processed/panel_mobility.csv"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ANTICIPATION_DIR = OUTPUT_DIR / "anticipation"
ANTICIPATION_DIR.mkdir(parents=True, exist_ok=True)


def run_and_save_cs_anticipation(df: pd.DataFrame, k: int) -> None:
    """
    Run CS with anticipation=k and save a small summary file.
    """
    cs = CallawaySantAnna(
        control_group="not_yet_treated",
        estimation_method="dr",
        anticipation=k,
        seed=42,
        cluster="unit",
    )

    res = cs.fit(
        df,
        outcome="outcome",
        unit="unit",
        time="time",
        first_treat="first_treat",
    )

    out_file = ANTICIPATION_DIR / f"cs_anticipation_{k}.txt"

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print(f"Callaway–Sant'Anna Anticipation Robustness (k={k})")
        print("=" * 60)
        print(f"Overall ATT : {res.overall_att:.4f}")
        print(f"SE          : {res.overall_se:.4f}")

    out_file.write_text(buffer.getvalue(), encoding="utf-8")

    print(buffer.getvalue())
    print(f"✅ Saved to: {out_file.resolve()}")


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing file: {DATA_PATH.resolve()}")

    df = pd.read_csv(DATA_PATH)

    # Daily data => k is in days
    for k in [0, 1, 7, 14]:
        run_and_save_cs_anticipation(df, k)


if __name__ == "__main__":
    main()

