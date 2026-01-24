import sys
import pandas as pd
import numpy as np

import diff_diff
# import statsmodels.formula.api as smf

import sys
import pandas as pd
from pathlib import Path

print("Python:", sys.version)
print("Python exe:", sys.executable)

url = "https://www.dol.gov/agencies/whd/state/minimum-wage/history"

print("Fetching minimum wage tables...")
tables = pd.read_html(url)

print("Tables found:", len(tables))

df = tables[0]

print("Preview:")
print(df.head())

# ---- FIXED OUTPUT PATH (Windows + Portable) ----
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

output_path = RAW_DIR / "min_wage_raw.csv"

df.to_csv(output_path, index=False)

print(f"Saved dataset to {output_path}")

