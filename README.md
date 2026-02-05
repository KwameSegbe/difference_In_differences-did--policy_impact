# <h2>Measuring Policy Impact with Difference-in-Differences</h2> #
<img src="assests/did_pictures.png" alt="Difference-in-Differences (DiD)" width="100%">

# Overview

This repository contains a Difference-in-Differences (DiD) analysis designed to estimate the causal impact of a treatment using panel data. The analysis emphasizes transparency and robustness through event study estimation, cohort-level visualization, and robustness checks across alternative estimators.

# Methodology

The primary estimation strategy follows a modern DiD framework that accounts for staggered treatment adoption. The analysis proceeds in three main stages:

# Main DiD Estimation
Estimation of average treatment effects using a cohort-aware DiD estimator.

# Event Study Analysis
Dynamic treatment effects are estimated relative to time since treatment adoption to:

Assess pre-treatment trends

Evaluate post-treatment dynamics

Support interpretation of the main estimator

The full event study output is included as a text file for transparency and auditability 

# event_study_results

.
# Robustness Checks
Results are compared across alternative DiD estimators, including Callaway–Sant’Anna and Sun–Abraham specifications, to assess sensitivity to modeling assumptions. Overall ATT estimates from these approaches are directionally consistent with the main results 

# robustness_results

.

# Visualizations

The current set of visualizations includes:

Cohort-level visualizations to highlight heterogeneity across treatment cohorts

Full-sample visualizations summarizing aggregate treatment effects

Event study output (TXT) for detailed inspection of dynamic effects over time

These visualizations are intended to support both diagnostic checks and interpretability.

# Results Summary

Event study estimates and robustness checks are broadly consistent with the main DiD estimator.

Post-treatment effects appear persistent over time.

Some pre-treatment coefficients show variability, underscoring the importance of cautious interpretation.

# Interpretation Notes

While results are directionally consistent across estimators and diagnostics, they should be interpreted with caution due to the relatively limited length of historical pre-treatment data. A longer pre-treatment period would strengthen confidence in parallel trends and dynamic estimates.

# Next Steps

Planned extensions include:

Additional robustness checks (placebo tests, alternative control groups)

Expanded visualization of dynamic effects

Sensitivity analysis around pre-treatment window length





