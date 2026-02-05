# Project Outcomes and Interpretation
## Outcome Summary

Stay-at-home orders led to a clear and sustained reduction in workplace mobility, averaging about 6–7 percentage points after adoption.

The effect:

Appears immediately after the policy starts

Persists over time rather than fading

Is consistent across states and estimation approaches

## Primary Result: Average Effect

Across all treated states and post-policy periods, workplace mobility declined by 6.66 percentage points on average relative to states that had not yet adopted the policy.

This estimate reflects the typical impact of a stay-at-home order, rather than a single day or state, and summarizes the full post-treatment period into one interpretable number.

## Interpretation:
After a stay-at-home order begins, people go to workplaces noticeably less than they otherwise would have.

## Figure reference:
Overall ATT summary output 
[`output/att_summary.txt`](../output/att_summary.txt).
att_summary


## Dynamic Effects Over Time

Looking beyond the average, the effect is visible right at adoption and becomes more negative in the days immediately following.

Key observations:

No delayed response — behavior changes quickly

Effects remain negative across long horizons

No evidence of reversal or short-lived impact

This pattern indicates that the policy changed behavior in a durable way rather than producing a brief shock.

Event study: Effect on workplace mobility over time since adoption
(output/event_study_plot.png)
![Event study: Effect of stay-at-home orders on workplace mobility over time](../output/event_study.png)
Source: Event study estimates 

event_study_results

Consistency Across Cohorts

States adopted stay-at-home orders at different times, but the direction of the effect is consistent across cohorts.

While the size of the reduction varies by state and timing, all treated groups show a drop in workplace mobility following adoption.

This reduces the risk that results are driven by a single early- or late-adopting state.

📌 Insert Figure Here:
Treatment effects by adoption cohort
(output/cohort_effects_plot.png)

Validity Check: Pre-Treatment Trends

Before any stay-at-home orders were introduced, treated and untreated states followed similar workplace mobility trends.

There is no visible divergence prior to policy adoption, which supports using untreated states as a comparison group.

This check matters because it shows the estimated effects are unlikely to be driven by pre-existing differences.

📌 Insert Figure Here:
Parallel trends check (pre-treatment only)
(output/parallel_trends.png)

Robustness Checks

Two additional checks were run to test whether the result depends on modeling choices:

Alternative estimators produce similar negative effects

Allowing for anticipation (people adjusting behavior before official dates) does not materially change the estimate

While point estimates differ slightly, the direction and interpretation remain the same.

Source: Robustness summaries


robustness_results




cs_anticipation_7

Practical Takeaway

From a policy perspective, stay-at-home orders were effective at reducing workplace movement, and they did so quickly and persistently.

From an analytics perspective, this project shows how staggered policy timing can be used to separate policy effects from broader trends during a rapidly changing period.