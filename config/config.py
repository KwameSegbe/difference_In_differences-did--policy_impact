from __future__ import annotations
from pathlib import Path

import pandas as pd

Y_COL = "workplaces_percent_change_from_baseline"
POLICY_DATE = pd.Timestamp("2020-03-15")
PRE_DAYS = 180  # pre-period window for parallel trends check

TREATED_STATES = ["New York", "California", "New Jersey", "Washington"]
CONTROL_STATES = ["Texas", "Florida", "Georgia", "South Dakota"]
