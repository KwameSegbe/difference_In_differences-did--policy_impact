import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import diff_diff as dd


# df = pd.read_csv('C:\Users\HP\Documents\did2\data\raw\covid_mobility\2020_US_Region_Mobility_Report.csv')
df = pd.read_csv('C:\\Users\\HP\\Documents\\did2\\data\\raw\\covid_mobility\\2020_US_Region_Mobility_Report.csv')   

print(df.head())

# Filter to US state-level rows and COPY safely
df_states = df[
    (df["country_region_code"] == "US") &
    (df["sub_region_1"].notna()) &
    (df["sub_region_2"].isna())
].copy()

# Define treated & control states
treated_states = ["New York", "California", "New Jersey", "Washington"]
control_states = ["Texas", "Florida", "Georgia", "South Dakota"]

keep_states = treated_states + control_states

# Keep only selected states
df_8 = df_states[df_states["sub_region_1"].isin(keep_states)].copy()

# Add treated label
df_8["treated"] = df_8["sub_region_1"].isin(treated_states).astype(int)

# Confirm treated vs control mapping
print(
    df_8[["sub_region_1", "treated"]]
    .drop_duplicates()
    .sort_values(["treated", "sub_region_1"], ascending=[False, True])
)

# print("Rows (8 states):", len(df_8))

# Outcome variable
y = "workplaces_percent_change_from_baseline"

# Policy date (NY lockdown announcement window)
policy_date = pd.Timestamp("2020-03-15")

# --- Ensure date is datetime ---
df_8["date"] = pd.to_datetime(df_8["date"])

# --- Aggregate to daily mean by treated status ---
trend = (
    df_8
    .groupby(["date", "treated"], as_index=False)[y]
    .mean()
)

print(trend.head())

# 6 months pre-policy window
pre_start = policy_date - pd.Timedelta(days=180)

trend_pre = trend[
    (trend["date"] >= pre_start) &
    (trend["date"] < policy_date)
].copy()

print(trend_pre["date"].min(), trend_pre["date"].max())


pivot = (
    trend_pre
    .pivot(index="date", columns="treated", values=y)
    .rename(columns={0: "Control", 1: "Treated"})
    .sort_index()
)

print(pivot.head())


ax = pivot.plot(figsize=(10, 5))

ax.set_title("Parallel Trends Check (Pre-COVID Policy Only)")
ax.set_ylabel("Workplaces % Change from Baseline")
ax.set_xlabel("Date")

plt.tight_layout()
plt.show()



