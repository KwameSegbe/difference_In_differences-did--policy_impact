# Causal Impact of Policy Adoption Using Difference-in-Differences (DiD)

## Project Summary
This project evaluates the causal impact of a real-world policy using Difference-in-Differences (DiD). 
I construct a panel dataset, define treatment and control groups, validate identification assumptions, 
and estimate treatment effects using modern DiD estimators.

Estimation is performed using the open-source `diff-diff` library, while all data engineering, 
causal design, diagnostics, and interpretation are my own.

## Research Question
Did the adoption of [POLICY NAME — e.g., Castle Doctrine Laws] causally affect [OUTCOME — e.g., homicide rates]?

## Identification Strategy
- Unit of analysis: State-year
- Treatment group: States adopting the policy
- Control group: States not adopting the policy
- Method: Two-Way Fixed Effects DiD + Sun & Abraham correction for staggered adoption
- Key assumption: Parallel trends (validated empirically)

## Methods & Robustness Checks
- Parallel trends and pre-trend tests
- Event study visualization
- Staggered adoption correction (Sun–Abraham)
- Placebo timing tests
- Leave-one-out robustness checks
- Sensitivity analysis (HonestDiD)

## Key Results
(Summary of estimated ATT and interpretation goes here)

## Tech Stack
Python, pandas, diff-diff, statsmodels, matplotlib

## Author
Francis Segbe
