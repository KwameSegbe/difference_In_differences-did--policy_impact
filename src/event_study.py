"""
Event Study Analysis: Period-by-Period Treatment Effects
---------------------------------------------------------
This script runs a Callaway-Sant'Anna event study to estimate the dynamic
treatment effects of stay-at-home orders on mobility at EACH time period
relative to treatment (e.g., -28, -27, ..., -1, 0, 1, 2, ...).

Key difference from standard CS estimator:
- aggregate="event_study" produces coefficients for each relative time period
- Allows us to visualize pre-treatment trends (parallel trends test) and
  post-treatment dynamics (how effects evolve over time)

Output: A table with estimates for periods -28 to +291 showing:
- Pre-treatment coefficients (should be ~0 and insignificant if parallel trends hold)
- Post-treatment coefficients (the actual treatment effect at each time)
"""

from pathlib import Path
import pandas as pd

from diff_diff import CallawaySantAnna

DATA_PATH = Path("data/processed/panel_mobility.csv")
OUTPUT_TXT = Path("output/event_study_results.txt")
OUTPUT_PNG = Path("output/event_study_plot.png")
OUTPUT_COHORT_PNG = Path("output/cohort_effects_plot.png")

# Optional plotting (only if you have matplotlib + the helper)
HAS_MATPLOTLIB = False
try:
    import matplotlib.pyplot as plt  # type: ignore
    HAS_MATPLOTLIB = True
except Exception:
    pass

try:
    from diff_diff import plot_event_study  # type: ignore
except Exception:
    plot_event_study = None

try:
    from diff_diff import plot_group_effects  # type: ignore
except Exception:
    plot_group_effects = None


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    cs = CallawaySantAnna(
        control_group="not_yet_treated",
        estimation_method="dr",
        anticipation=7,
        seed=42,
        cluster="unit",
    )

    # Run event study (populates res.event_study_effects)
    res = cs.fit(
        df,
        outcome="outcome",
        unit="unit",
        time="time",
        first_treat="first_treat",
        aggregate="event_study",
    )

    # Ensure output folder exists
    OUTPUT_TXT.parent.mkdir(parents=True, exist_ok=True)

    # ---- Build the event-study table ----
    lines = []
    lines.append("Event Study Results (Effect by Time Since Adoption)")
    lines.append("=" * 60)
    lines.append(f"{'Event Time':>12} {'ATT':>10} {'SE':>10} {'95% CI':>25}")
    lines.append("-" * 60)

    for e in sorted(res.event_study_effects.keys()):
        eff = res.event_study_effects[e]
        ci = eff["conf_int"]
        sig = "*" if eff["p_value"] < 0.05 else ""
        lines.append(
            f"{e:>12} {eff['effect']:>10.4f} {eff['se']:>10.4f} "
            f"[{ci[0]:>8.4f}, {ci[1]:>8.4f}] {sig}"
        )

    # Save TXT + print to console
    OUTPUT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n✅ Event study table saved to: {OUTPUT_TXT.resolve()}")

    # ---- Plot 1: Event study ----
    if HAS_MATPLOTLIB and plot_event_study is not None:
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_event_study(
            results=res,
            ax=ax,
            title="Stay-at-Home Orders: Effect on Mobility",
            xlabel="Time Since Adoption",
            ylabel="Effect on Mobility Outcome",
        )
        plt.tight_layout()
        fig.savefig(OUTPUT_PNG, dpi=200)
        print(f"✅ Event study plot saved to: {OUTPUT_PNG.resolve()}")
        plt.show()
    else:
        print("\n⚠️ Event study plot not created (missing matplotlib or diff_diff.plot_event_study).")

    # ---- Plot 2: Effects by cohort (separate figure) ----
    if HAS_MATPLOTLIB and plot_group_effects is not None:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        plot_group_effects(
            results=res,
            ax=ax2,
            title="Treatment Effects by Cohort",
        )
        plt.tight_layout()
        fig2.savefig(OUTPUT_COHORT_PNG, dpi=200)
        print(f"✅ Cohort effects plot saved to: {OUTPUT_COHORT_PNG.resolve()}")
        plt.show()
    else:
        print("\n⚠️ Cohort effects plot not created (missing matplotlib or diff_diff.plot_group_effects).")


if __name__ == "__main__":
    main()
