from pathlib import Path
import pandas as pd
import numpy as np

# ==========================================
# Task 34: Load Dataset & Inspect Data Types
# ==========================================
ROOT_DIR = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT_DIR / "DATA" / "03_bike_rental.csv")

print("Shape (Rows, Columns):", df.shape)
print("Columns:", df.columns.tolist())
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())

# ==========================================
# Task 35: Check & Handle Missing Humidity
# ==========================================
print(f"\nMissing Humidity_Percent before cleaning: {df['Humidity_Percent'].isnull().sum()}")
df["Humidity_Percent"] = df["Humidity_Percent"].fillna(
    df.groupby("Season")["Humidity_Percent"].transform("median")
)
df["Humidity_Percent"] = df["Humidity_Percent"].fillna(df["Humidity_Percent"].median())
print(f"Missing Humidity_Percent after cleaning: {df['Humidity_Percent'].isnull().sum()}")

# ==========================================
# Task 36: Convert DateTime & Extract Features
# ==========================================
df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")
df["Date"] = df["DateTime"].dt.date
df["Month"] = df["DateTime"].dt.month
df["Hour"] = df["DateTime"].dt.hour
df["DayOfWeek"] = df["DateTime"].dt.day_of_week

# ==========================================
# Task 37: Total & Average Rentals
# ==========================================
total_rentals = df["Rental_Count"].sum()
average_rentals = df["Rental_Count"].mean()

print(f"\nTotal Rentals: {total_rentals:,.0f}")
print(f"Average Rentals per Record: {average_rentals:.2f}")

# ==========================================
# Task 38: Top 10 Highest-Demand Time Records
# ==========================================
top_10_records = df.sort_values(by="Rental_Count", ascending=False).head(10)
print("\nTop 10 Highest-Demand Time Records:\n", top_10_records[["DateTime", "Season", "Weather", "Rental_Count"]])

# ==========================================
# Task 39: Compare Average Rentals by Season
# ==========================================
season_rentals = (
    df.groupby("Season")["Rental_Count"]
    .agg(Avg_Rentals="mean", Total_Rentals="sum", Records="count")
    .sort_values(by="Avg_Rentals", ascending=False)
)
print("\nAverage Rentals by Season:\n", season_rentals)

# ==========================================
# Task 40: Compare Weekends vs. Weekdays
# ==========================================
weekend_comparison = (
    df.groupby("Is_Weekend")["Rental_Count"]
    .agg(Avg_Rentals="mean", Median_Rentals="median", Total_Rentals="sum")
)
print("\nWeekend vs. Weekday Rental Demand:\n", weekend_comparison)

# ==========================================
# Task 41: Compare Demand Across Weather Conditions
# ==========================================
weather_comparison = (
    df.groupby("Weather")["Rental_Count"]
    .agg(Avg_Rentals="mean", Total_Rentals="sum", Records="count")
    .sort_values(by="Avg_Rentals", ascending=False)
)
print("\nDemand Across Weather Conditions:\n", weather_comparison)

# ==========================================
# Task 42: Analyze Rentals by Hour of Day
# ==========================================
hourly_demand = (
    df.groupby("Hour")["Rental_Count"]
    .agg(Avg_Rentals="mean", Total_Rentals="sum")
    .sort_index()
)
print("\nHourly Rental Demand:\n", hourly_demand)

# ==========================================
# Task 43: NumPy Mean for Temp & Rental Count
# ==========================================
rental_arr = df["Rental_Count"].to_numpy(dtype=float)
temp_arr = df["Temperature_C"].to_numpy(dtype=float)

np_avg_rentals = np.mean(rental_arr)
np_avg_temp = np.nanmean(temp_arr)

print(f"\nNumPy Average Temperature_C: {np_avg_temp:.2f}")
print(f"NumPy Average Rental Count: {np_avg_rentals:.2f}")

# ==========================================
# Task 44: Identify High Rental Outliers (IQR)
# ==========================================
q1, q3 = np.percentile(rental_arr, [25, 75])
iqr = q3 - q1
upper_fence = q3 + 1.5 * iqr

high_demand_outliers = df[df["Rental_Count"] > upper_fence]
print(f"\nIQR Upper Fence: {upper_fence:.2f} | Unusually High Demand Records: {len(high_demand_outliers)}")
if not high_demand_outliers.empty:
    print(high_demand_outliers[["DateTime", "Season", "Weather", "Rental_Count"]])

# ==========================================
# Task 45: Season-and-Weather Grouped Summary
# ==========================================
season_weather_summary = (
    df.groupby(["Season", "Weather"])["Rental_Count"]
    .agg(Avg_Rentals="mean", Total_Rentals="sum", Records="count")
    .reset_index()
)
print("\nSeason & Weather Grouped Summary:\n", season_weather_summary)

# ==========================================
# Task 46: Sort Days / Records by Rental Demand
# ==========================================
daily_demand = (
    df.groupby("Date")["Rental_Count"]
    .agg(Daily_Total_Rentals="sum", Daily_Avg_Rentals="mean")
    .sort_values(by="Daily_Total_Rentals", ascending=False)
)
print("\nTop 10 Busiest Days by Total Rentals:\n", daily_demand.head(10))

# ==========================================
# Task 47: Correlation (Temp vs. Rental Count)
# ==========================================
correlation = df["Temperature_C"].corr(df["Rental_Count"])
print(f"\nCorrelation between Temperature_C and Rental_Count: {correlation:.4f}")
print("Note: Correlation shows association, not causation.")

# ==========================================
# Task 48: Save Cleaned Dataset & Recommendations
# ==========================================

cleaned_path = ROOT_DIR / "DATA" / "03_bike_rental_cleaned.csv"
df.to_csv(cleaned_path, index=False)
print(f"\nCleaned dataset saved successfully at: {cleaned_path}")

recommendations = [
    "1. Peak-Hour Rebalancing: Increase bike availability before peak demand hours and schedule maintenance during low-demand overnight hours.",
    "2. Seasonal Fleet Adjustment: Allocate extra bikes and promotional offers during the highest-demand season while conducting major servicing in low-demand seasons.",
    "3. Weather-Based Operations: Reduce active field rebalancing during adverse weather conditions and utilize those hours for routine repairs.",
    "4. Weekend vs. Weekday Allocation: Position bikes near commercial/transit hubs on weekdays and recreational/park areas on weekends based on demand splits.",
    "5. High-Demand Spike Readiness: Monitor optimal temperature and weather conditions that trigger IQR demand spikes to deploy buffer stock proactively."
]

print("\nFive Operational Recommendations:")
for rec in recommendations:
    print(rec)
    