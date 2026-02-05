# <h2>Measuring Policy Impact with Difference-in-Differences</h2> #
<img src="assests/did_pictures.png" alt="Difference-in-Differences (DiD)" width="100%">

## Overview

This repository contains a Difference-in-Differences (DiD) analysis designed to estimate the causal impact of a treatment using panel data with staggered adoption. The goal of the project is to produce transparent, interpretable, and robust causal estimates while explicitly validating assumptions through event study analysis and robustness checks.

The analysis prioritizes methodological rigor, clear documentation, and cautious interpretation of results.

## Methodology
Main Estimation Strategy

The primary estimation approach follows a modern DiD framework that accounts for staggered treatment timing and heterogeneous treatment effects across cohorts. Average Treatment Effects on the Treated (ATT) are estimated using a cohort-aware estimator.

## Event Study Analysis

An event study specification is used to estimate dynamic treatment effects relative to time since treatment adoption. This serves multiple purposes:

Assessing pre-treatment trends (parallel trends diagnostics)

Evaluating the evolution and persistence of post-treatment effects

Supporting interpretation of the main DiD estimator

The full event study output is included as a text file for transparency and auditability:

event_study_results.txt 

event_study_results

Robustness Checks

To assess sensitivity to estimator choice and identifying assumptions, results are compared across alternative DiD estimators:

Callaway–Sant’Anna

Sun–Abraham

These checks help evaluate whether the main findings are driven by modeling choices or remain directionally stable across specifications. Summary robustness results are provided in:

robustness_results.txt 

robustness_results

## Visualizations

The current visualizations included in the analysis are designed to support both diagnostics and interpretability:

Cohort-level visualizations highlighting heterogeneity across treatment cohorts

Full-sample visualizations summarizing aggregate treatment effects

Event study output (TXT) providing detailed estimates by event time

Together, these views allow inspection of dynamic effects, cohort behavior, and overall trends.

# Results
## Main Findings

The estimated Average Treatment Effect on the Treated (ATT) is negative under the primary DiD specification.

Dynamic treatment effects from the event study indicate persistent post-treatment impacts relative to the treatment adoption period.

Estimated effects are directionally consistent across alternative DiD estimators.

## Event Study Results

Post-treatment coefficients are consistently negative and statistically significant across most post-adoption periods.

Event-time estimates suggest that treatment effects persist rather than dissipate quickly.

Pre-treatment coefficients exhibit some variability, highlighting the importance of cautious interpretation.

## Detailed event-time estimates are available in:

event_study_results.txt 

event_study_results

## Robustness Results

Robustness checks comparing alternative estimators show:

Callaway–Sant’Anna Overall ATT ≈ −6.66

Sun–Abraham Overall ATT ≈ −3.88

While magnitudes differ, both estimates are directionally aligned, supporting the robustness of the main findings:

robustness_results.txt 

robustness_results

Interpretation Notes

While the event study and robustness checks are broadly consistent with the main estimator results, findings should be interpreted with caution. The available historical pre-treatment period is relatively limited, which constrains the strength of parallel trends validation and increases uncertainty around dynamic estimates.

Accordingly, results are presented as evidence of directional and persistent effects rather than definitive causal magnitudes.

## Next Steps

Planned extensions to the analysis include:

Additional robustness checks (e.g., placebo tests, alternative control group definitions)

Sensitivity analysis around the length of the pre-treatment window

Expanded visualization of dynamic treatment effects

## Repository Structure

event_study_results.txt — Full event study output by event time

robustness_results.txt — Summary robustness comparisons across estimators

Visualization outputs — Cohort-level and full-sample plots

## Final Note

This project emphasizes responsible causal inference: validating assumptions, surfacing uncertainty, and separating estimation from interpretation. The structure and documentation are designed to support reproducibility, review, and clear communication of results.
